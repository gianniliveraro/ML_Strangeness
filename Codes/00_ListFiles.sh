#!/bin/bash

# Output file to store the paths
output_file="AO2D_paths.txt"

# Remove the output file if it already exists to avoid appending to an old file
rm -f "$output_file"

# Find all AO2D.root files and save their paths to the output file without the leading './'
find ../Dataset/Raw/Your-Dataset-directory/ -maxdepth 2 -type f -name "AO2D_*.root" | sort > "$output_file"

# Print a message indicating the completion
echo "Paths to all AO2D.root files have been saved in $output_file"
