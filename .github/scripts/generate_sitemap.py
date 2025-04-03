import os
import subprocess
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

# কনফিগারেশন
SITEMAP_FILE = "sitemap.xml"
BASE_URL = "https://kamilhussen24.github.io"
HTML_DIR = "./"
EXCLUDE_FILES = ['404.html']

def get_last_modified(file_path):
    """Git বা ফাইল সিস্টেম থেকে সর্বশেষ পরিবর্তনের সময়"""
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--pretty=%cI', '--', file_path],
            capture_output=True, text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    
    mtime = os.path.getmtime(file_path)
    return datetime.utcfromtimestamp(mtime).strftime('%Y-%m-%dT%H:%M:%SZ')

def generate_url(file_path):
    """HTML এক্সটেনশন ছাড়া URL তৈরি"""
    relative_path = os.path.relpath(file_path, HTML_DIR)
    
    # ইনডেক্স ফাইল হ্যান্ডলিং
    if file_path.endswith("index.html"):
        dir_path = os.path.dirname(relative_path)
        return f"{BASE_URL}/{dir_path}/".replace("\\", "/").replace("//", "/")
    
    # সাধারণ HTML ফাইল
    url = os.path.splitext(relative_path)[0].replace("\\", "/")
    return f"{BASE_URL}/{url}"

def generate_sitemap():
    urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    
    for root, _, files in os.walk(HTML_DIR):
        for file in files:
            if file in EXCLUDE_FILES or not file.endswith(".html"):
                continue
                
            full_path = os.path.join(root, file)
            loc = generate_url(full_path)
            lastmod = get_last_modified(full_path)
            
            url = ET.SubElement(urlset, 'url')
            ET.SubElement(url, 'loc').text = loc
            ET.SubElement(url, 'lastmod').text = lastmod
            ET.SubElement(url, 'changefreq').text = 'daily'
            ET.SubElement(url, 'priority').text = '1.0' if loc.endswith('/') else '0.8'
    
    # XML ফাইল সেভ
    xml_str = ET.tostring(urlset, encoding='utf-8')
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent='  ')
    
    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

if __name__ == "__main__":
    try:
        generate_sitemap()
        print("✅ সাইটম্যাপ সফলভাবে জেনারেট হয়েছে!")
    except Exception as e:
        print(f"❌ ত্রুটি: {str(e)}")
        exit(1)
