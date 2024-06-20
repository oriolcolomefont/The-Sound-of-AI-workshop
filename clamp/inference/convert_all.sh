#!/bin/bash

# Get the current working directory
current_dir=$(pwd)

# Create the output directory if it does not exist
mkdir -p "$current_dir/inference/wikifonia_abc"

# Iterate over each .mxl file in the inference/wikifonia_xml directory
for input_file in "$current_dir/wikifonia_mxl/"*.mxl; do
    # Extract the base name of the file (without directory and extension)
    base_name=$(basename "$input_file" .mxl)
    
    # Define the output file path
    output_file="$current_dir/wikifonia_abc/${base_name}.abc"
    
    # Run the python script with the specified parameters and redirect output
    python "$current_dir/xml2abc.py" -m 2 -c 8 -x "$input_file" > "$output_file"
done