#!/usr/bin/env python3
"""Genera dist/index.html y dist/cuenta.png con los días que faltan."""
import json
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).parent
SALIDA = RAIZ / "dist"
FUENTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
ANCHO, ALTO = 1200, 630


def cargar_config():
    cfg = json.loads((RAIZ / "config.json").read_text(encoding="utf-8"))
    cfg["fecha"] = date.fromisoformat(cfg["fecha"])
    cfg["base_url"] = cfg["base_url"].rstrip("/") + "/"
    return cfg


def textos(dias, titulo):
    if dias > 1:
        return str(dias), f"días para {titulo}"
    if dias == 1:
        return "1", f"día para {titulo}"
    if dias == 0:
        return "¡HOY!", titulo
    return "Ya pasó", titulo


def fuente(tam):
    return ImageFont.truetype(FUENTE, tam)


def ajustar(draw, texto, tam, max_ancho):
    while tam > 20 and draw.textlength(texto, font=fuente(tam)) > max_ancho:
        tam -= 2
    return fuente(tam)


def dibujar(numero, linea, ruta):
    img = Image.new("RGB", (ANCHO, ALTO))
    px = img.load()
    for y in range(ALTO):  # degradado vertical
        t = y / ALTO
        c = (int(20 + 40 * t), int(30 + 20 * t), int(80 + 70 * t))
        for x in range(ANCHO):
            px[x, y] = c
    d = ImageDraw.Draw(img)
    f_num = ajustar(d, numero, 330, ANCHO - 120)
    f_txt = ajustar(d, linea, 64, ANCHO - 120)
    d.text((ANCHO / 2, 270), numero, font=f_num, fill="white", anchor="mm")
    d.text((ANCHO / 2, 500), linea, font=f_txt, fill=(210, 220, 255), anchor="mm")
    img.save(ruta, optimize=True)


def html(cfg, numero, linea):
    hoy = datetime.now(ZoneInfo("Europe/Madrid")).strftime("%Y%m%d")
    imagen = f"{cfg['base_url']}cuenta.png?v={hoy}"
    titulo = f"{numero} {linea}"
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta property="og:type" content="website">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="Cuenta atrás">
<meta property="og:image" content="{imagen}">
<meta property="og:image:width" content="{ANCHO}">
<meta property="og:image:height" content="{ALTO}">
<meta property="og:url" content="{cfg['base_url']}">
<style>body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#1e2a5a;color:#fff;font-family:system-ui,sans-serif}}img{{max-width:100%;height:auto}}</style>
</head>
<body><img src="cuenta.png?v={hoy}" alt="{titulo}"></body>
</html>
"""


def main():
    cfg = cargar_config()
    hoy = datetime.now(ZoneInfo("Europe/Madrid")).date()
    dias = (cfg["fecha"] - hoy).days
    numero, linea = textos(dias, cfg["titulo"])
    SALIDA.mkdir(exist_ok=True)
    dibujar(numero, linea, SALIDA / "cuenta.png")
    (SALIDA / "index.html").write_text(html(cfg, numero, linea), encoding="utf-8")
    (SALIDA / ".nojekyll").touch()
    print(f"Hoy: {hoy} | Faltan {dias} días | {numero} {linea}")


if __name__ == "__main__":
    sys.exit(main())
