"""Sistema de diseño compartido: paleta, tipografía, logos incrustados y utilidades CSS/SVG.

Solo usa la biblioteca estándar, salvo `fontTools` (opcional, solo para convertir el nombre del hero en trazados).
"""
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, "..", "assets")
os.makedirs(SALIDA, exist_ok=True)

# ---------------------------------------------------------------- paleta "Obsidiana y Jade"
BG, S1, S2, LINE = "#08110E", "#0E1814", "#14231D", "#22362D"
JADE = "#3DBE8B"        # acento principal (esmeralda sobrio)
MENTA = "#8FE3BC"       # luz / resaltado
MUSGO = "#1F6B4F"       # sombra del acento
SALVIA = "#B9D6A0"      # acento puntual del proyecto de estudio (lima apagado)
ORO = "#D9B25F"         # ámbar cálido (RutaLibre y "en aprendizaje")
CORAL = "#E58A7B"       # alerta / destaque
TXT, MUTED = "#EEF3EF", "#9DB0A5"

SANS = "Inter,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

RUTA_LOGOS = os.path.join(AQUI, "logos")

# colores de marca ajustados para fondo oscuro (None = conserva los del propio logo)
COLOR_LOGO = {
    "python": "#4B8BBE", "openjdk": "#E76F00", "javascript": "#F7DF1E", "typescript": "#3B8EDB",
    "fastapi": "#05B8A3", "react": "#61DAFB", "vite": "#9B8CFF", "tailwindcss": "#38BDF8",
    "html5": "#E96228", "css": "#3C9CE0", "scikitlearn": "#F7931E", "pandas": "#E9559A",
    "mysql": "#5B9BC6", "postgresql": "#5B84E8", "supabase": "#3ECF8E", "git": "#F05032",
    "github": "#EEF3EF", "neon": "#00E599", "springboot": "#6DB33F", "mercadopago": "#35B8F0",
}


def css_base(extra=""):
    """CSS común: transforms sobre la caja del propio elemento y respeto a prefers-reduced-motion."""
    return ("<style>*{transform-box:fill-box}"
            + extra
            + "@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>")


def keyframes(nombre, paradas):
    """paradas: lista de (porcentaje, 'decl;decl', timing opcional del tramo que empieza ahí)."""
    out = []
    for p in paradas:
        pct, decl = p[0], p[1]
        t = f"animation-timing-function:{p[2]};" if len(p) > 2 and p[2] else ""
        out.append(f"{pct}%{{{decl};{t}}}")
    return f"@keyframes {nombre}{{{''.join(out)}}}"


def envolver(w, h, cuerpo, etiqueta, defs="", css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{etiqueta}">{css}<defs>{defs}</defs>{cuerpo}</svg>')


def guardar(nombre, contenido):
    ruta = os.path.join(SALIDA, nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    print("ok", nombre, os.path.getsize(ruta) // 1024, "KB")


# ---------------------------------------------------------------- logos reales
_cache = {}


def _leer(clave):
    if clave in _cache:
        return _cache[clave]
    for carpeta, nombre in (("simple-icons", f"{clave}.svg"), ("devicon", f"{clave}-original.svg")):
        ruta = os.path.join(RUTA_LOGOS, carpeta, nombre)
        if os.path.exists(ruta):
            _cache[clave] = (carpeta, open(ruta, encoding="utf-8").read())
            return _cache[clave]
    raise FileNotFoundError(f"Logo no disponible: {clave}")


def logo(clave, x, y, tam, color=None):
    """Incrusta el logo oficial como vector, centrado en una caja tam×tam con esquina (x, y)."""
    carpeta, src = _leer(clave)
    if carpeta == "simple-icons":
        d = re.search(r'<path d="([^"]+)"', src).group(1)
        c = color or COLOR_LOGO.get(clave, TXT)
        return (f'<svg x="{x}" y="{y}" width="{tam}" height="{tam}" viewBox="0 0 24 24">'
                f'<path d="{d}" fill="{c}"/></svg>')
    vb = re.search(r'viewBox="([^"]+)"', src).group(1)
    interior = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", src, flags=re.S)
    interior = interior.replace("#252f3e", "#E7EFEA").replace("#232F3E", "#E7EFEA")  # texto oscuro de AWS
    return f'<svg x="{x}" y="{y}" width="{tam}" height="{tam}" viewBox="{vb}">{interior}</svg>'


# ---------------------------------------------------------------- texto -> trazados
def texto_a_path(texto, tam, x, y, ruta_fuente, espaciado=0.0):
    """Devuelve (d, ancho). El texto se convierte a trazados para verse idéntico en cualquier dispositivo."""
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.ttLib import TTFont

    f = TTFont(ruta_fuente)
    gs, cmap, upm = f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm
    esc = tam / upm
    cursor = x
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
    for ch in texto:
        g = cmap[ord(ch)]
        tp = TransformPen(pen, (esc, 0, 0, -esc, cursor, y))
        gs[g].draw(tp)
        cursor += gs[g].width * esc + espaciado
    return pen.getCommands(), cursor - x - espaciado


def marco(w, h, fondo=S1, borde=LINE, r=18):
    return f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{r}" fill="{fondo}" stroke="{borde}"/>'
