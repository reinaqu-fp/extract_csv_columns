# -*- coding: utf-8 -*-
'''
Created on 22 oct 2021

@author: Belen Ramos
'''

import csv
import random
import numpy as np
from datetime import datetime, timedelta
from csv_extractor import *


def genera_columnas_csv(fichero_entrada, nuevas_columnas, delimiter=',', encoding='latin-1'):
    '''
        Esta función toma un csv dado como fichero de entrada, un diccionario con la 
        configuración de columnas a añadir, el delimitador con el que se separan los campos
        en el csv original, y la codificación del fichero original, y genera un nuevo
        csv con el mismo nombre que el fichero original, pero acabado en _generated.csv,
        que tiene las columnas del fichero original, más las generadas según la especificación
        dada como parámetro.
        @param fichero_entrada: Nombre y ruta del fichero csv original
        @type fichero_entrada: str
        @param nuevas_columnas: diccionario para especificar el nombre y tipo de cada una 
            de las columnas a añadirle al csv original. La clave del diccionario es
            el nombre de la nueva columna, y el valor otro diccionario para especificar
            el tipo de la nueva columna, y cómo se genera. Un ejemplo de este diccionario es
      
        <code>  
        nuevas_columnas = 
            {'TIENE_MATERNAL': {'type': 'boolean'},
             'NUM_CAMAS_MATERNAL': {'type': 'int', 'range': [0, 25]},
             'MEDIA_OCUPACION_MATERNAL': {'type': 'float', 'range': [1.0, 45.5], 'step': 0.5},
             'RESPONSABLE_REPETICION': {'type': 'str', 'values': ['R1', 'R2', 'R3'], 'randomize': True},
             'RESPONSABLE_SIN_REPETICION': {'type': 'str', 'values': ['R'] * 83, 'randomize': False},
             'FECHA_ULTIMA_REFORMA': {'type': 'datetime', 'range': ['01/01/2020', '31/12/2021'],
                                                  'format': "%d/%m/%Y"}}
        </code>
        
        con este diccionario se especifica lo  que se van a añadir las siguientes columnas:
            * TIENE_MATERNAL, de tipo boolean. Los valores se generarán de forma aleatoria.
            * NUM_CAMAS_MATERNAL, de tipo int. Los valores se generarán de forma aleatoria en el rango de 0 a 25.
            * MEDIA_OCUPACION_MATERNAL, de tipo float. Los valores se generarán de forma aleatoria en el
              rango 1.0, 45.5 con un paso de 0.5
            * RESPONSABLE_REPETICION, de tipo str. Los valores se escogerán de la lista de valores pasada
              como parámetro de forma aleatoria.
            * RESPONSABLE_SIN_REPETICION, de tipo str. Los valores se escogerán de la lista de valores 
              pasada como parámetro.
            * FECHA_ULTIMA_REFORMA: de tipo fechahora. Los valores se generarán en el rango de fechas
              del 1 de enero del 2020 al 31 de diciembre del 2021, y el formato de salida será "%d/%m/%Y"   
          
        @type nuevas_columnas: {str: Any}
        @param delimiter: Delimitador que se usa para separar lo campos en el fichero original
        @type delimiter: str
        @param encoding: Cadena que indica la codificación en la que está el fichero original. Si no se
        especifica, por defecto se supone que el archivo está codificado en latin-1.
        @type encoding: str
    '''

    with open(fichero_entrada, encoding=encoding) as rf:
        lector = csv.DictReader(rf, delimiter=delimiter)
        filas = [l for l in lector]
        for c_nombre, c_caracteristicas in nuevas_columnas.items():
            filas = add_nueva_columna(filas, c_nombre, c_caracteristicas)

        fichero_salida = nombre_fichero_mejorado_salida(fichero_entrada)
        escribe_fichero(fichero_salida, filas, encoding)


