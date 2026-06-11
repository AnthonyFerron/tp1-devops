# -*- coding: utf-8 -*-
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                PageBreak, Table, TableStyle, HRFlowable)
from PIL import Image as PILImage

BASE = r"C:\Users\lebos\OneDrive\Bureau\Documents\Projets-g4\3eme annee\cours agile\tp1-devops\rapport"
CAP = os.path.join(BASE, "captures")
OUT = os.path.join(BASE, "Rapport_TP1_DevOps.pdf")

# ---- Couleurs / styles ----
NAVY = colors.HexColor("#0B3D91")
ACCENT = colors.HexColor("#2563EB")
GREEN = colors.HexColor("#16A34A")
GREY = colors.HexColor("#4B5563")
LIGHT = colors.HexColor("#EEF2FF")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle("TitleBig", parent=styles["Title"], fontSize=26,
                          textColor=NAVY, spaceAfter=6, leading=30))
styles.add(ParagraphStyle("Sub", parent=styles["Normal"], fontSize=12,
                          textColor=GREY, alignment=TA_CENTER, leading=18))
styles.add(ParagraphStyle("H1", parent=styles["Heading1"], fontSize=16,
                          textColor=NAVY, spaceBefore=14, spaceAfter=6))
styles.add(ParagraphStyle("H2", parent=styles["Heading2"], fontSize=13,
                          textColor=ACCENT, spaceBefore=10, spaceAfter=4))
styles.add(ParagraphStyle("Body", parent=styles["Normal"], fontSize=10.5,
                          leading=15, alignment=TA_LEFT, spaceAfter=6))
styles.add(ParagraphStyle("Caption", parent=styles["Normal"], fontSize=9,
                          textColor=GREY, alignment=TA_CENTER, spaceBefore=3,
                          spaceAfter=10, fontName="Helvetica-Oblique"))
styles.add(ParagraphStyle("CodeBlk", parent=styles["Code"], fontSize=8.7,
                          leading=11, backColor=colors.HexColor("#0F172A"),
                          textColor=colors.HexColor("#E2E8F0"),
                          borderPadding=8, leftIndent=0))
styles.add(ParagraphStyle("BulletX", parent=styles["Normal"], fontSize=10.5,
                          leading=15, leftIndent=14, bulletIndent=2, spaceAfter=2))

story = []

def fig(name, caption, maxw=16*cm, maxh=15*cm):
    path = os.path.join(CAP, name)
    if not os.path.exists(path):
        return
    iw, ih = PILImage.open(path).size
    ratio = min(maxw/iw, maxh/ih)
    w, h = iw*ratio, ih*ratio
    img = Image(path, width=w, height=h)
    img.hAlign = "CENTER"
    # cadre
    t = Table([[img]], colWidths=[w])
    t.hAlign = "CENTER"
    t.setStyle(TableStyle([("BOX", (0,0), (-1,-1), 0.8, colors.HexColor("#CBD5E1")),
                           ("INNERGRID", (0,0), (-1,-1), 0, colors.white),
                           ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
                           ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0)]))
    story.append(t)
    story.append(Paragraph("📸 " + caption, styles["Caption"]))

def b(txt):
    story.append(Paragraph("• " + txt, styles["BulletX"]))

def p(txt):
    story.append(Paragraph(txt, styles["Body"]))

def h1(txt):
    story.append(Paragraph(txt, styles["H1"]))

def h2(txt):
    story.append(Paragraph(txt, styles["H2"]))

def rule():
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"),
                            spaceBefore=6, spaceAfter=8))

def code(txt):
    safe = (txt.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
               .replace("\n","<br/>").replace(" ","&nbsp;"))
    story.append(Paragraph(safe, styles["CodeBlk"]))
    story.append(Spacer(1, 8))

# ================= PAGE DE GARDE =================
story.append(Spacer(1, 3.2*cm))
story.append(Paragraph("TP 1 &mdash; DevOps", styles["TitleBig"]))
story.append(Paragraph("Mise en place d'une chaîne CI/CD&nbsp;: "
                       "GitHub &rarr; GitHub Actions &rarr; Render", styles["Sub"]))
