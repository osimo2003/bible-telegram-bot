import urllib.request
import json

print("📥 Downloading Bible data...")
print("This may take a minute...")

url = "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_kjv.json"

urllib.request.urlretrieve(url, "bible.json")

print("✅ Download complete!")
print("📁 File saved as: bible.json")

with open('bible.json', 'r', encoding='utf-8-sig') as f:
    bible = json.load(f)

print(f"📖 Total books downloaded: {len(bible)}")
print(f"📖 First book: {bible[0]['name']}")
print(f"📖 Last book: {bible[-1]['name']}")
