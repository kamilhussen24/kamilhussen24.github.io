import os
import requests
from datetime import datetime

# আপনার ওয়েবসাইটের মূল লিংক
SITE_URL = "https://kamilhussen24.github.io"

# সাইটম্যাপ ফাইলের নাম
SITEMAP_FILE = "sitemap.xml"

# নতুন পোস্ট লিস্ট
NEW_POSTS = [
    "/blog/post/online-scammer-identify-bangla",
    "/about-me",
    "/privacy-policy",
    "/blog",
    "/terms-of-service"
]

# বর্তমান তারিখ ISO 8601 ফরম্যাটে
current_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")

# নতুন সাইটম্যাপ XML তৈরি করা
sitemap_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''

# প্রতিটি লিংক অ্যাড করা
for post in NEW_POSTS:
    sitemap_content += f'''    <url>
        <loc>{SITE_URL}{post}</loc>
        <lastmod>{current_date}</lastmod>
        <priority>0.80</priority>
        <changefreq>weekly</changefreq>
    </url>\n'''

# সাইটম্যাপ শেষ করা
sitemap_content += "</urlset>"

# ফাইল সেভ করা
with open(SITEMAP_FILE, "w", encoding="utf-8") as file:
    file.write(sitemap_content)

print(f"✅ {SITEMAP_FILE} সফলভাবে আপডেট হয়েছে!")
