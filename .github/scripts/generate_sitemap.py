import os
import time
import subprocess
import xml.etree.ElementTree as ET
from xml.dom import minidom

# 🔹 কনফিগারেশন
SITEMAP_FILE = "sitemap.xml"
BASE_URL = "https://kamilhussen24.github.io"
HTML_DIR = "./"

# 🔹 Git রুট ডিরেক্টরি খুঁজে বের করা
def get_git_root():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

# 🔹 Git থেকে সঠিক লাস্ট মডিফাইড টাইম পাওয়ার ফাংশন
def get_git_last_modified_time(file_path):
    git_root = get_git_root()
    if not git_root:
        return None
    
    absolute_path = os.path.abspath(file_path)
    relative_path = os.path.relpath(absolute_path, git_root)
    
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", relative_path],
            capture_output=True, text=True, check=True
        )
        git_time = result.stdout.strip()
        return git_time if git_time else None
    except subprocess.CalledProcessError:
        return None

# 🔹 নতুন সাইটম্যাপ XML তৈরি
sitemap = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

# 🔹 মূল পেজ যোগ করা (প্রায়োরিটি ১.০)
index_path = os.path.join(HTML_DIR, "index.html")
if os.path.exists(index_path):
    index_lastmod = get_git_last_modified_time(index_path)
    
    if not index_lastmod:
        index_lastmod = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(os.path.getmtime(index_path)))

    index_url = ET.SubElement(sitemap, "url")
    ET.SubElement(index_url, "loc").text = BASE_URL
    ET.SubElement(index_url, "lastmod").text = index_lastmod
    ET.SubElement(index_url, "priority").text = "1.0"
    ET.SubElement(index_url, "changefreq").text = "daily"

# 🔹 সকল HTML ফাইল প্রসেস করা
for root, _, files in os.walk(HTML_DIR):
    for file in files:
        if file.endswith(".html") and file != "index.html":
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, HTML_DIR).replace("\\", "/")
            url = f"{BASE_URL}/{relative_path}"

            # 🔹 Git থেকে লাস্ট মডিফাইড টাইম
            last_mod = get_git_last_modified_time(file_path)
            
            # 🔹 ফাইল সিস্টেম থেকে টাইম নেওয়া (যদি Git টাইম না পাওয়া যায়)
            if not last_mod:
                file_mtime = os.path.getmtime(file_path)
                last_mod = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(file_mtime))

            # 🔹 XML এ এন্ট্রি যোগ করা
            url_entry = ET.SubElement(sitemap, "url")
            ET.SubElement(url_entry, "loc").text = url
            ET.SubElement(url_entry, "lastmod").text = last_mod
            ET.SubElement(url_entry, "priority").text = "0.8"
            ET.SubElement(url_entry, "changefreq").text = "weekly"

# 🔹 XML ফরম্যাটিং
xml_str = ET.tostring(sitemap, encoding='utf-8')
pretty_xml = minidom.parseString(xml_str).toprettyxml(indent='  ')

# 🔹 ফাইল সেভ করা
with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
    f.write(pretty_xml)

print("✅ সাইটম্যাপ সফলভাবে জেনারেট হয়েছে! প্রতিটি URL-এর আলাদা লাস্টমড ডেট!")
