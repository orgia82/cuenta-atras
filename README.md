# Cuenta atrás para WhatsApp

Página estática con una cuenta atrás **en vivo** (días, horas, minutos y segundos).
Se publica en GitHub Pages. Se comparte como enlace en WhatsApp.

## Cómo cambiar el evento

Edita `config.json`:

- `titulo`: nombre del evento.
- `fecha`: fecha en formato `AAAA-MM-DD`.
- `hora`: hora del evento (hora de Madrid).
- `base_url`: dirección de la página en GitHub Pages.

Cada `push` a `main` publica la página de nuevo.

## Cómo funciona

1. `generar.py` crea `dist/index.html` (desde `plantilla.html`) y `dist/cuenta.png`.
2. La página calcula la cuenta atrás en el navegador de cada visitante. Siempre muestra el dato actual.
3. La imagen de vista previa no lleva número. Muestra el título y la fecha.
4. La Action `.github/workflows/diario.yml` publica la carpeta `dist`.

## Prueba en local

    pip install pillow
    python generar.py

## WhatsApp

- La vista previa se guarda en el mensaje cuando alguien lo envía. No se actualiza.
- La página sí se actualiza cuando alguien toca el enlace.
- Un mensaje anclado dura como máximo 30 días.
