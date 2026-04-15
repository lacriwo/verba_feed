#!/usr/bin/env python3
import urllib.request
import xml.etree.ElementTree as ET

SOURCE_URL = "https://api.macroserver.ru/estate/export/yandex/OzA5_WiGLTOJUuUfZsa-aAnYrqeYWBlO7q97bDXLcTWdInddefntJn-Gx9oKQ2qDosqdi_K_c8t7HhEqgVzInjUi_sG_3P3HqxDZrIROtRuZqBKBbk-f9dF4USIHZkZnW3SzJXh8MTc2ODgwNjkwOHxjOGJiNg/394-yandex.xml?feed_id=8691"
TARGET_URL = "https://ligo-verba.ru"
OUTPUT_FILE = "public/394-yandex-patched.xml"

with urllib.request.urlopen(SOURCE_URL, timeout=90) as r:
    xml_data = r.read()

root = ET.fromstring(xml_data)

ns_uri = ""
if root.tag.startswith("{") and "}" in root.tag:
    ns_uri = root.tag[1:root.tag.index("}")]

ns = {"n": ns_uri} if ns_uri else {}
offers = root.findall(".//n:offer" if ns_uri else ".//offer", ns)

for offer in offers:
    url_node = offer.find("n:url" if ns_uri else "url", ns)
    if url_node is None:
        url_node = ET.SubElement(offer, "url")
    url_node.text = TARGET_URL

if ns_uri:
    ET.register_namespace("", ns_uri)

ET.ElementTree(root).write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)
print(f"Offers processed: {len(offers)}")
