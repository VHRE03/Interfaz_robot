import array
from ast import Index
from glob import glob
import string
from cairo import Matrix
from requests import post
import serial
import eel

from cmath import cos, sin
import math
import numpy as np

puerto_encontrado = False
puerto = ''
velocida = ''

for i in range(0,4):
    try:
        puerto = '/dev/ttyACM' + str(i)
        velocidad = '9600'
        Arduino = serial.Serial(puerto,velocidad)

        puerto_encontrado = True

        break
    except:
        pass

if puerto_encontrado == True:
    print('el puerto arduino es: ' + puerto)
else:
    print('No se ha encontrado Arduino')

@eel.expose
def movimiento(motor, direccion, pulsos):
    print(motor)
    print(direccion)
    print(pulsos)
    movimiento = str(motor) + str(direccion) + str(pulsos)
    print(movimiento)

    Arduino.write(movimiento.encode('ascii'))

#MODELO DIRECTO
sind = lambda degrees: float(np.sin(np.deg2rad(degrees)))
s = sind

cosd = lambda degrees: float(np.cos(np.deg2rad(degrees)))
c = cosd

@eel.expose
def modelo_directo(theta,d,a,alpha,num_matriz):
    theta = float(theta)
    d = float(d)
    a = float(a)
    alpha = float(alpha)
    num_matriz = int(num_matriz)

    x11 = c(theta)
    x12 = -s(theta)*c(alpha)
    x13 = s(theta)*s(alpha)
    x14 = a*c(theta)

    y11 = s(theta)
    y12 = c(alpha)*c(theta)
    y13 = -c(theta)*s(alpha)
    y14 = a*s(theta)

    z11 = 0
    z12 = s(alpha)
    z13 = c(alpha)
    z14 = d

    w11 = 0
    w12 = 0
    w13 = 0
    w14 = 1

    matriz = [[x11,x12,x13, x14],
              [y11,y12,y13,y14],
              [z11,z12,z13,z14],
              [w11,w12,w13,w14]]

    if(num_matriz == 1):
        global A
        A = matriz
    elif(num_matriz == 2):
        global B
        B = matriz
    elif(num_matriz == 3):
        global C
        C = matriz
    elif(num_matriz == 4):
        global D
        D = matriz
       
    eel.mostrar_matriz(matriz, num_matriz)

    matrizlen = len(matriz)
    for i in range(matrizlen):
        print(matriz[i])

    return matriz

@eel.expose
def matriz_t():
    ab = producto_matrices(A,B)
    abc = producto_matrices(ab,C)
    abcd = producto_matrices(abc,D)
    resultado = abcd
    eel.mostrar_matriz(resultado,int(5))

#CREDITOS A QUIEN CONRRESPONDA
def producto_matrices(a, b):
    filas_a = len(a)
    filas_b = len(b)
    columnas_a = len(a[0])
    columnas_b = len(b[0])
    if columnas_a != filas_b:
        return None
    # Asignar espacio al producto. Es decir, rellenar con "espacios vacíos"
    producto = []
    for i in range(filas_b):
        producto.append([])
        for j in range(columnas_b):
            producto[i].append(None)
    # Rellenar el producto
    for c in range(columnas_b):
        for i in range(filas_a):
            suma = 0
            for j in range(columnas_a):
                suma += a[i][j]*b[j][c]
            producto[i][c] = suma
    return producto

#MOVIMIENTO DE MOTORES
pos_mot1 = 0
pos_mot2 = 0
pos_mot3 = 0
pos_mot4 = 0

@eel.expose
def grados_pulsos(entrada, mot, pul, limite):

    entrada = float(entrada)

    global pos_mot1
    global pos_mot2
    global pos_mot3
    global pos_mot4

    if(mot == 1 and entrada != pos_mot1):
        aux = entrada
        entrada = entrada - float(pos_mot1)
        pos_mot1 = aux
        print(pos_mot1)
        print(entrada)
    elif(mot == 2 and entrada != pos_mot2):
        aux = entrada
        entrada = entrada - float(pos_mot2)
        pos_mot2 = aux
        print(pos_mot2)
        print(entrada)
    elif(mot == 3 and entrada != pos_mot3):
        aux = entrada
        entrada = entrada - float(pos_mot3)
        pos_mot3 = aux
        print(pos_mot3)
        print(entrada)
    elif(mot == 4 and entrada != pos_mot4):
        aux = entrada
        entrada = entrada - float(pos_mot4)
        pos_mot4 = aux
        print(pos_mot4)
        print(entrada)
    else:
        return

    '''
    if(entrada != pos_mot1):
        aux = entrada
        entrada = entrada - float(pos_mot1)
        pos_mot1 = aux
        print(pos_mot1)
        print(entrada)
    else:
        return
    '''
    pulsos = (entrada * int(pul)) / int(limite)

    if(pulsos == 0):
        entrada = pos_mot1 * -1
        pulsos = (entrada * int(pul)) / int(limite)

    if(entrada < 0):
        dir = "i"
        pulsos = pulsos * -1
        if(str(mot) == "3"):
            print("motor 3")
            pulsos = pulsos - 1

        if(str(mot) == "2"):
            pulsos = pulsos + 70

    else:
        dir = "d"

    movimiento = str(mot) + str(dir) + str(int(pulsos))
    print(movimiento)

    Arduino.write(movimiento.encode('ascii'))
    
    finalizar = Arduino.read()
    print(finalizar)

    if(finalizar):
        return

@eel.expose
def elemeto_terminal(dir):
    if(dir == "A"):
        movimiento = str(5) + str("d") + str(15)
        Arduino.write(movimiento.encode('ascii'))
    elif(dir == "C"):
        movimiento = str(5) + str("i") + str(15)
        Arduino.write(movimiento.encode('ascii'))

eel.init('Web')
eel.start('Index.html')