# 🌅 Bing Wallpaper App Image Downloader

A simple yet powerful tool to download **Bing Wallpaper App's images** in full resolution — neatly organized into theme folders, with smart deduplication and history tracking.  

---

## ✨ Features

- 📂 **Organized by Theme**  
  Images are saved into folders (e.g., Travel, Space, Dog, Flower) just like the Bing Wallpaper App.  

- 📝 **Readable File Names**  
  Uses the actual **title and copyright text**, not random IDs.  

- 🖼️ **High-Resolution Downloads**  
  Saves **UHD (3840×2160 or max)** for landscape and **1080×1920** for portrait (when available).  

- 🌍 **Multi-Region Support**  
  Fetches wallpapers from all available regions so you don’t miss any exclusives.  
  - Smart deduplication prioritizes English (`en_US`) names while eliminating duplicates, but you can swap priority for another language by moving it to first place in the list of `MARKETS`.  

- 🔄 **History Tracking**  
  Keeps a `downloaded images.txt` log to avoid re-downloading.  
  - Delete images you don’t like — they won’t come back in the next run, get just the new images!  

- 🤖 **Optional AI Images**  
  The script can also fetch Bing’s **AI-generated wallpapers** by enabling them in the config:  

  ```python
  BIC_FILTERS = [True, False]  # enables both filtered (AI) and unfiltered images, AI Images go into the "AI Images" Folder within the theme folder.
  ```
  
  ⚠️ Note: AI images are disabled by default since they often look poor.

---

## 💻 Supported OS

- Windows 11  

---

## 🚀 How to Run

1. Double-click the `.vbs` script.  
   - Opens a cmd window running the Python script.  
   - Shows status.  

2. Images will be downloaded into theme folders in the current directory or the directory path mentioned in `.download_location` file.  

---

## 🔁 Setup Auto run

1. `Win+R` and run `shell:startup`.

2. Create a shortcut to the `.vbs` file with the `/quiet` parameter and put it in here.

---

## 🔍 How’s this Different?

- ✅ Uses **title & copyright** for file name instead of ID.  
- ✅ Retrieves **40 images** for Bing theme from across regions via Bing image API (unlike Bing Theme app api with just 8).  
- ✅ Handles **deduplication smartly** across regions.  
- ✅ Downloads max resolutions of **both landscape & portrait wallpapers**.  

---

## 📌 Todo

- [ ] Download multi-region images for the Theme API (same as Bing image API).  

---

💡 Perfect for anyone who wants to keep **Bing’s stunning wallpapers** while choosing which ones to avoid.  
