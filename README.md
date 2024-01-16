## geospatial_coverage_analysis 

This repository contains two Python scripts for analyzing the coverage of points locations within shapefiles. The scripts are designed for different purposes:

main_notOptimized.py: This script counts all points locations that fall within the boundaries of multiple shapefiles, including duplicate points.
It calculates the redundancy of points covered by shapefiles and generates a CSV file with the redundancy results.

main_Optimized.py: This script avoids counting duplicate points and provides a more accurate coverage analysis. 
It is specifically designed to identify the best server among the shapefiles, which corresponds to the shapefile that covers the most unique points. 
In this script, each point is counted only once in the best server it falls within.

## Prerequisites
Python 3.x
Required Python packages: geopandas, shapely

## Setup
Extract the contents of the ZIP files in the SHP_FILES folder:

Place all the ZIP files containing shapefiles in the SHP_FILES folder.
Run the script Extract_ZIP.py to extract the shapefiles from the ZIP files. This will create a folder named shp_folder with the extracted shapefiles.
Prepare the CSV file:

Ensure that the CSV file containing the point coordinates is located at PointsLocation/Points Location Template.csv.

The CSV file should have the following format:

Longitude,Latitude
lon1,lat1
lon2,lat2
lon3,lat3
...

Replace lon1, lat1, etc., with the actual longitude and latitude values for each point.

## Usage
Open the script file point_location_analysis.py in a text editor or Python IDE.

Modify the following variables at the beginning of the script, if necessary:

shp_folder_path: Specify the folder path where the shapefiles are located (default: SHP_FILES).
csv_file_path: Specify the file path of the CSV file containing the point coordinates (default: PointsLocation/Points Location Template.csv).
final_result_csv: Specify the file name or path for the final result CSV file (default: final_result.csv).
Run the script point_location_analysis.py. The script will perform the following steps:

Read the CSV file and count the total number of locations.
Iterate over each shapefile in the shp_folder_path.
Check and fix invalid geometries, if present.
Count the number of points locations within each shapefile's coverage area.
Store the results in a table.
Sort the result table by the points count.
Create a final result CSV file with the rankings and points counted.
Calculate the coverage percentage of the points.
Display the coverage percentage and runtime.

## Output
The script will generate the following output:

optimized :
  - final_result.csv: This file contains the final results, including the rankings and the number of points counted for each shapefile, this script avoids counting duplicate points and provides a more accurate coverage analysis. 
  - Console output: The optimized script will display the coverage percentage of points and runtime in seconds.
  
notOptimized :

  - final_result.csv : This file contains the final results, including the rankings and the number of points counted for each shapefile, counting duplicate points. 
  - redundancy_csv : The notOptimized script will create the redundancy files which indicates how many shapefiles are covering the same points. After analyzing all the shapefiles, the script displays the redundancy count for each level. For example, the count for "1 shapefile" represents the number of points covered by only one shapefile, "2 shapefiles" represents the number of points covered by exactly two shapefiles, and so on.

## Notes

Make sure to have the necessary permissions to read the shapefiles and write the output files.
Ensure that the required Python packages (geopandas and shapely) are installed. You can install them using pip install geopandas shapely.
The script assumes that the shapefiles have been extracted using the Extract_ZIP.py script and are located in the shp_folder directory. If your shapefiles have a different folder structure or naming convention, you can modify the script accordingly.
The script handles invalid geometries by attempting to fix them using the buffer(0) method. If the fix fails, the script will still count the points within the shapefile's coverage area, but the results may not be accurate for that particular shapefile.
The script assumes that the CSV file has a header row. If your file does not have a header, remove the line next(reader)

Also be aware the time and space complexity for this script are high and requires optimisation to be able to run huge amount of data.


