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

def get_git_last_commit_date(file_path):
    """Git থেকে ফাইলের শেষ কমিটের তারিখ বের করুন"""
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--pretty=%cI', '--', file_path],
            capture_output=True, text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        else:
            return None
    except Exception as e:
        print(f"⚠️ Git Error: {str(e)}")
        return None

def get_file_modification_date(file_path):
    """ফাইল সিস্টেম থেকে মডিফিকেশন ডেট"""
    mtime = os.path.getmtime(file_path)
    return datetime.utcfromtimestamp(mtime).strftime('%Y-%m-%dT%H:%M:%SZ')

def generate_url(file_path):
    """URL জেনারেশন"""
    relative_path = os.path.relpath(file_path, HTML_DIR)
    
    if file_path.endswith("index.html"):
        dir_path = os.path.dirname(relative_path)
        return f"{BASE_URL}/{dir_path}/".replace("//", "/")
    
    url = os.path.splitext(relative_path)[0].replace("\\", "/")
    return f"{BASE_URL}/{url}"

def generate_sitemap():
    """প্রতিটি ফাইলের জন্য আলাদা ডেট সহ সাইটম্যাপ তৈরি"""
    urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    
    for root, _, files in os.walk(HTML_DIR):
        for file in files:
            if file in EXCLUDE_FILES or not file.endswith(".html"):
                continue
                
            full_path = os.path.join(root, file)
            
            # Git থেকে ডেট নিন (যদি কমিট করা থাকে)
            git_date = get_git_last_commit_date(full_path)
            
            # না পেলে ফাইল সিস্টেম থেকে নিন
            lastmod = git_date if git_date else get_file_modification_date(full_path)
            
            loc = generate_url(full_path)
            
            url = ET.SubElement(urlset, 'url')
            ET.SubElement(url, 'loc').text = loc
            ET.SubElement(url, 'lastmod').text = lastmod
            ET.SubElement(url, 'changefreq').text = 'monthly'
            ET.SubElement(url, 'priority').text = '1.0' if loc.endswith('/') else '0.8'
            print(f"✅ Processed: {loc} - Last Modified: {lastmod}")
    
    # XML সেভ করুন
    xml_str = ET.tostring(urlset, encoding='utf-8')
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent='  ')
    
    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)
    print("🎉 সাইটম্যাপ সফলভাবে তৈরি হয়েছে!")

if __name__ == "__main__":
    generate_sitemap()
