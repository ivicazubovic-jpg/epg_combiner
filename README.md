[combine_epg.py](https://github.com/user-attachments/files/22571784/combine_epg.py)
import requests
import xml.etree.ElementTree as ET

EPG_LINKS = [
    "https://www.epgeditor.com/2027/1ag.xml",
    "https://tvprofil.net/api/xmltv/epg/?accessKey=dpteam1wxy64Qhu9MT7R5V"
]

OUTPUT_FILE = "epg.xml"


def fetch_epg(url):
    print(f"[INFO] Preuzimam: {url}")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return ET.fromstring(response.content)


def combine_epgs():
    all_channels = {}
    all_programmes = []

    for url in EPG_LINKS:
        root = fetch_epg(url)

        for channel in root.findall("channel"):
            chan_id = channel.get("id")
            disp_name = channel.findtext("display-name", "").strip()

            # ključ za provjeru duplikata
            key = (chan_id, disp_name.lower())
            if key not in all_channels:
                all_channels[key] = channel

        for prog in root.findall("programme"):
            all_programmes.append(prog)

    tv = ET.Element("tv")

    # dodaj kanale
    for channel in all_channels.values():
        tv.append(channel)

    # dodaj programe
    for prog in all_programmes:
        tv.append(prog)

    tree = ET.ElementTree(tv)
    tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)
    print(f"[INFO] Spremljen fajl: {OUTPUT_FILE}")


if __name__ == "__main__":
    combine_epgs()