story.append(Spacer(1, 0.6*cm))
rule()
info = [
    ["Objectif", "Créer une application web, la versionner sur GitHub et la déployer\n"
                 "automatiquement sur Render, puis démontrer le redéploiement continu (CI/CD)."],
    ["Étudiant", "Anthony Ferron (AnthonyFerron)"],
    ["Cours", "3ème année — Méthodes Agiles / DevOps"],
    ["Date", "10 juin 2026"],
    ["Dépôt GitHub", "https://github.com/AnthonyFerron/tp1-devops"],
    ["Application en ligne", "https://tp1-devops-6vgr.onrender.com"],
]
rows = [[Paragraph("<b>"+k+"</b>", styles["Body"]),
         Paragraph(v.replace("\n","<br/>"), styles["Body"])] for k,v in info]
t = Table(rows, colWidths=[4.2*cm, 11.3*cm])
t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(0,-1), LIGHT),
    ("VALIGN",(0,0),(-1,-1),"TOP"),
    ("BOX",(0,0),(-1,-1),0.6, colors.HexColor("#CBD5E1")),
    ("INNERGRID",(0,0),(-1,-1),0.6, colors.HexColor("#E2E8F0")),
    ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
    ("LEFTPADDING",(0,0),(-1,-1),9),("RIGHTPADDING",(0,0),(-1,-1),9),
]))
story.append(t)
story.append(Spacer(1, 0.8*cm))
rule()
story.append(Paragraph("Chaîne DevOps réalisée", styles["H2"]))
story.append(Paragraph(
    "Code &nbsp;&rarr;&nbsp; GitHub &nbsp;&rarr;&nbsp; GitHub Actions (CI) "
    "&nbsp;&rarr;&nbsp; Build &nbsp;&rarr;&nbsp; Render &nbsp;&rarr;&nbsp; Production",
    ParagraphStyle("chain", parent=styles["Body"], alignment=TA_CENTER,
                   fontSize=11.5, textColor=NAVY)))
story.append(PageBreak())

# ================= SYNTHESE =================
h1("1. Synthèse des étapes")
p("Le tableau ci-dessous résume les huit étapes du TP et leur statut. Chaque étape "
  "est détaillée dans les sections suivantes, preuve (capture d'écran) à l'appui.")

syn = [["#", "Étape", "Statut"]]
steps = [
    ("1", "Création des comptes GitHub et Render"),
    ("2", "Création de l'application Node.js / Express (app.js)"),
    ("3", "Création du dépôt GitHub et premier push"),
    ("4", "Connexion Render &harr; GitHub"),
    ("5", "Création du Web Service (build / start)"),
    ("6", "Premier déploiement automatique (URL en ligne)"),
    ("7", "Démonstration CI/CD (modification &rarr; push &rarr; redéploiement auto)"),
    ("8", "Ajout de GitHub Actions (.github/workflows/main.yml)"),
]
for n, lab in steps:
    syn.append([n, Paragraph(lab, styles["Body"]),
                Paragraph('<b><font color="#16A34A">✔ Réalisé</font></b>', styles["Body"])])
t = Table(syn, colWidths=[1*cm, 11.5*cm, 3*cm])
t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0), NAVY),
    ("TEXTCOLOR",(0,0),(-1,0), colors.white),
    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
    ("ALIGN",(0,0),(0,-1),"CENTER"),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, LIGHT]),
    ("BOX",(0,0),(-1,-1),0.6, colors.HexColor("#CBD5E1")),
    ("INNERGRID",(0,0),(-1,-1),0.5, colors.HexColor("#E2E8F0")),
    ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
    ("LEFTPADDING",(0,0),(-1,-1),8),
]))
story.append(t)
story.append(PageBreak())

