import os
import subprocess
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import argparse

# কনফিগারেশন
SITEMAP_FILE = "sitemap.xml"
BASE_URL = "https://kamilhussen24.github.io"
HTML_DIR = "./"
EXCLUDE_FILES = ['404.html']

def delete_old_sitemap():
    """পুরাতন সাইটম্যাপ ডিলিট করুন"""
    try:
        os.remove(SITEMAP_FILE)
        print("♻️ পুরাতন সাইটম্যাপ ডিলিট করা হয়েছে")
    except FileNotFoundError:
        print("⚠️ কোনো পুরাতন সাইটম্যাপ পাওয়া যায়নি")
    except Exception as e:
        print(f"❌ সাইটম্যাপ ডিলিট করতে সমস্যা: {str(e)}")

def get_last_modified(file_path, force_update=False):
    """সর্বশেষ মডিফিকেশন ডেট সংগ্রহ"""
    if force_update:
        return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    
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
    """URL জেনারেশন"""
    relative_path = os.path.relpath(file_path, HTML_DIR)
    
    if file_path.endswith("index.html"):
        dir_path = os.path.dirname(relative_path)
        return f"{BASE_URL}/{dir_path}/".replace("\\", "/").replace("//", "/")
    
    url = os.path.splitext(relative_path)[0].replace("\\", "/")
    return f"{BASE_URL}/{url}"

def generate_sitemap(force_update=False):
    """সম্পূর্ণ নতুন সাইটম্যাপ তৈরি"""
    # পুরাতন সাইটম্যাপ ডিলিট করুন
    delete_old_sitemap()
    
    urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # সকল HTML ফাইল স্ক্যান
    html_files = []
    for root, _, files in os.walk(HTML_DIR):
        for file in files:
            if file.endswith(".html") and file not in EXCLUDE_FILES:
                full_path = os.path.join(root, file)
                html_files.append(full_path)
    
    print(f"🔍 মোট {len(html_files)} HTML ফাইল স্ক্যান করা হয়েছে")
    
    for file_path in html_files:
        loc = generate_url(file_path)
        lastmod = get_last_modified(file_path, force_update)
        
        url = ET.SubElement(urlset, 'url')
        ET.SubElement(url, 'loc').text = loc
        ET.SubElement(url, 'lastmod').text = lastmod
        ET.SubElement(url, 'changefreq').text = 'daily'
        ET.SubElement(url, 'priority').text = '1.0' if loc.endswith('/') else '0.8'
        print(f"➕ যোগ করা হয়েছে: {loc}")
    
    # XML ফাইল সেভ
    xml_str = ET.tostring(urlset, encoding='utf-8')
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent='  ')
    
    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)
    print(f"✅ সফলভাবে নতুন সাইটম্যাপ তৈরি হয়েছে: {SITEMAP_FILE}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--force', action='store_true', help='জোরপূর্বক নতুন সাইটম্যাপ তৈরি করুন')
    args = parser.parse_args()
    
    try:
        generate_sitemap(force_update=args.force)
        print("✨ স্ক্রিপ্ট সফলভাবে সম্পন্ন হয়েছে")
    except Exception as e:
        print(f"☠️ ক্রিটিক্যাল ত্রুটি: {str(e)}")
        exit(1)