def add_nueva_columna(filas, nombre_columna, caracteristicas_columna):
    '''
        Esta función añade al dataset una nueva columna con las características especificadas
        @param filas: las filas del dataset dadas como una lista de diccionarios
        @type filas: [dict]
        @param nombre_columna: nombre de la nueva columna que se añade al dataset original
        @type nombre_columna: str
        @param caracteristicas_columna: diccionario que contiene las características de la nueva columna a generar
        @type caracteristicas_columna: dict

        @return: la lista de filas modificada con la nueva columna añadida
        @rtype: list[dict]
    '''

    if caracteristicas_columna['type'] == 'boolean':

        boolean_muestra = [True, False]
        boolean_lista = np.random.choice(boolean_muestra, size=len(filas))
        filas = modifica_filas(filas, nombre_columna, boolean_lista)

    if caracteristicas_columna['type'] == 'int':
        int_lista = np.random.randint(caracteristicas_columna['range'][0], caracteristicas_columna['range'][1],
                                      len(filas))
        filas = modifica_filas(filas, nombre_columna, int_lista)

    if caracteristicas_columna['type'] == 'float':
        random_float = np.arange(caracteristicas_columna['range'][0], caracteristicas_columna['range'][1],
                                 caracteristicas_columna['step']).round(2)
        float_lista = np.random.choice(random_float, size=len(filas))
        filas = modifica_filas(filas, nombre_columna, float_lista)

    if caracteristicas_columna['type'] == 'str':
        if caracteristicas_columna['randomize']:
            str_lista = np.random.choice(caracteristicas_columna['values'], size=(len(filas)))
            filas = modifica_filas(filas, nombre_columna, str_lista)
        else:
            filas = modifica_filas(filas, nombre_columna, caracteristicas_columna['values'])

    if caracteristicas_columna['type'] == 'datetime':
        fecha1 = datetime.strptime(caracteristicas_columna['range'][0], caracteristicas_columna['format'])
        fecha2 = datetime.strptime(caracteristicas_columna['range'][1], caracteristicas_columna['format'])
        # dias entre las dos fechas
        resta_fechas = fecha2 - fecha1
        dias_totales = resta_fechas.days
        fechas_lista = []
        for idx in range(len(filas)):
            randay = random.randrange(dias_totales)
            fecha_aux = fecha1 + timedelta(days=randay)
            fecha_aux_str = fecha_aux.strftime(caracteristicas_columna['format'])
            fechas_lista.append(fecha_aux_str)

        filas = modifica_filas(filas, nombre_columna, fechas_lista)

    return filas


def modifica_filas(filas, nombre_columna, lista_valores):
    '''
        Esta función añade a cada fila del dataset la nueva columna
        @param filas: las filas del dataset dadas como una lista de diccionarios
        @type filas: [dict]
        @param nombre_columna: nombre de la nueva columna que se añade al dataset original
        @type nombre_columna: str
        @param lista_valores: lista que contiene todos los valores que tomará la nueva columna en cada fila
        @type lista_valores: list

        @return: la lista de filas modificada con la nueva columna añadida
        @rtype: list[dict]
    '''
    for i in range(0, len(filas)):
        filas[i].update({nombre_columna: lista_valores[i]})

    return filas


def escribe_fichero(fichero_salida, filas, encoding):
    with open(fichero_salida, 'w', encoding=encoding, newline='') as wf:
        dict_cabecera = {k: k for k in filas[0].keys()}
        dw = csv.DictWriter(wf, fieldnames=dict_cabecera, quoting=csv.QUOTE_ALL, quotechar='"')
        dw.writeheader()
        for f in filas:
            dw.writerow(f)
    wf.close()


def nombre_fichero_mejorado_salida(fichero_entrada):
    '''
    @param fichero_entrada: Nombre y ruta del fichero csv de entrada.
    @type fichero_entrada: str
    @return: El nombre del fichero de salida que se genera como el nombre del fichero de entrada,
        sin la cadena ".csv" y terminado en "_generated.csv"
    '''
    return fichero_entrada.replace(".csv", "") + "_generated.csv"


def main():
    '''
    Función principal para gestionar la línea de argumentos
    '''
    args = parse_arg()
    logging.basicConfig(level=logging.INFO)

    fichero_entrada = args.input[0]
    fichero_salida = nombre_fichero_mejorado_salida(fichero_entrada)
    encoding = 'utf-8'
    if args.encoding:
        encoding = args.encoding[0]
    logging.info("Escribiendo en ..." + fichero_salida)
    lee_fichero_modifica_dataset(fichero_entrada, args.cols, encoding=encoding)


def parse_arg():
    '''
    @return: Un objeto que define los argumentos que se esperan si se usa este módulo
    desde la linea de comandos
    @rtype: argparse.Namespace
    '''
    descr = 'The result is a new csv with the new columns specified in the argument new_cols'
    parser = argparse.ArgumentParser(prog='csv_improver', description=descr)
    parser.add_argument('-input', nargs=1, type=str, help='Original csv file')
    parser.add_argument('-new_cols', nargs='+', type=str,
                        help='Dictionary with the specifications of the new columns to be added.}')
    parser.add_argument('-encoding', nargs='?',
                        help='If omitted, the default value is utf-8, you can change it to utf-8')
    return parser.parse_args()


if __name__ == "__main__":
    main()
