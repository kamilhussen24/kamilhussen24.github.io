import os
import time
import subprocess
import xml.etree.ElementTree as ET
from xml.dom import minidom

# 🔹 কনফিগারেশন সেটআপ
SITEMAP_FILE = "sitemap.xml"
BASE_URL = "https://kamilhussen24.github.io"
HTML_DIR = "./"  # HTML ফাইল যেখানে আছে

# 🔹 নির্দিষ্ট ফাইলের Git থেকে লাস্ট মডিফাই টাইম বের করা
def get_git_last_modified_time(file_path):
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI", file_path],
            capture_output=True, text=True, check=True
        )
        git_time = result.stdout.strip()
        return git_time if git_time else None
    except subprocess.CalledProcessError:
        return None

# 🔹 নতুন সাইটম্যাপ XML তৈরি
sitemap = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

# 🔹 সমস্ত HTML ফাইল স্ক্যান করা এবং সঠিক লাস্ট মডিফাইড ডেট সেট করা
for root, _, files in os.walk(HTML_DIR):
    for file in files:
        if file.endswith(".html"):  
            file_path = os.path.join(root, file)

            # 🔹 Git থেকে লাস্ট মডিফাইড টাইম নেওয়ার চেষ্টা করবো
            last_mod_time = get_git_last_modified_time(file_path)

            # 🔹 যদি Git থেকে না পাওয়া যায়, তবে ফাইল সিস্টেমের লাস্ট মডিফাইড টাইম নেবো
            if not last_mod_time:
                last_mod_time = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(os.path.getmtime(file_path)))

            # 🔹 রিলেটিভ পাথ থেকে ক্লিন URL তৈরি
            relative_path = os.path.relpath(file_path, HTML_DIR).replace("\\", "/")
            url = f"{BASE_URL}/{relative_path}"

            # 🔹 XML এ লাস্ট মডিফাই তথ্য সহ URL যোগ করা
            url_entry = ET.SubElement(sitemap, "url")
            ET.SubElement(url_entry, "loc").text = url
            ET.SubElement(url_entry, "lastmod").text = last_mod_time
            ET.SubElement(url_entry, "priority").text = "0.8" if file != "index.html" else "1.0"
            ET.SubElement(url_entry, "changefreq").text = "weekly"

# 🔹 XML সুন্দরভাবে ফরম্যাট করা
xml_string = ET.tostring(sitemap, encoding="utf-8")
xml_pretty = minidom.parseString(xml_string).toprettyxml(indent="  ")

# 🔹 সাইটম্যাপ ফাইল সংরক্ষণ করা
with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
    f.write(xml_pretty)

print("✅ sitemap.xml সফলভাবে আপডেট হয়েছে!")