# ================= ETAPE 1 =================
h1("2. Étape 1 — Création des comptes GitHub et Render")
p("La première étape consiste à disposer d'un compte <b>GitHub</b> (hébergement du code "
  "et exécution de l'intégration continue) et d'un compte <b>Render</b> (plateforme de "
  "déploiement / hébergement de l'application). Le compte Render a été créé via "
  "« Sign in with GitHub », ce qui établit immédiatement le lien entre les deux services "
  "(cf. étape 4).")
b("Compte GitHub : <b>AnthonyFerron</b> — connecté et opérationnel.")
b("Compte Render : créé via GitHub OAuth, e-mail vérifié.")
fig("01_github_connecte.png", "Étape 1 — Tableau de bord GitHub, connecté en tant que « AnthonyFerron ».")
story.append(PageBreak())

# ================= ETAPE 2 =================
h1("3. Étape 2 — Application Node.js / Express")
p("Une application web minimale a été développée avec <b>Express</b>. Elle expose une "
  "route racine « / » renvoyant le message « Bonjour DevOps&nbsp;! ».")
h2("app.js")
code('const express = require("express");\n'
     'const app = express();\n\n'
     'app.get("/", (req, res) => {\n'
     '  res.send("Bonjour DevOps !");\n'
     '});\n\n'
     '// Render fournit le port via la variable d\'environnement PORT.\n'
     'const PORT = process.env.PORT || 3000;\n'
     'app.listen(PORT, () => {\n'
     '  console.log(`Serveur démarré sur le port ${PORT}`);\n'
     '});')
p("<b>Remarque technique importante&nbsp;:</b> l'énoncé utilise <font face='Courier'>app.listen(3000)</font> "
  "en dur. Or Render impose à l'application d'écouter sur le port fourni par la variable "
  "d'environnement <font face='Courier'>PORT</font>. Le code a donc été adapté avec "
  "<font face='Courier'>process.env.PORT || 3000</font> ; sans cela le déploiement échouerait "
  "(le port reste 3000 en repli pour le développement local).")
h2("package.json")
code('{\n'
     '  "name": "tp1-devops",\n'
     '  "version": "1.0.0",\n'
     '  "main": "app.js",\n'
     '  "scripts": { "start": "node app.js" },\n'
     '  "dependencies": { "express": "^4.21.2" }\n'
     '}')
story.append(PageBreak())

# ================= ETAPE 3 =================
h1("4. Étape 3 — Dépôt GitHub et premier push")
p("Le projet a été initialisé en dépôt Git puis poussé vers un nouveau dépôt public "
  "<b>tp1-devops</b> sur GitHub.")
h2("Commandes exécutées")
code('git init -b main\n'
     'git add .\n'
     'git commit -m "Initial commit"\n'
     'git remote add origin https://github.com/AnthonyFerron/tp1-devops.git\n'
     'git push -u origin main')
b("Le fichier <font face='Courier'>.gitignore</font> exclut <font face='Courier'>node_modules/</font> et <font face='Courier'>.env</font> du suivi.")
b("Fichiers versionnés : <font face='Courier'>app.js</font>, <font face='Courier'>package.json</font>, "
  "<font face='Courier'>package-lock.json</font>, <font face='Courier'>.gitignore</font>, "
  "<font face='Courier'>.github/workflows/main.yml</font>.")
fig("02_depot_github_fichiers.png", "Étape 3 — Dépôt « tp1-devops » sur GitHub avec l'ensemble des fichiers (commit « update message », 2 commits).")
story.append(PageBreak())

# ================= ETAPE 4 & 5 =================
h1("5. Étapes 4 & 5 — Render &harr; GitHub et Web Service")
p("Sur Render, un <b>Web Service</b> a été créé à partir du dépôt GitHub <b>tp1-devops</b>. "
  "Render a détecté automatiquement un projet <b>Node</b> et pré-rempli la configuration. "
  "L'offre <b>Free</b> (0,1 CPU / 512 Mo) a été choisie.")
