import os
import time
import xml.etree.ElementTree as ET

# 🔹 সাইটম্যাপ ফাইলের নাম
SITEMAP_FILE = "sitemap.xml"
BASE_URL = "https://kamilhussen24.github.io"

# 🔹 HTML ফাইল সংরক্ষিত ফোল্ডার (প্রোজেক্টের মূল ফোল্ডার সেট করুন)
HTML_DIR = "./"  # রুট ডিরেক্টরি থেকে শুরু হবে

# 🔹 সাইটম্যাপ XML স্ট্রাকচার তৈরি
sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>\n'''
sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

# 🔹 সকল HTML ফাইল খুঁজে বের করা
html_files = []
for root, _, files in os.walk(HTML_DIR):
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            html_files.append(file_path)

# 🔹 সাইটের মূল পৃষ্ঠার এন্ট্রি (priority বাড়ানো)
sitemap_content += f"""  <url>
    <loc>{BASE_URL}</loc>
    <lastmod>{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(os.path.getmtime('index.html')))}</lastmod>
    <priority>1.0</priority>
    <changefreq>daily</changefreq>
  </url>\n"""

# 🔹 প্রতিটি HTML ফাইলের জন্য সাইটম্যাপ এন্ট্রি তৈরি করা
for file_path in html_files:
    file_mod_time = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(os.path.getmtime(file_path)))

    # 🔹 ইউআরএল তৈরি করা (ডিরেক্টরি স্ট্রাকচার ধরে)
    relative_path = os.path.relpath(file_path, HTML_DIR).replace("\\", "/")
    url = f"{BASE_URL}/{relative_path}".replace(".html", "")  # 🔹 .html সরানো

    sitemap_content += f"""  <url>
    <loc>{url}</loc>
    <lastmod>{file_mod_time}</lastmod>
    <priority>0.8</priority>
    <changefreq>weekly</changefreq>
  </url>\n"""

sitemap_content += '</urlset>'

# 🔹 ফাইল লেখার মাধ্যমে সাইটম্যাপ তৈরি
with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
    f.write(sitemap_content)

print("✅ sitemap.xml সফলভাবে আপডেট হয়েছে!")
