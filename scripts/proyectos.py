"""Tarjetas animadas de los dos proyectos y sus botones de enlace.

Todas las animaciones son CSS dentro del SVG. El estado base (sin animación) es el fotograma final completo,
así quien tiene `prefers-reduced-motion` ve una versión estática equivalente.
"""
from diseno import *  # noqa: F401,F403
import math

W, H = 1000, 530
ST_X, ST_Y, ST_W, ST_H = 40, 184, 920, 240
EASE = "cubic-bezier(.2,.8,.2,1)"

REPO_ESTUDIO = "https://github.com/mathiassimoncastillosolano-eng/Plataforma-Estudio---AI"
DEMO_ESTUDIO = "https://plataforma-estudio-ai.vercel.app/"
REPO_RUTA = "https://github.com/mathiassimoncastillosolano-eng/Portal---Transportes"
DEMO_RUTA = "https://portal-transportes.vercel.app/"


def tarjeta_base(acento, acento2, categoria, titulo, d1, d2, logos):
    """Marco común: texto, escenario vacío, fila de logos y pista de interacción."""
    s = [marco(W, H, S1, LINE, 20),
         f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="20" fill="url(#glow)"/>',
         f'<text x="40" y="54" font-family="{MONO}" font-size="16" fill="{acento}" letter-spacing="3">{categoria}</text>',
         f'<text x="40" y="100" font-family="{SANS}" font-size="38" font-weight="800" fill="{TXT}" letter-spacing="-.8">{titulo}</text>',
         f'<text x="40" y="138" font-family="{SANS}" font-size="20" fill="#C3D2C9">{d1}</text>',
         f'<text x="40" y="166" font-family="{SANS}" font-size="20" fill="#C3D2C9">{d2}</text>',
         f'<rect x="{ST_X}" y="{ST_Y}" width="{ST_W}" height="{ST_H}" rx="14" fill="{BG}" stroke="{LINE}"/>']
    return s


def fila_logos(claves):
    """Logos oficiales de las tecnologías del proyecto, en pequeño."""
    s, x = [], 40
    for clave in claves:
        s.append(f'<rect x="{x}" y="462" width="44" height="44" rx="11" fill="{S2}" stroke="{LINE}"/>' + logo(clave, x + 8, 470, 28))
        x += 54
    return s


def pie_tarjeta(acento, logos=None):
    s = [f'<line x1="40" y1="446" x2="960" y2="446" stroke="{LINE}"/>']
    s.append(f'<g class="hint"><text x="934" y="491" text-anchor="end" font-family="{SANS}" font-size="20" font-weight="600" fill="{acento}">Toca para ver repositorio y demo</text>'
             f'<path d="M946 480L954 488L946 496" fill="none" stroke="{acento}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>')
    return s


CSS_HINT = (".hint{animation:hint 2.4s ease-in-out infinite}"
            + keyframes("hint", [(0, "transform:translateX(0)"), (50, "transform:translateX(-5px)"), (100, "transform:translateX(0)")]))


def aparece(nombre, ini, fin, desde="opacity:0;transform:scale(.4)", hasta="opacity:1;transform:scale(1)"):
    return keyframes(nombre, [(0, desde), (ini, desde, EASE), (fin, hasta), (100, hasta)])


