# ADR 0003 — RNG inyectable con 7-bag

## Contexto

El original usa `RND(1)` uniforme, semilla `RANDOMIZE TIMER`. Genera
secuencias horribles ("4 Z seguidas") y no es reproducible.

## Opciones consideradas

1. **Mantener uniforme + semilla**: poco fiel al Tetris moderno.
2. **7-bag (Tetris Guideline)**: cada bolsa contiene exactamente las 7
   piezas en orden aleatorio. Garantiza diversidad y previene
   "sequías" largas.
3. **Random bag de 14**: variante usada por NES Tetris. Más espera entre
   piezas concretas.

## Decisión

`SevenBagRandom`, implementación de `RandomSource` (Protocol) en
`application/protocols.py`. Acepta `seed: int | None` por constructor;
si es `None` usa `secrets.randbits(63)` y lo registra en logs para que
sea recuperable.

## Consecuencias

- Modo `--seed N` reproducible 100%.
- Modo `--demo` viable: con seed fija + secuencia de acciones fija, la
  partida es bit-a-bit reproducible.
- [LICENCIA CREATIVA] respecto al original, que es uniforme puro.
