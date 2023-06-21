import os
import geopandas as gpd
from shapely.geometry import Point
import csv
import time

# Define folder paths
shp_folder_path = r'SHP_FILES'
csv_file_path = r'PointsLocation/Points Location Template.csv'
final_result_csv = r'final_result.csv'

# Initialize variables to store the results
result_table = []
max_meter_count = 0
max_meter_folder = ""
total_meter_count = 0
covered_meters = set()

# Start the timer
start_time = time.time()

# Read the meter location CSV file and count the total number of locations
with open(csv_file_path, "r") as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # Skip header row if present
    total_meter_count = sum(1 for row in reader)

# Iterate over each directory and file in the shp_folder_path
for root, dirs, files in os.walk(shp_folder_path):
    for file in files:
        if file.endswith('.shp'):
            # Load the shapefile
            shapefile_path = os.path.join(root, file)
            gdf = gpd.read_file(shapefile_path)

            # Check the validity of the geometries
            invalid_geometries = gdf[~gdf.is_valid]
            if not invalid_geometries.empty:
                print("Invalid geometries found in", file, ". Attempting to fix...")
                gdf = gdf.buffer(0)

            # Count the number of meter locations within the PNG coverage area
            count = 0
            meters_covered_list = []  # List to store the meters covered in each shapefile

            with open(csv_file_path, "r") as csv_file:
                reader = csv.reader(csv_file)
                next(reader)  # Skip header row if present

                for row in reader:
                    lon, lat = float(row[0]), float(row[1])
                    point = Point(lon, lat)

                    if gdf.contains(point).any():
                        count += 1
                        meters_covered_list.append((lon, lat))

            # Update the maximum meter count and corresponding folder
            if count > max_meter_count:
                max_meter_count = count
                max_meter_folder = os.path.basename(root)

            # Store the result in the table
            result_table.append((os.path.basename(root), count, meters_covered_list))

# Sort the result table by the meter count
result_table.sort(key=lambda x: x[1], reverse=True)

# Create a CSV file to store the final result
with open(final_result_csv, 'w', newline='') as final_result_file:
    writer = csv.writer(final_result_file)
    writer.writerow(['Rank', 'Folder', 'Points Counted'])

    # Iterate over the shapefiles and tag the covered meters
    rank = 1
    while result_table:
        folder, count, meters_covered_list = result_table.pop(0)
        writer.writerow([rank, folder, count])
        rank += 1

        # Tag the covered meters
        for meter in meters_covered_list:
            covered_meters.add(meter)

        # Recalculate the meters covered by the remaining shapefiles
        for i in range(len(result_table)):
            _, _, meters_covered_list = result_table[i]
            meters_covered_list = [meter for meter in meters_covered_list if meter not in covered_meters]
            result_table[i] = (result_table[i][0], len(meters_covered_list), meters_covered_list)

        # Sort the result table by the updated meter count
        result_table.sort(key=lambda x: x[1], reverse=True)

# Calculate coverage percentage
meters_covered = len(covered_meters)
coverage_percentage = (meters_covered / total_meter_count) * 100

# Print the coverage percentage
print("Coverage Percentage: {:.2f}%".format(coverage_percentage))

# Measure the runtime
end_time = time.time()
runtime = end_time - start_time
print("Runtime:", runtime, "seconds")
