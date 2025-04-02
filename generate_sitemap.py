import os
import time

BASE_URL = "https://kamilhussen24.github.io"

# সাইটের লিংক এবং পাথ সেটআপ
pages = [
    "/",
    "/about-me",
    "/privacy-policy",
    "/terms-of-service",
    "/blog",
]

# অটোমেটিক পোস্ট লিস্ট বের করা (blog/post ফোল্ডারের সব HTML ফাইল)
blog_dir = "blog/post"
if os.path.exists(blog_dir):
    for file in os.listdir(blog_dir):
        if file.endswith(".html"):
            pages.append(f"/blog/post/{file}")

# সময় সেটআপ (Google-এর জন্য সঠিক ফরম্যাট)
timestamp = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())

# Sitemap.xml তৈরি করা
sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for page in pages:
    sitemap_content += f'    <url>\n        <loc>{BASE_URL}{page}</loc>\n        <lastmod>{timestamp}</lastmod>\n        <changefreq>weekly</changefreq>\n        <priority>0.80</priority>\n    </url>\n'
sitemap_content += "</urlset>"

# ফাইল সংরক্ষণ
with open("sitemap.xml", "w") as f:
    f.write(sitemap_content)

print("✅ Sitemap.xml আপডেট সম্পন্ন!")
