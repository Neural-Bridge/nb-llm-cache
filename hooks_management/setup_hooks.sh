#!/bin/bash

# Directory within the repository where the hooks are stored
HOOKS_DIR="hooks_management/hooks"

# Check if the hooks directory exists
if [ ! -d "$HOOKS_DIR" ]; then
    echo "The hooks directory does not exist. Please ensure you have a 'hooks' directory in your repository."
    exit 1
fi

# Copy the hooks to the .git/hooks directory
cp -a $HOOKS_DIR/. .git/hooks/

# Make the copied hooks executable
chmod +x .git/hooks/*

echo "Git hooks have been set up successfully."
