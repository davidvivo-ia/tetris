# ADR 0001 — Capa de presentación: Textual TUI

## Contexto

El programa original es texto puro con `LOCATE` y semigráficos. Las
reglas internas del proyecto dicen: "Si el original es texto puro con
INPUT/PRINT y menús → TUI con Textual".

## Opciones consideradas

1. **CLI Typer + Rich** estática: descartada por incompatible con un
   juego en tiempo real con teclas no bloqueantes.
2. **pygame-ce gráfico**: descartada. El original es texto; saltar a
   sprites traiciona el espíritu y multiplica assets.
3. **Curses puro**: descartada. Textual ofrece exactamente lo mismo con
   layout declarativo, CSS y un ciclo reactivo limpio.
4. **Textual + CSS**: elegida.

## Decisión

Capa de presentación construida con **Textual** (>= 0.85), estilos en
`src/tetris/assets/tetris.tcss`. El renderizado del tablero se hace con
un widget custom que escribe celdas como cadenas de bloques (`██`).

## Consecuencias

- El juego corre dentro de cualquier terminal moderno (≥ 80×24).
- Las animaciones se limitan a lo que el terminal permite (sin
  partículas reales), lo cual encaja con la estética retro.
- Se obtiene navegación por teclado y theming gratis.
- Requiere Python 3.13 y un terminal con buenas capacidades (24-bit
  color recomendado).
