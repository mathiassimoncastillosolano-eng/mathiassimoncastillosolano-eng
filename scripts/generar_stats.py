#!/usr/bin/env python3
"""Genera assets/stats.svg y assets/heatmap.svg con datos reales de la API de GitHub (solo biblioteca estándar).

Uso en el workflow: GITHUB_TOKEN y GITHUB_USER como variables de entorno.
Prueba local sin red:  python scripts/generar_stats.py --simulado   (datos de prueba, NO publicar)
Marcador sin cifras:   lo escribe construir_assets.py hasta la primera ejecución del workflow.
"""
import datetime as dt
import json
import os
import sys
import urllib.request

from diseno import (BG, S1, S2, LINE, JADE, MENTA, SALVIA, ORO, TXT, MUTED, SANS, MONO, SALIDA,
                    css_base, keyframes, envolver, marco)

CONSULTA = """
query($login:String!){user(login:$login){
  contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{contributionCount date}}}}
  repositories(first:100, ownerAffiliations:OWNER, isFork:false, privacy:PUBLIC){nodes{primaryLanguage{name}}}
}}"""

NIVELES = ["#14231D", "#1F6B4F", "#2E9A72", "#3DBE8B", "#8FE3BC"]   # 0 = sin actividad ... 4 = máxima


def consultar(usuario, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": CONSULTA, "variables": {"login": usuario}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "perfil-stats"})
    with urllib.request.urlopen(req, timeout=30) as r:
        datos = json.load(r)
    if "errors" in datos or not datos.get("data", {}).get("user"):
        raise RuntimeError(f"Respuesta inválida de GitHub: {datos.get('errors')}")
    return datos["data"]["user"]


def procesar(user):
    cal = user["contributionsCollection"]["contributionCalendar"]
    semanas_api = cal["weeks"]
    dias = sorted((d for w in semanas_api for d in w["contributionDays"]), key=lambda d: d["date"])
    hoy = dt.date.today().isoformat()
    dias = [d for d in dias if d["date"] <= hoy]
    mejor = racha = 0
    for d in dias:
        racha = racha + 1 if d["contributionCount"] > 0 else 0
        mejor = max(mejor, racha)
    actual = 0
    for d in reversed(dias):
        if d["contributionCount"] > 0:
            actual += 1
        elif d["date"] == hoy:
            continue  # hoy aún puede no tener actividad
        else:
            break
    semanales = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in semanas_api[-16:]]
    lenguajes = {}
    for r in user["repositories"]["nodes"]:
        if r.get("primaryLanguage"):
            n = r["primaryLanguage"]["name"]
            lenguajes[n] = lenguajes.get(n, 0) + 1
    top = sorted(lenguajes.items(), key=lambda kv: (-kv[1], kv[0]))[:5]
    return {"total": cal["totalContributions"], "actual": actual, "mejor": mejor, "semanas": semanales,
            "lenguajes": top, "calendario": [[(d["date"], d["contributionCount"]) for d in w["contributionDays"]] for w in semanas_api]}