h2("Configuration du service")
cfg = [["Paramètre", "Valeur"],
       ["Dépôt source", "AnthonyFerron/tp1-devops (branche main)"],
       ["Langage", "Node"],
       ["Build Command", "npm install"],
       ["Start Command", "node app.js"],
       ["Type d'instance", "Free — 0,1 CPU / 512 Mo"],
       ["Région", "Oregon (US West)"],
       ["Auto-Deploy", "On Commit (redéploiement à chaque push)"]]
rows = [[Paragraph("<b>"+r[0]+"</b>" if i==0 else r[0], styles["Body"]),
         Paragraph("<b>"+r[1]+"</b>" if i==0 else r[1], styles["Body"])]
        for i,r in enumerate(cfg)]
t = Table(rows, colWidths=[5*cm, 10.5*cm])
t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0), ACCENT),("TEXTCOLOR",(0,0),(-1,0),colors.white),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, LIGHT]),
    ("BOX",(0,0),(-1,-1),0.6, colors.HexColor("#CBD5E1")),
    ("INNERGRID",(0,0),(-1,-1),0.5, colors.HexColor("#E2E8F0")),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ("LEFTPADDING",(0,0),(-1,-1),8),
]))
story.append(t)
story.append(Spacer(1, 8))
fig("03_render_settings_top.png", "Étapes 4/5 — Web Service Render « tp1-devops » : type Node, offre Free, dépôt GitHub lié et URL de production.", maxh=12*cm)
story.append(PageBreak())
fig("03_render_build_command.png", "Étape 5 — Build Command : « npm install » (conforme à l'énoncé).", maxh=11*cm)
fig("04_render_start_autodeploy.png", "Étape 5/7 — Start Command : « node app.js » et Auto-Deploy réglé sur « On Commit ».", maxh=11*cm)
story.append(PageBreak())

# ================= ETAPE 6 =================
h1("6. Étape 6 — Premier déploiement")
p("Render a lancé automatiquement le premier build puis le déploiement. L'application est "
  "devenue accessible publiquement à l'adresse&nbsp;:")
story.append(Paragraph("https://tp1-devops-6vgr.onrender.com",
             ParagraphStyle("url", parent=styles["Body"], alignment=TA_CENTER,
                            fontSize=12, textColor=ACCENT, spaceAfter=8)))
b("Build : <font face='Courier'>npm install</font> &mdash; Démarrage : <font face='Courier'>node app.js</font>.")
b("Statut « <b><font color='#16A34A'>Deploy live</font></b> » obtenu pour le commit « Initial commit » (73ffad6).")
b("Vérification HTTP : la page répond <b>200</b> avec « Bonjour DevOps&nbsp;! ».")
story.append(PageBreak())

# ================= ETAPE 7 =================
h1("7. Étape 7 — Démonstration CI/CD (cœur du TP)")
p("Pour démontrer l'esprit DevOps, le message a été modifié dans le code source, "
  "« <b>Bonjour DevOps&nbsp;!</b> » &rarr; « <b>Bonjour DevOps 2026&nbsp;!</b> », puis simplement "
  "poussé sur GitHub&nbsp;:")
code('git add .\n'
     'git commit -m "update message"\n'
     'git push')
p("<b>Sans aucune action manuelle sur Render</b>, le push a déclenché toute la chaîne : "
  "nouveau commit détecté &rarr; nouveau build &rarr; nouveau déploiement &rarr; nouveau "
  "site en ligne. C'est exactement l'avantage du CI/CD.")
b("Render affiche « <b>Deploy started for 0260d00 — New commit via Auto-Deploy</b> » puis "
  "« <b><font color='#16A34A'>Deploy live</font></b> ».")
b("La page en ligne affiche désormais « Bonjour DevOps 2026&nbsp;! » (contenu mis à jour automatiquement).")
fig("05_render_events_autodeploy.png", "Étape 7 — Historique des déploiements Render : « Initial commit » (live), puis « New commit via Auto-Deploy » → « update message » (live). Aucune action manuelle.", maxh=11*cm)
fig("06_page_live_2026.png", "Étape 7 — Application en ligne après le push : « Bonjour DevOps 2026 ! » sur l'URL onrender.com.", maxh=8*cm)
story.append(PageBreak())

