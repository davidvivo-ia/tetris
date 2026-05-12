# Sistema de diseño

## Concepto

**"Phosphor 2026"**: Tetris con la calidez de un monitor CRT ámbar/verde
de 1986, ejecutado con la nitidez y los microdetalles de una TUI
moderna. Retro en el alma, contemporáneo en la artesanía.

## Paleta

Inspirada en monitores de fósforo verde y ámbar, recortada con acentos
saturados para las piezas (siguiendo la convención Tetris/Sega).

| Rol semántico   | Hex      | Nombre        | Uso                          |
|-----------------|----------|---------------|------------------------------|
| `background`    | `#0B0F0A`| obsidian      | Fondo principal              |
| `surface`       | `#11160F`| forest-ink    | Paneles, tableros            |
| `surface-alt`   | `#1A2018`| moss-ink      | Hover, focus                 |
| `primary`       | `#7FFFB2`| phosphor      | Texto principal, bordes      |
| `accent`        | `#E5C100`| amber         | Score, eventos clave         |
| `muted`         | `#4A5A4A`| ash           | Texto secundario             |
| `success`       | `#7FFFB2`| phosphor      | Mensajes positivos           |
| `warning`       | `#E5C100`| amber         | Avisos, pausa                |
| `danger`        | `#FF5C7A`| neon-rose     | Game over                    |

Colores de piezas (saturados, contrastan sobre `surface`):

| Pieza | Hex      | Nombre         |
|-------|----------|----------------|
| I     | `#5BE7F2`| cyan-ice       |
| O     | `#F5D44A`| sunlit-yellow  |
| T     | `#B271E3`| violet-bloom   |
| S     | `#6BE07F`| spring-green   |
| Z     | `#F26060`| ember-red      |
| J     | `#5C7BFF`| sapphire       |
| L     | `#F08A3A`| ember-orange   |

Contraste de `primary` (`#7FFFB2`) sobre `background` (`#0B0F0A`):
ratio ≈ 14.5:1 (cumple WCAG AAA). Los colores de piezas se usan como
**relleno con borde más claro**, nunca como texto sobre fondo, para no
depender del color como único canal informativo.

## Tipografía

- **UI/mono única**: la fuente del terminal del usuario. Recomendamos
  Nerd Font (FiraCode NF, JetBrains Mono NF) para glifos extras, pero
  no son obligatorios.
- **Jerarquía por peso y caja**:
  - Títulos: mayúsculas, espaciado expandido (e.g. `T E T R I S`).
  - Etiquetas (HUD): mayúsculas, color `muted`.
  - Valores: regular, color `primary` o `accent`.
- **Caracteres de bloque**: `█` `▓` `▒` `░` para gradientes; `┌─┐│└┘`
  para marcos.

## Espaciado

Sistema base **2 celdas de terminal** (≈ 1ch alto/ancho). Distancias
canónicas: 1, 2, 4, 8 celdas. Todo widget se alinea a la rejilla.

Tablero: **20 filas × 10 columnas**; cada celda son **2 caracteres**
(`██`) para acercarse a un cuadrado visual en terminales con celdas
verticales rectangulares.

## Iconografía

Set ASCII custom y emojis monocromos solo cuando aportan claridad:

- `▶` jugar  ·  `⏸` pausa  ·  `⏹` salir
- `◆` tetris  ·  `◇` línea sencilla
- `↑↓←→` controles

## Estados clave

| Estado     | Indicación                                                  |
|------------|-------------------------------------------------------------|
| Splash     | Logo grande "T E T R I S", subtítulo, "Pulsa cualquier tecla"|
| Normal     | Tablero + HUD lateral con NEXT (cola 5), HOLD, score        |
| Pausa      | Overlay traslúcido, texto centrado `▌ PAUSA ▐`              |
| Línea limpiada | Flash 80ms del color de pieza recién bloqueada          |
| Game over  | Overlay rojizo, texto `GAME OVER`, mejor puntuación         |
| Vacío      | Splash si no hay partida activa                             |

## Accesibilidad

- **Navegación por teclado completa**, sin dependencia de ratón.
- Atajos visibles en pantalla en todo momento.
- **No se usa color como único canal**: las piezas tienen además un
  carácter distintivo en su borde y, en modo `--high-contrast`, glifos
  Unicode únicos por tipo.
- Modo claro (`--theme light`) y oscuro (default).
- Animaciones suaves pero deshabilitables con `--no-animations`.

## Toque distintivo

**"Phosphor glow trail"**: cuando una pieza cae con hard drop, deja
durante 120ms una estela tenue (color de pieza al 30% alpha) en las
columnas atravesadas. Sutil, evocador del rasgo persistente del fósforo
de un monitor CRT.

Como cierre estético: el splash hace un breve efecto de "encendido CRT"
de 400ms (línea blanca expandiéndose) y un pitido sintetizado de PC
speaker (si está disponible la salida de audio del terminal).

[LICENCIA CREATIVA] El original no tenía ningún efecto visual. Este toque
se añade como firma de la versión 2026.
