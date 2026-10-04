"""The single-page SAPW photo and film exhibit, generated with the core pages."""
import json
from html import escape
from pathlib import Path
from site_components import head, BASE_URL, customer_map, asset_version

ROOT = Path(__file__).resolve().parents[1]
MEDIA = "images/palm-journal/when-sapw-became-local/"


GALLERY = json.loads((ROOT / "site-config" / "sapw_gallery.json").read_text(encoding="utf-8"))
DIMENSIONS = {item["src"]: (item["width"], item["height"]) for item in GALLERY}


def photo(src, alt, *, eager=False):
    width, height = DIMENSIONS[src]
    return f'<a class="sapw-photo" href="./{src}" data-sapw-photo aria-label="Enlarge photograph"><img src="./{src}" alt="{escape(alt)}" width="{width}" height="{height}" loading="{"eager" if eager else "lazy"}" decoding="async"></a>'


def render():
    adult = MEDIA + "01-june-15-adult-sapw.jpg"
    return f'''<!doctype html>
<html lang="en">
<head>
{head("SAPW & CIDP Photos | South American Palm Weevil | SDPP", "Original SAPW (South American palm weevil) and CIDP (Canary Island date palm) photographs, crown decline and field video from San Diego Palm Protection.", "sapw.html", adult, schema_type="ImageGallery")}
<meta name="robots" content="index,follow,max-image-preview:large">
</head>
<body class="sapw-raw">
<div class="sapw-raw-titles"><h1 class="sapw-raw-heading">SOUTH AMERICAN PALM WEEVIL.</h1><p class="sapw-raw-subheading">CANARY ISLAND DATE PALM DESTRUCTION.</p></div>
<main id="main" aria-label="Palm weevil and palm photographs and video">
{photo(GALLERY[0]["src"], GALLERY[0]["alt"], eager=True)}
<video controls playsinline preload="none" poster="./{MEDIA}05-june-26-adult-on-trunk-poster.jpg" aria-label="Palm weevil moving on a palm trunk"><source src="./{MEDIA}05-june-26-adult-on-trunk.mp4" type="video/mp4"></video>
{chr(10).join(photo(item["src"], item["alt"], eager=index < 3) for index, item in enumerate(GALLERY[1:]))}
</main>
{customer_map()}
<footer class="sapw-raw-footer"><a href="{BASE_URL}/">SDPP</a><span>© 2026 SDPP</span></footer>
<dialog class="sapw-lightbox" aria-label="Full photograph"><button type="button" class="sapw-close" aria-label="Close full photograph">×</button><img alt="Selected full photograph"></dialog>
<script src="./site-assets/site.js?v={asset_version('site-assets/site.js')}" defer></script>
</body>
</html>'''
