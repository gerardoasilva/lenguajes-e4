# A011356536 - Gerardo Silva
# A01570079 - Mónica Nava

# Implementación de un parser
# Reconoce expresiones mediante la gramática:
# ASIG  -> id = EXP
# EXP   -> ARIT | {COND}
# ARIT  -> const ARIT1 | id ARIT1 | (ARIT) ARIT1
# ARIT1 -> op ARIT ARIT1 | vacio
# COND  -> EXP opr EXP ? EXP : EXP
# los elementos léxicos (delimitadores, constantes y operadores)
# son reconocidos por el scanner
#
# Autor: Dr. Santiago Conant, Agosto 2014 (modificado Agosto 2015)

import sys
import a01136536_A01570079_obten_token as scanner

# Empata y obtiene el siguiente token
def match(tokenEsperado):
    global token
    if token == tokenEsperado:
        token = scanner.obten_token()
    else:
        error("token equivocado")

# Función principal: implementa el análisis sintáctico
def parser():
    global token 
    token = scanner.obten_token() # inicializa con el primer token
    asig()
    if token == scanner.END:
        print("Expresion bien construida!!")
    else:
        error("expresion mal terminada")

# # Módulo que reconoce expresiones
def asig():
    if token == scanner.IDE:
        match(token) # reconoce identificador
        match(scanner.OPA) # reconoce operador de =
        exp()
    else:
        error("asignacion mal iniciada")
# Módulo auxiliar para reconocimiento de expresiones
def exp():
    if token == scanner.LRC:
         match(token) # reconoce corchete {
         cond()
         match(scanner.RRC) # reconoce corchete }
    else:
        arit()

# Módulo auxiliar para reconocimiento de expresiones  
def arit():
    if token == scanner.INT or token == scanner.FLT:
        match(token) # reconoce constante
        arit1()
    elif token == scanner.IDE:
        match(token) # reconoce id
        arit1()
    elif token == scanner.LRP:
        match(token) # reconoce delimitador (
        arit()
        match(scanner.RRP) # reconoce delimitador )
        arit1()
    elif token == scanner.LRC:
        match(token) # reconoce delimitador {
        cond()
        match(scanner.RRC)
    else:
        error("expresion aritmetica mal iniciada")

# Módulo auxiliar para reconocimiento de expresiones
def arit1():
    if token == scanner.OPB:
        match(token)
        arit()
        arit1()

# Módulo auxiliar para reconocimiento de expresiones
def cond():
    exp()
    match(scanner.OPR) # reconoce operador relacional
    exp()
    match(scanner.OPC) # reconoce operador condicional ?
    exp()
    match(scanner.OPD) # reconoce operador condicional :
    exp()


# Termina con un mensaje de error
def error(mensaje):
    print("ERROR:", mensaje)
    sys.exit(1)

parser()