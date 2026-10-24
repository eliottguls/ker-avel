"""Génère les pages chambres des trois pistes : <piste>/chambre-<id>.html.

Usage : python3 outils/chambres.py && python3 outils/site.py  (depuis la racine du dépôt)
Les textes et les photos sont dans CHAMBRES ; chaque piste a sa propre mise en page.
"""
from html import escape
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent

# Chaque chambre : id, nom, accroche, deux paragraphes, fiche, photos (chambre, détail, bain, vue)
CHAMBRES = {
    "grand-large": [
        dict(id="emeraude", nom="Émeraude", sous="La plus grande, sous les combles",
             p=["Un balcon sur la baie, une baignoire face à la fenêtre et le phare du Grand Jardin dans l'axe du lit.",
                "Le matin, la lumière entre par les deux lucarnes et l'on entend la mer avant de la voir."],
             lit="Lit 180", surface="28 m²", vue="Vue mer", bain="Baignoire et douche",
             photos=["maison/chambre-plaid", "maison/bibliotheque", "maison/salle-de-bain", "pointe"], fond="c-ocre"),
        dict(id="goemon", nom="Goémon", sous="De plain-pied sur le jardin",
             p=["Une porte-fenêtre ouvre sur les hortensias. On prend le café dehors avant que la maison se réveille.",
                "Baignoire à pattes, douche à l'italienne et un grand placard pour les bottes et les cirés."],
             lit="Lit 160", surface="22 m²", vue="Vue jardin", bain="Baignoire à pattes",
             photos=["maison/chambre-tropicale", "maison/jardin-enfants", "maison/salle-de-bain", "maison/terrasse"], fond="c-lin"),
        dict(id="mousses", nom="Les Mousses", sous="La chambre des enfants",
             p=["Quatre lits simples sous la charpente, des hublots sur la mer et une malle pleine de jeux de plage.",
                "Une salle d'eau à hauteur d'enfant juste à côté, et l'escalier qui descend droit vers la cuisine."],
             lit="4 lits 90", surface="26 m²", vue="Vue mer", bain="Salle d'eau",
             photos=["chambre-soleil", "estran", "maison/salle-de-bain", "voilier"], fond="c-ardoise"),
        dict(id="phare", nom="Le Phare", sous="Au bout du couloir, face au large",
             p=["Une petite chambre ronde dans la tour, avec une fenêtre sur chaque horizon.",
                "On s'y endort en comptant les éclats du phare du Grand Jardin."],
             lit="Lit 160", surface="20 m²", vue="Vue mer", bain="Salle d'eau",
             photos=["maison/chambre-verte", "pointe", "maison/salle-de-bain", "saint-malo-couchant"], fond="c-ocre"),
        dict(id="lingerie", nom="La Lingerie", sous="Calme, côté pins",
             p=["L'ancienne lingerie de la maison, devenue une chambre douce aux murs chaulés.",
                "La plus fraîche en août, avec un bureau sous la fenêtre pour lire ou écrire."],
             lit="Lit 140", surface="16 m²", vue="Vue pins", bain="Douche",
             photos=["chambre-sombre", "maison/bibliotheque", "maison/salle-de-bain", "landes"], fond="c-lin"),
    ],
    "domaine": [
        dict(id="armateur", nom="L'Armateur", sous="La chambre d'honneur, face à la baie",
             p=["La chambre du propriétaire de 1912, avec sa cheminée de granit et ses deux fenêtres sur la baie.",
                "Le parquet de chêne d'origine, un lit de 180 et une salle de bain en marbre avec baignoire."],
             lit="Lit 180", surface="28 m²", vue="Vue baie", bain="Baignoire",
             photos=["chambre-soleil", "estran", "maison/salle-de-bain", "maison/bibliotheque"]),
        dict(id="capitainerie", nom="La Capitainerie", sous="Sous les toits, la vue la plus haute",
             p=["Au deuxième étage, une chambre mansardée d'où l'on voit les voiliers entrer dans la baie.",
                "Une longue-vue est posée sur le rebord de la fenêtre, et le petit-déjeuner peut y être servi."],
             lit="Lit 160", surface="24 m²", vue="Vue baie", bain="Douche à l'italienne",
             photos=["maison/chambre-tropicale", "voilier", "maison/salle-de-bain", "pointe"]),
        dict(id="hortensias", nom="Les Hortensias", sous="Rez-de-jardin, entrée indépendante",
             p=["De plain-pied sur le parc, avec sa propre porte sur l'allée des hortensias.",
                "Idéale pour les parents qui veulent un peu de calme, ou pour les grands-parents."],
             lit="Lit 160", surface="22 m²", vue="Vue parc", bain="Baignoire à pattes",
             photos=["maison/chambre-plaid", "maison/jardin-enfants", "maison/salle-de-bain", "maison/terrasse"]),
        dict(id="lingerie", nom="La Lingerie", sous="Intime, sur le parc",
             p=["L'ancienne lingerie de la demeure, aux murs chaulés et aux rideaux de lin.",
                "Une chambre douce et sombre, la plus fraîche de la maison en plein été."],
             lit="Lit 140", surface="18 m²", vue="Vue parc", bain="Douche",
             photos=["chambre-sombre", "maison/bibliotheque", "maison/salle-de-bain", "maison/jardin-enfants"]),
        dict(id="mousses", nom="Les Mousses", sous="La chambre des enfants",
             p=["Quatre lits sous la charpente, une cabane de lecture et des hublots sur la mer.",
                "Une salle d'eau à hauteur d'enfant et une malle de jeux de plage."],
             lit="4 lits 90", surface="26 m²", vue="Vue mer", bain="Salle d'eau",
             photos=["maison/chambre-verte", "estran", "maison/salle-de-bain", "piscine-mer"]),
    ],
    "cire": [
        dict(id="lin", nom="Lin", sous="Sous les combles, face à la baie",
             note="la préférée des lève-tôt",
             p=["Un balcon face à la baie et le phare du Grand Jardin dans l'axe du lit.",
                "On y laisse les volets ouverts la nuit pour se réveiller avec la marée."],
             lit="Lit 180", surface="24 m²", vue="Vue mer", bain="Salle d'eau",
             aime=["le café sur le balcon", "le phare dans l'axe du lit", "le plaid de laine de Plouguerneau"],
             photos=["maison/chambre-tropicale", "pointe", "maison/salle-de-bain", "maison/bibliotheque"]),
        dict(id="chanvre", nom="Chanvre", sous="De plain-pied sur le jardin",
             note="pour les bains qui durent",
             p=["De plain-pied sur le jardin, avec une baignoire à pattes sous la fenêtre.",
                "Les enfants passent par là pour aller à la plage : on y entend les rires plus que la mer."],
             lit="Lit 160", surface="22 m²", vue="Vue jardin", bain="Baignoire",
             aime=["la baignoire sous la fenêtre", "la porte sur les hortensias", "le grand placard à cirés"],
             photos=["maison/chambre-plaid", "maison/salle-de-bain", "maison/jardin-enfants", "maison/terrasse"]),
        dict(id="ardoise", nom="Ardoise", sous="La plus calme, côté pins",
             note="idéale pour lire",
             p=["La plus calme de la maison, côté pins, avec un bureau sous la fenêtre.",
                "Pour ceux qui travaillent un peu le matin et filent à la plage l'après-midi."],
             lit="Lit 160", surface="18 m²", vue="Vue pins", bain="Salle d'eau",
             aime=["le bureau face aux pins", "le silence", "la fraîcheur en août"],
             photos=["chambre-sombre", "landes", "maison/salle-de-bain", "maison/bibliotheque"]),
        dict(id="mousses", nom="Les Mousses", sous="La chambre des enfants",
             note="cabane garantie",
             p=["Quatre lits simples sous la charpente, des hublots sur la mer et une malle de jeux de plage.",
                "Les seaux et les épuisettes attendent au pied de l'escalier."],
             lit="4 lits 90", surface="26 m²", vue="Vue mer", bain="Salle d'eau",
             aime=["les hublots sur la mer", "la malle de jeux", "les lits sous la charpente"],
             photos=["chambre-soleil", "estran", "maison/salle-de-bain", "voilier"]),
        dict(id="jardinier", nom="Le Jardinier", sous="La petite maison du fond du jardin",
             note="pour les grands-parents",
             p=["Dans la petite maison du fond du jardin, indépendante, avec sa terrasse.",
                "À trente pas de la grande maison : on vient pour le dîner et on rentre au calme."],
             lit="Lit 160", surface="20 m²", vue="Vue jardin", bain="Douche",
             aime=["sa terrasse au soleil du soir", "l'indépendance", "le figuier devant la porte"],
             photos=["maison/chambre-verte", "maison/terrasse", "maison/salle-de-bain", "maison/facade"]),
    ],
}

