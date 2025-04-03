import os
import subprocess
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

# মেইন কনফিগারেশন
SITEMAP_FILE = "sitemap.xml"
BASE_URL = "https://kamilhussen24.github.io"
HTML_DIR = "./"
EXCLUDE_FILES = ['404.html','kamil.html']
EXCLUDE_DIRS = ['blog', 'experimental']

def get_last_modified(file_path):
    """Git কমিট বা ফাইল সিস্টেম থেকে ডেট সংগ্রহ"""
    try:
        # Git থেকে শেষ কমিটের তারিখ
        result = subprocess.run(
            ['git', 'log', '-1', '--pretty=%cI', '--', file_path],
            capture_output=True, text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    
    # ফাইল মডিফিকেশন ডেট
    mtime = os.path.getmtime(file_path)
    return datetime.utcfromtimestamp(mtime).strftime('%Y-%m-%dT%H:%M:%SZ')

def generate_url(file_path):
    """URL জেনারেশন"""
    relative_path = os.path.relpath(file_path, HTML_DIR)
    
    # মেইন পেজ (index.html) হ্যান্ডলিং
    if file_path.endswith("index.html"):
        dir_path = os.path.dirname(relative_path)
        # ডাবল স্ল্যাশ সমস্যা সমাধান
        if dir_path in (".", ""):
            return f"{BASE_URL}/"
        return f"{BASE_URL}/{dir_path}/"
    
    # সাধারণ পেজ
    url = os.path.splitext(relative_path)[0].replace("\\", "/")
    return f"{BASE_URL}/{url}"

def generate_sitemap():
    """সাইটম্যাপ জেনারেটর"""
    urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    
    for root, _, files in os.walk(HTML_DIR):
        for file in files:
            if file in EXCLUDE_FILES or not file.endswith(".html"):
                continue
                
            full_path = os.path.join(root, file)
            loc = generate_url(full_path)
            
            # প্রায়োরিটি এবং চেঞ্জফ্রিকোয়েন্সি সেটিং
            is_main_page = loc.endswith('/')
            priority = "1.0" if is_main_page else "0.8"
            changefreq = "weekly"
            
            url = ET.SubElement(urlset, 'url')
            ET.SubElement(url, 'loc').text = loc
            ET.SubElement(url, 'lastmod').text = get_last_modified(full_path)
            ET.SubElement(url, 'changefreq').text = changefreq
            ET.SubElement(url, 'priority').text = priority
    
    # XML ফাইল সেভ
    xml_str = ET.tostring(urlset, encoding='utf-8')
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent='  ')
    
    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

if __name__ == "__main__":
    generate_sitemap()
