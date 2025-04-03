import os
import subprocess
import time

SITEMAP_FILE = "sitemap.xml"
BASE_URL = "https://kamilhussen24.github.io"
HTML_DIR = "./"

# 🔹 নির্দিষ্ট ফাইলের Git থেকে লাস্ট মডিফাইড টাইম বের করার ফাংশন
def get_git_last_modified_time(file_path):
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI", file_path],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None  # যদি Git থেকে ডেট পাওয়া না যায়

# 🔹 সাইটম্যাপ XML তৈরি শুরু
sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>\n'''
sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

# 🔹 মূল ওয়েবসাইটের URL
sitemap_content += f"""  <url>
    <loc>{BASE_URL}</loc>
    <lastmod>{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(os.path.getmtime('index.html')))}</lastmod>
    <priority>1.0</priority>
    <changefreq>daily</changefreq>
  </url>\n"""

# 🔹 HTML ফাইল স্ক্যান করা
for root, _, files in os.walk(HTML_DIR):
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            git_mod_time = get_git_last_modified_time(file_path)

            if git_mod_time is None:
                file_mod_time = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(os.path.getmtime(file_path)))
            else:
                file_mod_time = git_mod_time

            # 🔹 .html বাদ দিয়ে ক্লিন URL তৈরি
            relative_path = os.path.relpath(file_path, HTML_DIR).replace("\\", "/")
            url = f"{BASE_URL}/{relative_path}".replace(".html", "")

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