NOMS = {"grand-large": "Grand Large", "domaine": "Domaine", "cire": "Ciré"}
POLICES = {
    "grand-large": "family=Federo&family=Josefin+Sans:wght@300;400;600",
    "domaine": "family=Caladea:ital,wght@0,400;1,400&family=Barlow:ital,wght@0,300;0,400;0,500;1,300",
    "cire": "family=Gloock&family=Jost:ital,wght@0,300;0,400;0,500;1,300&family=Caveat:wght@500",
}


def e(t):
    return escape(t, quote=True)


def img(nom):
    return f"../img/{nom}.jpg"


def tete(piste, c):
    titre = f"Chambre {c['nom']} · Ker Avel, gîte en Bretagne"
    desc = f"{c['nom']} : {c['sous'].lower()}. {c['lit']}, {c['surface']}, {c['vue'].lower()}. Une des cinq chambres de Ker Avel, gîte pour 10 personnes en Bretagne."
    return f"""<!doctype html>
<html lang="fr" data-page="{piste}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titre)}</title>
<meta name="description" content="{e(desc)}">
<!--seo--><!--/seo-->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{POLICES[piste]}&display=swap">
<link rel="stylesheet" href="piste.css">
<link rel="stylesheet" href="../assets/chartes.css">
<script src="../assets/chartes.js"></script>
</head>
<body class="page-chambre">
<a class="tag" href="../" style="text-decoration:none">← Les trois pistes</a>
"""


