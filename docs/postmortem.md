# Postmortem

40 años separan `legacy/TETRIS.BAS` de este `src/tetris/`. Mismo juego,
otro oficio.

**Lo que se ganó.** Aislar el dominio en `dataclass(frozen=True,
slots=True)` y un reducer puro `step(state, action) -> (state, events)`
hace que cada regla del juego sea testeable sin pantalla, sin tiempo y
sin RNG. Las pruebas basadas en propiedades (Hypothesis) verifican
invariantes que un humano no se habría planteado en 1986: que la pieza
siempre cabe, que la puntuación es monótona, que las dimensiones del
tablero no cambian. La gravedad ya no es un `FOR W=1 TO 5` dependiente
del intérprete, sino una función del nivel y de un reloj inyectado, lo
que vuelve el modo `--demo --seed 42` 100 % reproducible y permite
correr smoke tests en CI sin TTY. El tipado estricto, el lint
implacable y la cobertura del 94 % cierran el círculo: la versión
moderna es modificable con confianza.

**Lo que se perdió.** Que el listado original cupiese íntegro en una
revista de dos páginas. Tecleabas, ejecutabas, jugabas. Aquí necesitas
`uv`, Python 3.13, un terminal con 24-bit color, un paquete de docs y
diez ADRs para entender una decisión de diseño. La inmediatez
artesanal — abrir el ordenador, escribir, ver el cursor parpadear y la
pieza caer — ha sido reemplazada por una cadena de abstracciones que
solo paga su deuda en proyectos grandes. Para "hacer Tetris" puede
sobrar; para entregarlo a 2026 hace falta.

**Lo que dice del oficio.** Hemos cambiado el coraje de tirar líneas
de BASIC al estilo *ahora-veremos* por la disciplina de garantizar que
nada se rompa. Hemos cambiado la pantalla CRT ámbar por terminales con
24-bit color y CSS propio. Y hemos cambiado al lector solitario de la
revista por un equipo que necesita ADRs para no repetirse las decisiones.
La esencia — siete piezas, gravedad, líneas que desaparecen — no ha
cambiado. Probablemente sea lo mejor que se puede decir del oficio:
sigue habiendo gente que disfruta resolviendo los mismos problemas con
herramientas nuevas.
