#!/bin/bash

# Check if a directory path is provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <directory_path>"
  exit 1
fi

DIR=$1

# Check if the directory exists
if [ -d "$DIR" ]; then
  echo "Directory '$DIR' already exists."
else
  # Create the directory if it does not exist
  mkdir -p "$DIR"
  if [ $? -eq 0 ]; then
    echo "Directory '$DIR' has been created."
  else
    echo "Failed to create directory '$DIR'."
    exit 1
  fi
fi

# Run the first Python script
python region.py --output_dir $DIR

# Check if the current script executed successfully
if [ $? -ne 0 ]; then
  echo "region.py failed to execute."
  exit 1
fi

# Run the next Python script
python matrix.py --output_dir $DIR

# Check if the current script executed successfully
if [ $? -ne 0 ]; then
  echo "matrix.py failed to execute."
  exit 1
fi

# Run the next Python script
python classi_merc_mezzi_ger.py --output_dir $DIR

# Check if the current script executed successfully
if [ $? -ne 0 ]; then
  echo "classi_merc_mezzi_ger.py failed to execute."
  exit 1
fi

# Run the next Python script
python mezzi.py --output_dir $DIR

# Check if the current script executed successfully
if [ $? -ne 0 ]; then
  echo "mezzi.py failed to execute."
  exit 1
fi

# Run the next Python script
python spedizioni.py --output_dir $DIR

# Check if the current script executed successfully
if [ $? -ne 0 ]; then
  echo "spedizioni.py failed to execute."
  exit 1
fi

echo "All scripts executed successfully."
