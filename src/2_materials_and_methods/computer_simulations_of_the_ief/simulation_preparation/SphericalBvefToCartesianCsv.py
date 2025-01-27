"""
Description:
------------
This script converts BrainVision BVEF files with spherical coordinates to CSV files with
Cartesian coordinates.
"""

from Utils import brainvision_bvef_to_xyz_coordinates

# Define file paths
bvef_file_path = "eeg_coordinates/brainvision_acticap128.bvef"
csv_file_path = "eeg_coordinates/brainvision_acticap128.csv"

# Call the brainvision_bvef_to_xyz_coordinates function to convert BrainVision BVEF to XYZ
# coordinates
# and save the result to a CSV file
brainvision_bvef_to_xyz_coordinates(bvef_file_path, csv_file_path)
