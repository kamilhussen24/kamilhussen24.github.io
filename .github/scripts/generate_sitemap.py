import os

SITEMAP_FILE = "sitemap.xml"
BASE_URL = "https://kamilhussen24.github.io"

pages = [
    "",
    "about-me",
    "blog",
    "blog/post/online-scammer-identify-bangla",
    "privacy-policy",
    "terms-of-service"
]

sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''

for page in pages:
    url = f"{BASE_URL}/{page}" if page else BASE_URL
    sitemap_content += f"""
    <url>
        <loc>{url}</loc>
        <lastmod>{os.popen('date -u +"%Y-%m-%dT%H:%M:%SZ"').read().strip()}</lastmod>
        <priority>0.8</priority>
        <changefreq>weekly</changefreq>
    </url>
    """

sitemap_content += "\n</urlset>"

with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
    f.write(sitemap_content)

print("✅ sitemap.xml তৈরি হয়েছে!")
