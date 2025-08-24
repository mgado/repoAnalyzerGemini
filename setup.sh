#!/bin/bash

# setup.sh

echo "--- 🤖 Setting up GitHub Repo Analyzer Agent (Gemini api version with URL context)---"

# Check if pip is installed
if ! command -v pip &> /dev/null
then
    echo "pip could not be found. Please install Python and pip first."
    exit
fi

# Install required Python packages
echo "--- Installing Python packages from requirements.txt ---"
pip install -r requirements.txt

echo "--- ✅ Setup complete! ---"
echo "You can now run the application with: python app_core.py"