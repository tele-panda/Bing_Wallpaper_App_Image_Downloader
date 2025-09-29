import requests
from pathlib import Path
import re
import itertools
import asyncio
import threading

# ---------------------------
# Configuration
# ---------------------------
BING_THEME_DIR = Path("Bing")
TRACK_FILE = Path("downloaded images.txt")  # tracking file in script directory
MARKETS = ["en-US", "ja-JP", "en-AU", "en-GB", "de-DE", "en-NZ", "en-CA",
           "en-IN", "fr-FR", "fr-CA", "it-IT", "es-ES", "pt-BR", "en-ROW"]

BING_WALLPAPER_URL = "https://www.bing.com/HPImageArchive.aspx"
BING_DOMAIN = "https://www.bing.com"
BING_THEME_WALLPAPER_URL = "https://services.bingapis.com/ge-apps/api/v2/bwc/hpimages"

THEMES = ["Bing", "Abstract", "Cat", "Dog", "Flower", "Ocean", "Space", "Travel", "Wild Animal"]

BIC_FILTERS = [True]  # True = AI filtered, False = AI unfiltered.
# You can add both [True, False] to get all images, AI images go into a separate folder. AI images look awful btw.

bing_downloaded = 0
bing_skipped = 0
theme_downloaded = 0
theme_skipped = 0

# ---------------------------
# Utility Functions
# ---------------------------
spinner_cycle = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
_spinner_running = False
_loop = None
_task = None

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def read_tracking():
    lines = []
    ids = set()
    if TRACK_FILE.exists():
        with TRACK_FILE.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    lines.append(line)
                    ids.add(line.split("  |  ")[1])
    return set(lines), ids

def append_tracking(name, id_val):
    with TRACK_FILE.open("a", encoding="utf-8") as f:
        f.write(f"{name}  |  {id_val}\n")

def download_image(url, filepath):
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(filepath, "wb") as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)
      
async def _spinner_loop():
    """Internal loop for spinner animation."""
    global _spinner_running
    while _spinner_running:
        symbol = next(spinner_cycle)
        print(f"\rSkipping {symbol} ", end="", flush=True)
        await asyncio.sleep(0.1)
    print("\r", end="", flush=True)  # clear line when stopped

def show_spinner(state: bool):
    """Sync-friendly spinner toggle."""
    global _spinner_running, _loop, _task

    if state and not _spinner_running:
        _spinner_running = True
        if _loop is None:
            _loop = asyncio.new_event_loop()
            threading.Thread(target=_loop.run_forever, daemon=True).start()
        _task = asyncio.run_coroutine_threadsafe(_spinner_loop(), _loop)

    elif not state and _spinner_running:
        _spinner_running = False
        if _task:
            _task = None

# ---------------------------
# Bing Image API
# ---------------------------
def fetch_bing_images():
    BING_THEME_DIR.mkdir(exist_ok=True)
    seen, seen_ids = read_tracking()
    global bing_downloaded
    global bing_skipped

    for market in MARKETS:
        for idx in range(8):  # idx 0-7
            params = {"format": "js", "idx": idx, "n": 8, "mkt": market}
            try:
                resp = requests.get(BING_WALLPAPER_URL, params=params)
                resp.raise_for_status()
                data = resp.json()
                for img in data.get("images", []):
                    urlbase = img["urlbase"]
                    copyright_text = img.get("copyright", img.get("copyrighttext", "Unknown"))
                    image_id = urlbase.split("_")[0].split("id=")[-1]

                    if image_id in seen_ids:
                        bing_skipped += 1
                        # print(f"Skipping existing image: {BING_DIR} / {copyright_text}")
                        show_spinner(True)
                        continue
                    show_spinner(False)
                    for res in ["_UHD.jpg", "_1080x1920.jpg"]:
                        filename = f"{sanitize_filename(copyright_text)}{res}"
                        filepath = BING_THEME_DIR / filename
                        if filepath.exists():
                            bing_skipped += 1
                            # print(f"Skipping existing image: {filepath}")
                            show_spinner(True)
                            continue
                        show_spinner(False)
                        download_image(f"{BING_DOMAIN}{urlbase}{res}", filepath)
                    append_tracking(f"{BING_THEME_DIR} / {copyright_text}", image_id)
                    seen.add(f"{BING_THEME_DIR} / {copyright_text}  |  {image_id}")
                    seen_ids.add(image_id)
                    bing_downloaded += 1
                    print(f"Downloaded: {BING_THEME_DIR} / {copyright_text}")
            except Exception as e:
                print(f"Error fetching homepage images for market {market} idx {idx}: {e}")
    show_spinner(False)

# ---------------------------
# Bing Wallpaper API
# ---------------------------
def fetch_other_theme_images():
    seen, seen_ids = read_tracking()
    global theme_downloaded
    global theme_skipped

    for theme in THEMES:
        if theme.lower() in ["bing"]:
            continue  # skip Bing theme
        theme_dir = Path(theme)
        theme_dir.mkdir(exist_ok=True)
        for bic in BIC_FILTERS:
            img_dir = theme_dir if bic else theme_dir / "AI Images"
            img_dir.mkdir(exist_ok=True)
            try:
                params = {
                    "mkt": "en-US",
                    "theme": theme.lower(),
                    "defaultBrowser": "ME",
                    "IsBicFilterEnabled": str(bic)
                }
                resp = requests.get(BING_THEME_WALLPAPER_URL, params=params)
                resp.raise_for_status()
                data = resp.json()
                for img in data.get("images", []):
                    urlbase = img["urlbase"]
                    title = img.get("title", "Unknown")
                    copyright_text = img.get("copyrighttext", "Unknown")
                    id_val = urlbase.split("id=")[-1]

                    imagename = f"{sanitize_filename(title)} ({sanitize_filename(copyright_text)})"
                    if id_val in seen_ids:
                        theme_skipped += 1
                        # print(f"Skipping existing image: {img_dir} / {imagename}")
                        show_spinner(True)
                        continue
                    show_spinner(False)
                    filepath = (img_dir / imagename).with_suffix(".jpg")
                    if filepath.exists():
                        theme_skipped += 1
                        # print(f"Skipping existing image: {img_dir} / {imagename}")
                        show_spinner(True)
                        continue
                    show_spinner(False)

                    download_image(urlbase, filepath)
                    print(f"Downloaded: {img_dir} / {imagename}")
                    append_tracking(f"{img_dir} / {imagename}", id_val)
                    seen.add(f"{img_dir} / {imagename}  |  {id_val}")
                    seen_ids.add(id_val)
                    theme_downloaded += 1
            except Exception as e:
                print(f"Error fetching theme {theme} bic {bic}: {e}")
    show_spinner(False)

# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    fetch_bing_images()
    fetch_other_theme_images()
    print()
    print(f"Bing Theme images: Downloaded {bing_downloaded}, Skipped {bing_skipped}")
    print(f"Other Theme images: Downloaded {theme_downloaded}, Skipped {theme_skipped}")
    print("All done. Press Enter to close.")
    input()
