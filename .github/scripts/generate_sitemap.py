import os
import time
import subprocess
import xml.etree.ElementTree as ET
from xml.dom import minidom

# 🔹 কনফিগারেশন
SITEMAP_FILE = "sitemap.xml"
BASE_URL = "https://kamilhussen24.github.io"
HTML_DIR = "./"

def get_git_root():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def get_git_last_modified_time(file_path):
    git_root = get_git_root()
    if not git_root:
        return None
    
    try:
        file_abs = os.path.abspath(file_path)
        relative_path = os.path.relpath(file_abs, git_root)
        
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", relative_path],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip() or None
    except Exception:
        return None

def generate_clean_url(relative_path):
    # 🔹 .html এক্সটেনশন রিমুভ করা
    path_without_ext = os.path.splitext(relative_path)[0]
    # 🔹 স্ল্যাশ নরমালাইজেশন
    return f"{BASE_URL}/{path_without_ext}".replace("\\", "/")

# 🔹 সাইটম্যাপ জেনারেশন শুরু
sitemap = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

# 🔹 সকল HTML ফাইল প্রসেসিং
for root, _, files in os.walk(HTML_DIR):
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            
            # 🔹 লাস্ট মডিফাই ডেট সংগ্রহ
            last_mod = get_git_last_modified_time(file_path)
            if not last_mod:
                mtime = os.path.getmtime(file_path)
                last_mod = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(mtime))
            
            # 🔹 ক্লিন URL জেনারেট
            relative_path = os.path.relpath(file_path, HTML_DIR)
            clean_url = generate_clean_url(relative_path)
            
            # 🔹 XML নোড তৈরি
            url_node = ET.SubElement(sitemap, "url")
            ET.SubElement(url_node, "loc").text = clean_url
            ET.SubElement(url_node, "lastmod").text = last_mod
            ET.SubElement(url_node, "priority").text = "0.8" if "index.html" not in file else "1.0"
            ET.SubElement(url_node, "changefreq").text = "weekly"

# 🔹 XML ফরম্যাটিং এবং সেভ
xml_str = ET.tostring(sitemap, encoding='utf-8')
pretty_xml = minidom.parseString(xml_str).toprettyxml(indent='  ')

with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
    f.write(pretty_xml)

print("✅ সাইটম্যাপ সফলভাবে জেনারেট হয়েছে! প্রতিটি URL ইউনিক লাস্টমড সহ!")