# ===================================================================== Plataforma Estudio AI
def estudio():
    acento, acento2 = JADE, SALVIA
    DOC_X, DOC_Y, DOC_W, DOC_H = 62, 236, 190, 176
    barras = [(120, 0), (150, 0), (110, 0), (150, 0), (140, 0), (90, 0), (150, 0), (120, 0)]
    paso = 19
    by = lambda i: DOC_Y + 34 + i * paso
    resalta = {1: 17, 4: 23, 6: 29}                 # índice de línea -> % del bucle en que el haz la alcanza
    CARD_X, CARD_Y, CARD_W = 300, 236, 262
    lineas_card = [(218, 0), (196, 0), (222, 0), (160, 0), (190, 0)]
    cy = lambda j: CARD_Y + 56 + j * 24
    css = [CSS_HINT]
    css.append(".todo{animation:todo 12s linear infinite}" + keyframes("todo", [(0, "opacity:0"), (4, "opacity:1"), (93, "opacity:1"), (98, "opacity:0"), (100, "opacity:0")]))
    css.append(".doc{animation:doc 12s linear infinite}" + keyframes("doc", [(0, "transform:translateX(-36px);opacity:0"), (8, "transform:translateX(0);opacity:1", EASE), (60, "opacity:1"), (66, "opacity:.38"), (100, "opacity:.38")]))
    css.append(".haz{animation:haz 12s linear infinite}" + keyframes("haz", [(0, "transform:translateY(0);opacity:0"), (10, "transform:translateY(0);opacity:0"), (12, "opacity:1"), (31, "transform:translateY(138px);opacity:1", "ease-in-out"), (34, "transform:translateY(138px);opacity:0"), (100, "opacity:0")]))
    for k, (i, p) in enumerate(resalta.items()):
        dx, dy = CARD_X + 20 - (DOC_X + 14), cy(k) - by(i)
        css.append(f".g{k}{{animation:g{k} 12s linear infinite}}" + keyframes(f"g{k}", [
            (0, "opacity:0;transform:translate(0,0)"), (p, "opacity:0;transform:translate(0,0)"), (p + 2, "opacity:1;transform:translate(0,0)"),
            (38, "opacity:1;transform:translate(0,0)", "cubic-bezier(.5,0,.3,1)"), (50, f"opacity:1;transform:translate({dx}px,{dy}px)"),
            (53, f"opacity:0;transform:translate({dx}px,{dy}px)"), (100, "opacity:0")]))
        css.append(f".ds{k}{{animation:ds{k} 12s linear infinite}}" + keyframes(f"ds{k}", [(0, "opacity:0"), (p, "opacity:0"), (p + 2, "opacity:1"), (100, "opacity:1")]))
    css.append(".card{animation:card 12s linear infinite}" + aparece("card", 36, 42, "opacity:0;transform:translateY(10px)", "opacity:1;transform:translateY(0)"))
    for j in range(len(lineas_card)):
        a = 47 + j * 2.4
        css.append(f".t{j}{{transform-origin:left center;animation:t{j} 12s linear infinite}}" + keyframes(f"t{j}", [(0, "transform:scaleX(0)"), (a, "transform:scaleX(0)", "ease-out"), (a + 3, "transform:scaleX(1)"), (100, "transform:scaleX(1)")]))
    css.append(".cardo{animation:cardo 12s linear infinite}" + keyframes("cardo", [(0, "opacity:1"), (64, "opacity:1"), (70, "opacity:.5"), (100, "opacity:.5")]))
    # pestañas
    for n, (a, b) in enumerate([(6, 36), (36, 64), (64, 93)]):
        css.append(f".q{n}{{animation:q{n} 12s linear infinite}}" + keyframes(f"q{n}", [(0, f"fill:{MUTED}"), (a - 1, f"fill:{MUTED}"), (a + 1, f"fill:{TXT}"), (b - 1, f"fill:{TXT}"), (b + 1, f"fill:{MUTED}"), (100, f"fill:{MUTED}")]))
        css.append(f".p{n}{{animation:p{n} 12s linear infinite}}" + keyframes(f"p{n}", [(0, "opacity:0"), (a - 1, "opacity:0"), (a + 1, "opacity:1"), (b - 1, "opacity:1"), (b + 1, "opacity:0"), (100, "opacity:0")]))
    # mapa
    MX, MY = 778, 330
    sat = [(668, 276), (672, 376), (782, 262), (884, 280), (902, 372), (788, 392)]
    css.append(".nc{transform-origin:center;animation:nc 12s linear infinite}" + aparece("nc", 66, 70))
    for k in range(len(sat)):
        a = 70 + k * 2.6
        css.append(f".e{k}{{animation:e{k} 12s linear infinite}}" + keyframes(f"e{k}", [(0, "stroke-dashoffset:1"), (a, "stroke-dashoffset:1", "ease-out"), (a + 3, "stroke-dashoffset:0"), (100, "stroke-dashoffset:0")]))
        css.append(f".n{k}{{transform-origin:center;animation:n{k} 12s linear infinite}}" + aparece(f"n{k}", a + 1.5, a + 4.5))
    defs = (f'<radialGradient id="glow" cx=".85" cy="0" r=".9"><stop offset="0" stop-color="{acento}" stop-opacity=".16"/><stop offset="1" stop-color="{acento}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="hz" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{MENTA}" stop-opacity="0"/><stop offset=".55" stop-color="{MENTA}" stop-opacity=".55"/><stop offset="1" stop-color="{MENTA}" stop-opacity="0"/></linearGradient>'
            f'<clipPath id="stg"><rect x="{ST_X}" y="{ST_Y}" width="{ST_W}" height="{ST_H}" rx="14"/></clipPath>')
    s = tarjeta_base(acento, acento2, "IA APLICADA AL ESTUDIO", "Plataforma Estudio AI",
                     "Sube texto o PDF y obtén un resumen general, un resumen esencial y un mapa",
                     "conceptual con IA (OpenAI). Acceso con Google y sin base de datos.", None)
    s.append('<g clip-path="url(#stg)"><g class="todo">')
    # pestañas (nombres reales de las funciones)
    ATTR = ['opacity="0"', 'opacity="0"', '']
    tabs = [("Resumen general", 62, 196), ("Resumen esencial", 270, 202), ("Mapa conceptual", 486, 196)]
    s.append(f'<line x1="{ST_X}" y1="{ST_Y + 44}" x2="{ST_X + ST_W}" y2="{ST_Y + 44}" stroke="{LINE}"/>')
    for n, (t, x, w) in enumerate(tabs):
        s.append(f'<rect class="p{n}" x="{x - 10}" y="{ST_Y + 8}" width="{w + 20}" height="30" rx="15" fill="{acento}" fill-opacity=".18" stroke="{acento}" stroke-opacity=".7" {ATTR[n]}/>'
                 f'<text class="q{n}" x="{x + w / 2}" y="{ST_Y + 29}" text-anchor="middle" font-family="{SANS}" font-size="18" font-weight="600" fill="{TXT if n == 2 else MUTED}">{t}</text>')
    # documento
    s.append(f'<g class="doc"><rect x="{DOC_X}" y="{DOC_Y}" width="{DOC_W}" height="{DOC_H}" rx="10" fill="{S2}" stroke="{LINE}"/>'
             f'<rect x="{DOC_X + 14}" y="{DOC_Y + 12}" width="70" height="8" rx="4" fill="{MUTED}" fill-opacity=".7"/>')
    for i, (w, _) in enumerate(barras):
        s.append(f'<rect x="{DOC_X + 14}" y="{by(i)}" width="{w}" height="8" rx="4" fill="{MUTED}" fill-opacity=".35"/>')
    for k, i in enumerate(resalta):
        s.append(f'<rect class="ds{k}" x="{DOC_X + 10}" y="{by(i) - 3}" width="{barras[i][0] + 8}" height="14" rx="5" fill="{acento}" fill-opacity=".28"/>')
    s.append(f'<rect class="haz" x="{DOC_X}" y="{DOC_Y + 6}" width="{DOC_W}" height="30" fill="url(#hz)" opacity="0"/></g>')
    # tarjeta de resumen esencial
    s.append(f'<g class="cardo"><g class="card"><rect x="{CARD_X}" y="{CARD_Y}" width="{CARD_W}" height="{DOC_H}" rx="12" fill="{S2}" stroke="{acento}" stroke-opacity=".6"/>'
             f'<path d="M{CARD_X + 26} {CARD_Y + 18}l4 9 9 4-9 4-4 9-4-9-9-4 9-4z" fill="{MENTA}"/>'
             f'<rect x="{CARD_X + 50}" y="{CARD_Y + 22}" width="110" height="10" rx="5" fill="{TXT}" fill-opacity=".85"/>')
    for j, (w, _) in enumerate(lineas_card):
        s.append(f'<rect class="t{j}" x="{CARD_X + 20}" y="{cy(j)}" width="{w}" height="9" rx="4.5" fill="{TXT}" fill-opacity="{.8 if j < 3 else .45}"/>')
    s.append('</g></g>')
    # ideas que viajan
    for k, i in enumerate(resalta):
        s.append(f'<rect class="g{k}" x="{DOC_X + 14}" y="{by(i)}" width="{barras[i][0]}" height="8" rx="4" fill="{MENTA}"/>')
    # mapa conceptual
    for k, (x, y) in enumerate(sat):
        s.append(f'<path class="e{k}" pathLength="1" style="stroke-dasharray:1;stroke-dashoffset:0" d="M{MX} {MY}Q{(MX + x) / 2 + (6 if k % 2 else -6)} {(MY + y) / 2} {x} {y}" fill="none" stroke="{acento}" stroke-opacity=".75" stroke-width="2"/>')
    cols = [acento, MENTA, acento2]
    for k, (x, y) in enumerate(sat):
        c = cols[k % 3]
        s.append(f'<g class="n{k}"><rect x="{x - 40}" y="{y - 15}" width="80" height="30" rx="15" fill="{S2}" stroke="{c}" stroke-width="1.8"/><rect x="{x - 24}" y="{y - 4}" width="{34 + (k * 7) % 14}" height="8" rx="4" fill="{c}" fill-opacity=".8"/></g>')
    s.append(f'<g class="nc"><circle cx="{MX}" cy="{MY}" r="30" fill="{S2}" stroke="{MENTA}" stroke-width="2.4"/><circle cx="{MX}" cy="{MY}" r="10" fill="{MENTA}"/></g>')
    s.append('</g></g>')
    s += pie_tarjeta(acento, None)
    s += fila_logos(["react", "vite", "typescript", "fastapi", "python"])
    guardar("proyecto-estudio.svg", envolver(W, H, "".join(s),
            "Plataforma Estudio AI. Animación: una hoja o PDF es escaneada por un haz de luz, la IA resalta las ideas clave, se condensan en una tarjeta de resumen esencial y aparece un mapa conceptual con sus nodos conectados. Pestañas: Resumen general, Resumen esencial y Mapa conceptual. Tecnologías: React, Vite, TypeScript, FastAPI y Python. Toca para ver repositorio y demo.",
            defs, css_base("".join(css))))


