"""The single-page SAPW photo and film exhibit, generated with the core pages."""
import json
from html import escape
from pathlib import Path
from site_components import head, BASE_URL, customer_map, asset_version

ROOT = Path(__file__).resolve().parents[1]
GALLERY = json.loads((ROOT / "site-config" / "sapw_gallery.json").read_text(encoding="utf-8"))
DIMENSIONS = {item["src"]: (item["width"], item["height"]) for item in GALLERY}


def photo(src, alt, *, eager=False):
    width, height = DIMENSIONS[src]
    return f'<a class="sapw-photo" href="./{src}" data-sapw-photo aria-label="Enlarge photograph"><img src="./{src}" alt="{escape(alt)}" width="{width}" height="{height}" loading="{"eager" if eager else "lazy"}" decoding="async"></a>'


def render():
    adult = GALLERY[0]["src"]
    return f'''<!doctype html>
<html lang="en">
<head>
{head("SAPW & Palm Photos | South American Palm Weevil | SDPP", "Original SAPW photographs, palm decline, and San Diego field video, with host guidance for Canary Island date, Chilean wine, and Bismarck palms.", "sapw.html", adult, schema_type="ImageGallery")}
<meta name="robots" content="index,follow,max-image-preview:large">
</head>
<body class="sapw-raw">
<div class="sapw-raw-titles"><h1 class="sapw-raw-heading">SOUTH AMERICAN PALM WEEVIL.</h1><p class="sapw-raw-subheading">CANARY ISLAND DATE PALM DESTRUCTION.</p></div>
<p class="sapw-raw-host-note">Canary Island date palms remain the primary local target. Chilean wine and Bismarck palms are confirmed California hosts too. <a href="./south-american-palm-weevil-treatment-san-diego.html">See prevention and treatment.</a></p>
<main id="main" aria-label="Palm weevil and palm photographs and video">
{photo(GALLERY[0]["src"], GALLERY[0]["alt"], eager=True)}
{chr(10).join(photo(item["src"], item["alt"], eager=index < 3) for index, item in enumerate(GALLERY[1:]))}
</main>
{customer_map()}
<footer class="sapw-raw-footer"><a href="{BASE_URL}/">SDPP</a><span>© 2026 SDPP</span></footer>
<dialog class="sapw-lightbox" aria-label="Full photograph"><button type="button" class="sapw-close" aria-label="Close full photograph">×</button><img alt="Selected full photograph"></dialog>
<script src="./site-assets/site.js?v={asset_version('site-assets/site.js')}" defer></script>
</body>
</html>'''
