#A00827826 Edgar Castillo
#A01570852 Luis Martínez

"""
Programa del juego Pacman.
"""
#Librerías
from random import choice
from turtle import *
from freegames import floor, vector

state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)
title = Turtle(visible=False)
aim = vector(5, 0) #Dirección inicial del Pac-Man
pacman = vector(-40, -80) #Posición inicial del Pac-Man

#Estos son los fantasmas, se les añadieron los colores del juego original.
ghosts = [
    [vector(-180, 160), vector(5, 0), 'red'],
    [vector(-180, -160), vector(0, 5), 'light blue'],
    [vector(100, 160), vector(0, -5), 'orange'],
    [vector(100, -160), vector(-5, 0), 'pink']
]

#Este es el tablero propuesto de juego. Ceros son paredes y unos es el camino.
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

def square(x, y):
    #Se dibuja el cuadrado que representa el tablero. Será llamado en world() y move().
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()

def offset(point):
    #Muestra el desplazamiento de uno de los personajes en el tablero.
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

def valid(point):
    """Toda esta función es la que se encarga de determinar en cada
    movimiento de posición si el Pac-Man o algún fantasma puede seguir
    avanzando o no en el mapa. Si se topa con alguna pared o se acaba el
    camino azul en la dirección que lleva, deberá cambiar de dirección.
    Esto último se ve en la función move() y change()."""
    
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0

def world():
    #Se establece que los colores del mapa serán negro y azul.
    bgcolor('black')
    path.color('blue')
    
    """Se crea el tablero de juego. Si es 0, será una pared y si es azul es parte del camino.
    Además, se crea la comida en el camino, con un color blanco y más pequeña a los personajes."""
    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(5, 'white')

def move():
    #Se muestra el marcador.
    writer.undo()
    writer.write('Score: '+ str(state['score']))

    clear()
    #Se mueve el Pac-Man hasta que llegue a una pared.
    if valid(pacman + aim):
        pacman.move(aim)
    
    """Se añaden puntos al marcador conforme pase el Pac-Man
    por encima de la comida."""
    index = offset(pacman)
    
    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow') #Pac-Man será amarillo.

    for point, course, color in ghosts:
        #Se mueve el fantasma hasta que llegue a una pared.
        if valid(point + course):
            point.move(course)
            
            """Todos los movimientos de los fantasmas serán de 10 unidades de paso turtle. Esto hará que vayan más rápido
            que el Pac-Man"""
        else:
            if pacman.x > point.x and pacman.y > point.y:
                """
                Primer caso: Cuando el Pac-Man se encuentra en una posición arriba a la derecha respecto a
                cualquier fantasma. Esto da las opciones de que este último se mueva hacia la derecha o hacia
                arriba.
                """
                options = [
                    vector(10,0),
                    vector(0,10)
                ]
                
            elif pacman.x < point.x and pacman.y > point.y:
                """
                Segundo caso: Cuando el Pac-Man se encuentra en una posición arriba a la izquierda respecto a
                cualquier fantasma. Esto da las opciones de que este último se mueva hacia la izquierda o hacia
                arriba.
                """
                options = [
                    vector(-10,0),
                    vector(0,10)
                ]
            
            elif pacman.x > point.x and pacman.y < point.y:
                """
                Tercer caso: Cuando el Pac-Man se encuentra en una posición abajo a la derecha respecto a
                cualquier fantasma. Esto da las opciones de que este último se mueva hacia la derecha o hacia
                abajo.
                """
                options = [
                    vector(10,0),
                    vector(0,-10)
                ]    
                
            elif pacman.x > point.x and pacman.y > point.y:
                """
                Cuarto caso: Cuando el Pac-Man se encuentra en una posición abajo a la izquierda respecto a
                cualquier fantasma. Esto da las opciones de que este último se mueva hacia la izquierda o hacia
                abajo.
                """
                options = [
                    vector(-10,0),
                    vector(0,-10)
                ]    
                
            elif pacman.x == point.x:
                """
                Quinto caso: Cuando el Pac-Man se encuentra en una posición arriba o abajo pero con el mismo valor
                del eje x respecto a cualquier fantasma. Esto da las opciones de que este último se mueva hacia
                abajo o hacia arriba.
                """
                options = [
                    vector(0,10),
                    vector(0,-10)
                ]    

            elif pacman.y == point.y:
                """
                Sexto caso: Cuando el Pac-Man se encuentra en una posición a la izquierda o derecha pero con el
                mismo valor del eje y respecto a cualquier fantasma. Esto da las opciones de que este último se
                mueva hacia la derecha o hacia la izquierda.
                """
                options = [
                    vector(10,0),
                    vector(-10,0)
                ]
                
            else:
                #Se mantiene el código inicial en el else como última instancia, aunque entre con menos frecuencia en este.
                options = [
                    vector(10, 0),
                    vector(-10, 0),
                    vector(0, 10),
                    vector(0, -10)
                ]
            """Se toma de manera aleatoria alguna de las opciones que existan. Se asigna el movimiento.
            Al ser aleatorio deja posibilidad de que el juego no sea imposible."""
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10) 
        dot(20, color) #Se asigna el tamaño y color a cada fantasma

    update()
    
    #Ciclo for para revisar si el jugador ha perdido o no. Finaliza el juego.
    for point, course, color in ghosts:
        if abs(pacman - point) < 20:
            return
    """
    Llamará la función move cada 100 milisegundos, si se disminuye esta cantidad, el
    juego iría más rápido, pero sería todo el juego (incluidos fantasmas y pacman).
    """
    ontimer(move, 100)
    
def change(x, y):
    #Esta función sirve para mover el pacman con las flechas del teclado.
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

setup(460, 460, 370, 0) #Se amplió un poco la ventana para meter el título del juego a la misma.
hideturtle()
tracer(False)
title.goto(-30,185) #Ubicación del título
title.color('yellow') #Color del título
title.write('Pac-Man', align="center", font = ("Arial",12,"bold")) #Contenido del título, otros detalles del mismo.
writer.goto(130, 160) #Posición del marcador
writer.color('white') #Color del marcador
writer.write(state['score'])
listen()

"""Se observa que el pacman se mueve 5 en unidades de turtle hacia cualquier dirección. Por eso es más lento que los
fantasmas, ya que estos se mueven a velocidad de 10 unidades."""
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()
done()