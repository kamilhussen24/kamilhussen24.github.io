import os
import time
import xml.dom.minidom
from xml.etree.ElementTree import Element, SubElement, tostring

SITEMAP_FILE = "sitemap.xml"
BASE_URL = "https://kamilhussen24.github.io"
HTML_FOLDER = "."  # HTML ফাইল স্ক্যান করবে

def get_all_html_files(directory):
    """ সব .html ফাইল রিকার্সিভলি খুঁজে বের করবে """
    html_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, directory)  # রিলেটিভ পাথ
                html_files.append(relative_path)
    return html_files

def get_last_modified_date(file_path):
    """ ফাইলের লাস্ট মডিফাইড টাইম বের করবে (ISO format) """
    timestamp = os.path.getmtime(file_path)
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(timestamp))

def generate_sitemap():
    """ নতুন sitemap.xml ফাইল তৈরি করবে """
    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    # ✅ মেইন ওয়েবসাইটের ইউআরএল (প্রায়োরিটি 1.0)
    url_element = SubElement(urlset, "url")
    SubElement(url_element, "loc").text = BASE_URL
    SubElement(url_element, "lastmod").text = get_last_modified_date("index.html") if os.path.exists("index.html") else get_last_modified_date(".")
    SubElement(url_element, "priority").text = "1.0"
    SubElement(url_element, "changefreq").text = "daily"

    html_files = get_all_html_files(HTML_FOLDER)
    
    for file in html_files:
        if "node_modules" in file or ".git" in file:
            continue  # অপ্রয়োজনীয় ফোল্ডার বাদ দেওয়া
        
        url_path = file.replace(".html", "")  # .html সরিয়ে ক্লিন URL বানানো
        url = f"{BASE_URL}/{url_path}"
        lastmod = get_last_modified_date(file)

        url_element = SubElement(urlset, "url")
        SubElement(url_element, "loc").text = url
        SubElement(url_element, "lastmod").text = lastmod
        SubElement(url_element, "priority").text = "0.8"
        SubElement(url_element, "changefreq").text = "weekly"

    # ✅ XML কে সুন্দরভাবে (pretty-print) ফরম্যাট করা
    rough_string = tostring(urlset, encoding="utf-8", method="xml")
    reparsed = xml.dom.minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print("✅ Sitemap.xml আপডেট হয়েছে!")

if __name__ == "__main__":
    generate_sitemap()
