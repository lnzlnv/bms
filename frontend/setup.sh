#!/bin/bash

# Check if GNOME Terminal is installed
if ! command -v gnome-terminal &> /dev/null; then
    echo "GNOME Terminal is not installed. Please install it to use this script."
    exit 1
fi

# Command to execute in the first tab
tab1_command="npm run start"

# Command to execute in the second tab
tab2_command="npm run tailwind"

# Open the first tab with the specified command
gnome-terminal --tab -- bash -c "$tab1_command; exec bash"

# Open the second tab with the specified command
gnome-terminal --tab -- bash -c "$tab2_command; exec bash"