def fiche_dl(c, cls="fiche"):
    rows = [("Couchage", c["lit"]), ("Surface", c["surface"]), ("Vue", c["vue"].replace("Vue ", "").capitalize()), ("Bain", c["bain"])]
    return f'<dl class="{cls}">' + "".join(f"<div><dt>{a}</dt><dd>{e(b)}</dd></div>" for a, b in rows) + "</dl>"


def voisins(liste, i):
    return liste[(i - 1) % len(liste)], liste[(i + 1) % len(liste)]


# ---------- Piste A : galerie verticale + panneau fixe en aplat ----------
def page_a(liste, i):
    c = liste[i]
    prec, suiv = voisins(liste, i)
    autres = [x for x in liste if x is not c]
    photos = "".join(f'<figure class="ph" style="background:url({img(p)}) center/cover"></figure>' for p in c["photos"])
    autres_html = "".join(
        f'<a class="autre" href="chambre-{x["id"]}.html"><figure class="ph" style="background:url({img(x["photos"][0])}) center/cover"></figure>'
        f'<span class="cap"><h3>{e(x["nom"])}</h3><span>{e(x["sous"])}</span></span></a>' for x in autres)
    return tete("grand-large", c) + f"""
{ANNONCE_A}
<header class="top gut">
  <div class="in">
    <a class="brand" href="./">Ker Avel<small>Saint-Coulomb</small></a>
    <nav aria-label="Navigation principale">
      <a href="./#maison">La maison</a><a href="./#chambres" aria-current="page">Chambres</a><a href="./#alentours">Alentours</a><details class="menu"><summary>Menu</summary><div class="menu-liens"><a href="./#maison">La maison</a><a href="./#chambres">Chambres</a><a href="./#alentours">Alentours</a><a href="./#reserver">Réserver</a></div></details><a class="btn" data-airbnb target="_blank" rel="noopener" href="https://www.airbnb.fr/">Réservez</a>
    </nav>
  </div>
</header>

<main>
  <div class="band"></div>
  <section class="ch-a">
    <div class="ch-galerie" tabindex="0" aria-label="Photos de la chambre {e(c['nom'])}">{photos}</div>
    <div class="ch-panneau {c['fond']} gut"><div class="inner">
      <p class="fil"><a href="./#chambres">Les chambres</a></p>
      <h1>{e(c['nom'])}</h1>
      <p class="sub">{e(c['sous'])}</p>
      <span class="rule"></span>
      {''.join(f'<p>{e(x)}</p>' for x in c['p'])}
      {fiche_dl(c)}
      <div class="btns"><a class="btn" data-airbnb target="_blank" rel="noopener" href="https://www.airbnb.fr/">Réserver cette chambre</a></div>
      <nav class="suite" aria-label="Autres chambres"><a href="chambre-{prec['id']}.html">‹ {e(prec['nom'])}</a><a href="chambre-{suiv['id']}.html">{e(suiv['nom'])} ›</a></nav>
    </div></div>
  </section>

  <section class="autres gut" aria-labelledby="t-autres">
    <h2 id="t-autres">Les autres chambres</h2>
    <span class="rule"></span>
  </section>
  <div class="autres-grille">{autres_html}</div>
</main>
{PIED_A}
</body>
</html>
"""


