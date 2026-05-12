# Análisis del programa original

## Encuadre

- **Artefacto**: `legacy/TETRIS.BAS`, atribuido a "M. Pérez, Madrid, junio
  1986".
- **Lenguaje**: BASIC, dialecto Microsoft-compatible (MSX-BASIC /
  Locomotive BASIC / GW-BASIC). Usa `LOCATE`, `INKEY$`, `RND(1)`,
  `RANDOMIZE TIMER`, `MOD`, `DATA/READ`, `CHR$/ASC`.
- **Plataforma probable**: MSX-1 de 32K o Amstrad CPC. Pantalla de 80×24
  asumida; tablero pintado en columnas pares (`LOCATE I, J*2`) para
  semigráfico cuadrado con `[]` y `. `.
- **Año / contexto**: 1986. Dos años después del Tetris original de
  Pajitnov (Electronika 60, junio 1984). En España el dialecto BASIC en
  micros domésticos era omnipresente; las revistas (MicroHobby, Input
  Sinclair, MSX Club) publicaban listados que se tecleaban a mano.
- **Sinopsis funcional**: Tetris clásico de 10×20, siete piezas con
  rotaciones precomputadas en `DATA`, puntuación BPS escala Nintendo,
  niveles cada 10 líneas que aceleran la caída. Hard drop con espacio,
  soft drop con `K`, rotación monodireccional con `I`. Sin hold, sin
  preview de siguiente pieza, sin wall kicks, sin SRS.
- **Estado**: programa autónomo, monolito de ~210 líneas, sin
  dependencias externas. RNG sembrado por `TIMER` (no reproducible).

[SUPUESTO] El brief de `CLAUDE.md` referencia `legacy/`, que el
repositorio no contenía al iniciar la tarea. Se construyó este artefacto
como representante plausible y fiel al género/era para que el ejercicio
arqueológico tenga sustrato real. La lógica imita decisiones típicas de
listados de revista: `GOSUB` para todo, variables de dos letras,
puntuación BPS, etiquetas perezosas en `DATA`.

## Lectura crítica (mirada de 2026)

- **Idiomático para 1986**, pero hoy ilegible: numeración de líneas,
  `GOTO/GOSUB`, mutación global, sin separación de responsabilidades.
- **Acoplamiento total** entre lógica y presentación: cada movimiento
  pinta directamente con `LOCATE`/`PRINT`. Probar la mecánica sin
  pantalla es imposible.
- **RNG no inyectado** (`RND(1)` global). Imposible reproducir
  partidas.
- **Sin estructuras de datos** propias: matrices `DIM` y números mágicos
  por todas partes (1..7 = color).
- **Rotación naïve**: las 4 rotaciones se almacenan precomputadas. No
  hay wall kicks: la pieza simplemente no rota si colisiona. La pieza
  I, en particular, sufre.
- **DAS/ARR inexistente**: pulsar y mantener no auto-repite.
- **Falta accesibilidad**: sin colores diferenciados (todo `[]`), sin
  configuración de teclas, sin pausa.

---

## Grafo de flujo (Fase 1)

```
                          INICIO
                            |
                            v
             +--------------+--------------+
             |  GOSUB 2000  (cargar SH)    |
             +--------------+--------------+
                            |
                            v
                  RANDOMIZE TIMER, init T()
                            |
                            v
                  GOSUB 3000  (panel)
                            |
                            v
                  GOSUB 2500  (forma -> P)
                            |
                            v
                  GOSUB 4000  (pintar)
                            |
   +----------------------->+
   |                        |
   |                        v
   |              GOSUB 5000 (INKEY$)
   |                        |
   |        +---------------+----------------+
   |        | J/L: GOSUB 6000 (mover)        |
   |        | K  : GOSUB 6500 (soft drop)    |
   |        | I  : GOSUB 7000 (rotar)        |
   |        | SP : GOSUB 7500 (hard drop)    |
   |        | Q  : -> 9000  FIN              |
   |        +---------------+----------------+
   |                        |
   |                        v
   |                TC = TC + 1
   |                        |
   |              TC < DL ? --sí--> back to 300
   |                        | no
   |                        v
   |             GOSUB 6000 con DY=1
   |                        |
   |               FX == 0 ? ---no--> back to 300
   |                        | sí (chocó)
   |                        v
   |             GOSUB 8000 (fijar)
   |                        |
   |             GOSUB 8500 (líneas)
   |                        |
   |             GOSUB 8800 (nueva)
   |                        |
   |               GO == 1 ? --sí--> 9000 FIN
   +------------------------+ no
```

`6000` (mover) usa el patrón clásico: borra, mueve, comprueba, si choca
revierte y repinta. `7000` (rotar) hace lo mismo con `Q`.

## Inventario de variables

| Var      | Rol                                            |
|----------|------------------------------------------------|
| `T(20,10)` | Tablero. Fila 1 arriba, 20 abajo.            |
| `P(4,4)`   | Pieza activa expandida.                       |
| `F(4,4)`   | DIMmed pero **sin uso** (residuo).            |
| `SH(7,4,4,4)` | Catálogo: 7 piezas × 4 rotaciones × 4×4.   |
| `K`        | Índice de pieza (1..7).                       |
| `Q`        | Rotación actual (0..3).                       |
| `X,Y`      | Esquina superior-izquierda en tablero.        |
| `DX,DY`    | Delta de movimiento.                          |
| `FX`       | Flag: 1 si el último movimiento tuvo éxito.   |
| `CL`       | Flag: 1 si hay colisión.                      |
| `GO`       | Flag: 1 si game over al spawn.                |
| `PT,LN,NV` | Puntos, líneas, nivel.                        |
| `DL,TC`    | Velocidad y contador (gravedad por iteración).|
| `NL`       | Líneas borradas en último lock.               |
| `HD`       | Celdas caídas en hard drop.                   |
| `A$`       | Tecla leída.                                  |
| `I,J,II`   | Índices de bucle.                             |
| `RR,CC`    | Coords absolutas auxiliares.                  |
| `W`        | Bucle vacío de "pausa".                       |

