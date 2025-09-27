name: Update EPG

on:
  schedule:
    - cron: "0 3 * * *"   # svaki dan u 03:00 UTC
  workflow_dispatch:       # možeš i ručno pokrenuti

jobs:
  update-epg:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install requests

      - name: Run EPG combiner
        run: python combine_epg.py

      - name: Commit and push changes
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add epg.xml
          git commit -m "Automatski update EPG"
          git push
