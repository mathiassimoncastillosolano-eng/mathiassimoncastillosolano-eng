#!/usr/bin/env python3
"""Genera todos los SVG del perfil en ../assets.

Uso:  python scripts/construir_assets.py
Requisitos: Python 3.9+ y `fontTools` (pip install fonttools) solo para convertir el nombre del hero a trazados.
Los logos están en scripts/logos (simple-icons CC0 y devicon MIT); no se descarga nada.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diseno import *  # noqa: E402,F401,F403
import generar_stats  # noqa: E402

FUENTE_HERO = os.path.join(AQUI, "fuentes", "Inter-ExtraBold.otf")

DEFS_COMUN = f"""
<linearGradient id="gTxt" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{MENTA}"/><stop offset="1" stop-color="{JADE}"/></linearGradient>
<linearGradient id="gLine" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{JADE}"/><stop offset="1" stop-color="{JADE}" stop-opacity="0"/></linearGradient>
"""


def contorno(cx, cy, r, k, n=72):
    """Curva de nivel cerrada y suave (Catmull-Rom -> Bézier)."""
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * (1 + .10 * math.sin(3 * a + k * .21) + .06 * math.sin(5 * a - k * .33 + 1.3) + .04 * math.sin(2 * a + .8))
        pts.append((cx + rr * math.cos(a) + k * 1.6, cy + rr * math.sin(a) * .86 - k * 1.1))
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(n):
        p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d + "Z"


# ------------------------------------------------------------------------ hero
def header():
    """Concepto: curvas de nivel (cartografía) que respiran; el pin marca Trujillo."""
    W, H, CX, CY = 1000, 420, 740, 215
    css = css_base(
        ".c{transform-box:view-box;transform-origin:740px 215px;animation:resp 22s ease-in-out infinite alternate}"
        + keyframes("resp", [(0, "transform:rotate(-1.5deg) scale(.995)"), (100, "transform:rotate(2.5deg) scale(1.015)")])
        + ".pulso{transform-origin:center;animation:pulso 3.4s ease-out infinite}"
        + keyframes("pulso", [(0, "transform:scale(1);opacity:.7"), (100, "transform:scale(3.4);opacity:0")])
        + ".mer{animation:mer 12s linear infinite}"
        + keyframes("mer", [(0, "transform:translateX(-200px);opacity:0"), (10, "opacity:.9"), (85, "opacity:.9"),
                            (100, "transform:translateX(560px);opacity:0")])
        + ".sub{transform-origin:left center;animation:sub 7s ease-in-out infinite}"
        + keyframes("sub", [(0, "transform:scaleX(0)"), (22, "transform:scaleX(1)"), (92, "transform:scaleX(1)"), (100, "transform:scaleX(0)")])
        + ".punto{animation:punto 2.4s ease-in-out infinite}"
        + keyframes("punto", [(0, "opacity:1"), (50, "opacity:.25"), (100, "opacity:1")]))
    defs = (DEFS_COMUN
            + f'<radialGradient id="luz" cx="{CX / W}" cy="{CY / H}" r=".55"><stop offset="0" stop-color="{JADE}" stop-opacity=".22"/><stop offset="1" stop-color="{JADE}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="vel" x1="0" y1="0" x2="1" y2="0"><stop offset=".22" stop-color="{BG}"/><stop offset=".66" stop-color="{BG}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="merG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{MENTA}" stop-opacity="0"/><stop offset=".5" stop-color="{MENTA}" stop-opacity=".5"/><stop offset="1" stop-color="{MENTA}" stop-opacity="0"/></linearGradient>'
            '<clipPath id="cl"><rect width="1000" height="420" rx="20"/></clipPath>')
    s = [f'<rect width="{W}" height="{H}" rx="20" fill="{BG}"/>', '<g clip-path="url(#cl)">',
         f'<rect width="{W}" height="{H}" fill="url(#luz)"/>']
    for k in range(1, 19):
        r = 18 + k * 21
        marca = k % 4 == 0
        op = max(.10, .62 - k * .028)
        s.append(f'<path class="c" style="animation-duration:{18 + k * 1.3:.1f}s" d="{contorno(CX, CY, r, k)}" fill="none" '
                 f'stroke="{MENTA if marca else JADE}" stroke-opacity="{op + (.12 if marca else 0):.2f}" stroke-width="{1.7 if marca else 1}"/>')
    s.append(f'<rect class="mer" x="560" y="0" width="140" height="{H}" fill="url(#merG)" opacity="0"/>')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#vel)"/>')
    # pin de ubicación
    s.append(f'<circle class="pulso" cx="{CX}" cy="{CY}" r="9" fill="none" stroke="{MENTA}" stroke-width="2"/>'
             f'<circle cx="{CX}" cy="{CY}" r="7" fill="{BG}" stroke="{MENTA}" stroke-width="2.2"/><circle cx="{CX}" cy="{CY}" r="3" fill="{MENTA}"/>'
             f'<text x="{CX + 22}" y="{CY - 12}" font-family="{MONO}" font-size="16" fill="{MENTA}" letter-spacing="1.5">TRUJILLO</text>'
             f'<text x="{CX + 22}" y="{CY + 12}" font-family="{MONO}" font-size="16" fill="{MUTED}" letter-spacing="1">8.11°S 79.03°W</text>')
    s.append('</g>')
    s.append(f'<circle class="punto" cx="62" cy="64" r="5" fill="{JADE}"/>'
             f'<text x="80" y="70" font-family="{MONO}" font-size="18" fill="{MENTA}" letter-spacing="3.5">SOFTWARE ENGINEERING</text>')
    try:
        d1, _ = texto_a_path("Mathias", 108, 52, 192, FUENTE_HERO, -2.5)
        d2, _ = texto_a_path("Castillo", 108, 52, 292, FUENTE_HERO, -2.5)
        s.append(f'<path d="{d1}" fill="{TXT}"/><path d="{d2}" fill="url(#gTxt)"/>')
    except Exception as e:  # sin fontTools: texto normal como respaldo
        print("aviso: sin fontTools, el nombre queda como texto:", e)
        s.append(f'<text x="52" y="192" font-family="{SANS}" font-size="108" font-weight="800" fill="{TXT}" letter-spacing="-3">Mathias</text>'
                 f'<text x="52" y="292" font-family="{SANS}" font-size="108" font-weight="800" fill="url(#gTxt)" letter-spacing="-3">Castillo</text>')
    s.append(f'<rect class="sub" x="56" y="314" width="150" height="4" rx="2" fill="url(#gTxt)"/>')
    s.append(f'<text x="56" y="354" font-family="{SANS}" font-size="24" fill="{MUTED}">Backend <tspan fill="{JADE}">/</tspan> AI &amp; Data <tspan fill="{JADE}">/</tspan> Software Architecture</text>')
    s.append(f'<line x1="54" y1="376" x2="946" y2="376" stroke="{LINE}"/>')
    s.append(f'<text x="56" y="402" font-family="{MONO}" font-size="16" fill="{MUTED}" letter-spacing="1.5">UPAO · INGENIERÍA DE SISTEMAS E IA · TRUJILLO, PE</text>')
    s.append(f'<rect x=".5" y=".5" width="999" height="419" rx="20" fill="none" stroke="{LINE}"/>')
    guardar("header.svg", envolver(W, H, "".join(s), "Mathias Castillo — Software Engineering. Backend, AI y Data, Software Architecture. Curvas de nivel verdes animadas con un pin sobre Trujillo.", defs, css))


# --------------------------------------------------------------------- secciones
def titulo(n, texto, etiqueta, archivo):
    W, H = 1000, 80
    css = css_base(".pt{animation:rec 9s ease-in-out infinite}" + keyframes("rec", [(0, "transform:translateX(0)"), (50, "transform:translateX(930px)"), (100, "transform:translateX(0)")]))
    s = [marco(W, H, S1, LINE, 16),
         f'<text x="30" y="49" font-family="{MONO}" font-size="18" fill="{JADE}" letter-spacing="2">{n:02d}</text>',
         f'<text x="80" y="52" font-family="{SANS}" font-size="30" font-weight="800" fill="{TXT}" letter-spacing="-.5">{texto}</text>',
         f'<text x="970" y="49" text-anchor="end" font-family="{MONO}" font-size="16" fill="{MUTED}" letter-spacing="2">// {etiqueta}</text>',
         f'<rect x="30" y="68" width="940" height="2" rx="1" fill="{LINE}"/><rect x="30" y="68" width="280" height="2" rx="1" fill="url(#gLine)"/>',
         f'<circle class="pt" cx="35" cy="69" r="4" fill="{MENTA}"/>']
    guardar(archivo, envolver(W, H, "".join(s), f"{n:02d} {texto}", DEFS_COMUN, css))


def ahora():
    W, H = 1000, 128
    css = css_base(".on{transform-origin:center;animation:on 2.4s ease-out infinite}" + keyframes("on", [(0, "transform:scale(1);opacity:.6"), (100, "transform:scale(2.6);opacity:0")]))
    s = [marco(W, H, S1, LINE, 18),
         f'<circle class="on" cx="46" cy="46" r="7" fill="none" stroke="{JADE}" stroke-width="2"/><circle cx="46" cy="46" r="6" fill="{JADE}"/>',
         f'<text x="70" y="52" font-family="{MONO}" font-size="16" fill="{JADE}" letter-spacing="3">CONSTRUYENDO</text>',
         f'<text x="40" y="94" font-family="{SANS}" font-size="21" font-weight="600" fill="{TXT}">Sistemas full stack con IA, bases de datos y backend</text>',
         f'<line x1="652" y1="26" x2="652" y2="102" stroke="{LINE}"/>',
         f'<circle cx="690" cy="46" r="6" fill="none" stroke="{ORO}" stroke-width="2" stroke-dasharray="3 3"/>',
         f'<text x="710" y="52" font-family="{MONO}" font-size="16" fill="{ORO}" letter-spacing="3">APRENDIENDO</text>',
         f'<text x="680" y="94" font-family="{SANS}" font-size="21" font-weight="600" fill="{TXT}">IaC · CI/CD · AWS</text>']
    guardar("ahora.svg", envolver(W, H, "".join(s), "Construyendo sistemas full stack con IA, bases de datos y backend. Aprendiendo IaC, CI/CD y AWS", DEFS_COMUN, css))


def sobre_mi():
    W, H = 1000, 350
    lineas = ["Estudio Ingeniería de Sistemas e IA en la UPAO, en Trujillo.",
              "Antes de escribir código intento entender el problema: defino el alcance",
              "en historias de usuario, diseño la arquitectura y recién después implemento.",
              "Trabajo con Scrum y XP en proyectos que combinan frontend, backend,",
              "bases de datos e IA."]
    css = css_base(".l{animation:ap 1s ease-out both}" + keyframes("ap", [(0, "opacity:0;transform:translateY(8px)"), (100, "opacity:1;transform:translateY(0)")]))
    s = [marco(W, H, S1, LINE, 18), f'<rect x="0" y="30" width="5" height="190" rx="2.5" fill="url(#gTxt)"/>']
    for i, t in enumerate(lineas):
        s.append(f'<text class="l" style="animation-delay:{i * .25:.2f}s" x="44" y="{66 + i * 36}" font-family="{SANS}" font-size="21" fill="{TXT}">{t}</text>')
    s.append(f'<text x="44" y="262" font-family="{SANS}" font-size="17" fill="{MUTED}">Sigo en formación: más abajo separo lo que ya usé en proyectos de lo que estoy aprendiendo.</text>')
    chips = [("ESTUDIO", "UPAO · 6.º ciclo", JADE, 44), ("LUGAR", "Trujillo, Perú", MENTA, 348), ("MÉTODO", "Scrum · XP", ORO, 652)]
    for k, v, c, x in chips:
        s.append(f'<rect x="{x}" y="286" width="290" height="44" rx="12" fill="{S2}" stroke="{c}" stroke-opacity=".55"/><circle cx="{x + 20}" cy="308" r="4.5" fill="{c}"/>'
                 f'<text x="{x + 36}" y="313" font-family="{MONO}" font-size="16" fill="{MUTED}" letter-spacing="1">{k}</text>'
                 f'<text x="{x + 274}" y="314" text-anchor="end" font-family="{SANS}" font-size="18" font-weight="600" fill="{TXT}">{v}</text>')
    guardar("sobre-mi.svg", envolver(W, H, "".join(s), "Estudio Ingeniería de Sistemas e IA en la UPAO, en Trujillo. Defino el alcance, diseño la arquitectura y luego implemento. Trabajo con Scrum y XP en proyectos de frontend, backend, bases de datos e IA.", DEFS_COMUN, css))


# ------------------------------------------------------------------------ stack
CAPAS = [
    ("Interfaz", "UI", JADE, [("react", "React"), ("vite", "Vite"), ("tailwindcss", "Tailwind"), ("html5", "HTML"), ("css", "CSS"), ("javascript", "JavaScript"), ("typescript", "TypeScript")]),
    ("Servicios", "API · LÓGICA", MENTA, [("python", "Python"), ("java", "Java"), ("csharp", "C#"), ("fastapi", "FastAPI"), ("springboot", "Spring Boot")]),
    ("Datos e IA", "DATOS · ML", SALVIA, [("scikitlearn", "scikit-learn"), ("pandas", "pandas"), ("mysql", "MySQL"), ("oracle", "Oracle"), ("postgresql", "PostgreSQL"), ("neon", "Neon"), ("supabase", "Supabase")]),
    ("Entrega y método", "FLUJO", "#C9D6CF", [("git", "Git"), ("github", "GitHub")]),
]


def stack():
    W, ALTO, GAP, Y0 = 1000, 118, 28, 28
    capas = len(CAPAS) + 1
    H = Y0 * 2 + capas * ALTO + (capas - 1) * GAP
    css = css_base(".fl{stroke-dasharray:4 8;animation:fl 1.3s linear infinite}" + keyframes("fl", [(0, "stroke-dashoffset:0"), (100, "stroke-dashoffset:-24")])
                   + ".pk{animation:pk 2.6s ease-in-out infinite}" + keyframes("pk", [(0, "transform:translateY(-14px);opacity:0"), (30, "opacity:1"), (70, "opacity:1"), (100, "transform:translateY(14px);opacity:0")])
                   + ".ap{animation:apd 3s linear infinite}" + keyframes("apd", [(0, "stroke-dashoffset:0"), (100, "stroke-dashoffset:-36")]))
    s, defs = [], DEFS_COMUN
    for i, (nombre, sub, c, logos) in enumerate(CAPAS):
        y = Y0 + i * (ALTO + GAP)
        s.append(f'<rect x="28" y="{y}" width="944" height="{ALTO}" rx="16" fill="{S1}" stroke="{LINE}"/>'
                 f'<rect x="28" y="{y}" width="5" height="{ALTO}" rx="2.5" fill="{c}"/>'
                 f'<text x="56" y="{y + 52}" font-family="{SANS}" font-size="22" font-weight="800" fill="{TXT}">{nombre}</text>'
                 f'<text x="56" y="{y + 80}" font-family="{MONO}" font-size="16" fill="{c}" letter-spacing="1.5">{sub}</text>')
        x = 250
        for clave, nom in logos:
            tam = 58 if clave == "oracle" else 44
            s.append(logo(clave, x + 51 - tam // 2, y + 42 - tam // 2, tam) + f'<text x="{x + 51}" y="{y + 90}" text-anchor="middle" font-family="{SANS}" font-size="16" fill="{MUTED}">{nom}</text>')
            x += 102
        if nombre == "Entrega y método":
            for j, p in enumerate(("Scrum", "XP")):
                px = x + 40 + j * 130
                s.append(f'<rect x="{px}" y="{y + 38}" width="112" height="42" rx="21" fill="{S2}" stroke="#C9D6CF" stroke-opacity=".5"/>'
                         f'<text x="{px + 56}" y="{y + 66}" text-anchor="middle" font-family="{SANS}" font-size="19" font-weight="600" fill="{TXT}">{p}</text>')
        if i < len(CAPAS):
            for cx in (330, 520, 710, 880):
                yy = y + ALTO
                s.append(f'<line class="fl" x1="{cx}" y1="{yy + 2}" x2="{cx}" y2="{yy + GAP - 2}" stroke="{c}" stroke-opacity=".7" stroke-width="2"/>'
                         f'<circle class="pk" style="animation-delay:{(cx % 7) * .15:.2f}s" cx="{cx}" cy="{yy + GAP / 2}" r="3.5" fill="{MENTA}"/>')
    # capa en aprendizaje (diferenciada: borde discontinuo, color oro)
    y = Y0 + len(CAPAS) * (ALTO + GAP)
    s.append(f'<rect class="ap" x="28" y="{y}" width="944" height="{ALTO}" rx="16" fill="{BG}" stroke="{ORO}" stroke-width="1.6" stroke-dasharray="9 7"/>'
             f'<text x="56" y="{y + 52}" font-family="{SANS}" font-size="22" font-weight="800" fill="{TXT}">En aprendizaje</text>'
             f'<text x="56" y="{y + 80}" font-family="{MONO}" font-size="16" fill="{ORO}" letter-spacing="1.5">NIVEL DE CURSO</text>')
    s.append(logo("amazonwebservices", 250 + 29, y + 20, 44) + f'<text x="{250 + 51}" y="{y + 90}" text-anchor="middle" font-family="{SANS}" font-size="16" fill="{MUTED}">AWS</text>')
    for j, p in enumerate(("IaC", "CI/CD")):
        px = 420 + j * 150
        s.append(f'<rect x="{px}" y="{y + 38}" width="130" height="42" rx="21" fill="none" stroke="{ORO}" stroke-opacity=".8" stroke-dasharray="4 4"/>'
                 f'<text x="{px + 65}" y="{y + 66}" text-anchor="middle" font-family="{SANS}" font-size="19" font-weight="600" fill="{ORO}">{p}</text>')
    s.append(f'<text x="960" y="{y + 90}" text-anchor="end" font-family="{SANS}" font-size="16" fill="{MUTED}">Aprendiendo a nivel de curso</text>')
    guardar("stack.svg", envolver(W, H, "".join(s), "Stack técnico en capas. Interfaz: React, Vite, Tailwind, HTML, CSS, JavaScript y TypeScript. Servicios: Python, Java, C#, FastAPI y Spring Boot. Datos e IA: scikit-learn, pandas, MySQL, Oracle, PostgreSQL, Neon y Supabase. Entrega y método: Git, GitHub, Scrum y XP. En aprendizaje, a nivel de curso: AWS, IaC y CI/CD.", defs, css))


# ------------------------------------------------------------ botones y pie
def boton_enlace(archivo, texto, acento, acento2, tipo, etiqueta):
    """tipo 'repo' (contorno + logo de GitHub) o 'demo' (relleno + flecha)."""
    W, H = 280, 60
    css = css_base(".b{animation:b 3.5s linear infinite}" + keyframes("b", [(0, "stroke-dashoffset:0"), (100, "stroke-dashoffset:-340")]))
    g = f'<linearGradient id="gb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{acento}"/><stop offset="1" stop-color="{acento2}"/></linearGradient>'
    if tipo == "repo":
        s = [f'<rect x="1" y="1" width="278" height="58" rx="29" fill="{S1}" stroke="{acento}" stroke-opacity=".75" stroke-width="1.6"/>',
             f'<rect class="b" x="1" y="1" width="278" height="58" rx="29" fill="none" stroke="{acento2}" stroke-width="2.4" stroke-dasharray="46 294"/>',
             logo("github", 26, 15, 30, TXT),
             f'<text x="70" y="38" font-family="{SANS}" font-size="21" font-weight="700" fill="{TXT}">{texto}</text>']
    else:
        s = [f'<rect x="1" y="1" width="278" height="58" rx="29" fill="url(#gb)"/>',
             f'<path d="M30 40L44 26M33 26H44V37" fill="none" stroke="{BG}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>',
             f'<text x="64" y="38" font-family="{SANS}" font-size="21" font-weight="800" fill="{BG}">{texto}</text>']
    guardar(archivo, envolver(W, H, "".join(s), etiqueta, g, css))


def boton_contacto(archivo, texto, glifo_logo, etiqueta):
    W, H = 300, 64
    css = css_base(".b{animation:b 4s linear infinite}" + keyframes("b", [(0, "stroke-dashoffset:0"), (100, "stroke-dashoffset:-380")]))
    s = [f'<rect x="1" y="1" width="298" height="62" rx="31" fill="{S1}" stroke="{JADE}" stroke-opacity=".6" stroke-width="1.6"/>',
         f'<rect class="b" x="1" y="1" width="298" height="62" rx="31" fill="none" stroke="{MENTA}" stroke-width="2.4" stroke-dasharray="46 334"/>']
    if glifo_logo:
        s.append(logo(glifo_logo, 28, 16, 32, TXT))
    pos = 'x="74"' if glifo_logo else 'x="150" text-anchor="middle"'
    s.append(f'<text {pos} y="41" font-family="{SANS}" font-size="22" font-weight="700" fill="{TXT}">{texto}</text>')
    guardar(archivo, envolver(W, H, "".join(s), etiqueta, "", css))


def pie():
    W, H = 1000, 120
    css = css_base(".pt{animation:rec 10s ease-in-out infinite}" + keyframes("rec", [(0, "transform:translateX(0)"), (50, "transform:translateX(920px)"), (100, "transform:translateX(0)")]))
    s = [marco(W, H, S1, LINE, 18), f'<line x1="40" y1="32" x2="960" y2="32" stroke="{LINE}"/><circle class="pt" cx="40" cy="32" r="4" fill="{MENTA}"/>',
         f'<text x="500" y="76" text-anchor="middle" font-family="{SANS}" font-size="22" font-weight="700" fill="url(#gTxt)">Gracias por pasar</text>',
         f'<text x="500" y="102" text-anchor="middle" font-family="{MONO}" font-size="16" fill="{MUTED}" letter-spacing="2">MATHIAS CASTILLO · SOFTWARE ENGINEERING</text>']
    guardar("pie.svg", envolver(W, H, "".join(s), "Gracias por pasar. Mathias Castillo, Software Engineering", DEFS_COMUN, css))


def principal():
    header()
    ahora()
    titulo(1, "Sobre mí", "about", "titulo-sobre-mi.svg")
    sobre_mi()
    titulo(2, "Stack técnico", "stack", "titulo-stack.svg")
    stack()
    titulo(3, "Proyectos", "projects", "titulo-proyectos.svg")
    import proyectos  # tarjetas animadas y botones
    proyectos.generar(boton_enlace)
    titulo(4, "Actividad", "analytics", "titulo-actividad.svg")
    titulo(5, "Contacto", "connect", "titulo-contacto.svg")
    boton_contacto("contacto-github.svg", "GitHub", "github", "Ir al perfil de GitHub")
    boton_contacto("contacto-linkedin.svg", "LinkedIn", None, "Ir al perfil de LinkedIn")
    pie()
    # marcadores sin cifras hasta que el workflow genere datos reales (no se pisan los datos reales)
    for nombre, fn in (("stats.svg", generar_stats.svg_panel), ("heatmap.svg", generar_stats.svg_heatmap)):
        ruta = os.path.join(SALIDA, nombre)
        if not (os.path.exists(ruta) and "Actualizado" in open(ruta, encoding="utf-8").read()):
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(fn(None))
            print("ok", nombre, "(marcador)")


if __name__ == "__main__":
    principal()
