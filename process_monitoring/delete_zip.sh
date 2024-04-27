#!/bin/bash

# dir containing all zip files
target_dir="."

for zipfile in "$target_dir"/*.zip; do
  # Check if zip file
  if [[ $(file -b "$zipfile" | grep -o 'Zip archive') ]]; then
    echo "This is a zip"
    # Unzip file in the current directory
    7z x "$zipfile" -aoa -pinfected
    # Delete the zip file
    rm "$zipfile"
  fi
done

echo "Unzipped all .zip files and deleted them from $target_dir"
for file in "$target_dir"/*.elf; do
    hash=$(sha256sum "$file" | cut -d' ' -f1)
    known_hash="${file%.*}"
    parsed="${known_hash#./}"
    echo $hash
    echo $parsed
    if [[ "$hash" != "$parsed" ]]; then
      echo "Error: Variables $file  and $hash are not the same!"
      exit 1 
    fi
done
