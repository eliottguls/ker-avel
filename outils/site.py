"""Réglages communs aux trois pistes, appliqués à toutes les pages.

Usage : python3 outils/site.py  (depuis la racine du dépôt)
- AIRBNB : lien de l'annonce ; remplace le href de chaque lien marqué data-airbnb.
- La carte de Bretagne du pied de page, insérée entre <!--carte--> et <!--/carte-->.
Contour : régions de France (github.com/gregoiredavid/france-geojson), simplifié.
"""
import json
import re
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
AIRBNB = "https://www.airbnb.fr/"
ADRESSE = "Pointe du Meinga, 35350 Saint-Coulomb"
ITINERAIRE = "https://www.google.com/maps/dir/?api=1&destination=Saint-Coulomb%2C%20Bretagne"

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


def appliquer(html):
    html = re.sub(r'(<a\b[^>]*?\bdata-airbnb\b[^>]*?\bhref=")[^"]*(")', r"\g<1>" + AIRBNB + r"\2", html)
    html = re.sub(r'(<a\b[^>]*?\bhref=")[^"]*("[^>]*?\bdata-airbnb\b)', r"\g<1>" + AIRBNB + r"\2", html)
    html = re.sub(r"<!--carte-->.*?<!--/carte-->", lambda m: bloc_carte(), html, flags=re.S)
    return html


if __name__ == "__main__":
    for f in sorted(RACINE.glob("*/*.html")):
        s = f.read_text(encoding="utf-8")
        n = appliquer(s)
        if n != s:
            f.write_text(n, encoding="utf-8")
            print(f.relative_to(RACINE))
