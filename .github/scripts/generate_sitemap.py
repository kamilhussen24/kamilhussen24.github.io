import os
import subprocess
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

# কনফিগারেশন
SITEMAP_FILE = "sitemap.xml"
BASE_URL = "https://kamilhussen24.github.io"
HTML_DIR = "./"
EXCLUDE_FILES = ['404.html']  # বাদ দিতে চাইলে ফাইলনেম এখানে যোগ করুন

def get_git_history_date(file_path):
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--pretty=%cI', '--', file_path],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except Exception:
        return None

def get_file_mod_date(file_path):
    timestamp = os.path.getmtime(file_path)
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%SZ')

def generate_clean_url(file_path):
    relative_path = os.path.relpath(file_path, start=HTML_DIR)
    url_path = os.path.splitext(relative_path)[0]
    url_path = url_path.replace(os.path.sep, '/')
    return f"{BASE_URL}/{url_path}"

def generate_sitemap():
    urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    
    for root, _, files in os.walk(HTML_DIR):
        for file in files:
            if file.endswith('.html') and file not in EXCLUDE_FILES:
                full_path = os.path.join(root, file)
                
                # URL জেনারেট
                loc = generate_clean_url(full_path)
                
                # লাস্ট মডিফাই ডেট
                lastmod = get_git_history_date(full_path)
                if not lastmod:
                    lastmod = get_file_mod_date(full_path)
                
                # XML নোড তৈরি
                url = ET.SubElement(urlset, 'url')
                ET.SubElement(url, 'loc').text = loc
                ET.SubElement(url, 'lastmod').text = lastmod
                ET.SubElement(url, 'changefreq').text = 'monthly'
                ET.SubElement(url, 'priority').text = '0.8' if 'index' not in file else '1.0'
    
    # XML ফরম্যাটিং
    xml_str = ET.tostring(urlset, encoding='utf-8')
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent='  ')
    
    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

if __name__ == "__main__":
    generate_sitemap()
    print("✅ সাইটম্যাপ সফলভাবে তৈরি হয়েছে! ফাইল চেক করুন ->", SITEMAP_FILE)
