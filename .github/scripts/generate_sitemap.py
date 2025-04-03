import os
import subprocess
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

# কনফিগারেশন
SITEMAP_FILE = "sitemap.xml"
BASE_URL = "https://kamilhussen24.github.io"
HTML_DIR = "./"

def get_file_lastmod(file_path):
    """Git বা ফাইল সিস্টেম থেকে সঠিক লাস্টমড ডেট সংগ্রহ"""
    try:
        # Git থেকে কমিট তারিখ
        git_cmd = ['git', 'log', '-1', '--pretty=%cI', '--', file_path]
        result = subprocess.run(git_cmd, capture_output=True, text=True)
        if result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    
    # ফাইল সিস্টেম থেকে মডিফিকেশন টাইম (UTC ফরম্যাট)
    mtime = os.path.getmtime(file_path)
    return datetime.utcfromtimestamp(mtime).strftime('%Y-%m-%dT%H:%M:%SZ')

def generate_clean_url(file_path):
    """HTML এক্সটেনশন বাদ দিয়ে ক্লিন URL তৈরি"""
    relative_path = os.path.relpath(file_path, HTML_DIR)
    if relative_path == "index.html":
        return BASE_URL  # রুট URL
    url = os.path.splitext(relative_path)[0].replace('\\', '/')
    return f"{BASE_URL}/{url}"

def build_sitemap():
    urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    
    for root, dirs, files in os.walk(HTML_DIR):
        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file)
                
                # URL জেনারেট
                loc = generate_clean_url(full_path)
                
                # লাস্টমড সংগ্রহ
                lastmod = get_file_lastmod(full_path)
                
                # XML এন্ট্রি তৈরি
                url = ET.SubElement(urlset, 'url')
                ET.SubElement(url, 'loc').text = loc
                ET.SubElement(url, 'lastmod').text = lastmod
                ET.SubElement(url, 'changefreq').text = 'monthly'
                ET.SubElement(url, 'priority').text = '1.0' if loc == BASE_URL else '0.8'
    
    # XML সেভ করুন
    xml_str = ET.tostring(urlset, encoding='utf-8')
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent='  ')
    
    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

if __name__ == "__main__":
    build_sitemap()
    print("✅ সাইটম্যাপ তৈরি সম্পূর্ণ! প্রতিটি URL-এর আলাদা লাস্টমড!")
