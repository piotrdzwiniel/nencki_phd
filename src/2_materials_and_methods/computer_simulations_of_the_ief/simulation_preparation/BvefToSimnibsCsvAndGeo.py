"""
Description:
------------
This script converts EEG electrode coordinates from a BrainVision BVEF file to a
SimNIBS-compatible CSV file with Cartesian coordinates. It then converts the CSV file to a
Gmsh (.geo) file format for further use in simulations or analyses.
"""

from Utils import brainvision_bvef_spherical_to_simnibs_csv_cartesian, simnibs_csv_to_geo

# Define file paths
bvef_file_path = "eeg_coordinates/brainvision_acticap128.bvef"
csv_file_path = "eeg_coordinates/brainvision_acticap128_simnibs4_m2m_mni152.csv"
geo_file_path = "eeg_coordinates/brainvision_acticap128_simnibs4_m2m_mni152.geo"

# Convert BrainVision BVEF file to SimNIBS-compatible CSV with Cartesian coordinates
# using custom conversion function (brainvision_bvef_spherical_to_simnibs_csv_cartesian)
brainvision_bvef_spherical_to_simnibs_csv_cartesian(bvef_file_path, csv_file_path,
                                                    mltpr_x=90.0, mltpr_y=105.0, mltpr_z=100.0,
                                                    shift_y=-17.5)

# Convert SimNIBS-compatible CSV to Gmsh (.geo) file using custom conversion function (
# simnibs_csv_to_geo)
simnibs_csv_to_geo(csv_file_path, geo_file_path)