# ------------------------------------------------------------------ panel
def svg_panel(d):
    W, H = 1000, 400
    vacio = d is None
    css = css_base(".b{transform-origin:bottom;animation:sube 1s ease-out both}.w{transform-origin:left;animation:ancho 1.1s ease-out both}"
                   ".v{animation:vivo 2.4s ease-in-out infinite}"
                   + keyframes("sube", [(0, "transform:scaleY(0)"), (100, "transform:scaleY(1)")])
                   + keyframes("ancho", [(0, "transform:scaleX(0)"), (100, "transform:scaleX(1)")])
                   + keyframes("vivo", [(0, "opacity:1"), (50, "opacity:.25"), (100, "opacity:1")]))
    defs = (f'<linearGradient id="gb" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{NIVELES[1]}"/><stop offset="1" stop-color="{MENTA}"/></linearGradient>'
            f'<linearGradient id="gh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{JADE}"/><stop offset="1" stop-color="{MENTA}"/></linearGradient>')
    s = [marco(W, H, S1, LINE, 18)]
    metricas = [("CONTRIBUCIONES · 12 MESES", "—" if vacio else f"{d['total']:,}".replace(",", " "), JADE),
                ("RACHA ACTUAL · DÍAS", "—" if vacio else str(d["actual"]), MENTA),
                ("RACHA MÁS LARGA · DÍAS", "—" if vacio else str(d["mejor"]), ORO)]
    for i, (k, v, c) in enumerate(metricas):
        y = 28 + i * 104
        s.append(f'<rect x="28" y="{y}" width="318" height="92" rx="14" fill="{S2}" stroke="{c}" stroke-opacity=".5"/>'
                 f'<rect x="28" y="{y + 16}" width="4" height="60" rx="2" fill="{c}"/>'
                 f'<text x="50" y="{y + 30}" font-family="{MONO}" font-size="16" fill="{MUTED}" letter-spacing="1">{k}</text>'
                 f'<text x="50" y="{y + 76}" font-family="{SANS}" font-size="44" font-weight="800" fill="{TXT}">{v}</text>')
    s.append(f'<text x="384" y="54" font-family="{MONO}" font-size="16" fill="{JADE}" letter-spacing="2">ACTIVIDAD SEMANAL</text>'
             f'<text x="384" y="80" font-family="{SANS}" font-size="16" fill="{MUTED}">Contribuciones por semana, últimas 16</text>')
    base, alto = 318, 190
    semanas = d["semanas"] if not vacio else [0] * 16
    mx = max(semanas + [1])
    for i, v in enumerate(semanas):
        h = max(4, v / mx * alto) if not vacio else 4
        x = 384 + i * 19
        s.append(f'<rect class="b" style="animation-delay:{i * .05:.2f}s" x="{x}" y="{base - h:.1f}" width="13" height="{h:.1f}" rx="4" fill="url(#gb)" fill-opacity="{.95 if v else .3}"/>')
    s.append(f'<line x1="378" y1="{base + 8}" x2="696" y2="{base + 8}" stroke="{LINE}"/>')
    s.append(f'<text x="736" y="54" font-family="{MONO}" font-size="16" fill="{JADE}" letter-spacing="2">LENGUAJES</text>'
             f'<text x="736" y="80" font-family="{SANS}" font-size="16" fill="{MUTED}">Repos públicos por lenguaje</text>')
    top = d["lenguajes"] if not vacio else []
    mxl = max([n for _, n in top] + [1])
    for i, (nom, n) in enumerate(top):
        y = 120 + i * 44
        w = 236 * n / mxl
        s.append(f'<text x="736" y="{y}" font-family="{SANS}" font-size="18" font-weight="600" fill="{TXT}">{nom}</text>'
                 f'<text x="972" y="{y}" text-anchor="end" font-family="{MONO}" font-size="16" fill="{MUTED}">{n}</text>'
                 f'<rect x="736" y="{y + 10}" width="236" height="8" rx="4" fill="{S2}"/>'
                 f'<rect class="w" style="animation-delay:{i * .12:.2f}s" x="736" y="{y + 10}" width="{w:.0f}" height="8" rx="4" fill="url(#gh)"/>')
    if vacio:
        s.append(f'<text x="854" y="200" text-anchor="middle" font-family="{SANS}" font-size="18" fill="{MUTED}">Se completa con el primer</text>'
                 f'<text x="854" y="226" text-anchor="middle" font-family="{SANS}" font-size="18" fill="{MUTED}">workflow de GitHub Actions</text>')
    pie = "Pendiente de la primera ejecución del workflow" if vacio else f"Actualizado {dt.date.today().isoformat()} · fuente: API de GitHub"
    s.append(f'<text x="28" y="378" font-family="{MONO}" font-size="16" fill="{MUTED}">{pie}</text>'
             f'<text x="972" y="378" text-anchor="end" font-family="{SANS}" font-size="16" fill="{MUTED}">Los lenguajes no miden nivel de dominio</text>')
    s.append(f'<circle class="v" cx="{W - 28}" cy="30" r="5" fill="{MENTA}"/>')
    return envolver(W, H, "".join(s), "Panel de actividad en GitHub: contribuciones del último año, racha actual, racha más larga, actividad semanal y lenguajes de los repositorios públicos. Los lenguajes no miden nivel de dominio.", defs, css)


# ------------------------------------------------------------------ mapa de calor
def nivel(n, mx):
    if n <= 0:
        return 0
    q = n / max(mx, 1)
    return 1 if q <= .25 else 2 if q <= .5 else 3 if q <= .75 else 4


