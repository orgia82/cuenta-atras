# Cuenta atrás para WhatsApp

Página estática que muestra los días que faltan para una fecha.
Cuando pegas el enlace en WhatsApp, la vista previa muestra una imagen con el número del día.

## Cómo cambiar la fecha

Edita `config.json`:

- `titulo`: nombre del evento.
- `fecha`: fecha en formato `AAAA-MM-DD`.
- `base_url`: dirección de la página en GitHub Pages.

Cada `push` a `main` publica la página de nuevo.

## Cómo funciona

1. `generar.py` calcula los días (hora de Madrid) y crea `dist/cuenta.png` y `dist/index.html`.
2. La Action `.github/workflows/diario.yml` ejecuta el script cada día a las 00:05.
3. La Action publica la carpeta `dist` en GitHub Pages. No hace commits.

## Prueba en local

    pip install pillow
    python generar.py

## Nota sobre la caché de WhatsApp

WhatsApp guarda la vista previa. Si el número parece viejo, añade un parámetro al enlace.
Ejemplo: `https://orgia82.github.io/cuenta-atras/?d=27oct`
