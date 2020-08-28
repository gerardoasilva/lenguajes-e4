# Implementación de un parser
# Reconoce expresiones mediante la gramática:
# EXP -> EXP op EXP | EXP -> (EXP) | cte
# la cual fué modificada para eliminar ambigüedad a:
# EXP  -> cte EXP1 | (EXP) EXP1
# EXP1 -> op EXP EXP1 | vacío
# los elementos léxicos (delimitadores, constantes y operadores)
# son reconocidos por el scanner
#
# Autor: Dr. Santiago Conant, Agosto 2014 (modificado Agosto 2015)

import sys
import ejercicio3 as scanner

# Empata y obtiene el siguiente token
def match(tokenEsperado):
    global token
    if token == tokenEsperado:
        token = scanner.ejercicio3()
    else:
        error("token equivocado")

# Función principal: implementa el análisis sintáctico
def parser():
    global token 
    token = scanner.ejercicio3() # inicializa con el primer token
    exp()
    if token == scanner.END:
        print("Expresion bien construida!!")
    else:
        error("expresion mal terminada")

# Módulo que reconoce expresiones
def exp():
    if token == scanner.INT or token == scanner.FLT:
        match(token) # reconoce Constantes
        exp1()
    elif token == scanner.LRP:
        match(token) # reconoce Delimitador (
        exp()
        match(scanner.RRP)
        exp()
        exp1()
    elif token == scanner.OPB:
        match(token) #reconoce operadores
        exp1()
    elif token == scanner.IDE: 
        match(token) #reconoce letras / identif
        exp1()
    else:
        error("expresion mal iniciada")

# Módulo auxiliar para reconocimiento de expresiones
def exp1():
    if token == scanner.OPB:
        match(token) # reconoce operador
        exp2()

# Módulo auxiliar para reconocimiento de expresiones
def exp2():
    if token == scanner.INT:
        match(token)
        exp1()
        exp2()
    elif token == scanner.FLT:
        match(token)
        exp1()
        exp2()
 
# Módulo auxiliar para reconocimiento de regla \var.
def exp3():
    if token == scanner.IDE:
        match(token)
        exp4()

# Módulo auxiliar para reconocimiento de regla \var.
def exp4():
    if token == scanner.IDE:
        match(token)
        exp3()
        exp4()


# Termina con un mensaje de error
def error(mensaje):
    print("ERROR:", mensaje)
    sys.exit(1)
    