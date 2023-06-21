import os
import geopandas as gpd
from shapely.geometry import Point
import csv
import time
from collections import defaultdict

# Define folder paths
shp_folder_path = r'SHP_FILES'
csv_file_path = r'Points Location Template.csv'
final_result_csv = r'final_result.csv'
redundancy_csv = r'redundancy.csv'

# Initialize variables to store the results
result_table = []
total_meter_count = 0
meter_coverage = defaultdict(int)
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

            # Count the number of meter locations within the shapefile coverage area
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
                        covered_meters.add((lon, lat))
                        meter_coverage[(lon, lat)] += 1

            # Store the result in the table
            result_table.append((os.path.basename(root), count, meters_covered_list))

# Sort the result table by the meter count
result_table.sort(key=lambda x: x[1], reverse=True)

# Create a CSV file to store the final result
with open(final_result_csv, 'w', newline='') as final_result_file:
    writer = csv.writer(final_result_file)
    writer.writerow(['Rank', 'Folder', 'Points Counted'])

    # Iterate over the shapefiles and write the covered meters count
    rank = 1
    for folder, count, _ in result_table:
        writer.writerow([rank, folder, count])
        rank += 1

# Count the redundancy of meters covered by multiple shapefiles
redundancy_count = defaultdict(int)
for _, count, _ in result_table:
    redundancy_count[count] += 1

# Calculate the redundancy count of covered meters
covered_meter_redundancy = defaultdict(int)
for meter, count in meter_coverage.items():
    covered_meter_redundancy[count] += 1

# Write the redundancy count to a CSV file
with open(redundancy_csv, 'w', newline='') as redundancy_file:
    writer = csv.writer(redundancy_file)
    writer.writerow(['Redundancy', 'Count'])

    # Write the redundancy count
    for count, redundancy in sorted(covered_meter_redundancy.items()):
        writer.writerow([count, redundancy])

# Calculate coverage percentage
meters_covered = len(covered_meters)
coverage_percentage = (meters_covered / total_meter_count) * 100

# Print the coverage percentage
print("Coverage Percentage: {:.2f}%".format(coverage_percentage))

# Measure the runtime
end_time = time.time()
runtime = end_time - start_time
print("Runtime:", runtime, "seconds")
