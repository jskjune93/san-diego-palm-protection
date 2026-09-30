"""The single-page SAPW photo and film exhibit, generated with the core pages."""
from html import escape
from pathlib import Path
from site_components import head, BASE_URL

ROOT = Path(__file__).resolve().parents[1]
MEDIA = "images/palm-journal/when-sapw-became-local/"


DIMENSIONS = {'images/palm-journal/when-sapw-became-local/01-june-15-adult-sapw.jpg': (1800, 1080), 'images/palm-journal/the-palm-is-only-part-of-the-site/september-complete-crown.webp': (1200, 1600), 'images/palm-journal/when-sapw-became-local/03-june-16-six-captured-adults.jpg': (1800, 1692), 'images/palm-journal/when-sapw-became-local/04-june-16-specimen-profiles.jpg': (1800, 1157), 'images/old-escondido-ufmp/old-home-mature-cidps-golden-hour.jpg': (3000, 4000), 'images/las-palmas/09-severe-decline-2026-07-10-las-palmas-declining-palm-central-frond-necrosis-detail-03.jpg': (3000, 4000)}

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
{photo(adult, "Adult South American palm weevil in profile", eager=True)}
<video controls playsinline preload="none" poster="./{MEDIA}05-june-26-adult-on-trunk-poster.jpg" aria-label="Palm weevil moving on a palm trunk"><source src="./{MEDIA}05-june-26-adult-on-trunk.mp4" type="video/mp4"></video>
{photo(MEDIA + "03-june-16-six-captured-adults.jpg", "Six captured adult palm weevils", eager=True)}
{photo("images/palm-journal/the-palm-is-only-part-of-the-site/september-complete-crown.webp", "Canary Island date palm crown against a blue sky", eager=True)}
{photo(MEDIA + "04-june-16-specimen-profiles.jpg", "Side profiles of captured palm weevils")}
{photo("images/old-escondido-ufmp/old-home-mature-cidps-golden-hour.jpg", "Mature Canary Island date palms in evening light")}
{photo("images/las-palmas/09-severe-decline-2026-07-10-las-palmas-declining-palm-central-frond-necrosis-detail-03.jpg", "Declining palm crown with brown central fronds; cause unconfirmed")}
</main>
<footer class="sapw-raw-footer"><a href="{BASE_URL}/">SDPP</a><span>© 2026 SDPP</span></footer>
<dialog class="sapw-lightbox" aria-label="Full photograph"><button type="button" class="sapw-close" aria-label="Close full photograph">×</button><img alt="Selected full photograph"></dialog>
<script src="./site-assets/site.js" defer></script>
</body>
</html>'''
