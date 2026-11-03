#!/usr/bin/env python3
"""Genera assets/stats.svg con datos reales de la API de GitHub (solo biblioteca estándar).

Uso en el workflow: GITHUB_TOKEN y GITHUB_USER como variables de entorno.
Prueba local sin red:  python scripts/generar_stats.py --simulado   (datos de prueba, no publicar)
"""
import datetime as dt
import json
import os
import sys
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, "..", "assets", "stats.svg")

S1, S2, LINE = "#0D1421", "#111C2B", "#1E293B"
BLUE, CYAN, PURPLE = "#3B82F6", "#22D3EE", "#8B5CF6"
TXT, MUTED = "#F8FAFC", "#94A3B8"
SANS = "Inter,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

CONSULTA = """
query($login:String!){user(login:$login){
  contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{contributionCount date}}}}
  repositories(first:100, ownerAffiliations:OWNER, isFork:false, privacy:PUBLIC){nodes{primaryLanguage{name}}}
}}"""


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
    dias = [d for w in cal["weeks"] for d in w["contributionDays"]]
    dias.sort(key=lambda d: d["date"])
    hoy = dt.date.today().isoformat()
    dias = [d for d in dias if d["date"] <= hoy]
    mejor = actual = 0
    racha = 0
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
    semanas = []
    for w in cal["weeks"][-16:]:
        semanas.append(sum(d["contributionCount"] for d in w["contributionDays"]))
    lenguajes = {}
    for r in user["repositories"]["nodes"]:
        if r.get("primaryLanguage"):
            n = r["primaryLanguage"]["name"]
            lenguajes[n] = lenguajes.get(n, 0) + 1
    top = sorted(lenguajes.items(), key=lambda kv: (-kv[1], kv[0]))[:5]
    return {"total": cal["totalContributions"], "actual": actual, "mejor": mejor, "semanas": semanas, "lenguajes": top}