ANNONCE_A = """<p class="annonce gut">Prochaines disponibilités : la semaine du 7 novembre, puis les vacances de Noël. <a data-airbnb target="_blank" rel="noopener" href="https://www.airbnb.fr/">Réserver une date</a></p>"""
PIED_A = """<footer class="foot gut">
  <div class="in">
    <div class="brand">Ker Avel<small>Saint-Coulomb</small></div>
    <div>Pointe du Meinga<br>35350 Saint-Coulomb</div>
    <div>contact@ker-avel.bzh<br>+33 6 00 00 00 00<br><small>Photos d'illustration : Unsplash</small></div>
    <!--carte--><!--/carte-->
  </div>
</footer>"""


# ---------- Piste B : plein écran, fiche sur fond nuit, diaporama ----------
NAV_B = """<header class="top gut">
  <div class="wrap">
    <nav class="l" aria-label="Navigation principale"><a href="./#demeure"><span>La demeure</span><small>& son parc</small></a><a href="./#chambres"{cur}><span>Chambres</span><small>cinq au total</small></a><a href="./#alentours"><span>Alentours</span><small>la Côte d'Émeraude</small></a></nav>
    <a class="logo" href="./">
      <svg viewBox="0 0 42 34" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.2"><path d="M3 33h36M7 33V15L21 4l14 11v18M16 33v-9h10v9M11 18h4v4h-4zM27 18h4v4h-4zM21 4V1"/></svg>
      <span>Ker Avel</span><small>Demeure · Bretagne</small>
    </a>
    <nav class="r" aria-label="Réservation"><details class="menu"><summary>Menu</summary><div class="menu-liens"><a href="./#demeure">La demeure</a><a href="./#chambres">Chambres</a><a href="./#alentours">Alentours</a><a href="./#reserver">Réserver</a></div></details><a class="gold" data-airbnb target="_blank" rel="noopener" href="https://www.airbnb.fr/">Réserver</a></nav>
  </div>
</header>"""


def bandeau_b(liste, actif=None):
    liens = "".join(
        f'<a href="chambre-{x["id"]}.html"' + (' aria-current="page"' if x["id"] == actif else "") + f'>{e(x["nom"])}</a>' for x in liste)
    return f'<nav class="noms gut" aria-label="Les chambres"><div class="wrap">{liens}</div></nav>'


