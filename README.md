# Public Logo Assets

This folder is intended to be hosted in a **Public GitHub Repository**.

## Instructions:
1. Create a **New Repository** on GitHub (e.g., named `tv-assets` or `tv-logos`).
2. Make sure to select **Public** (not Private).
3. Upload your logo images (PNG/JPG) to this folder.
   - **Note:** Images will be automatically optimized to be under **60KB**.
4. Once uploaded, click on an image on GitHub, right-click "Raw" or the image itself, and select "Copy Image Link".
5. The link will look like: 
   `https://raw.githubusercontent.com/YourUsername/tv-assets/main/channel_name.png`
6. Use this link in your `playlist.csv` or `playlist.m3u`.

## Auto-Optimization
This repository uses a GitHub Action to automatically resize and compress images that exceed **60KB**.
- If you upload a large image (e.g., 5MB), it will be resized/compressed to < 60KB automatically.
- Check the "Actions" tab to see the process.

## Why Separate Repo?
- Takes load off your App Source Code.
- Allows the App Code to remain **Private** while Images remain **Public** (required for the app to load them).
