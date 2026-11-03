#!/usr/bin/env python3
"""Genera los SVG animados del perfil en ../assets (solo biblioteca estándar)."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import generar_stats  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, "..", "assets")
os.makedirs(SALIDA, exist_ok=True)

BG, S1, S2 = "#070B12", "#0D1421", "#111C2B"
BLUE, CYAN, PURPLE = "#3B82F6", "#22D3EE", "#8B5CF6"
TXT, MUTED, LINE = "#F8FAFC", "#94A3B8", "#1E293B"
SANS = "Inter,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

COMUN = f"""
<linearGradient id="gTxt" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset=".55" stop-color="{BLUE}"/><stop offset="1" stop-color="{PURPLE}"/></linearGradient>
<linearGradient id="gLine" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></linearGradient>
<linearGradient id="gSweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".10"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="gScan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}" stop-opacity=".55"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{MUTED}" stroke-opacity=".08"/></pattern>
<filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
"""


def envolver(w, h, cuerpo, etiqueta, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{etiqueta}"><defs>{COMUN}{defs}</defs>{cuerpo}</svg>')


def guardar(nombre, contenido):
    with open(os.path.join(SALIDA, nombre), "w", encoding="utf-8") as f:
        f.write(contenido)
    print("ok", nombre, len(contenido) // 1024, "KB")


def parpadeo(x, y, w, h, color):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}">'
            f'<animate attributeName="opacity" values="1;0" dur="1.1s" repeatCount="indefinite" calcMode="discrete"/></rect>')


# --------------------------------------------------------------------- header
def header():
    W, H = 1000, 420
    nodos = [(600, 80), (690, 50), (780, 110), (880, 60), (950, 130), (640, 190), (740, 225),
             (840, 180), (930, 245), (610, 305), (710, 340), (810, 305), (900, 350), (960, 320)]
    aristas = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (2, 7), (1, 6), (5, 6), (6, 7), (7, 8), (4, 8), (5, 9),
               (6, 10), (6, 11), (7, 11), (8, 12), (9, 10), (10, 11), (11, 12), (12, 13), (8, 13), (2, 6), (3, 7)]
    s = [f'<rect width="{W}" height="{H}" rx="20" fill="{BG}"/>',
         '<clipPath id="cl"><rect width="1000" height="420" rx="20"/></clipPath><g clip-path="url(#cl)">',
         f'<rect width="{W}" height="{H}" fill="url(#grid)"/>',
         f'<radialGradient id="b1"><stop offset="0" stop-color="{BLUE}" stop-opacity=".38"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>',
         f'<radialGradient id="b2"><stop offset="0" stop-color="{PURPLE}" stop-opacity=".34"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></radialGradient>',
         f'<radialGradient id="b3"><stop offset="0" stop-color="{CYAN}" stop-opacity=".22"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>',
         '<circle cx="820" cy="130" r="260" fill="url(#b1)"><animateTransform attributeName="transform" type="translate" values="0 0;-40 30;0 0" dur="11s" repeatCount="indefinite"/></circle>',
         '<circle cx="960" cy="400" r="240" fill="url(#b2)"><animateTransform attributeName="transform" type="translate" values="0 0;-50 -20;0 0" dur="13s" repeatCount="indefinite"/></circle>',
         '<circle cx="120" cy="60" r="200" fill="url(#b3)"><animateTransform attributeName="transform" type="translate" values="0 0;40 30;0 0" dur="15s" repeatCount="indefinite"/></circle>']
    for i, (a, b) in enumerate(aristas):
        (x1, y1), (x2, y2) = nodos[a], nodos[b]
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{BLUE}" stroke-opacity=".42" stroke-width="1.3"/>')
        if i % 3 == 0:
            s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{CYAN}" stroke-width="1.5" stroke-dasharray="5 9">'
                     f'<animate attributeName="stroke-dashoffset" from="0" to="-28" dur="{1.1 + (i % 4) * .3:.1f}s" repeatCount="indefinite"/></line>')
    for i, (a, b) in enumerate(aristas):
        if i % 2 == 0:
            (x1, y1), (x2, y2) = nodos[a], nodos[b]
            col = CYAN if i % 4 == 0 else PURPLE
            s.append(f'<circle r="3.2" fill="{col}" filter="url(#glow)"><animateMotion dur="{2.2 + (i % 5) * .5:.1f}s" begin="{(i % 7) * .35:.2f}s" '
                     f'repeatCount="indefinite" path="M{x1} {y1} L{x2} {y2}"/></circle>')
    cols = [CYAN, BLUE, PURPLE]
    for i, (x, y) in enumerate(nodos):
        r = 9 if i in (2, 7, 6) else 6
        s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{S1}" stroke="{cols[i % 3]}" stroke-width="1.8">'
                 f'<animate attributeName="r" values="{r};{r + 2.5};{r}" dur="3.2s" begin="{i * .23:.2f}s" repeatCount="indefinite"/></circle>'
                 f'<circle cx="{x}" cy="{y}" r="2.4" fill="{cols[i % 3]}"/>')
    for txt, (x, y) in {"API": nodos[2], "ML": nodos[7], "DB": nodos[10], "UI": nodos[8], "DATA": nodos[5]}.items():
        s.append(f'<text x="{x + 14}" y="{y - 12}" font-family="{MONO}" font-size="11" fill="{CYAN}" fill-opacity=".85" letter-spacing="1.5">{txt}</text>')
    s.append('<rect x="0" y="0" width="2" height="420" fill="url(#gScan)"><animateTransform attributeName="transform" type="translate" values="-10 0;1010 0" dur="8s" repeatCount="indefinite"/></rect>')
    s.append('</g>')
    s.append(f'<path d="M30 54V30H54M970 366V390H946" fill="none" stroke="{MUTED}" stroke-opacity=".45" stroke-width="1.4"/>')
    # texto
    s.append(f'<circle cx="62" cy="60" r="4.5" fill="{CYAN}"><animate attributeName="opacity" values="1;.25;1" dur="1.8s" repeatCount="indefinite"/></circle>')
    s.append(f'<text x="76" y="64.5" font-family="{MONO}" font-size="13" fill="{CYAN}" letter-spacing="3">SOFTWARE ENGINEERING</text>')
    s.append(parpadeo(300, 52, 8, 16, CYAN))
    s.append(f'<text x="54" y="178" font-family="{SANS}" font-size="100" font-weight="800" fill="{TXT}" letter-spacing="-3">Mathias</text>')
    s.append(f'<text x="54" y="276" font-family="{SANS}" font-size="100" font-weight="800" fill="url(#gTxt)" letter-spacing="-3">Castillo</text>')
    s.append(f'<rect x="58" y="298" width="150" height="4" rx="2" fill="url(#gTxt)"><animate attributeName="width" values="0;150;150" keyTimes="0;.15;1" dur="6s" repeatCount="indefinite"/></rect>')
    s.append(f'<text x="58" y="340" font-family="{SANS}" font-size="21" fill="{MUTED}">Backend  <tspan fill="{CYAN}">/</tspan>  AI &amp; Data  <tspan fill="{CYAN}">/</tspan>  Software Architecture</text>')
    s.append(f'<line x1="54" y1="372" x2="946" y2="372" stroke="{LINE}"/>')
    s.append(f'<text x="58" y="396" font-family="{MONO}" font-size="12" fill="{MUTED}" letter-spacing="2">UPAO · INGENIERÍA DE SISTEMAS E IA · TRUJILLO, PE</text>')
    s.append(f'<text x="946" y="396" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUTED}" fill-opacity=".8" letter-spacing="2">8.11°S 79.03°W</text>')
    s.append(f'<rect x=".5" y=".5" width="999" height="419" rx="20" fill="none" stroke="{LINE}"/>')
    guardar("header.svg", envolver(W, H, "".join(s), "Mathias Castillo — Software Engineering. Backend, AI y Data, Software Architecture"))


# ------------------------------------------------------------------ secciones
def titulo(n, texto, etiqueta, archivo):
    W, H = 1000, 74
    s = [f'<rect x=".5" y=".5" width="999" height="73" rx="16" fill="{S1}" stroke="{LINE}"/>',
         f'<text x="28" y="45" font-family="{MONO}" font-size="14" fill="{CYAN}" letter-spacing="2">{n:02d}</text>',
         f'<text x="72" y="47" font-family="{SANS}" font-size="28" font-weight="800" fill="{TXT}" letter-spacing="-.5">{texto}</text>',
         f'<text x="972" y="45" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUTED}" letter-spacing="2">// {etiqueta}</text>',
         f'<rect x="28" y="62" width="944" height="2" rx="1" fill="{LINE}"/>',
         f'<rect x="28" y="62" width="260" height="2" rx="1" fill="url(#gLine)"/>',
         f'<circle cy="63" r="3.5" fill="{CYAN}" filter="url(#glow)"><animate attributeName="cx" values="28;972;28" dur="9s" repeatCount="indefinite"/></circle>']
    guardar(archivo, envolver(W, H, "".join(s), texto))


def ahora():
    W, H = 1000, 84
    s = [f'<rect x=".5" y=".5" width="999" height="83" rx="16" fill="{S1}" stroke="{LINE}"/>',
         f'<rect x="0" y="0" width="999" height="83" rx="16" fill="url(#gSweep)" opacity=".7"><animateTransform attributeName="transform" type="translate" values="-1000 0;1000 0" dur="7s" repeatCount="indefinite"/></rect>',
         f'<circle cx="34" cy="42" r="12" fill="{CYAN}" fill-opacity=".18"><animate attributeName="r" values="7;15;7" dur="2s" repeatCount="indefinite"/><animate attributeName="fill-opacity" values=".35;0;.35" dur="2s" repeatCount="indefinite"/></circle>',
         f'<circle cx="34" cy="42" r="5" fill="{CYAN}"/>',
         f'<text x="62" y="36" font-family="{MONO}" font-size="11" fill="{CYAN}" letter-spacing="3">CONSTRUYENDO</text>',
         f'<text x="62" y="60" font-family="{SANS}" font-size="18" font-weight="600" fill="{TXT}">Sistemas full stack con IA, bases de datos y backend</text>',
         f'<line x1="640" y1="20" x2="640" y2="64" stroke="{LINE}"/>',
         f'<text x="666" y="36" font-family="{MONO}" font-size="11" fill="{PURPLE}" letter-spacing="3">APRENDIENDO</text>',
         f'<text x="666" y="60" font-family="{SANS}" font-size="18" font-weight="600" fill="{TXT}">IaC · CI/CD · AWS</text>']
    guardar("ahora.svg", envolver(W, H, "".join(s), "Construyendo sistemas full stack con IA, bases de datos y backend. Aprendiendo IaC, CI/CD y AWS"))


def sobre_mi():
    W, H = 1000, 250
    lineas = ["Estudio Ingeniería de Sistemas e IA en la UPAO. Antes de escribir código intento entender el problema:",
              "defino el alcance en historias de usuario, diseño la arquitectura y recién después implemento.",
              "Trabajo con Scrum y XP en proyectos que combinan frontend, backend, bases de datos e IA."]
    s = [f'<rect x=".5" y=".5" width="999" height="249" rx="16" fill="{S1}" stroke="{LINE}"/>',
         f'<rect x="0" y="24" width="4" height="120" rx="2" fill="url(#gTxt)"/>']
    for i, t in enumerate(lineas):
        s.append(f'<text x="40" y="{58 + i * 32}" font-family="{SANS}" font-size="18" fill="{TXT}" fill-opacity="0">{t}'
                 f'<animate attributeName="fill-opacity" values="0;0;1;1" keyTimes="0;{.05 + i * .1:.2f};{.2 + i * .1:.2f};1" dur="1.6s" fill="freeze"/></text>')
    s.append(f'<text x="40" y="164" font-family="{SANS}" font-size="15" fill="{MUTED}">Estoy en etapa de formación: más abajo separo lo que ya usé en proyectos de lo que estoy aprendiendo.</text>')
    chips = [("FORMACIÓN", "UPAO · 6.º ciclo", CYAN), ("UBICACIÓN", "Trujillo, Perú", BLUE), ("METODOLOGÍA", "Scrum · XP", PURPLE)]
    for i, (k, v, c) in enumerate(chips):
        x = 40 + i * 310
        s.append(f'<rect x="{x}" y="188" width="290" height="38" rx="10" fill="{S2}" stroke="{c}" stroke-opacity=".5"/>'
                 f'<circle cx="{x + 18}" cy="207" r="4" fill="{c}"/>'
                 f'<text x="{x + 34}" y="211" font-family="{MONO}" font-size="11" fill="{MUTED}" letter-spacing="2">{k}</text>'
                 f'<text x="{x + 142}" y="212" font-family="{SANS}" font-size="15" font-weight="600" fill="{TXT}">{v}</text>')
    guardar("sobre-mi.svg", envolver(W, H, "".join(s), "Estudio Ingeniería de Sistemas e IA en la UPAO. Trabajo con Scrum y XP en proyectos de frontend, backend, bases de datos e IA"))


# ---------------------------------------------------------------------- stack
def stack():
    W, H = 1000, 440
    cat = {"len": CYAN, "web": BLUE, "dat": PURPLE, "met": "#CBD5E1", "apr": MUTED}
    celdas = [("Py", "Python", "len"), ("Jv", "Java", "len"), ("C#", "C#", "len"), ("JS", "JavaScript", "len"), ("TS", "TypeScript", "len"),
              ("Fa", "FastAPI", "web"), ("Re", "React", "web"), ("Vi", "Vite", "web"),
              ("Tw", "Tailwind", "web"), ("H5", "HTML", "web"), ("C3", "CSS", "web"),
              ("Sk", "scikit-learn", "dat"), ("Pd", "pandas", "dat"), ("Oa", "OpenAI API", "dat"),
              ("My", "MySQL", "dat"), ("Or", "Oracle", "dat"), ("Pg", "PostgreSQL", "dat"), ("Ne", "Neon", "dat"),
              ("Su", "Supabase", "dat"), ("Sc", "Scrum", "met"), ("XP", "Extreme Prog.", "met"),
              ("IaC", "Infra. como código", "apr"), ("CI", "CI/CD", "apr"), ("Aw", "AWS", "apr")]
    leyenda = [("Lenguajes", "len", False), ("Backend y frontend", "web", False), ("Datos e IA", "dat", False), ("Metodología", "met", False), ("En aprendizaje", "apr", True)]
    s = [f'<rect x=".5" y=".5" width="999" height="439" rx="16" fill="{S1}" stroke="{LINE}"/>']
    x = 40
    for nombre, k, dash in leyenda:
        s.append(f'<rect x="{x}" y="28" width="12" height="12" rx="3" fill="none" stroke="{cat[k]}" stroke-width="1.6"{" stroke-dasharray=\"3 2\"" if dash else ""}/>'
                 f'<rect x="{x + 3}" y="31" width="6" height="6" rx="1.5" fill="{cat[k]}"{" fill-opacity=\".45\"" if dash else ""}/>'
                 f'<text x="{x + 20}" y="39" font-family="{MONO}" font-size="12" fill="{MUTED}" letter-spacing="1">{nombre}</text>')
        x += 40 + len(nombre) * 8 + 24
    cw, ch, gap, x0, y0 = 108, 104, 8, 40, 64
    s.append(f'<clipPath id="cg"><rect x="{x0}" y="{y0}" width="920" height="{3 * ch + 2 * gap}"/></clipPath><g clip-path="url(#cg)">')
    for i, (sim, nom, k) in enumerate(celdas):
        cx, cy = x0 + (i % 8) * (cw + gap), y0 + (i // 8) * (ch + gap)
        c = cat[k]
        dash = ' stroke-dasharray="5 4"' if k == "apr" else ""
        d = i * .03
        s.append(f'<g><animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{d / 1.8:.3f};{(d + .35) / 1.8:.3f};1" dur="1.8s" fill="freeze"/>'
                 f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="12" fill="{S2}" stroke="{c}" stroke-opacity=".6"{dash}/>'
                 f'<rect x="{cx + 12}" y="{cy}" width="{cw - 24}" height="3" rx="1.5" fill="{c}"><animate attributeName="opacity" values="1;.35;1" dur="{3 + (i % 5) * .4:.1f}s" repeatCount="indefinite"/></rect>'
                 f'<text x="{cx + 12}" y="{cy + 24}" font-family="{MONO}" font-size="10" fill="{MUTED}" letter-spacing="1">{i + 1:02d}</text>'
                 f'<text x="{cx + cw / 2}" y="{cy + 62}" text-anchor="middle" font-family="{SANS}" font-size="{30 if len(sim) < 3 else 26}" font-weight="800" fill="{c}">{sim}</text>'
                 f'<text x="{cx + cw / 2}" y="{cy + 88}" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="{MUTED}">{nom}</text></g>')
    s.append(f'<rect x="0" y="{y0}" width="130" height="{3 * ch + 2 * gap}" fill="url(#gSweep)"><animateTransform attributeName="transform" type="translate" values="-200 0;1100 0" dur="6s" repeatCount="indefinite"/></rect></g>')
    guardar("stack.svg", envolver(W, H, "".join(s), "Stack técnico. Lenguajes: Python, Java, C#, JavaScript, TypeScript. Backend y frontend: FastAPI, React, Vite, Tailwind, HTML, CSS. Datos e IA: scikit-learn, pandas, OpenAI API, MySQL, Oracle, PostgreSQL, Neon, Supabase. Metodología: Scrum, XP. En aprendizaje: IaC, CI/CD, AWS"))


# ------------------------------------------------------------------ proyectos
def tarjeta(archivo, pid, categoria, nombre, desc, chips, color, visual, etiqueta):
    W, H = 490, 352
    s = [f'<rect x=".5" y=".5" width="489" height="351" rx="16" fill="{S1}" stroke="{color}" stroke-opacity=".45"/>',
         f'<rect x="1" y="1" width="488" height="168" rx="15" fill="{color}" fill-opacity=".05"/>',
         f'<rect x="16" y="1" width="458" height="2.5" rx="1" fill="{color}" fill-opacity=".35"/>',
         f'<rect x="16" y="0.5" width="80" height="3" rx="1.5" fill="{color}" filter="url(#glow)"><animate attributeName="x" values="16;394;16" dur="7s" repeatCount="indefinite"/></rect>',
         f'<text x="24" y="34" font-family="{MONO}" font-size="12" fill="{color}" letter-spacing="2">{pid}</text>',
         f'<text x="466" y="34" text-anchor="end" font-family="{MONO}" font-size="11" fill="{MUTED}" letter-spacing="2">{categoria}</text>',
         visual,
         f'<text x="24" y="206" font-family="{SANS}" font-size="25" font-weight="800" fill="{TXT}" letter-spacing="-.3">{nombre}</text>']
    for i, t in enumerate(desc):
        s.append(f'<text x="24" y="{232 + i * 20}" font-family="{SANS}" font-size="14.5" fill="{MUTED}">{t}</text>')
    x = 24
    for c in chips:
        w = 18 + len(c) * 7.8
        s.append(f'<rect x="{x}" y="278" width="{w:.0f}" height="26" rx="13" fill="{S2}" stroke="{LINE}"/>'
                 f'<text x="{x + w / 2:.0f}" y="295" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{TXT}">{c}</text>')
        x += w + 8
    s.append(f'<text x="24" y="333" font-family="{MONO}" font-size="12" fill="{color}" letter-spacing="1">VER PROYECTO <tspan>'
             f'<animate attributeName="dx" values="0;6;0" dur="1.6s" repeatCount="indefinite"/>→</tspan></text>')
    guardar(archivo, envolver(W, H, "".join(s), etiqueta))


def vis_pipeline():
    cajas = [("React + Vite", 28), ("FastAPI", 190), ("OpenAI API", 352)]
    s = []
    for t, x in cajas:
        s.append(f'<rect x="{x}" y="64" width="110" height="52" rx="12" fill="{S2}" stroke="{CYAN}" stroke-opacity=".6"/>'
                 f'<text x="{x + 55}" y="95" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="700" fill="{TXT}">{t}</text>')
    for x1, x2 in ((138, 190), (300, 352)):
        s.append(f'<line x1="{x1}" y1="90" x2="{x2}" y2="90" stroke="{CYAN}" stroke-width="1.6" stroke-dasharray="4 5"><animate attributeName="stroke-dashoffset" from="0" to="-18" dur=".9s" repeatCount="indefinite"/></line>'
                 f'<circle r="3.5" fill="{CYAN}" filter="url(#glow)"><animateMotion dur="1.8s" repeatCount="indefinite" path="M{x1} 90 L{x2} 90"/></circle>')
    s.append(f'<text x="83" y="146" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{MUTED}">texto / PDF</text>'
             f'<text x="245" y="146" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{MUTED}">sin guardar datos</text>'
             f'<text x="407" y="146" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{MUTED}">resumen · mapa</text>')
    return "".join(s)


def vis_asientos():
    s = []
    for f in range(4):
        for c in range(10):
            x = 90 + c * 30 + (18 if c >= 5 else 0)
            y = 48 + f * 22 + (8 if f >= 2 else 0)
            idx = f * 10 + c
            ocupado = idx in (2, 3, 11, 17, 23, 31, 36)
            sel = idx in (14, 15)
            fill = MUTED if ocupado else S2
            op = .45 if ocupado else 1
            stroke = BLUE if not ocupado else MUTED
            extra = ""
            if sel:
                extra = f'<animate attributeName="fill" values="{S2};{BLUE};{S2}" dur="2.4s" repeatCount="indefinite"/>'
            s.append(f'<rect x="{x}" y="{y}" width="22" height="18" rx="5" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-opacity=".7">{extra}</rect>')
    s.append(f'<text x="24" y="160" font-family="{MONO}" font-size="10.5" fill="{MUTED}">selección de asiento · compra · ticket electrónico</text>')
    return "".join(s)


def vis_regresion():
    s = [f'<path d="M40 134V52M40 134H458" stroke="{MUTED}" stroke-opacity=".5" fill="none"/>']
    puntos = []
    for i in range(22):
        x = 56 + i * 18.5
        t = i / 21
        y = 118 - t * 56 + ((i * 37) % 17 - 8) * 1.5
        puntos.append((x, y))
    for i, (x, y) in enumerate(puntos):
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="{PURPLE}" fill-opacity="0"><animate attributeName="fill-opacity" values="0;0;.9;.9" keyTimes="0;{i / 40:.2f};{i / 40 + .1:.2f};1" dur="3s" repeatCount="indefinite"/></circle>')
    s.append(f'<path d="M52 116 L450 60" stroke="{CYAN}" stroke-width="2" fill="none" stroke-dasharray="420" stroke-dashoffset="420" filter="url(#glow)">'
             f'<animate attributeName="stroke-dashoffset" values="420;420;0;0" keyTimes="0;.35;.75;1" dur="3s" repeatCount="indefinite"/></path>')
    s.append(f'<text x="44" y="46" font-family="{MONO}" font-size="10.5" fill="{MUTED}">nivel_conocimiento ∈ [0, 1]</text>'
             f'<text x="458" y="152" text-anchor="end" font-family="{MONO}" font-size="10.5" fill="{MUTED}">períodos de práctica</text>')
    return "".join(s)


def vis_tabla():
    s = [f'<rect x="28" y="50" width="434" height="22" rx="6" fill="{S2}"/>']
    for x, w in ((40, 70), (210, 50), (340, 60)):
        s.append(f'<rect x="{x}" y="57" width="{w}" height="8" rx="4" fill="{MUTED}" fill-opacity=".6"/>')
    anchos = [(110, 70), (90, 56), (130, 78), (100, 64)]
    for i, (a, b) in enumerate(anchos):
        y = 82 + i * 22
        col = [CYAN, BLUE, PURPLE, CYAN][i]
        s.append(f'<rect x="40" y="{y + 3}" width="{a}" height="7" rx="3.5" fill="{MUTED}" fill-opacity=".28"/>'
                 f'<rect x="210" y="{y + 3}" width="{b}" height="7" rx="3.5" fill="{col}" fill-opacity=".7"><animate attributeName="width" values="0;{b};{b}" keyTimes="0;.4;1" dur="3s" begin="{i * .25:.2f}s" repeatCount="indefinite"/></rect>'
                 f'<circle cx="352" cy="{y + 6.5}" r="4" fill="{col}"><animate attributeName="opacity" values="1;.3;1" dur="{2 + i * .4:.1f}s" repeatCount="indefinite"/></circle>')
    return "".join(s)


def proyectos():
    tarjeta("proyecto-01.svg", "P-01", "FULL STACK · IA", "Plataforma Estudio AI",
            ["Resúmenes y mapas conceptuales con IA a partir de", "texto o PDF. Backend en FastAPI, sin base de datos."],
            ["React", "FastAPI", "OpenAI", "Google OAuth"], CYAN, vis_pipeline(),
            "Proyecto P-01 Plataforma Estudio AI: resúmenes y mapas conceptuales con IA. React, FastAPI, OpenAI, Google OAuth")
    tarjeta("proyecto-02.svg", "P-02", "FRONTEND · WEB", "RutaLibre",
            ["Portal de transporte terrestre: búsqueda de viajes,", "compra de pasajes y tickets electrónicos."],
            ["React", "Vite", "Scrum"], BLUE, vis_asientos(),
            "Proyecto P-02 RutaLibre: portal web de transporte terrestre. React, Vite, Scrum")
    tarjeta("proyecto-03.svg", "P-03", "MACHINE LEARNING", "Agente Educativo Inteligente",
            ["Regresión que estima el nivel de conocimiento (0–1)", "por estudiante y concepto. Dataset sintético de 125 000."],
            ["Python", "scikit-learn", "pandas"], PURPLE, vis_regresion(),
            "Proyecto P-03 Agente Educativo Inteligente: modelo de regresión del nivel de conocimiento. Python, scikit-learn, pandas")
    tarjeta("proyecto-04.svg", "P-04", "SISTEMA EMPRESARIAL", "NEXORA Finance",
            ["Gestión y auditoría de préstamos para una financiera", "con varias agencias. Base de datos en Supabase en curso."],
            ["React", "TypeScript", "Tailwind", "Supabase"], BLUE, vis_tabla(),
            "Proyecto P-04 NEXORA Finance: gestión y auditoría de préstamos. React, TypeScript, Tailwind, Supabase")


# ------------------------------------------------------------ contacto / pie
def boton(archivo, texto, color, glifo):
    W, H = 200, 54
    s = [f'<rect x=".5" y=".5" width="199" height="53" rx="27" fill="{S1}" stroke="{color}" stroke-opacity=".7"/>',
         f'<rect x=".5" y=".5" width="199" height="53" rx="27" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="40 340" filter="url(#glow)"><animate attributeName="stroke-dashoffset" from="0" to="-380" dur="4s" repeatCount="indefinite"/></rect>',
         f'<circle cx="34" cy="27" r="14" fill="{color}" fill-opacity=".15"/>',
         f'<text x="34" y="32" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="800" fill="{color}">{glifo}</text>',
         f'<text x="62" y="32" font-family="{SANS}" font-size="16" font-weight="700" fill="{TXT}">{texto}</text>']
    guardar(archivo, envolver(W, H, "".join(s), texto))


def pie():
    W, H = 1000, 110
    s = [f'<rect x=".5" y=".5" width="999" height="109" rx="16" fill="{S1}" stroke="{LINE}"/>',
         f'<line x1="40" y1="30" x2="960" y2="30" stroke="{LINE}"/>',
         f'<circle cy="30" r="3.5" fill="{CYAN}" filter="url(#glow)"><animate attributeName="cx" values="40;960;40" dur="10s" repeatCount="indefinite"/></circle>',
         f'<text x="500" y="70" text-anchor="middle" font-family="{SANS}" font-size="20" font-weight="700" fill="url(#gTxt)">Gracias por pasar</text>',
         f'<text x="500" y="94" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}" letter-spacing="3">MATHIAS CASTILLO · SOFTWARE ENGINEERING</text>']
    guardar("pie.svg", envolver(W, H, "".join(s), "Gracias por pasar. Mathias Castillo, Software Engineering"))


def marcador_serpiente():
    W, H = 1000, 120
    s = [f'<rect x=".5" y=".5" width="999" height="119" rx="16" fill="{S1}" stroke="{LINE}"/>',
         f'<text x="500" y="56" text-anchor="middle" font-family="{SANS}" font-size="15" fill="{MUTED}">El gráfico de contribuciones animado se genera con el primer workflow de GitHub Actions</text>',
         f'<circle cx="500" cy="84" r="4" fill="{CYAN}" filter="url(#glow)"><animate attributeName="opacity" values="1;.3;1" dur="2s" repeatCount="indefinite"/></circle>']
    guardar("snake.svg", envolver(W, H, "".join(s), "Gráfico de contribuciones animado, pendiente de generar"))


if __name__ == "__main__":
    header()
    ahora()
    titulo(1, "Sobre mí", "about", "titulo-sobre-mi.svg")
    sobre_mi()
    titulo(2, "Stack técnico", "stack", "titulo-stack.svg")
    stack()
    titulo(3, "Proyectos", "projects", "titulo-proyectos.svg")
    proyectos()
    titulo(4, "Actividad", "analytics", "titulo-actividad.svg")
    titulo(5, "Contacto", "connect", "titulo-contacto.svg")
    boton("contacto-github.svg", "GitHub", CYAN, "GH")
    boton("contacto-linkedin.svg", "LinkedIn", BLUE, "in")
    pie()
    marcador_serpiente()
    # marcadores hasta que el workflow genere los datos reales
    generar_stats.escribir_marcador(os.path.join(SALIDA, "stats.svg"))