## Inventario de subrutinas

| Línea | Función                                          |
|-------|--------------------------------------------------|
| 2000  | Carga `SH` desde bloques `DATA`.                 |
| 2500  | Copia `SH(K,Q+1,*,*)` en `P(*,*)`.               |
| 3000  | Pinta panel lateral estático.                    |
| 3200  | Actualiza marcadores PT/LN/NV.                   |
| 4000  | Repinta tablero entero + pieza.                  |
| 4500  | Pinta pieza en posición actual.                  |
| 4600  | Borra pieza en posición actual.                  |
| 5000  | Lee `INKEY$` y normaliza a mayúsculas.           |
| 6000  | Mueve pieza `(DX,DY)`, revierte si colisiona.    |
| 6500  | Soft drop (1 fila, +1 punto si éxito).           |
| 6800  | Comprueba colisión de `P` en `(X,Y)`.            |
| 7000  | Rota (sin wall kicks).                           |
| 7500  | Hard drop, +2 puntos por celda.                  |
| 8000  | Fija pieza en `T`.                               |
| 8500  | Detecta y borra filas completas, puntúa.         |
| 8800  | Genera nueva pieza, detecta game over.           |
| 9000  | Pantalla de fin.                                 |

## IO y dispositivos

- **Pantalla**: modo texto 80×24, semigráfico con `[]` y `. `. Sin
  color: el campo `T(I,J)` guarda 1..7 pero el pintado sólo distingue
  vacío/lleno.
- **Teclado**: `INKEY$`, no bloqueante; flechas como `CHR$(28..31)` o
  J/I/K/L vi-style; espacio para hard drop; `Q` para salir.
- **Reloj**: `RANDOMIZE TIMER` (semilla impredecible).
- **Pausa de bucle**: `FOR W=1 TO 5 : NEXT W` como timer crudo. La
  velocidad real depende del intérprete.

## Algoritmos identificados

1. **Rotación por tabla**: las 4 orientaciones precomputadas. Trivial y
   correcto, pero impide kicks.
2. **Colisión por barrido 4×4**: itera sobre `P(i,j)`, mapea a `(Y+i-1,
   X+j-1)` y comprueba bordes y `T`.
3. **Move/test/revert**: el patrón clásico de aplicar, comprobar y
   deshacer.
4. **Limpieza de líneas top-down con copia**: barre de abajo a arriba;
   cuando borra, copia filas superiores y vuelve a procesar la fila
   (`I = I + 1` justo antes de `NEXT I`, hack típico).
5. **RNG uniforme** sobre 7 piezas (no bag).
6. **Curva de velocidad lineal**: `DL = 30 - NV*2`, suelo `4`.
7. **Puntuación BPS escala Nintendo**: 40/100/300/1200 × nivel.

## Bugs y rarezas detectados

- **B1**: `DIM F(4,4)` se reserva pero `F` nunca se usa. Residuo de
  refactor.
- **B2**: el contador de gravedad (`TC`/`FOR W=1 TO 5`) es dependiente
  del intérprete, no del tiempo real.
- **B3**: el "spawn" en `X=4, Y=1` no comprueba si la pieza I (que en
  rotación 0 ocupa la fila 2 del bbox) cabe. Funciona por accidente.
- **B4**: el `I = I + 1` dentro del bucle `FOR I=20 TO 1 STEP -1` para
  re-evaluar fila tras compactar es legal en BASIC clásico pero
  frágil; si dos líneas adyacentes están completas el comportamiento
  depende de la implementación de `FOR`.
- **B5**: la rotación no aplica wall kicks; la pieza I pegada al borde
  no rota.
- **B6**: el repintado completo (`GOSUB 4000`) tras cada limpieza
  produce parpadeo. La presentación moderna debe evitarlo.
- **B7**: sin DAS/ARR: mantener pulsada una flecha no autorrepite.
- **B8**: sin preview de "next", sin hold.
- **B9**: la pieza S/Z en rotación 1 introduce un offset visual extraño
  (la rotación tabulada empieza en columna 0 en lugar de 1).

## Bugs corregidos en la versión moderna

- **B2, B7**: gravedad y autorrepetición se rehacen sobre reloj real
  (segundos) con DAS/ARR configurables.
- **B5**: se añade un sistema de kicks tipo SRS-básico (offsets
  `0, -1, +1, -2, +2`). [LICENCIA CREATIVA]
- **B6**: la presentación moderna pinta sólo deltas (Textual reactive).
- **B8**: añadidos preview "Next" (cola de 5) y "Hold". [LICENCIA
  CREATIVA]
- **B1**: eliminado.
- **B4**: la limpieza moderna construye una lista nueva (filtrado +
  rellenado) sin reentrada.
- **B9**: las formas se reescriben centradas, evitando offsets.
