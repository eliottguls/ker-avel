"""Réglages communs aux trois pistes, appliqués à toutes les pages.

Usage : python3 outils/site.py  (depuis la racine du dépôt)
- AIRBNB : lien de l'annonce ; remplace le href de chaque lien marqué data-airbnb.
- La carte de Bretagne du pied de page, insérée entre <!--carte--> et <!--/carte-->.
Contour : régions de France (github.com/gregoiredavid/france-geojson), simplifié.
- Référencement : titre et description des accueils, balises de partage, données
  structurées (schema.org), questions fréquentes entre <!--faq--> et <!--/faq-->,
  photos en <img> avec texte alternatif, robots.txt et sitemap.xml à la racine.
  EN_LIGNE = False garde toutes les pages en « noindex » tant que le site est en aperçu.
- Feuilles de style et scripts appelés avec ?v=<empreinte> : le navigateur recharge
  la nouvelle version dès qu'un fichier change, au lieu de garder l'ancienne en cache.
"""
import hashlib
import html as h
import json
import re
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
AIRBNB = "https://www.airbnb.fr/"
ADRESSE = "Pointe du Meinga, 35350 Saint-Coulomb"
ITINERAIRE = "https://www.google.com/maps/dir/?api=1&destination=Saint-Coulomb%2C%20Bretagne"

DOMAINE = "https://eliottguls.github.io/ker-avel"  # à remplacer par le nom de domaine définitif
EN_LIGNE = False  # True le jour de la mise en production : retire le noindex
VILLE, CODE_POSTAL, REGION = "Saint-Coulomb", "35350", "Bretagne"
TITRE = f"Ker Avel, gîte de charme pour 10 personnes à {VILLE} ({REGION})"
DESCRIPTION = (f"Ker Avel, gîte en pierre pour 10 personnes à {VILLE}, en {REGION} : 5 chambres, "
               "grand jardin, terrasse et cuisine équipée. Réservation sur Airbnb.")
PISTES = ["grand-large", "domaine", "cire"]

# Questions fréquentes : affichées sur l'accueil de chaque piste et reprises pour Google
FAQ = [
    ("Combien de personnes peut accueillir Ker Avel ?",
     "Jusqu'à 10 personnes, dans 5 chambres doubles qui ont chacune leur salle de bain. "
     "La maison se loue en entier, pour une famille ou un groupe d'amis."),
    ("Comment réserver le gîte ?",
     "Les réservations se font sur notre annonce Airbnb, où le calendrier des disponibilités est à jour. "
     "Pour une question avant de réserver, vous pouvez aussi nous écrire."),
    ("Que trouve-t-on dans la maison ?",
     "Une cuisine équipée avec piano de cuisson et grand îlot, une bibliothèque sous l'escalier, "
     "une terrasse ombragée et un grand jardin où les enfants peuvent courir. Les lits sont faits à votre arrivée."),
    (f"Où se trouve Ker Avel et comment y venir ?",
     f"À {VILLE}, entre Saint-Malo et Cancale. Saint-Malo est à 15 minutes en voiture, "
     "Rennes à une heure, et Paris à 3 heures en TGV jusqu'à Saint-Malo."),
    ("Que faire autour du gîte ?",
     "Les remparts de Saint-Malo, les huîtres de Cancale, le sentier des douaniers et les plages "
     "de la Côte d'Émeraude, à pied ou à vélo depuis la maison."),
]

# Texte alternatif de chaque photo (lu par Google Images et les lecteurs d'écran)
ALT = {
    "maison/facade": "Façade de la longère en pierre de Ker Avel aux volets bleus",
    "maison/terrasse": "Terrasse ombragée du gîte, table et chaises jaunes face au jardin",
    "maison/jardin-enfants": "Enfants qui courent sur la pelouse du jardin de Ker Avel",
    "maison/cuisine": "Cuisine équipée du gîte avec îlot en bois et piano de cuisson",
    "maison/bibliotheque": "Bibliothèque aménagée sous l'escalier de la maison",
    "maison/salle-de-bain": "Salle de bain avec baignoire et vasque",
    "maison/chambre-tropicale": "Chambre double aux tableaux tropicaux et dessus-de-lit à carreaux",
    "maison/chambre-plaid": "Chambre double avec plaid rose et gris et lampes de chevet",
    "maison/chambre-verte": "Chambre double au mur de cadres et plaid vert",
    "chambre-soleil": "Chambre lumineuse avec banquette sous la fenêtre",
    "chambre-sombre": "Chambre aux tons sombres et linge de lit clair",
    "pointe": "Pointe rocheuse de la Côte d'Émeraude",
    "estran": "Estran à marée basse sur la côte bretonne",
    "voilier": "Voilier dans la baie de Saint-Malo",
    "landes": "Landes et ajoncs sur le sentier des douaniers",
    "saint-malo": "Remparts de Saint-Malo",
    "saint-malo-couchant": "Saint-Malo au coucher du soleil",
    "piscine-mer": "Piscine d'eau de mer à marée haute",
    "huitres": "Huîtres de Cancale",
    "huitres-table": "Plateau d'huîtres sur une table",
    "guirlandes": "Maison décorée de guirlandes à Noël",
}