PIED_B = """<footer class="gut"><div class="wrap"><span><b>Ker Avel</b>Pointe du Meinga · 35350 Saint-Coulomb</span><span>contact@ker-avel.bzh<br>+33 6 00 00 00 00<br><small>Photos d'illustration : Unsplash</small></span><!--carte--><!--/carte--></div></footer>"""


def page_b(liste, i):
    c = liste[i]
    prec, suiv = voisins(liste, i)
    vues = "".join(
        f'<figure class="ph{" on" if k == 0 else ""}" style="background:url({img(p)}) center/cover" aria-hidden="{"false" if k == 0 else "true"}"></figure>'
        for k, p in enumerate(c["photos"]))
    carte = lambda x, lbl: (f'<a class="card" href="chambre-{x["id"]}.html"><figure class="ph" style="background:url({img(x["photos"][0])}) center/cover"></figure>'
                            f'<span class="lbl"><span class="k">{lbl}</span><h3>{e(x["nom"])}</h3><span class="more">Découvrir</span></span></a>')
    return tete("domaine", c) + NAV_B.format(cur=' aria-current="page"') + f"""

<main>
  <section class="hero ph gut" aria-label="{e(c['nom'])}" style="background:url({img(c['photos'][0])}) center/cover">
    <div class="in">
      <p class="fil"><a href="./#chambres">Les chambres</a></p>
      <h1>{e(c['nom'])}</h1>
      <p class="sub">{e(c['sous'])}</p>
    </div>
  </section>
  <div class="lin-band" aria-hidden="true"></div>

  <section class="intro gut">
    <div class="wrap">
      {''.join(f'<p>{e(x)}</p>' for x in c['p'])}
    </div>
  </section>

  <section class="dark ch-b gut" aria-label="La chambre en bref">
    <div class="wrap">
      {fiche_dl(c, "fiche-b")}
      <div class="diapo" data-diapo>
        <div class="vues">{vues}</div>
        <div class="diapo-nav">
          <button type="button" data-d="-1" aria-label="Photo précédente">‹</button>
          <p class="compte" aria-live="polite">1 / {len(c['photos'])}</p>
          <button type="button" data-d="1" aria-label="Photo suivante">›</button>
        </div>
      </div>
      <a class="gold" data-airbnb target="_blank" rel="noopener" href="https://www.airbnb.fr/">Réserver cette chambre</a>
    </div>
  </section>

  <section class="disc gut" aria-labelledby="t-suite">
    <div class="wrap">
      <h2 id="t-suite">Poursuivre la visite</h2>
      <div class="duo">{carte(prec, "Chambre précédente")}{carte(suiv, "Chambre suivante")}</div>
    </div>
  </section>
</main>
{bandeau_b(liste, c['id'])}
{PIED_B}
<script>
(function(){{
  var d=document.querySelector("[data-diapo]");if(!d)return;
  var vues=d.querySelectorAll(".vues figure"),compte=d.querySelector(".compte"),i=0;
  d.querySelectorAll("[data-d]").forEach(function(b){{b.addEventListener("click",function(){{
    i=(i+ +b.getAttribute("data-d")+vues.length)%vues.length;
    vues.forEach(function(v,k){{v.classList.toggle("on",k===i);v.setAttribute("aria-hidden",k===i?"false":"true")}});
    compte.textContent=(i+1)+" / "+vues.length;
  }})}});
}})();
</script>
</body>
</html>
"""


# ---------- Piste C : carnet de famille, collage et note manuscrite ----------
def entete_c(plein=False):
    return f"""<header class="top gut{' plein' if plein else ''}">
  <div class="wrap">
    <a class="ruban" href="./" aria-label="Ker Avel, accueil"><span>Bretagne</span></a>
    <a class="brand" href="./">Ker Avel</a>
    <nav aria-label="Navigation principale"><a href="./#maison">La maison</a><a href="./#journee">Une journée</a><a href="./#chambres">Chambres</a><details class="menu"><summary>Menu</summary><div class="menu-liens"><a href="./#maison">La maison</a><a href="./#journee">Une journée</a><a href="./#chambres">Chambres</a></div></details><a class="btn" data-airbnb target="_blank" rel="noopener" href="https://www.airbnb.fr/">Réserver</a></nav>
  </div>
</header>"""


