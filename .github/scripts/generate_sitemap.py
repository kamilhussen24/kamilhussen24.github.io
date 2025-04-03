import os
import time
import xml.etree.ElementTree as ET

SITEMAP_FILE = "sitemap.xml"
BASE_URL = "https://kamilhussen24.github.io"
HTML_FOLDER = "."  # মূল ফোল্ডার যেখানে .html ফাইলগুলো আছে

def get_html_files(directory):
    """ নির্দিষ্ট ফোল্ডার থেকে সব .html ফাইল রিকার্সিভলি খুঁজে বের করবে """
    html_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file)
                html_files.append(full_path)
    return html_files

def get_last_modified(file_path):
    """ নির্দিষ্ট HTML ফাইলের লাস্ট মডিফাই ডেট বের করবে """
    if os.path.exists(file_path):
        timestamp = os.path.getmtime(file_path)  # লাস্ট মডিফাই টাইম স্ট্যাম্প
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(timestamp))
    return None

def generate_sitemap():
    """ নতুন `sitemap.xml` ফাইল তৈরি করবে এবং আপডেট করবে """
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    html_files = get_html_files(HTML_FOLDER)
    
    for file in html_files:
        relative_path = os.path.relpath(file, HTML_FOLDER)  # রিলেটিভ পাথ বের করা
        url_path = relative_path.replace("\\", "/").replace(".html", "")  # উইন্ডোজের জন্য "\" -> "/"
        url = f"{BASE_URL}/{url_path}"
        lastmod = get_last_modified(file)

        url_element = ET.SubElement(urlset, "url")
        ET.SubElement(url_element, "loc").text = url
        if lastmod:
            ET.SubElement(url_element, "lastmod").text = lastmod
        ET.SubElement(url_element, "priority").text = "0.8"
        ET.SubElement(url_element, "changefreq").text = "weekly"

    # ✅ XML সুন্দরভাবে ফরম্যাট করা
    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ", level=0)

    with open(SITEMAP_FILE, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)

    print("✅ sitemap.xml সফলভাবে আপডেট হয়েছে!")

if __name__ == "__main__":
    generate_sitemap()