# Villes repères : nom, position du libellé par rapport au point
VILLES = [("Saint-Malo", "bas"), ("Rennes", "gauche"), ("Brest", "droite"), ("Vannes", "haut")]


def carte_svg():
    d = json.loads((Path(__file__).parent / "carte-bretagne.json").read_text())
    W, H, v = d["W"], d["H"], d["villes"]
    villes = []
    for nom, pos in VILLES:
        x, y = v[nom]
        tx, ty, ancre = {"bas": (x - 4, y + 32, "end"), "haut": (x, y - 14, "middle"),
                         "droite": (x + 12, y + 9, "start"), "gauche": (x - 12, y + 9, "end")}[pos]
        villes.append(f'<circle class="ville" cx="{x}" cy="{y}" r="4"/>'
                      f'<text x="{tx}" y="{ty}" text-anchor="{ancre}">{nom}</text>')
    px, py = v["Saint-Coulomb"]
    return (f'<svg class="carte" viewBox="0 0 {W} {H}" role="img" aria-labelledby="carte-titre">'
            f'<title id="carte-titre">Ker Avel se trouve à Saint-Coulomb, entre Saint-Malo et Cancale, sur la côte nord de la Bretagne</title>'
            f'<rect class="mer" width="{W}" height="{H}"/>'
            f'<path class="voisins" d="{d["voisins"]}"/>'
            f'<path class="terre" d="{d["bzh"]}"/>'
            + "".join(villes) +
            f'<g class="pin" transform="translate({px} {py})"><circle r="16" class="halo"/>'
            f'<path d="M0 0c-6-8-11-13-11-19a11 11 0 0 1 22 0c0 6-5 11-11 19z" transform="translate(0 -2)"/>'
            f'<circle cy="-21" r="4" class="oeil"/></g>'
            f'<text class="nom" x="{px - 22}" y="{py - 30}" text-anchor="end">Ker Avel</text>'
            "</svg>")


def bloc_carte():
    return ('<!--carte--><figure class="plan">' + carte_svg() +
            f'<figcaption><span>{ADRESSE}</span><span>Saint-Malo à 15 min, Rennes à 1 h, Paris à 3 h en TGV</span>'
            f'<a href="{ITINERAIRE}" target="_blank" rel="noopener">Préparer l\'itinéraire</a></figcaption></figure><!--/carte-->')


def bloc_faq():
    return "<!--faq-->" + "".join(
        f"<details><summary>{h.escape(q, False)}</summary><p>{h.escape(r, False)}</p></details>" for q, r in FAQ
    ) + "<!--/faq-->"


def en_img(html):
    """Photos posées en fond CSS sur un élément de décor → vraie balise <img> avec texte alternatif."""
    motif = re.compile(r'<(figure|span|div)\b([^>]*?) style="background(?:-image)?:url\(\.\./img/([\w/-]+)\.jpg\)([^"]*)"([^>]*)>')

    def rempl(m):
        tag, avant, nom, pos, apres = m.groups()
        pos = pos.split("/")[0].strip()
        style = f' style="object-position:{pos}"' if pos and pos != "center" else ""
        return (f'<{tag}{avant}{apres}><img src="../img/{nom}.jpg" alt="{h.escape(ALT.get(nom, ""))}"'
                f' loading="lazy" decoding="async"{style}>')
    return motif.sub(rempl, html)


def absolu(chemin):
    return DOMAINE + "/" + chemin.replace("index.html", "")


def donnees(chemin, html, titre, desc):
    """Données structurées schema.org de la page."""
    piste = chemin.split("/")[0]
    accueil = absolu(piste + "/")
    photos = [DOMAINE + "/img/" + n + ".jpg" for n in ALT if n.startswith("maison/")]
    if chemin.endswith("index.html"):
        gite = {
            "@context": "https://schema.org", "@type": "VacationRental", "name": "Ker Avel",
            "description": DESCRIPTION, "url": accueil, "image": photos,
            "address": {"@type": "PostalAddress", "addressLocality": VILLE, "postalCode": CODE_POSTAL,
                        "addressRegion": REGION, "addressCountry": "FR"},
            "containsPlace": {"@type": "Accommodation", "additionalType": "EntirePlace", "numberOfBedrooms": 5,
                              "numberOfBathroomsTotal": 5, "occupancy": {"@type": "QuantitativeValue", "maxValue": 10},
                              "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": a, "value": True}
                                                 for a in ["Jardin", "Terrasse", "Cuisine équipée", "Linge de lit fourni"]]},
            "sameAs": [AIRBNB],
        }
        faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in FAQ]}
        return [gite, faq]
    nom = h.unescape(re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S).group(1))
    nom = re.sub(r"<[^>]+>", "", nom).strip()
    image = re.search(r'src="\.\./(img/[^"]+)"', html)
    chambre = {"@context": "https://schema.org", "@type": "Accommodation", "name": f"Chambre {nom}",
               "description": desc, "url": absolu(chemin), "occupancy": {"@type": "QuantitativeValue", "maxValue": 2},
               "containedInPlace": {"@type": "VacationRental", "name": "Ker Avel", "url": accueil}}
    if image:
        chambre["image"] = DOMAINE + "/" + image.group(1)
    fil = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Ker Avel", "item": accueil},
        {"@type": "ListItem", "position": 2, "name": "Chambres", "item": accueil + "#chambres"},
        {"@type": "ListItem", "position": 3, "name": f"Chambre {nom}", "item": absolu(chemin)}]}
    return [chambre, fil]