# ===================================================================== RutaLibre
D_CAP, T_FRAC = 1280, [(0, 0.0), (10, .0794), (60, .8737), (76, 1.0)]


def mov(nombre, escala, signo=-1, prop="translateX", unidad="px", inicio=0.0):
    """Keyframes de avance sincronizado: arranque suave, velocidad constante y frenada con easing."""
    t = {
        0: ("cubic-bezier(.4,0,.5,0)",), 10: (None,), 60: ("cubic-bezier(.2,.4,.4,1)",), 76: (None,)}
    paradas = []
    for pct, fr in T_FRAC:
        val = inicio + signo * escala * fr
        paradas.append((pct, f"transform:{prop}({val:.2f}{unidad})", t[pct][0]))
    paradas.append((100, f"transform:{prop}({inicio + signo * escala:.2f}{unidad})"))
    return keyframes(nombre, paradas)


def periodico(ancho_periodo, repeticiones, base, perfil, bajo=0):
    """Polígono periódico (montañas/colinas). perfil: [(x dentro del periodo, altura)], el primero=último altura."""
    pts = []
    for k in range(repeticiones):
        for px, h in perfil:
            pts.append((k * ancho_periodo + px, base - h))
    pts.append((repeticiones * ancho_periodo, base - perfil[0][1]))
    d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts)
    return d + f" L{repeticiones * ancho_periodo} {base + bajo} L0 {base + bajo}Z"


