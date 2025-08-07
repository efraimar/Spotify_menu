# Spotify-Style Song Search App

A simple Python desktop application that allows you to search and explore songs from a custom music database, inspired by the Spotify search experience.

## 📦 Features

- Search by song name, album name, or lyrics (real-time filtering)
- Scrollable view of all songs in a selected album
- Full lyrics display for any selected song
- Shows album name and song duration
- Built-in GUI with Tkinter
- Clean and minimal design

## 🧱 Tech Stack

- **Python**
- **Tkinter** – for GUI
- **pandas** – for efficient data management

## 📂 File Structure

- `Spotify_menu.py` – Main application logic and GUI
- `Pink_Floyd_DB.TXT` – Sample music database in a structured text format

## 📄 Data Format

The `.TXT` file includes song information using markers:

- Lines starting with `#` indicate a new album and year  
  Format: `#Album Name::Year`
  
- Lines starting with `*` indicate a new song  
  Format: `*Song Name::Composer::Duration::First line of lyrics`

- Following lines are continued lyrics

You can replace this file with your own formatted database to use different artists or genres.

## 🚀 Getting Started

1. Clone the repo:
   ```bash
   git clone https://github.com/efraimar/Spotify_menu.git
   cd Spotify_menu