def svg(d):
    W, H = 1000, 360
    vacio = d is None
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Panel de actividad en GitHub: contribuciones, rachas, actividad semanal y lenguajes">',
         '<defs><filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
         f'<linearGradient id="gb" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>'
         f'<linearGradient id="gh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{PURPLE}"/></linearGradient></defs>',
         f'<rect x=".5" y=".5" width="999" height="359" rx="16" fill="{S1}" stroke="{LINE}"/>']
    # columna izquierda: métricas
    metricas = [("CONTRIBUCIONES · 12 MESES", "—" if vacio else f"{d['total']:,}".replace(",", " "), CYAN),
                ("RACHA ACTUAL · DÍAS", "—" if vacio else str(d["actual"]), BLUE),
                ("RACHA MÁS LARGA · DÍAS", "—" if vacio else str(d["mejor"]), PURPLE)]
    for i, (k, v, c) in enumerate(metricas):
        y = 40 + i * 92
        s.append(f'<rect x="28" y="{y}" width="290" height="80" rx="12" fill="{S2}" stroke="{c}" stroke-opacity=".45"/>'
                 f'<rect x="28" y="{y + 14}" width="3" height="52" rx="1.5" fill="{c}"/>'
                 f'<text x="48" y="{y + 28}" font-family="{MONO}" font-size="10.5" fill="{MUTED}" letter-spacing="2">{k}</text>'
                 f'<text x="48" y="{y + 66}" font-family="{SANS}" font-size="38" font-weight="800" fill="{TXT}">{v}</text>')
    # centro: actividad semanal
    s.append(f'<text x="350" y="56" font-family="{MONO}" font-size="11" fill="{CYAN}" letter-spacing="2">ACTIVIDAD SEMANAL</text>'
             f'<text x="350" y="74" font-family="{SANS}" font-size="12" fill="{MUTED}">Contribuciones por semana, últimas 16</text>')
    base, alto = 300, 170
    semanas = d["semanas"] if not vacio else [0] * 16
    mx = max(semanas + [1])
    for i, v in enumerate(semanas):
        h = max(3, v / mx * alto) if not vacio else 3
        x = 350 + i * 19
        s.append(f'<rect x="{x}" y="{base - h:.1f}" width="13" height="{h:.1f}" rx="4" fill="url(#gb)" fill-opacity="{.9 if v else .25}">'
                 f'<animate attributeName="height" from="0" to="{h:.1f}" dur=".9s" begin="{i * .05:.2f}s" fill="freeze"/>'
                 f'<animate attributeName="y" from="{base}" to="{base - h:.1f}" dur=".9s" begin="{i * .05:.2f}s" fill="freeze"/></rect>')
    s.append(f'<line x1="346" y1="{base + 6}" x2="660" y2="{base + 6}" stroke="{LINE}"/>')
    # derecha: lenguajes
    s.append(f'<text x="700" y="56" font-family="{MONO}" font-size="11" fill="{CYAN}" letter-spacing="2">LENGUAJES</text>'
             f'<text x="700" y="74" font-family="{SANS}" font-size="12" fill="{MUTED}">Repos públicos por lenguaje principal</text>')
    top = d["lenguajes"] if not vacio else []
    mxl = max([n for _, n in top] + [1])
    for i, (nom, n) in enumerate(top):
        y = 104 + i * 40
        w = 270 * n / mxl
        s.append(f'<text x="700" y="{y}" font-family="{SANS}" font-size="13" font-weight="600" fill="{TXT}">{nom}</text>'
                 f'<text x="970" y="{y}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUTED}">{n}</text>'
                 f'<rect x="700" y="{y + 8}" width="270" height="7" rx="3.5" fill="{S2}"/>'
                 f'<rect x="700" y="{y + 8}" width="{w:.0f}" height="7" rx="3.5" fill="url(#gh)"><animate attributeName="width" from="0" to="{w:.0f}" dur="1s" begin="{i * .12:.2f}s" fill="freeze"/></rect>')
    if vacio:
        s.append(f'<text x="835" y="190" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{MUTED}">Se completa con el primer</text>'
                 f'<text x="835" y="210" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{MUTED}">workflow de GitHub Actions</text>')
    pie = "Pendiente de la primera ejecución" if vacio else f"Actualizado {dt.date.today().isoformat()} · fuente: API de GitHub · los lenguajes no miden nivel de dominio"
    s.append(f'<text x="28" y="344" font-family="{MONO}" font-size="10.5" fill="{MUTED}" letter-spacing="1">{pie}</text>'
             f'<circle cx="972" cy="340" r="4" fill="{CYAN}" filter="url(#glow)"><animate attributeName="opacity" values="1;.3;1" dur="2s" repeatCount="indefinite"/></circle>')
    s.append("</svg>")
    return "".join(s)


def escribir_marcador(ruta):
    """Panel sin cifras: se usa solo hasta que el workflow genere datos reales."""
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(svg(None))


def principal():
    if "--simulado" in sys.argv:
        user = {"contributionsCollection": {"contributionCalendar": {"totalContributions": 123, "weeks": [
            {"contributionDays": [{"contributionCount": (i * 7 + j) % 5, "date": (dt.date.today() - dt.timedelta(days=(40 - i) * 7 - j)).isoformat()} for j in range(7)]} for i in range(40)]}},
            "repositories": {"nodes": [{"primaryLanguage": {"name": n}} for n in ["TypeScript"] * 4 + ["Java", "Python", "Python", "JavaScript"]]}}
    else:
        token, usuario = os.environ.get("GITHUB_TOKEN"), os.environ.get("GITHUB_USER")
        if not token or not usuario:
            sys.exit("Faltan GITHUB_TOKEN o GITHUB_USER")
        user = consultar(usuario, token)
    with open(SALIDA, "w", encoding="utf-8") as f:
        f.write(svg(procesar(user)))
    print("stats.svg escrito")


if __name__ == "__main__":
    principal()
