import curses, random

ANCHO = 41   # columnas (más grande = más confuso)
ALTO = 21    # filas

# Generar laberinto lleno de paredes
laberinto = [[1 for _ in range(ANCHO)] for _ in range(ALTO)]

def generar(x, y):
    direcciones = [(0,-2),(0,2),(-2,0),(2,0)]
    random.shuffle(direcciones)
    for dx, dy in direcciones:
        nx, ny = x+dx, y+dy
        if 1 <= nx < ANCHO-1 and 1 <= ny < ALTO-1 and laberinto[ny][nx] == 1:
            laberinto[ny][nx] = 0
            laberinto[y+dy//2][x+dx//2] = 0
            generar(nx, ny)

# Crear caminos
laberinto[1][1] = 0
generar(1,1)

jugador_x, jugador_y = 1, 1
salida_x, salida_y = ANCHO-2, ALTO-2

def dibujar(stdscr):
    stdscr.clear()
    alto, ancho = stdscr.getmaxyx()
    offset_y = (alto - ALTO) // 2
    offset_x = (ancho - ANCHO) // 2

    for y, fila in enumerate(laberinto):
        linea = ""
        for x, celda in enumerate(fila):
            if x == jugador_x and y == jugador_y:
                linea += "O"
            elif x == salida_x and y == salida_y:
                linea += "X"
            elif celda == 1:
                linea += "l"
            else:
                linea += " "
        stdscr.addstr(offset_y + y, offset_x, linea)
    stdscr.refresh()

def main(stdscr):
    global jugador_x, jugador_y
    curses.curs_set(0)
    while True:
        dibujar(stdscr)
        if jugador_x == salida_x and jugador_y == salida_y:
            stdscr.addstr(ALTO+2, 0, "¡Has escapado del Lostyx Aleatorio y SúperGrande!")
            stdscr.refresh()
            stdscr.getch()
            break

        tecla = stdscr.getch()
        if tecla in [ord("w"), curses.KEY_UP] and laberinto[jugador_y-1][jugador_x] == 0:
            jugador_y -= 1
        elif tecla in [ord("s"), curses.KEY_DOWN] and laberinto[jugador_y+1][jugador_x] == 0:
            jugador_y += 1
        elif tecla in [ord("a"), curses.KEY_LEFT] and laberinto[jugador_y][jugador_x-1] == 0:
            jugador_x -= 1
        elif tecla in [ord("d"), curses.KEY_RIGHT] and laberinto[jugador_y][jugador_x+1] == 0:
            jugador_x += 1

curses.wrapper(main)

