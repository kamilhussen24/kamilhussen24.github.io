import os
import subprocess
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import fnmatch  # নতুন ইম্পোর্ট

# মেইন কনফিগারেশন
SITEMAP_FILE = "sitemap.xml"
BASE_URL = "https://kamilhussen24.github.io"
HTML_DIR = "./"
EXCLUDE_FILES = ['404.html', 'kamil.html', 'temp/*']
EXCLUDE_DIRS = ['private', 'experimental']

def get_last_modified(file_path):
    """Git কমিট বা ফাইল সিস্টেম থেকে ডেট সংগ্রহ"""
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
        if dir_path in (".", ""):
            return f"{BASE_URL}/"
        return f"{BASE_URL}/{dir_path}/"
    
    url = os.path.splitext(relative_path)[0].replace("\\", "/")
    return f"{BASE_URL}/{url}"

def generate_sitemap():
    """সাইটম্যাপ জেনারেটর"""
    urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    
    for root, dirs, files in os.walk(HTML_DIR):
        # ডিরেক্টরি এক্সক্লুড
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, HTML_DIR)
            
            # এক্সক্লুড চেক #1: সরাসরি ফাইলনেম
            if file in EXCLUDE_FILES:
                print(f"⏩ এক্সক্লুড করা হয়েছে: {file}")
                continue
                
            # এক্সক্লুড চেক #2: Wildcard প্যাটার্ন
            if any(fnmatch.fnmatch(file, pattern) for pattern in EXCLUDE_FILES if '*' in pattern):
                print(f"⏩ প্যাটার্ন ম্যাচ: {file}")
                continue
                
            # এক্সক্লুড চেক #3: রিলেটিভ পাথ
            if any(relative_path.startswith(ex_dir) for ex_dir in EXCLUDE_DIRS):
                print(f"⏩ এক্সক্লুড ফোল্ডার: {relative_path}")
                continue
                
            # এক্সক্লুড চেক #4: ফুল পাথ প্যাটার্ন (যেমন: temp/*)
            if any(fnmatch.fnmatch(relative_path, pattern) for pattern in EXCLUDE_FILES):
                print(f"⏩ পাথ প্যাটার্ন ম্যাচ: {relative_path}")
                continue
                
            loc = generate_url(file_path)
            
            is_main_page = loc.endswith('/')
            priority = "1.0" if is_main_page else "0.8"
            changefreq = "weekly"
            
            url = ET.SubElement(urlset, 'url')
            ET.SubElement(url, 'loc').text = loc
            ET.SubElement(url, 'lastmod').text = get_last_modified(file_path)
            ET.SubElement(url, 'changefreq').text = changefreq
            ET.SubElement(url, 'priority').text = priority
    
    xml_str = ET.tostring(urlset, encoding='utf-8')
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent='  ')
    
    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

if __name__ == "__main__":
    generate_sitemap()
