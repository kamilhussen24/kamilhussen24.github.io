import os
import subprocess
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

# কনফিগারেশন
SITEMAP_FILE = "sitemap.xml"
BASE_URL = "https://kamilhussen24.github.io"
HTML_DIR = "./"
EXCLUDE_FILES = ['404.html']  # বাদ দেওয়ার ফাইললিস্ট

def get_last_modified(file_path):
    """Git কমিট বা ফাইল মডিফিকেশন ডেট সংগ্রহ"""
    try:
        git_cmd = ['git', 'log', '-1', '--pretty=%cI', '--', file_path]
        result = subprocess.run(git_cmd, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    
    mtime = os.path.getmtime(file_path)
    return datetime.utcfromtimestamp(mtime).strftime('%Y-%m-%dT%H:%M:%SZ')

def generate_url(file_path):
    """HTML এক্সটেনশন বাদ ও ইনডেক্স হ্যান্ডলিং"""
    relative_path = os.path.relpath(file_path, HTML_DIR)
    
    # ইনডেক্স ফাইল বিশেষ হ্যান্ডলিং
    if os.path.basename(file_path) == "index.html":
        dir_path = os.path.dirname(relative_path)
        if dir_path == ".":
            return BASE_URL + "/"
        return f"{BASE_URL}/{dir_path}/"
    
    # সাধারণ HTML ফাইল প্রসেসিং
    url = os.path.splitext(relative_path)[0]
    url = url.replace("\\", "/")  # উইন্ডোজ পাথ ফিক্স
    return f"{BASE_URL}/{url}"

def build_sitemap():
    urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    
    for root, dirs, files in os.walk(HTML_DIR):
        for file in files:
            if file in EXCLUDE_FILES:
                continue
                
            if file.endswith(".html"):
                full_path = os.path.join(root, file)
                
                # URL জেনারেট
                loc = generate_url(full_path)
                
                # লাস্ট মডিফাইড ডেট
                lastmod = get_last_modified(full_path)
                
                # XML নোড তৈরি
                url = ET.SubElement(urlset, 'url')
                ET.SubElement(url, 'loc').text = loc
                ET.SubElement(url, 'lastmod').text = lastmod
                ET.SubElement(url, 'changefreq').text = 'monthly'
                ET.SubElement(url, 'priority').text = '1.0' if loc.endswith('/') else '0.8'
    
    # XML ফাইল সেভ
    xml_str = ET.tostring(urlset, encoding='utf-8')
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent='  ')
    
    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

if __name__ == "__main__":
    build_sitemap()
    print("✅ সম্পূর্ণ সাইটম্যাপ তৈরি হয়েছে! প্রতিটি URL ইউনিক লাস্টমড সহ!")
