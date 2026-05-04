#!/bin/bash

echo "Backing up journal to iCloud..."
rclone sync ~/journal/ icloud:Documents/journal/ --progress

if [ $? -eq 0 ]; then
    echo "Backup complete!"
else
    echo "Something went wrong. Check your rclone config."
fi
