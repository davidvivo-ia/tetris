# TODO — v1.1 y más allá

Aplazado conscientemente para mantener el alcance de v1.0.

## Limitaciones conocidas v1.0

- **Sonido**: la TUI no emite audio. El "beep PC-speaker sintetizado"
  prometido en `docs/design.md` requiere acceso al audio del terminal,
  que Textual no expone uniformemente. Aplazado a v1.1 con `numpy` +
  `simpleaudio`.
- **DAS/ARR manual**: actualmente se delega al auto-repeat del terminal.
  Implementar DAS/ARR propio daría sensación competitiva.
- **Flash al limpiar líneas**: previsto en `docs/design.md` (80 ms en
  color de pieza). No implementado en v1.0; el render reactivo de
  Textual no parpadea, pero falta la animación distintiva.
- **Phosphor glow trail**: el efecto durante el hard drop está descrito
  en el sistema de diseño pero no implementado. Requiere overlay
  temporal de 120 ms.
- **Splash de encendido CRT**: la animación de 400 ms al arrancar no
  está; arranca directamente en la pantalla de juego.
- **Sin pantalla de high scores**: la persistencia funciona y se cubre
  con tests, pero la UI no la muestra. Falta vista + flujo de entrada
  de nombre al game over.

## Mejoras priorizadas para v1.1

1. **Animaciones**: flash de líneas + glow trail + splash CRT.
2. **UI de high scores**: pantalla dedicada, ingreso de nombre.
3. **DAS/ARR propios** con configurables `--das-ms`, `--arr-ms`.
4. **Modo "marathon" / "sprint"**: 40 líneas a contrarreloj.
5. **Tema claro accesible** (`--theme light`) con paleta WCAG AA.

## Mejoras técnicas

- **Snapshots de la TUI** con `textual-dev` para regresión visual.
- **Replay**: grabar acciones + seed para reproducir partidas.
- **Configuración de teclas** vía `~/.config/tetris/keybindings.toml`.
- **Localización**: actualmente español; el dominio ya está en inglés.