def svg_heatmap(d):
    """Calendario de 12 meses propio. Sin datos (d=None) muestra la cuadrícula vacía y un aviso."""
    W, H = 1000, 250
    CELL, PASO, X0, Y0 = 14, 17.2, 40, 74
    vacio = d is None
    semanas = d["calendario"] if not vacio else [[None] * 7 for _ in range(53)]
    mx = max([c for w in semanas for _, c in w if c is not None] + [1]) if not vacio else 1
    css = css_base(".c{animation:ap .6s ease-out both}" + keyframes("ap", [(0, "opacity:0"), (100, "opacity:1")]))
    s = [marco(W, H, S1, LINE, 18),
         f'<text x="40" y="44" font-family="{MONO}" font-size="16" fill="{JADE}" letter-spacing="2">MAPA DE CALOR · ÚLTIMOS 12 MESES</text>']
    meses = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
    ultimo = None
    for i, w in enumerate(semanas):
        x = X0 + i * PASO
        if not vacio and w and w[0][0]:
            m = int(w[0][0][5:7])
            if m != ultimo and i < 51:
                s.append(f'<text x="{x:.1f}" y="66" font-family="{SANS}" font-size="16" fill="{MUTED}">{meses[m - 1]}</text>')
                ultimo = m
        for j, c in enumerate(w):
            lv = 0 if vacio or c[1] is None else nivel(c[1], mx)
            tit = "" if vacio else f"<title>{c[0]}: {c[1]}</title>"
            s.append(f'<rect class="c" style="animation-delay:{i * .012:.3f}s" x="{x:.1f}" y="{Y0 + j * PASO:.1f}" width="{CELL}" height="{CELL}" rx="3.5" fill="{NIVELES[lv]}"{">" + tit + "</rect>" if tit else "/>"}')
    s.append(f'<text x="40" y="226" font-family="{SANS}" font-size="16" fill="{MUTED}">{"Pendiente de la primera ejecución del workflow" if vacio else "Actualizado " + dt.date.today().isoformat()}</text>')
    s.append(f'<text x="770" y="226" text-anchor="end" font-family="{SANS}" font-size="16" fill="{MUTED}">Menos</text>')
    for k, c in enumerate(NIVELES):
        s.append(f'<rect x="{782 + k * 20}" y="213" width="14" height="14" rx="3.5" fill="{c}"/>')
    s.append(f'<text x="{786 + 5 * 20}" y="226" font-family="{SANS}" font-size="16" fill="{MUTED}">Más</text>')
    return envolver(W, H, "".join(s), "Mapa de calor de contribuciones en GitHub durante los últimos 12 meses. Cuanto más intenso el verde, más contribuciones ese día.", "", css)


def _simulado():
    hoy = dt.date.today()
    inicio = hoy - dt.timedelta(days=52 * 7 + hoy.weekday() + 1)
    semanas = []
    for i in range(53):
        w = []
        for j in range(7):
            f = inicio + dt.timedelta(days=i * 7 + j)
            if f <= hoy:
                w.append({"contributionCount": (i * 7 + j * 3) % 7 if (i + j) % 3 else 0, "date": f.isoformat()})
        semanas.append({"contributionDays": w})
    return {"contributionsCollection": {"contributionCalendar": {"totalContributions": 123, "weeks": semanas}},
            "repositories": {"nodes": [{"primaryLanguage": {"name": n}} for n in ["TypeScript"] * 4 + ["Java", "Python", "Python", "JavaScript"]]}}


def principal():
    if "--simulado" in sys.argv:
        user = _simulado()
    else:
        token, usuario = os.environ.get("GITHUB_TOKEN"), os.environ.get("GITHUB_USER")
        if not token or not usuario:
            sys.exit("Faltan GITHUB_TOKEN o GITHUB_USER")
        user = consultar(usuario, token)
    d = procesar(user)
    destino = SALIDA if "--simulado" not in sys.argv else (sys.argv[sys.argv.index("--simulado") + 1] if len(sys.argv) > sys.argv.index("--simulado") + 1 else SALIDA)
    os.makedirs(destino, exist_ok=True)
    for nombre, svg in (("stats.svg", svg_panel(d)), ("heatmap.svg", svg_heatmap(d))):
        with open(os.path.join(destino, nombre), "w", encoding="utf-8") as f:
            f.write(svg)
    print("stats.svg y heatmap.svg escritos en", destino)


if __name__ == "__main__":
    principal()
