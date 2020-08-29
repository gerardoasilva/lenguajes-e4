# A011356536 - Gerardo Silva
# A01570079 - Mónica Nava

# Implementación de un scanner mediante la codificación de un Autómata
# Finito Determinista como una Matríz de Transiciones
# Autor: Dr. Santiago Conant, Agosto 2014 (modificado en Agosto 2015)

import sys

# tokens
INT = 100  # Número entero
FLT = 101  # Número de punto flotante
OPB = 102  # Operador binario
LRP = 103  # Delimitador: paréntesis (
RRP = 104  # Delimitador: paréntesis )
END = 105  # Fin de la entrada
OPA = 106  # Operador asignación
OPC = 107  # Operador condicional ?
OPD = 108  # Operador condicional :
OPR = 109  # Operador relacional
IDE = 110  # Identificador
LRC = 111  # Delimitador: corchete {
RRC = 112  # Delimitador: corchete }
ERR = 200  # Error léxico: palabra desconocida

# Matriz de transiciones: codificación del AFD
# [renglón, columna] = [estado no final, transición]
# Estados > 99 son finales (ACEPTORES)
# Caso especial: Estado 200 = ERROR
#      dig   op   (    )  raro  esp  .   $    =   ?     :   ><    !   ID    {    }
MT = [[  1, OPB, LRP, RRP,   4,   0, 4, END,   5, OPC, OPD,   7,   9,  10, LRC, RRC], # edo 0 - estado inicial
      [  1, INT, INT, INT, INT, INT, 2, INT, INT, INT, INT, INT, INT, INT, ERR, INT], # edo 1 - dígitos enteros
      [  3, ERR, ERR, ERR,   4, ERR, 4, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR], # edo 2 - primer decimal flotante
      [  3, FLT, FLT, FLT, FLT, FLT, 4, FLT, FLT, FLT, FLT, FLT, FLT, FLT, ERR, FLT], # edo 3 - decimales restantes flotante
      [ERR, ERR, ERR, ERR,   4, ERR, 4, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR], # edo 4 - estado de error
      [OPA, ERR, OPA, ERR,   4, OPA, 4, ERR,   6, ERR, ERR, ERR, ERR, OPA, OPA, ERR], # edo 5 - primer signo de igual
      [OPR, ERR, OPR, ERR,   4, OPR, 4, ERR, ERR, ERR, ERR, ERR, ERR, OPR, OPA, ERR], # edo 6 - segundo signo de igual
      [OPR, ERR, OPR, ERR,   4, OPR, 4, ERR,   8, ERR, ERR, ERR, ERR, OPR, OPR, ERR], # edo 7 - primer operador relacional
      [OPR, ERR, OPR, ERR,   4, OPR, 4, ERR, ERR, ERR, ERR, ERR, ERR, OPR, OPR, ERR], # edo 8 - segundo operador relacional
      [ERR, ERR, ERR, ERR,   4, ERR, 4, ERR, OPR, ERR, ERR, ERR, ERR, ERR, ERR, ERR], # edo 9 - operador relacional !
      [ERR, IDE, IDE, IDE,   4, IDE, 4, IDE, IDE, IDE, IDE, IDE, IDE,  10, ERR, IDE]] # edo 10 - identidicador


# Filtro de caracteres: regresa el número de columna de la matriz de transiciones
# de acuerdo al caracter dado
def filtro(c):
    """Regresa el número de columna asociado al tipo de caracter dado(c)"""
    if c == '0' or c == '1' or c == '2' or \
       c == '3' or c == '4' or c == '5' or \
       c == '6' or c == '7' or c == '8' or c == '9': # dígitos
        return 0
    elif c == '+' or c == '-' or c == '*' or \
         c == '/': # operadores
        return 1
    elif c == '(': # delimitador (
        return 2
    elif c == ')': # delimitador )
        return 3
    elif c == ' ' or ord(c) == 9 or ord(c) == 10 or ord(c) == 13: # blancos
        return 5
    elif c == '.': # punto
        return 6
    elif c == '$': # fin de entrada
        return 7
    elif c == '=': # igual
        return 8
    elif c == '?': # operador condicional ?
        return 9
    elif c == ':': # operador condicional :
        return 10
    elif c == '<' or c == '>': # operadores relacionales
        return 11
    elif c == '!': # operador relacional !
        return 12
    elif ord(c) >= 97 and ord(c) <= 122: # letras
        return 13
    elif c == '{':
        return 14
    elif c == '}':
        return 15
    else: # caracter raro
        return 4

_c = None   # siguiente caracter
_leer = True # indica si se requiere leer un caracter de la entradaestandar

# Función principal: implementa el análisis léxico
def obten_token():
    """Implementa un analizador léxico: lee los caracteres de la entrada estándar"""
    global _c, _leer
    edo = 0 # número de estado en el autómata
    lexema = "" # palabra que genera el token
    while (True):
        while edo < 100:    # mientras el estado no sea ACEPTOR ni ERROR
            if _leer: _c = sys.stdin.read(1)
            else: _leer = True
            edo = MT[edo][filtro(_c)]
            if edo < 100 and edo != 0: lexema += _c
        if edo == INT:    
            _leer = False # ya se leyó el siguiente caracter
            print("Entero", lexema)
            return INT
        elif edo == FLT:   
            _leer = False # ya se leyó el siguiente caracter
            print("Flotante", lexema)
            return FLT
        elif edo == OPB:   
            lexema += _c  # el último caracter forma el lexema
            print("Operador", lexema)
            return OPB
        elif edo == LRP:   
            lexema += _c  # el último caracter forma el lexema
            print("Delimitador", lexema)
            return LRP
        elif edo == RRP:  
            lexema += _c  # el último caracter forma el lexema
            print("Delimitador", lexema)
            return RRP
        elif edo == OPA:
            _leer = False # ya se leyó el siguiente caracter
            print("Operador asignación", lexema)
            return OPA
        elif edo == OPC:
            lexema += _c  # el último dígito forma el lexema
            print("Operador condicional", lexema)   
            return OPC 
        elif edo == OPD:
            lexema += _c  # el último dígito forma el lexema
            print("Operador condicional", lexema)  
            return OPD
        elif edo == OPR:
            lexema += _c  # el último dígito forma el lexema
            print("Operador relacional", lexema)
            return OPR
        elif edo == IDE:
            _leer = False # ya se leyó el último dígito
            print("Identificador", lexema)
            return IDE
        elif edo == LRC:
            lexema += _c  # el ultimo caracter forma el lexema
            print("Delimitador", lexema)
            return LRC
        elif edo == RRC:
            lexema += _c # el ultimo caracter forma el lexema
            print("Delimitador", lexema)
            return RRC
        elif edo == ERR:   
            _leer = False # el último caracter no es raro
            print("ERROR! palabra ilegal", lexema)
            return ERR
        elif edo == END:
            print("Fin de expresion")
            return END
        else:   
            _leer = False # el último caracter no es raro
            print("ERROR! palabra ilegal", lexema)
            return ERR