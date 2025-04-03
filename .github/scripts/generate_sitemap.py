import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

# 🔹 কনফিগারেশন
SITEMAP_FILE = "sitemap.xml"
BASE_URL = "https://kamilhussen24.github.io"
HTML_DIR = "./"  # যেখানে HTML ফাইল আছে
TIMEZONE_OFFSET = "+06:00"  # বাংলাদেশ টাইমজোন

# 🔹 ফাইল থেকে লাস্ট মডিফাই টাইম বের করা
def get_file_last_modified_time(file_path):
    mod_time = os.path.getmtime(file_path)
    return datetime.utcfromtimestamp(mod_time).strftime('%Y-%m-%dT%H:%M:%S') + TIMEZONE_OFFSET

# 🔹 XML সাইটম্যাপ তৈরি করা
sitemap = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

# 🔹 HTML ফাইল খুঁজে বের করা
for root, _, files in os.walk(HTML_DIR):
    for file in files:
        if file.endswith(".html"):  
            file_path = os.path.join(root, file)

            # 🔹 ফাইলের লাস্ট মডিফাই টাইম বের করা
            last_mod_time = get_file_last_modified_time(file_path)

            # 🔹 রিলেটিভ URL তৈরি করা (".html" ছাড়া ও সাথে)
            relative_path = os.path.relpath(file_path, HTML_DIR).replace("\\", "/")
            url_with_html = f"{BASE_URL}/{relative_path}"
            url_without_html = url_with_html.replace(".html", "")

            # 🔹 XML-এ প্রথম URL বসানো (.html ছাড়া)
            url_entry = ET.SubElement(sitemap, "url")
            ET.SubElement(url_entry, "loc").text = url_without_html
            ET.SubElement(url_entry, "lastmod").text = last_mod_time
            ET.SubElement(url_entry, "priority").text = "1.0" if "index" in file else "0.8"
            ET.SubElement(url_entry, "changefreq").text = "weekly"

            # 🔹 XML-এ দ্বিতীয় URL বসানো (.html সহ)
            url_entry_html = ET.SubElement(sitemap, "url")
            ET.SubElement(url_entry_html, "loc").text = url_with_html
            ET.SubElement(url_entry_html, "lastmod").text = last_mod_time
            ET.SubElement(url_entry_html, "priority").text = "1.0" if "index" in file else "0.8"
            ET.SubElement(url_entry_html, "changefreq").text = "weekly"

# 🔹 XML ফরম্যাট সুন্দর করা
xml_string = ET.tostring(sitemap, encoding="utf-8")
xml_pretty = minidom.parseString(xml_string).toprettyxml(indent="  ")

# 🔹 ফাইল সংরক্ষণ
with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
    f.write(xml_pretty)

print("✅ সফলভাবে সাইটম্যাপ তৈরি হয়েছে!")
