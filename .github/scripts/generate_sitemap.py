import os
import time

# 📁 যেই ফোল্ডার থেকে HTML ফাইলগুলো সংগ্রহ করা হবে
ROOT_DIR = "path/to/your/html/files"  # 🔄 এখানে আপনার প্রকৃত path দিন

# 🌍 সাইটের বেস URL (আপনার GitHub Pages লিংক)
BASE_URL = "https://kamilhussen24.github.io/"

# 📄 সাইটম্যাপ ফাইল
SITEMAP_FILE = "sitemap.xml"

# 🌐 সাইটম্যাপের টেমপ্লেট
SITEMAP_HEADER = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

SITEMAP_FOOTER = "</urlset>"

def get_last_modified(file_path):
    """ 🔄 ফাইলের লাস্ট মডিফাই তারিখ সংগ্রহ করা """
    timestamp = os.path.getmtime(file_path)  # ⏳ Unix timestamp
    return time.strftime('%Y-%m-%dT%H:%M:%S+06:00', time.localtime(timestamp))  # 🕒 BD Timezone

def generate_sitemap():
    urls = []

    # 📂 সব HTML ফাইল সংগ্রহ করা
    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file)
                last_modified = get_last_modified(full_path)

                # 🌍 URL তৈরি করা (".html" বাদ দিয়ে)
                relative_path = os.path.relpath(full_path, ROOT_DIR).replace("\\", "/")
                url = BASE_URL + relative_path.replace(".html", "")

                # 📝 সাইটম্যাপে URL যুক্ত করা
                urls.append(f"""
    <url>
        <loc>{url}</loc>
        <lastmod>{last_modified}</lastmod>
        <priority>0.8</priority>
        <changefreq>weekly</changefreq>
    </url>""")

    # 🏁 XML ফাইল তৈরি করা
    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write(SITEMAP_HEADER + "\n".join(urls) + SITEMAP_FOOTER)

    print(f"✅ সাইটম্যাপ তৈরি হয়েছে: {SITEMAP_FILE}")

# 🔥 স্ক্রিপ্ট রান করা
if __name__ == "__main__":
    generate_sitemap()
