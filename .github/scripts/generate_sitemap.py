import os
import time
import xml.etree.ElementTree as ET

# 📁 HTML ফাইলগুলোর মূল ফোল্ডার (আপনার প্রকৃত path দিন)
ROOT_DIR = "./public_html"  # ⚠️ এখানে আপনার HTML ফাইলের মূল ফোল্ডার দিন

# 🌍 ওয়েবসাইটের মূল URL (নিজের সাইটের URL দিন)
BASE_URL = "https://kamilhussen24.github.io/"

# 📄 সাইটম্যাপ ফাইলের নাম
SITEMAP_FILE = "sitemap.xml"

def get_last_modified(file_path):
    """ 🔄 নির্দিষ্ট ফাইলের সর্বশেষ পরিবর্তনের সময় সংগ্রহ করা """
    timestamp = os.path.getmtime(file_path)
    return time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime(timestamp))  # UTC টাইম ফরম্যাট

def generate_sitemap():
    urls = []

    # 📂 সকল HTML ফাইল স্ক্যান করা
    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file)  # ফাইলের সম্পূর্ণ পাথ
                last_modified = get_last_modified(full_path)  # লাস্ট মডিফাই সময় সংগ্রহ
                
                # 🌍 রিলেটিভ পাথ বের করে ".html" বাদ দেওয়া
                relative_path = os.path.relpath(full_path, ROOT_DIR).replace("\\", "/")
                url = BASE_URL + relative_path.replace(".html", "")

                # 📝 URL এবং লাস্টমডিফাইড ডেট যোগ করা
                urls.append((url, last_modified))

    # 🔄 Google Sitemap XML তৈরি করা
    root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for url, lastmod in urls:
        url_element = ET.SubElement(root, "url")
        ET.SubElement(url_element, "loc").text = url
        ET.SubElement(url_element, "lastmod").text = lastmod
        ET.SubElement(url_element, "priority").text = "0.8"
        ET.SubElement(url_element, "changefreq").text = "weekly"

    # 🏁 XML ফাইল তৈরি
    tree = ET.ElementTree(root)
    tree.write(SITEMAP_FILE, encoding="utf-8", xml_declaration=True)

    print(f"✅ সাইটম্যাপ সফলভাবে তৈরি হয়েছে: {SITEMAP_FILE}")

# 🔥 রান করুন
if __name__ == "__main__":
    generate_sitemap()
