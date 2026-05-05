# Tetris

Tetris clásico en Python con pygame.

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecutar

```bash
python tetris.py
```

## Controles

- ← / → : mover
- ↑ o X : rotar (horario)
- Z : rotar (antihorario)
- ↓ : soft drop
- Espacio : hard drop
- C : hold
- P : pausa
- R : reiniciar

## Características

- 7 tetrominós estándar (I, O, T, S, Z, J, L) con colores clásicos
- Sistema de "bag" 7-piece para reparto justo
- Pieza fantasma (ghost) para previsualizar caída
- Hold, next, scoring (single/double/triple/tetris), niveles y velocidad progresiva
- DAS/ARR para movimiento lateral fluido
- Wall kicks básicos al rotar
