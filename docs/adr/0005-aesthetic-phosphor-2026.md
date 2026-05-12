# ADR 0005 — Estética "Phosphor 2026"

## Contexto

El original es texto plano con `[]` y `. `. Funcional pero anodino. El
brief pide "un toque distintivo memorable".

## Opciones consideradas

1. **Moderno plano (flat dark UI)**: limpio pero sin alma.
2. **Retro estricto (PETSCII fielmente)**: pintoresco, pero recorta
   accesibilidad y choca con terminales modernas.
3. **Fusión moderna-retro ("Phosphor 2026")**: paleta de monitor de
   fósforo verde como base, acentos saturados Tetris, microefectos
   (flash, glow trail). Es la opción por defecto del brief.

## Decisión

Fusión moderna-retro. Paleta y tipografía detalladas en `docs/design.md`.
Tres efectos distintivos:

1. Splash con "encendido CRT" (línea blanca expandiéndose, 400ms).
2. Flash 80ms en color de pieza al fijar líneas.
3. "Phosphor glow trail" durante 120ms al hard drop.

Todos deshabilitables con `--no-animations`.

## Consecuencias

- Aporta carácter sin entorpecer el juego.
- Compatible con cualquier terminal 24-bit. En terminales 16-color, los
  efectos degradan a la paleta más cercana (Textual lo gestiona).
- [LICENCIA CREATIVA] respecto al original.
