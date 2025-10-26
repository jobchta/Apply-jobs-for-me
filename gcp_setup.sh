#!/bin/bash

# This script automates the setup of the Wells Fargo Job Application Bot
# on a fresh Debian-based Linux VM (like the default Google Cloud VMs).

echo "--- Starting Automated Setup for Job Application Bot ---"

# --- 1. Update System ---
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# --- 2. Install Google Chrome ---
echo "Installing Google Chrome..."
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt-get update
sudo apt-get install -y google-chrome-stable

# --- 3. Install Python & Pip ---
echo "Installing Python and Pip..."
sudo apt-get install -y python3 python3-pip

# --- 4. Install Selenium ---
echo "Installing Selenium library..."
pip3 install selenium

# --- 5. Install ChromeDriver ---
# This is the tricky part - we need to match the Chrome version.
CHROME_VERSION=$(google-chrome --version | cut -f 3 -d ' ' | cut -d '.' -f 1)
echo "Detected Chrome version: $CHROME_VERSION"

# Note: This URL might become outdated. This is a best-effort attempt to get the right driver.
# You can find the latest at: https://googlechromelabs.github.io/chrome-for-testing/
LATEST_DRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" | jq -r ".versions[] | select(.version | startswith(\"$CHROME_VERSION.\")) | .downloads.chromedriver[0].url")

if [ -z "$LATEST_DRIVER_VERSION" ]; then
    echo "Could not automatically find a matching ChromeDriver version. Please install it manually."
    exit 1
fi

echo "Downloading ChromeDriver from: $LATEST_DRIVER_VERSION"
wget -O chromedriver_linux64.zip $LATEST_DRIVER_VERSION
unzip chromedriver_linux64.zip
rm chromedriver_linux64.zip
# The driver is often in a nested directory, let's find it and move it
CHROME_DRIVER_PATH=$(find . -type f -name "chromedriver")
sudo mv $CHROME_DRIVER_PATH /usr/local/bin/chromedriver
sudo chmod +x /usr/local/bin/chromedriver

echo "--- Setup Complete! ---"
echo "You can now configure the bot by running: python3 setup.py"
echo "Then, run the bot itself with: python3 apply_bot.py"
