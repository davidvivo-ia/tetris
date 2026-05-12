# ADR 0004 — Persistencia local

## Contexto

El original no persistía nada. Cerrar el intérprete eliminaba el récord.

## Opciones consideradas

1. **Sin persistencia**: fiel al original, pero pobre para 2026.
2. **JSON en XDG_DATA_HOME**: ligero, inspeccionable, portable.
3. **SQLite**: sobreingeniería para 10 high scores.

## Decisión

`JsonScoreRepository` persiste en
`${XDG_DATA_HOME:-~/.local/share}/tetris/scores.json`. Formato:

```json
{
  "version": 1,
  "scores": [
    {"name": "AAA", "score": 12345, "lines": 87, "level": 9,
     "played_at": "2026-05-12T10:00:00Z", "seed": 42}
  ]
}
```

Top 10 ordenado descendente.

## Consecuencias

- Mejor experiencia de usuario.
- Cero secretos: archivo plano legible y editable.
- En entornos sin permisos de escritura (CI), el repo cae en modo
  in-memory silencioso.
