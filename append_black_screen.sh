#!/bin/bash

# Script to prepend a 0.5-second black screen and append a 1-second black screen to each video in videos_raw folder

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: ffmpeg is not installed. Please install it first."
    exit 1
fi

# Check if videos_raw directory exists
if [ ! -d "../data_saumya/videos_from_screenshots" ]; then
    echo "Error: videos_raw directory not found"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p ../data_saumya/videos_black_screenshots/

# Counter for processed videos
count=0

# Process each video file
for video in ../data_saumya/videos_from_screenshots/*.{mp4,MP4,avi,AVI,mov,MOV,mkv,MKV}; do
    # Skip if no files match the pattern
    [ -e "$video" ] || continue
    # Get the filename without path
    filename=$(basename "$video")
    filename_no_ext="${filename%.*}"
    extension="${filename##*.}"

    # Output file path
    output="../data_saumya/videos_black_screenshots/${filename_no_ext}.${extension}"

    echo "Processing: $filename"

    # Get video properties (width, height, fps)
    width=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$video")
    height=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$video")
    fps=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$video")

    # Create temporary black screen videos
    temp_black_before="/tmp/temp_black_before_${filename_no_ext}.mp4"
    temp_black_after="/tmp/temp_black_after_${filename_no_ext}.mp4"

    # Generate 0.5 second black screen for before
    ffmpeg -f lavfi -i color=c=black:s=${width}x${height}:r=${fps}:d=0.5 \
           -c:v libx264 -pix_fmt yuv420p "$temp_black_before" -y 2>&1 | grep -v "^frame=" || true

    # Generate 1 second black screen for after
    ffmpeg -f lavfi -i color=c=black:s=${width}x${height}:r=${fps}:d=1 \
           -c:v libx264 -pix_fmt yuv420p "$temp_black_after" -y 2>&1 | grep -v "^frame=" || true

    # Create concat file with absolute paths
    concat_file="/tmp/temp_concat_${filename_no_ext}.txt"
    echo "file '$temp_black_before'" > "$concat_file"
    echo "file '$(realpath "$video")'" >> "$concat_file"
    echo "file '$temp_black_after'" >> "$concat_file"

    # Concatenate original video with black screen
    ffmpeg -f concat -safe 0 -i "$concat_file" -c copy "$output" -y 2>&1 | grep -v "^frame=" || true

    # Clean up temporary files
    rm -f "$temp_black_before" "$temp_black_after" "$concat_file"

    echo "✓ Saved to: $output"
    ((count++))
done

echo ""
echo "Processed $count video(s)"
echo "Output files are in: ../data_saumya/videos_black_screenshots"
