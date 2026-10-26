#!/usr/bin/env python3
"""Genera dist/index.html (cuenta atrás en vivo) y dist/cuenta.png (vista previa)."""
import hashlib
import html as h
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).parent
SALIDA = RAIZ / "dist"
ANCHO, ALTO = 1200, 630
TZ = ZoneInfo("Europe/Madrid")
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]


def cargar_config():
    cfg = json.loads((RAIZ / "config.json").read_text(encoding="utf-8"))
    cfg.setdefault("hora", "12:00")
    cfg["base_url"] = cfg["base_url"].rstrip("/") + "/"
    cfg["objetivo"] = datetime.fromisoformat(f"{cfg['fecha']}T{cfg['hora']}").replace(tzinfo=TZ)
    return cfg


def fecha_larga(dt):
    return f"{DIAS[dt.weekday()].capitalize()} {dt.day} de {MESES[dt.month - 1]}"


def f(ruta, tam):
    return ImageFont.truetype(ruta, tam)


def ajustar(d, texto, ruta, tam, max_ancho):
    while tam > 20 and d.textlength(texto, font=f(ruta, tam)) > max_ancho:
        tam -= 2
    return f(ruta, tam)


def imagen_previa(cfg, ruta):
    img = Image.new("RGB", (ANCHO, ALTO))
    px = img.load()
    for y in range(ALTO):  # degradado vertical otoñal
        t = y / ALTO
        c = (int(150 - 105 * t), int(66 - 48 * t), int(30 - 18 * t))
        for x in range(ANCHO):
            px[x, y] = c
    img = img.convert("RGBA")
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)

    # copa de vermut (izquierda)
    d.polygon([(150, 250), (430, 250), (405, 545), (175, 545)], fill=(255, 243, 224, 40),
              outline=(255, 228, 196, 255), width=7)
    d.polygon([(158, 330), (422, 330), (404, 535), (176, 535)], fill=(158, 52, 22, 255))
    d.rounded_rectangle((215, 355, 300, 440), 14, fill=(255, 255, 255, 70))
    d.rounded_rectangle((300, 410, 375, 485), 14, fill=(255, 255, 255, 55))
    d.line([(430, 60), (330, 270)], fill=(217, 199, 160, 255), width=9)  # pincho
    d.ellipse((315, 150, 365, 190), fill=(124, 143, 44, 255))              # aceituna
    d.ellipse((335, 160, 349, 174), fill=(192, 57, 43, 255))
    cx, cy = 440, 255                                                      # naranja
    d.ellipse((cx - 70, cy - 70, cx + 70, cy + 70), fill=(242, 140, 30, 255),
              outline=(255, 180, 84, 255), width=10)
    for dx, dy in [(0, 58), (50, 29), (50, -29)]:
        d.line([(cx - dx, cy - dy), (cx + dx, cy + dy)], fill=(255, 224, 168, 255), width=6)
    img = Image.alpha_composite(img, capa).convert("RGB")

    d = ImageDraw.Draw(img)
    x0, ancho = 560, ANCHO - 560 - 60
    partes = cfg["titulo"].split(" ", 1)
    t1 = partes[0]
    d.text((x0, 190), t1, font=ajustar(d, t1, SERIF, 120, ancho), fill=(255, 216, 168))
    if len(partes) > 1:
        t2 = partes[1]
        d.text((x0, 320), t2, font=ajustar(d, t2, SERIF, 120, ancho), fill=(255, 216, 168))
    d.text((x0, 455), fecha_larga(cfg["objetivo"]), font=ajustar(d, "x" * 26, SERIF_I, 40, ancho),
           fill=(243, 184, 138))
    # botón
    texto = "Toca para ver la cuenta atrás"
    fb = ajustar(d, texto, SANS, 30, ancho - 60)
    w = d.textlength(texto, font=fb)
    d.rounded_rectangle((x0, 520, x0 + w + 60, 580), 30, fill=(255, 216, 168))
    d.text((x0 + 30, 550), texto, font=fb, fill=(74, 20, 16), anchor="lm")
    img.save(ruta, optimize=True)


def main():
    cfg = cargar_config()
    SALIDA.mkdir(exist_ok=True)
    png = SALIDA / "cuenta.png"
    imagen_previa(cfg, png)
    version = hashlib.md5(png.read_bytes()).hexdigest()[:8]

    ahora = datetime.now(TZ)
    dias = max((cfg["objetivo"].date() - ahora.date()).days, 0)
    pagina = (RAIZ / "plantilla.html").read_text(encoding="utf-8")
    cambios = {
        "__TITULO__": h.escape(cfg["titulo"]),
        "__FECHA_LARGA__": fecha_larga(cfg["objetivo"]),
        "__HORA__": cfg["hora"],
        "__IMAGEN__": f"{cfg['base_url']}cuenta.png?v={version}",
        "__URL__": cfg["base_url"],
        "__OBJETIVO__": cfg["objetivo"].isoformat(),
        "__DIAS__": str(dias),
        "__ETQ__": ("día" if dias == 1 else "días") + " para brindar",
    }
    for k, v in cambios.items():
        pagina = pagina.replace(k, v)
    (SALIDA / "index.html").write_text(pagina, encoding="utf-8")
    (SALIDA / ".nojekyll").touch()
    print(f"Objetivo: {cfg['objetivo'].isoformat()} | faltan {dias} días | imagen v={version}")


if __name__ == "__main__":
    sys.exit(main())
