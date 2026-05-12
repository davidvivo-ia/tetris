# ADR 0002 — Modelo de dominio inmutable

## Contexto

El original mantiene un tablero mutable global (`T(20,10)`) y muta `X`,
`Y`, `Q` sobre la pieza activa. Funciona, pero impide testear, deshacer
estados y razonar formalmente.

## Opciones consideradas

1. **Objetos mutables (estilo OOP clásico)**: `Board.move_piece()`. Más
   barato en líneas, peor en testeo.
2. **`dataclass(frozen=True, slots=True)` + reducers puros**:
   transiciones devuelven estados nuevos.
3. **Modelos pydantic en el dominio**: descartado. Pydantic es excelente
   en fronteras IO, pero introduce coste y validación impropia del
   núcleo.

## Decisión

Dominio puro con `dataclass(frozen=True, slots=True)`. Cada acción del
juego es un reducer `(state, action) -> (state', events)`. El tablero
se modela como `tuple[tuple[TetrominoKind | None, ...], ...]`.

## Consecuencias

- Tests triviales y deterministas, sin mocks.
- Replays gratis (lista de acciones + seed = partida exacta).
- Sobrecoste de memoria despreciable (10×20 celdas).
- El reducer concentra la lógica; debe quedar legible y bien dividido en
  helpers privados.