def bandeau_c(liste, actif=None):
    liens = "".join(
        f'<a href="chambre-{x["id"]}.html"' + (' aria-current="page"' if x["id"] == actif else "") + f'>{e(x["nom"])}</a>' for x in liste)
    return f'<nav class="noms gut" aria-label="Les chambres"><div class="wrap">{liens}</div></nav>'


PIED_C = """<footer class="gut"><div class="wrap"><span><b>Ker Avel</b>Pointe du Meinga, 35350 Saint-Coulomb</span><span>contact@ker-avel.bzh<br>+33 6 00 00 00 00<br><small>Photos d'illustration : Unsplash</small></span><!--carte--><!--/carte--></div></footer>"""
FLOTTANT_C = """<a class="flottant" data-airbnb target="_blank" rel="noopener" href="https://www.airbnb.fr/">Réserver</a>
<script>
(function(){
  var b=document.querySelector(".flottant"),h=document.querySelector(".hero")||document.querySelector(".top");if(!b||!h)return;
  new IntersectionObserver(function(es){b.classList.toggle("visible",!es[0].isIntersecting)}).observe(h);
})();
</script>"""


def page_c(liste, i):
    c = liste[i]
    autres = [x for x in liste if x is not c]
    ph = c["photos"]
    lignes = "".join(
        f'<li><a href="chambre-{x["id"]}.html"><span class="n">{e(x["nom"])}</span><span class="s">{e(x["sous"])}</span></a></li>' for x in autres)
    return tete("cire", c) + entete_c(plein=True) + f"""

<main>
  <section class="ch-c gut">
    <div class="wrap">
      <p class="fil"><a href="./#chambres">Les chambres</a></p>
      <div class="ch-titre">
        <h1>{e(c['nom'])}</h1>
        <p class="note">{e(c['note'])}</p>
      </div>
      <ul class="hero-meta"><li>{e(c['lit'])}</li><li>{e(c['surface'])}</li><li>{e(c['vue'])}</li><li>{e(c['bain'])}</li></ul>
    </div>
  </section>
  <div class="collage gut"><div class="wrap">
    <figure class="ph a" style="background:url({img(ph[0])}) center/cover"></figure>
    <figure class="ph b" style="background:url({img(ph[1])}) center/cover"></figure>
    <figure class="ph c" style="background:url({img(ph[2])}) center/cover"></figure>
  </div></div>
  <section class="gut">
    <div class="wrap ch-texte">
      <div>
        <h2>{e(c['sous'])}</h2>
        {''.join(f'<p>{e(x)}</p>' for x in c['p'])}
        <a class="btn" data-airbnb target="_blank" rel="noopener" href="https://www.airbnb.fr/">Réserver cette chambre</a>
      </div>
      <aside class="aime">
        <h3>Ce qu'on aime ici</h3>
        <ul>{''.join(f'<li>{e(x)}</li>' for x in c['aime'])}</ul>
      </aside>
    </div>
  </section>
  <figure class="ph vue" style="background:url({img(ph[3])}) center/cover"></figure>
  <section class="gut liste-autres" aria-labelledby="t-autres">
    <div class="wrap">
      <h2 id="t-autres">Les autres chambres</h2>
      <ul>{lignes}</ul>
    </div>
  </section>
</main>
{PIED_C}
{FLOTTANT_C}
</body>
</html>
"""


PAGES = {"grand-large": page_a, "domaine": page_b, "cire": page_c}

if __name__ == "__main__":
    for piste, liste in CHAMBRES.items():
        for i, c in enumerate(liste):
            chemin = RACINE / piste / f"chambre-{c['id']}.html"
            chemin.write_text(PAGES[piste](liste, i), encoding="utf-8")
            print(chemin.relative_to(RACINE))
