/* Sélecteur de charte graphique. Chargé dans le <head> de chaque piste :
   applique la charte mémorisée tout de suite, puis ajoute le panneau de choix. */
(function () {
  var CHARTES = [
    { id: "", nom: "Originale", desc: "La piste telle que dessinée", couleurs: null },
    { id: "ocre", nom: "Ocre & Ardoise", desc: "Lumineuse, Art déco", couleurs: ["#edeae5", "#c19e60", "#a3afb7", "#2a2b2e"],
      police: "family=Josefin+Sans:wght@300;400;600&family=Lora:ital,wght@0,400;0,500;1,400" },
    { id: "nuit", nom: "Nuit & Or", desc: "Feutrée, hôtel de charme", couleurs: ["#1a171b", "#bd9e56", "#e7d3a0", "#efe7d8"],
      police: "family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Jost:wght@300;400;500" },
    { id: "granit", nom: "Granit rose", desc: "Douce, côte et voile", couleurs: ["#f1e6df", "#d9a594", "#1f3347", "#9a5b49"],
      police: "family=Italiana&family=Karla:wght@300;400;500;700" },
    { id: "lande", nom: "Lande & Bruyère", desc: "Profonde, campagne bretonne", couleurs: ["#2f3a2c", "#8b5a78", "#d1ad73", "#ece5d8"],
      police: "family=Bodoni+Moda:ital,opsz,wght@0,6..96,500;1,6..96,500&family=Work+Sans:wght@300;400;500;600" }
  ];
  var PAGES = [
    { id: "grand-large", nom: "A · Grand Large" },
    { id: "domaine", nom: "B · Domaine" },
    { id: "cire", nom: "C · Ciré" }
  ];
  var CLE = "ker-avel-charte";
  var root = document.documentElement;

  function trouver(id) {
    for (var i = 0; i < CHARTES.length; i++) if (CHARTES[i].id === id) return CHARTES[i];
    return null;
  }
  function lireChoix() {
    var p = new URLSearchParams(location.search).get("charte");
    if (p !== null && trouver(p)) return p;
    try { var s = localStorage.getItem(CLE); if (s && trouver(s)) return s; } catch (e) {}
    return "";
  }
  function chargerPolice(c) {
    if (!c.police || document.getElementById("police-" + c.id)) return;
    var l = document.createElement("link");
    l.rel = "stylesheet";
    l.id = "police-" + c.id;
    l.href = "https://fonts.googleapis.com/css2?" + c.police + "&display=swap";
    document.head.appendChild(l);
  }
  function appliquer(id) {
    var c = trouver(id) || CHARTES[0];
    if (c.id) { root.setAttribute("data-charte", c.id); chargerPolice(c); }
    else root.removeAttribute("data-charte");
    try { if (c.id) localStorage.setItem(CLE, c.id); else localStorage.removeItem(CLE); } catch (e) {}
    var url = new URL(location.href);
    if (c.id) url.searchParams.set("charte", c.id); else url.searchParams.delete("charte");
    history.replaceState(null, "", url);
    return c;
  }

  var actuelle = appliquer(lireChoix());

  function barre(couleurs) {
    var cs = couleurs || ["#bdb4a6", "#8a847b", "#5c5852", "#3a3733"];
    return '<span class="ch-bar" aria-hidden="true">' + cs.map(function (x) { return '<i style="background:' + x + '"></i>'; }).join("") + "</span>";
  }

  function construire() {
    var page = root.getAttribute("data-page");
    var panel = document.createElement("div");
    panel.className = "ch-panel";
    panel.innerHTML =
      '<div class="ch-box" id="ch-box" hidden>' +
        '<h2>Charte graphique</h2><div class="ch-list">' +
        CHARTES.map(function (c) {
          return '<button type="button" class="ch-opt" data-id="' + c.id + '">' + barre(c.couleurs) +
            "<span><b>" + c.nom + "</b><span>" + c.desc + "</span></span></button>";
        }).join("") +
        "</div><h2>Mise en page</h2><nav class=\"ch-pages\" aria-label=\"Pistes\">" +
        PAGES.map(function (p) {
          return '<a href="../' + p.id + '/"' + (p.id === page ? ' aria-current="page"' : "") + ' data-page="' + p.id + '">' + p.nom + "</a>";
        }).join("") +
        "</nav></div>" +
      '<button type="button" class="ch-toggle" aria-expanded="false" aria-controls="ch-box"></button>';
    document.body.appendChild(panel);

    var box = panel.querySelector(".ch-box");
    var toggle = panel.querySelector(".ch-toggle");

    function maj() {
      toggle.innerHTML = barre(actuelle.couleurs) + '<span class="ch-lbl">Charte : ' + actuelle.nom + "</span>";
      toggle.setAttribute("aria-label", "Charte : " + actuelle.nom);
      panel.querySelectorAll(".ch-opt").forEach(function (b) {
        b.setAttribute("aria-pressed", b.getAttribute("data-id") === actuelle.id ? "true" : "false");
      });
      panel.querySelectorAll(".ch-pages a").forEach(function (a) {
        a.href = "../" + a.getAttribute("data-page") + "/" + (actuelle.id ? "?charte=" + actuelle.id : "");
      });
    }
    toggle.addEventListener("click", function () {
      var ouvrir = box.hidden;
      box.hidden = !ouvrir;
      toggle.setAttribute("aria-expanded", ouvrir ? "true" : "false");
    });
    panel.querySelectorAll(".ch-opt").forEach(function (b) {
      b.addEventListener("click", function () { actuelle = appliquer(b.getAttribute("data-id")); maj(); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !box.hidden) { box.hidden = true; toggle.setAttribute("aria-expanded", "false"); toggle.focus(); }
    });
    maj();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", construire);
  else construire();
})();
