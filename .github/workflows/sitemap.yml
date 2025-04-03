name: Update Sitemap

on:
  schedule:
    - cron: '0 0 * * *'  # দৈনিক আপডেট
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0  # সম্পূর্ণ Git হিস্ট্রি ফেচ করতে

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: pip install -r requirements.txt

    - name: Generate sitemap
      run: python sitemap_generator.py

    - name: Commit and push changes
      run: |
        git config --global user.name "GitHub Actions"
        git config --global user.email "actions@github.com"
        git pull --rebase origin main  # রিমোট পরিবর্তনগুলি ম্যানুয়ালি মার্জ করুন
        git add sitemap.xml
        git commit -m "Auto-update sitemap"
        git push origin main
