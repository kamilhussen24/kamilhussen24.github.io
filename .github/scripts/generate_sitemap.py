import os
import time
import xml.dom.minidom
from xml.etree.ElementTree import Element, SubElement, tostring

SITEMAP_FILE = "sitemap.xml"
BASE_URL = "https://kamilhussen24.github.io"
HTML_FOLDER = "."  # মূল ফোল্ডার যেখানে .html ফাইল আছে

def get_all_html_files(directory):
    """ সব .html ফাইল রিকার্সিভলি খুঁজে বের করবে """
    html_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file)
                html_files.append(full_path)  # সম্পূর্ণ ফাইল পাথ সংগ্রহ
    return html_files

def get_last_modified_date(file_path):
    """ নির্দিষ্ট HTML ফাইলের সর্বশেষ পরিবর্তনের তারিখ বের করবে """
    if os.path.exists(file_path):
        timestamp = os.path.getmtime(file_path)  # লাস্ট মডিফাই টাইম স্ট্যাম্প
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(timestamp))
    return None  # যদি ফাইল না থাকে

def generate_sitemap():
    """ নতুন sitemap.xml ফাইল তৈরি করবে """
    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    html_files = get_all_html_files(HTML_FOLDER)

    for file in html_files:
        if "node_modules" in file or ".git" in file:
            continue  # অপ্রয়োজনীয় ফোল্ডার বাদ দেওয়া

        relative_path = os.path.relpath(file, HTML_FOLDER)  # রিলেটিভ পাথ
        url_path = relative_path.replace("\\", "/").replace(".html", "")  # উইন্ডোজের জন্য "\" -> "/" কনভার্ট
        url = f"{BASE_URL}/{url_path}"
        lastmod = get_last_modified_date(file)

        url_element = SubElement(urlset, "url")
        SubElement(url_element, "loc").text = url
        if lastmod:
            SubElement(url_element, "lastmod").text = lastmod  # শুধুমাত্র যদি লাস্ট মডিফাই পাওয়া যায়
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