def bloc_seo(chemin, html):
    titre = h.unescape(re.search(r"<title>(.*?)</title>", html).group(1))
    desc = h.unescape(re.search(r'<meta name="description" content="([^"]*)"', html).group(1))
    image = re.search(r"url\(\.\./(img/[^)]+)\)", html) or re.search(r'src="\.\./(img/[^"]+)"', html)
    meta = [
        '<meta name="robots" content="index, follow">' if EN_LIGNE else '<meta name="robots" content="noindex, nofollow">',
        f'<link rel="canonical" href="{absolu(chemin)}">',
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="Ker Avel">',
        '<meta property="og:locale" content="fr_FR">',
        f'<meta property="og:title" content="{h.escape(titre)}">',
        f'<meta property="og:description" content="{h.escape(desc)}">',
        f'<meta property="og:url" content="{absolu(chemin)}">',
        f'<meta property="og:image" content="{DOMAINE}/{image.group(1)}">' if image else "",
        '<meta name="twitter:card" content="summary_large_image">',
    ] + [f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>'
         for d in donnees(chemin, html, titre, desc)]
    return "<!--seo-->\n" + "\n".join(m for m in meta if m) + "\n<!--/seo-->"


def referencement(chemin, html):
    if chemin.endswith("index.html"):
        html = re.sub(r"<title>.*?</title>", f"<title>{h.escape(TITRE, False)}</title>", html)
        html = re.sub(r'<meta name="description" content="[^"]*">',
                      f'<meta name="description" content="{h.escape(DESCRIPTION)}">', html)
        html = re.sub(r'<script type="application/ld\+json">.*?</script>\n', "", html, flags=re.S)
        if "<!--seo-->" not in html:
            html = re.sub(r'(<meta name="description"[^>]*>\n)', r"\1<!--seo--><!--/seo-->\n", html)
    return re.sub(r"<!--seo-->.*?<!--/seo-->", lambda m: bloc_seo(chemin, html), html, flags=re.S)


def plan_du_site():
    pages = [f"{p}/" for p in PISTES] + sorted(
        str(f.relative_to(RACINE)) for p in PISTES for f in (RACINE / p).glob("chambre-*.html"))
    urls = "".join(f"  <url><loc>{DOMAINE}/{u}</loc></url>\n" for u in pages)
    (RACINE / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n", encoding="utf-8")
    (RACINE / "robots.txt").write_text(
        "# Les pages restent en noindex tant que EN_LIGNE = False dans outils/site.py.\n"
        "# À la mise en production, ce fichier doit être servi à la racine du nom de domaine.\n"
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {DOMAINE}/sitemap.xml\n", encoding="utf-8")


def versionner(f, html):
    """Ajoute ?v=<empreinte du fichier> aux liens vers les .css et .js locaux."""
    def rempl(m):
        cible = (f.parent / m.group(2)).resolve()
        if not cible.exists():
            return m.group(0)
        v = hashlib.md5(cible.read_bytes()).hexdigest()[:8]
        return f'{m.group(1)}="{m.group(2)}?v={v}"'
    return re.sub(r'\b(href|src)="((?!https?:)[^"?]+\.(?:css|js))(?:\?v=\w+)?"', rempl, html)


def appliquer(html):
    html = re.sub(r'(<a\b[^>]*?\bdata-airbnb\b[^>]*?\bhref=")[^"]*(")', r"\g<1>" + AIRBNB + r"\2", html)
    html = re.sub(r'(<a\b[^>]*?\bhref=")[^"]*("[^>]*?\bdata-airbnb\b)', r"\g<1>" + AIRBNB + r"\2", html)
    html = re.sub(r"<!--carte-->.*?<!--/carte-->", lambda m: bloc_carte(), html, flags=re.S)
    html = re.sub(r"<!--faq-->.*?<!--/faq-->", lambda m: bloc_faq(), html, flags=re.S)
    return html


if __name__ == "__main__":
    for f in sorted(RACINE.glob("*/*.html")):
        s = f.read_text(encoding="utf-8")
        n = appliquer(s)
        chemin = str(f.relative_to(RACINE))
        if chemin.split("/")[0] in PISTES:
            n = referencement(chemin, en_img(n))
        n = versionner(f, n)
        if n != s:
            f.write_text(n, encoding="utf-8")
            print(f.relative_to(RACINE))
    plan_du_site()
