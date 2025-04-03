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
    """Git কমিট বা ফাইল মডিফিকেশন ডেট সংগ্রহ"""
    # প্রথমে Git থেকে চেষ্টা করুন
    try:
        if not os.path.exists('.git'):
            raise FileNotFoundError("Git repository not initialized")
            
        git_cmd = ['git', 'log', '-1', '--pretty=%cI', '--', file_path]
        result = subprocess.run(git_cmd, capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception as e:
        print(f"Git error for {file_path}: {str(e)}")
    
    # Git থেকে না পেলে ফাইল সিস্টেম থেকে নিন
    try:
        mtime = os.path.getmtime(file_path)
        return datetime.utcfromtimestamp(mtime).strftime('%Y-%m-%dT%H:%M:%SZ')
    except Exception as e:
        print(f"File error for {file_path}: {str(e)}")
        return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

def generate_url(file_path):
    """HTML এক্সটেনশন বাদ ও ইনডেক্স হ্যান্ডলিং"""
    relative_path = os.path.relpath(file_path, HTML_DIR)
    
    if os.path.basename(file_path) == "index.html":
        dir_path = os.path.dirname(relative_path)
        return f"{BASE_URL}/{dir_path}/" if dir_path != "." else f"{BASE_URL}/"
    
    url = os.path.splitext(relative_path)[0].replace("\\", "/")
    return f"{BASE_URL}/{url}"

def build_sitemap():
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
            ET.SubElement(url, 'changefreq').text = 'monthly'
            ET.SubElement(url, 'priority').text = '1.0' if loc.endswith('/') else '0.8'
    
    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(minidom.parseString(ET.tostring(urlset)).toprettyxml(indent='  '))

if __name__ == "__main__":
    try:
        build_sitemap()
        print(f"✅ সাইটম্যাপ তৈরি সম্পূর্ণ! ফাইল: {os.path.abspath(SITEMAP_FILE)}")
    except Exception as e:
        print(f"❌ ত্রুটি: {str(e)}")
        exit(1)