# ================= ETAPE 8 =================
h1("8. Étape 8 — GitHub Actions (CI)")
p("Un workflow d'intégration continue a été ajouté. À chaque <font face='Courier'>push</font>, "
  "GitHub Actions récupère le code, installe Node 20 et exécute "
  "<font face='Courier'>npm install</font> — ce qui valide que le projet se construit correctement.")
h2(".github/workflows/main.yml")
code('name: CI\n\n'
     'on:\n'
     '  push:\n\n'
     'jobs:\n'
     '  test:\n'
     '    runs-on: ubuntu-latest\n'
     '    steps:\n'
     '      - uses: actions/checkout@v4\n'
     '      - uses: actions/setup-node@v4\n'
     '        with:\n'
     '          node-version: 20\n'
     '      - run: npm install')
p("Résultat observé dans l'onglet <b>Actions</b> du dépôt : <b>2 exécutions du workflow CI</b>, "
  "toutes deux <b><font color='#16A34A'>réussies (vertes)</font></b> :")
ci = [["Run", "Commit", "Déclencheur", "Statut", "Durée"],
      ["CI #1", "73ffad6 — Initial commit", "push", "✔ Réussi", "~13 s"],
      ["CI #2", "0260d00 — update message", "push", "✔ Réussi", "~14 s"]]
rows=[]
for i,r in enumerate(ci):
    if i==0:
        rows.append([Paragraph("<b>"+c+"</b>", styles["Body"]) for c in r])
    else:
        rows.append([Paragraph(c, styles["Body"]) for c in r[:3]] +
                    [Paragraph('<b><font color="#16A34A">'+r[3]+'</font></b>', styles["Body"]),
                     Paragraph(r[4], styles["Body"])])
t = Table(rows, colWidths=[1.8*cm, 6.2*cm, 2.4*cm, 2.6*cm, 2.5*cm])
t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0), NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, LIGHT]),
    ("BOX",(0,0),(-1,-1),0.6, colors.HexColor("#CBD5E1")),
    ("INNERGRID",(0,0),(-1,-1),0.5, colors.HexColor("#E2E8F0")),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ("LEFTPADDING",(0,0),(-1,-1),7),
]))
story.append(t)
story.append(Spacer(1, 10))

# ================= CONCLUSION =================
rule()
h1("9. Conclusion")
p("L'ensemble des objectifs du TP a été atteint. Une chaîne DevOps complète et fonctionnelle "
  "a été mise en place :")
story.append(Paragraph(
    "<b>Code &rarr; GitHub &rarr; GitHub Actions (CI) &rarr; Build &rarr; Render &rarr; Production</b>",
    ParagraphStyle("ccl", parent=styles["Body"], alignment=TA_CENTER, fontSize=11.5,
                   textColor=NAVY, spaceBefore=4, spaceAfter=8)))
p("La démonstration clé (étape 7) prouve l'automatisation complète&nbsp;: une simple "
  "modification du code, validée par un <font face='Courier'>git push</font>, déclenche "
  "l'intégration continue (GitHub Actions) et le déploiement continu (Render) "
  "<b>sans aucune intervention manuelle</b>. C'est précisément la valeur ajoutée du CI/CD.")

# ---- Pied de page / numérotation ----
def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#CBD5E1"))
    canvas.line(2*cm, 1.5*cm, A4[0]-2*cm, 1.5*cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GREY)
    canvas.drawString(2*cm, 1.1*cm, "TP 1 DevOps — Rapport de réalisation — Anthony Ferron")
    canvas.drawRightString(A4[0]-2*cm, 1.1*cm, "Page %d" % doc.page)
    canvas.restoreState()

doc = SimpleDocTemplate(OUT, pagesize=A4, topMargin=2*cm, bottomMargin=2.2*cm,
                        leftMargin=2.2*cm, rightMargin=2.2*cm,
                        title="Rapport TP1 DevOps", author="Anthony Ferron")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("OK ->", OUT, os.path.getsize(OUT), "bytes")