def ruta():
    acento, acento2 = ORO, CORAL
    SX, SY, SW, SH = ST_X, ST_Y, ST_W, 188               # escena
    ROAD_Y = SY + 150                                      # 334: borde superior de la calzada
    WHEEL_Y, BUS_X = ROAD_Y + 6, SX + 210                  # centro de ruedas y x del parachoques trasero
    BUSW = 320
    css = [CSS_HINT]
    css.append(".todo{animation:todo 18s linear infinite}" + keyframes("todo", [(0, "opacity:0"), (3, "opacity:1"), (95, "opacity:1"), (99, "opacity:0"), (100, "opacity:0")]))
    css.append(".mont{animation:mont 18s linear infinite}" + mov("mont", 500))
    css.append(".coli{animation:coli 18s linear infinite}" + mov("coli", 800))
    css.append(".arb{animation:arb 18s linear infinite}" + mov("arb", 1280))
    css.append(".via{animation:via 18s linear infinite}" + mov("via", 1280))
    # el pin llega desde la derecha: arranca 1280 px a la derecha y termina en su sitio
    pines = []
    for pct, fr in T_FRAC:
        pines.append((pct, f"transform:translateX({1280 * (1 - fr):.2f}px)", {0: "cubic-bezier(.4,0,.5,0)", 60: "cubic-bezier(.2,.4,.4,1)"}.get(pct)))
    pines.append((100, "transform:translateX(0px)"))
    css.append(".pin{animation:pin 18s linear infinite}" + keyframes("pin", pines))
    # ruedas
    rueda = [(pct, f"transform:rotate({3600 * fr:.1f}deg)", {0: "cubic-bezier(.4,0,.5,0)", 60: "cubic-bezier(.2,.4,.4,1)"}.get(pct)) for pct, fr in T_FRAC] + [(100, "transform:rotate(3600deg)")]
    css.append(".rue{transform-origin:center;animation:rue 18s linear infinite}" + keyframes("rue", rueda))
    # progreso de ruta (viñeta del recorrido)
    prog = [(pct, f"stroke-dashoffset:{1 - fr:.4f}", {0: "cubic-bezier(.4,0,.5,0)", 60: "cubic-bezier(.2,.4,.4,1)"}.get(pct)) for pct, fr in T_FRAC] + [(100, "stroke-dashoffset:0")]
    css.append(".prog{animation:prog 18s linear infinite}" + keyframes("prog", prog))
    css.append(".marc{animation:marc 18s linear infinite}" + mov("marc", 820, signo=1, inicio=-820).replace("translateX(-820.00px)", "translateX(-820px)"))
    # cielo, sol y luces
    css.append(".alba{animation:alba 18s linear infinite}" + keyframes("alba", [(0, "opacity:1"), (14, "opacity:1"), (30, "opacity:0"), (100, "opacity:0")]))
    css.append(".dia{animation:dia 18s linear infinite}" + keyframes("dia", [(0, "opacity:0"), (16, "opacity:0"), (32, "opacity:1"), (48, "opacity:1"), (68, "opacity:0"), (100, "opacity:0")]))
    sol = [(0, "transform:translate(-760px,6px)"), (19, "transform:translate(-570px,-58px)"), (38, "transform:translate(-380px,-84px)"), (57, "transform:translate(-190px,-58px)"), (76, "transform:translate(0px,0px)"), (100, "transform:translate(0px,0px)")]
    css.append(".sol{animation:sol 18s linear infinite}" + keyframes("sol", sol))
    css.append(".faro{animation:faro 18s linear infinite}" + keyframes("faro", [(0, "opacity:0"), (52, "opacity:0"), (64, "opacity:1"), (100, "opacity:1")]))
    css.append(".freno{animation:freno 18s linear infinite}" + keyframes("freno", [(0, "opacity:0"), (59, "opacity:0"), (60.5, "opacity:1"), (100, "opacity:1")]))
    css.append(".polvo{animation:polvo 18s linear infinite}" + keyframes("polvo", [(0, "opacity:0"), (6, "opacity:1"), (58, "opacity:1"), (70, "opacity:0"), (100, "opacity:0")]))
    css.append(".p1,.p2,.p3{transform-origin:center;animation:pf 1s ease-out infinite}.p2{animation-delay:-.33s}.p3{animation-delay:-.66s}"
               + keyframes("pf", [(0, "transform:translate(0,0) scale(.5);opacity:.55"), (100, "transform:translate(-46px,-8px) scale(2.1);opacity:0")]))
    css.append(".reb{animation:reb .42s ease-in-out infinite alternate}" + keyframes("reb", [(0, "transform:translateY(0)"), (100, "transform:translateY(-1.6px)")]))
    css.append(".cab{transform-origin:center;animation:cab 18s linear infinite}" + keyframes("cab", [(0, "transform:rotate(0)"), (58, "transform:rotate(0)"), (63, "transform:rotate(1.1deg)", "ease-in-out"), (74, "transform:rotate(0deg)"), (100, "transform:rotate(0)")]))
    # llegada: ondas, boleto
    for n, d in enumerate((0, 3)):
        css.append(f".on{n}{{transform-origin:center;animation:on{n} 18s linear infinite}}" + keyframes(f"on{n}", [(0, "opacity:0;transform:scale(.3)"), (76 + d, "opacity:0;transform:scale(.3)"), (77 + d, "opacity:.9;transform:scale(.3)", "ease-out"), (88 + d, "opacity:0;transform:scale(3.2)"), (100, "opacity:0;transform:scale(3.2)")]))
    css.append(".bol{animation:bol 18s linear infinite}" + keyframes("bol", [(0, "opacity:0;transform:translate(50px,40px)"), (79, "opacity:0;transform:translate(50px,40px)", EASE), (87, "opacity:1;transform:translate(0,0)"), (100, "opacity:1;transform:translate(0,0)")]))
    css.append(".pcaida{animation:pcaida 18s linear infinite}" + keyframes("pcaida", [(0, "opacity:1;transform:translateY(0)"), (100, "opacity:1;transform:translateY(0)")]))

    defs = (f'<radialGradient id="glow" cx=".85" cy="0" r=".9"><stop offset="0" stop-color="{acento}" stop-opacity=".13"/><stop offset="1" stop-color="{acento}" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="cDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#231F42"/><stop offset=".6" stop-color="#8A4A5F"/><stop offset="1" stop-color="#F2985E"/></linearGradient>'
            '<linearGradient id="cAlba" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1B2A4A"/><stop offset=".6" stop-color="#6E5C80"/><stop offset="1" stop-color="#F0B27E"/></linearGradient>'
            '<linearGradient id="cDia" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#256E86"/><stop offset="1" stop-color="#BFE5D3"/></linearGradient>'
            f'<linearGradient id="haz" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFE9B0" stop-opacity=".75"/><stop offset="1" stop-color="#FFE9B0" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="cuerpo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F6F1E4"/><stop offset="1" stop-color="#D9D2BF"/></linearGradient>'
            f'<clipPath id="esc"><rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="14"/></clipPath>'
            f'<clipPath id="stg"><rect x="{ST_X}" y="{ST_Y}" width="{ST_W}" height="{ST_H}" rx="14"/></clipPath>')
    s = tarjeta_base(acento, acento2, "PORTAL WEB · TRANSPORTE TERRESTRE", "RutaLibre",
                     "Búsqueda de viajes, mapa de asientos, pago con Mercado Pago y boletos",
                     "electrónicos. Frontend React con API Spring Boot y PostgreSQL en Supabase.", None)
    s.append('<g clip-path="url(#stg)"><g class="todo"><g clip-path="url(#esc)">')
    s.append(f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" fill="url(#cDusk)"/>')
    s.append(f'<rect class="alba" x="{SX}" y="{SY}" width="{SW}" height="{SH}" fill="url(#cAlba)" opacity="0"/>')
    s.append(f'<rect class="dia" x="{SX}" y="{SY}" width="{SW}" height="{SH}" fill="url(#cDia)" opacity="0"/>')
    s.append(f'<g class="sol"><circle cx="{SX + 800}" cy="{ROAD_Y - 30}" r="20" fill="#FFD79A"/><circle cx="{SX + 800}" cy="{ROAD_Y - 30}" r="34" fill="#FFD79A" fill-opacity=".18"/></g>')
    s.append(f'<g class="mont"><path d="{periodico(500, 4, ROAD_Y - 10, [(0, 62), (120, 118), (210, 78), (330, 130), (420, 70)], 40)}" transform="translate({SX} 0)" fill="#1B3B34" fill-opacity=".92"/></g>')
    s.append(f'<g class="coli"><path d="{periodico(400, 5, ROAD_Y + 2, [(0, 30), (90, 56), (200, 34), (300, 52)], 40)}" transform="translate({SX} 0)" fill="#17332A"/></g>')
    # árboles y postes (capa cercana)
    d_arb, d_pos = [], []
    for k in range(5):
        for off, h in ((60, 52), (110, 38), (250, 60), (420, 44), (560, 56)):
            x = SX + k * 640 + off
            for lvl, (hh, ww) in enumerate(((h, h * .62), (h * .68, h * .5))):
                yb = ROAD_Y + 2 - lvl * h * .28
                d_arb.append(f"M{x - ww / 2:.0f} {yb:.0f}L{x:.0f} {yb - hh:.0f}L{x + ww / 2:.0f} {yb:.0f}Z")
    pos = [SX + k * 320 + 150 for k in range(8)]
    for i, x in enumerate(pos):
        d_pos.append(f"M{x} {ROAD_Y + 2}V{ROAD_Y - 74}M{x - 14} {ROAD_Y - 66}H{x + 14}")
        if i + 1 < len(pos):
            d_pos.append(f"M{x} {ROAD_Y - 66}Q{x + 160} {ROAD_Y - 44} {pos[i + 1]} {ROAD_Y - 66}")
    s.append(f'<g class="arb"><path d="{"".join(d_arb)}" fill="#10261E"/><path d="{"".join(d_pos)}" fill="none" stroke="#0B1713" stroke-width="2.4"/></g>')
    # calzada
    s.append(f'<rect x="{SX}" y="{ROAD_Y}" width="{SW}" height="{SH - 150}" fill="#18251F"/><rect x="{SX}" y="{ROAD_Y}" width="{SW}" height="3" fill="#2B3F36"/>')
    marcas = "".join(f"M{SX + k * 80 + 6} {ROAD_Y + 26}h38" for k in range(30))
    s.append(f'<g class="via"><path d="{marcas}" stroke="#C9D6CF" stroke-opacity=".75" stroke-width="4" stroke-linecap="round" fill="none"/></g>')
    # destino: pin que llega con el paisaje
    PX = SX + 640
    s.append(f'<g class="pin"><ellipse cx="{PX}" cy="{ROAD_Y + 4}" rx="16" ry="4" fill="#000" fill-opacity=".35"/>'
             f'<ellipse class="on0" cx="{PX}" cy="{ROAD_Y + 2}" rx="14" ry="5" fill="none" stroke="{acento2}" stroke-width="2.4" opacity="0"/>'
             f'<ellipse class="on1" cx="{PX}" cy="{ROAD_Y + 2}" rx="14" ry="5" fill="none" stroke="{acento}" stroke-width="2" opacity="0"/>'
             f'<path d="M{PX} {ROAD_Y + 2}C{PX - 8} {ROAD_Y - 18} {PX - 20} {ROAD_Y - 28} {PX - 20} {ROAD_Y - 44}A20 20 0 1 1 {PX + 20} {ROAD_Y - 44}C{PX + 20} {ROAD_Y - 28} {PX + 8} {ROAD_Y - 18} {PX} {ROAD_Y + 2}Z" fill="{acento2}"/>'
             f'<circle cx="{PX}" cy="{ROAD_Y - 44}" r="8" fill="#FFF3EA"/></g>')
    # bus
    bx, by_ = BUS_X, ROAD_Y - 84
    ruedas = (bx + 70, bx + 250)
    bus = [f'<ellipse cx="{bx + BUSW / 2}" cy="{ROAD_Y + 28}" rx="170" ry="7" fill="#000" fill-opacity=".4"/>',
           f'<g class="polvo" opacity="0"><circle class="p1" cx="{bx - 4}" cy="{ROAD_Y + 24}" r="8" fill="#C9D6CF"/><circle class="p2" cx="{bx - 4}" cy="{ROAD_Y + 24}" r="6" fill="#C9D6CF"/><circle class="p3" cx="{bx - 4}" cy="{ROAD_Y + 24}" r="7" fill="#C9D6CF"/></g>',
           f'<g class="cab"><g class="reb">',
           f'<rect x="{bx}" y="{by_}" width="{BUSW}" height="{ROAD_Y - by_ + 14}" rx="18" fill="url(#cuerpo)"/>',
           f'<rect x="{bx + 6}" y="{by_ - 8}" width="100" height="10" rx="5" fill="#CFC8B3"/>',
           f'<rect x="{bx}" y="{by_ + 66}" width="{BUSW}" height="6" fill="{acento}"/><rect x="{bx}" y="{by_ + 72}" width="{BUSW}" height="3" fill="{acento2}"/>',
           f'<rect x="{bx}" y="{ROAD_Y - 8}" width="{BUSW}" height="22" rx="8" fill="#2A3B34"/>']
    for k in range(5):
        bus.append(f'<rect x="{bx + 18 + k * 40}" y="{by_ + 10}" width="32" height="28" rx="7" fill="#1B3A45"/><rect x="{bx + 22 + k * 40}" y="{by_ + 14}" width="10" height="8" rx="3" fill="#7FB6C4" fill-opacity=".45"/>')
    bus.append(f'<rect x="{bx + 222}" y="{by_ + 12}" width="34" height="{ROAD_Y - by_ - 14}" rx="6" fill="#B9B29C"/><rect x="{bx + 227}" y="{by_ + 16}" width="24" height="30" rx="5" fill="#1B3A45"/>')
    bus.append(f'<path d="M{bx + 266} {by_ + 10}H{bx + 296}Q{bx + 314} {by_ + 12} {bx + 316} {by_ + 34}L{bx + 316} {by_ + 46}H{bx + 266}Z" fill="#1B3A45"/>')
    bus.append(f'<text x="{bx + 20}" y="{by_ + 60}" font-family="{SANS}" font-size="17" font-weight="800" fill="#2A3B34" letter-spacing=".5">RutaLibre</text>')
    bus.append(f'<rect x="{bx - 3}" y="{by_ + 58}" width="9" height="16" rx="4" fill="{acento2}"/>'
               f'<ellipse class="freno" cx="{bx - 4}" cy="{by_ + 66}" rx="14" ry="13" fill="{acento2}" fill-opacity=".5" opacity="0"/>')
    bus.append(f'<rect x="{bx + BUSW - 8}" y="{by_ + 60}" width="10" height="14" rx="5" fill="#FFE9B0"/>')
    bus.append('</g>')                                           # cierre .reb
    for rx_ in ruedas:                                           # ruedas fuera del rebote: apoyan en la calzada
        bus.append(f'<circle cx="{rx_}" cy="{WHEEL_Y + 8}" r="27" fill="#0B1411"/>')
        bus.append(f'<g class="rue"><circle cx="{rx_}" cy="{WHEEL_Y + 8}" r="21" fill="#101A16" stroke="#26372F" stroke-width="2"/>'
                   f'<circle cx="{rx_}" cy="{WHEEL_Y + 8}" r="12" fill="#C9D6CF"/>'
                   + "".join(f'<line x1="{rx_}" y1="{WHEEL_Y + 8}" x2="{rx_ + 11 * math.cos(math.radians(a)):.1f}" y2="{WHEEL_Y + 8 + 11 * math.sin(math.radians(a)):.1f}" stroke="#4A5E54" stroke-width="2.4"/>' for a in range(0, 360, 72))
                   + f'<circle cx="{rx_}" cy="{WHEEL_Y + 8}" r="3.6" fill="#4A5E54"/></g>')
    bus.append('</g>')                                           # cierre .cab
    s += bus
    s.append(f'<path class="faro" d="M{bx + BUSW - 2} {by_ + 62}L{bx + BUSW + 230} {by_ + 36}L{bx + BUSW + 230} {by_ + 116}Z" fill="url(#haz)" opacity="0"/>')
    # boleto electrónico
    TX, TY = SX + 710, SY + 18
    bol = [f'<g class="bol"><rect x="{TX}" y="{TY}" width="180" height="104" rx="12" fill="#F6F1E4"/>',
           f'<path d="M{TX} {TY + 12}a12 12 0 0 1 12 -12H{TX + 168}a12 12 0 0 1 12 12V{TY + 32}H{TX}Z" fill="{acento}"/>',
           f'<text x="{TX + 90}" y="{TY + 23}" text-anchor="middle" font-family="{SANS}" font-size="17" font-weight="800" fill="#2A3B34">Boleto electrónico</text>',
           f'<circle cx="{TX}" cy="{TY + 54}" r="7" fill="{BG}"/><circle cx="{TX + 180}" cy="{TY + 54}" r="7" fill="{BG}"/><line x1="{TX + 10}" y1="{TY + 54}" x2="{TX + 170}" y2="{TY + 54}" stroke="#B9B29C" stroke-dasharray="4 4"/>']
    xx = TX + 22
    for i, w in enumerate((3, 2, 5, 2, 3, 6, 2, 4, 2, 3, 5, 2, 3, 4, 2, 5, 3, 2, 4, 3)):
        bol.append(f'<rect x="{xx}" y="{TY + 66}" width="{w}" height="26" fill="#2A3B34"/>')
        xx += w + 2.5
    bol.append('</g>')
    s += bol
    s.append('</g>')                                              # cierre clip escena
    # tira de ruta
    RY, X0, X1 = SY + SH + 24, SX + 50, SX + SW - 50
    s.append(f'<rect x="{SX}" y="{SY + SH}" width="{SW}" height="{ST_H - SH}" fill="{S1}"/>')
    s.append(f'<line x1="{X0}" y1="{RY}" x2="{X1}" y2="{RY}" stroke="{LINE}" stroke-width="5" stroke-linecap="round"/>')
    s.append(f'<line class="prog" pathLength="1" x1="{X0}" y1="{RY}" x2="{X1}" y2="{RY}" stroke="{acento}" stroke-width="5" stroke-linecap="round" style="stroke-dasharray:1;stroke-dashoffset:0"/>')
    for fx in (1 / 3, 2 / 3):
        s.append(f'<circle cx="{X0 + (X1 - X0) * fx:.0f}" cy="{RY}" r="6" fill="{S1}" stroke="{acento}" stroke-width="2.4"/>')
    s.append(f'<circle cx="{X0}" cy="{RY}" r="8" fill="{acento}"/><circle cx="{X1}" cy="{RY}" r="8" fill="{acento2}"/>')
    s.append(f'<g class="marc"><circle cx="{X1}" cy="{RY}" r="10" fill="{BG}" stroke="{MENTA}" stroke-width="3"/><circle cx="{X1}" cy="{RY}" r="3.5" fill="{MENTA}"/></g>')
    s.append(f'<text x="{X0 - 6}" y="{RY + 24}" font-family="{SANS}" font-size="16" fill="{MUTED}">Origen</text>'
             f'<text x="{X1 + 6}" y="{RY + 24}" text-anchor="end" font-family="{SANS}" font-size="16" fill="{MUTED}">Destino</text>')
    s.append('</g></g>')
    s += pie_tarjeta(acento, None)
    s += fila_logos(["react", "vite", "javascript", "springboot", "postgresql", "supabase", "mercadopago"])
    guardar("proyecto-rutalibre.svg", envolver(W, H, "".join(s),
            "RutaLibre. Animación: un bus avanza por una carretera con montañas, colinas, árboles y postes que se mueven a distinta velocidad mientras el cielo pasa del amanecer al atardecer. Una línea de ruta con origen, dos hitos y destino avanza al ritmo del bus. Al llegar, el bus frena con las luces de freno encendidas, aparece el pin del destino con una onda y se muestra un boleto electrónico. Tecnologías: React, Vite, JavaScript, Spring Boot, PostgreSQL, Supabase y Mercado Pago. Toca para ver repositorio y demo.",
            defs, css_base("".join(css))))



def generar(boton_enlace):
    estudio()
    ruta()
    boton_enlace("btn-repo-estudio.svg", "Repositorio", JADE, SALVIA, "repo", "Ver repositorio de Plataforma Estudio AI en GitHub")
    boton_enlace("btn-demo-estudio.svg", "Demo en vivo", JADE, SALVIA, "demo", "Ver demo en vivo de Plataforma Estudio AI")
    boton_enlace("btn-repo-rutalibre.svg", "Repositorio", ORO, CORAL, "repo", "Ver repositorio de RutaLibre en GitHub")
    boton_enlace("btn-demo-rutalibre.svg", "Demo en vivo", ORO, CORAL, "demo", "Ver demo en vivo de RutaLibre")
