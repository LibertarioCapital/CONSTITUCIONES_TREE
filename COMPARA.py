
import sys
from os import listdir
from os.path import isfile, isdir
import os, subprocess

import pandas as pd
import numpy as np


#crea diccionario desde CODIGOS.xls

BASE = pd.read_excel('CODIGOS.xls') 
BASEnp= BASE.to_numpy()
filas,cols = BASEnp.shape

DICC = {' ':'AAA'}

for fila in range(filas):
	DICC[BASEnp[fila][0]] = BASEnp[fila][4]



def LISTADO(path):   #entrega lista de archivos .txt , no 'TRAD_PAIS.txt' 
	return [obj for obj in listdir(path) if isfile(path + obj) and obj[-4:]=='.txt' and obj[:4] != 'TRAD']


def TRADUCE(txt):
	
	txt=txt.lower()
	txt=txt.replace('á','a')
	txt=txt.replace('é','e')
	txt=txt.replace('í','i')
	txt=txt.replace('ó','o')
	txt=txt.replace('ú','u')


	trad=''

	for i in txt:

		try:
			trad += DICC[i]
		except:
			trad += 'TTT'


	return trad




def TRADUCIR(listadi):  #convierte textos 'PAIS.txt' a ADN, 'TRAD_PAIS.txt'

	for archivo in listadi:

		txt = open(archivo,'r').read()
		nombre = archivo[:-4]

		trad = TRADUCE(txt)

		salida = open(f'TRAD_{nombre}.txt','w')

		salida.write(trad)
		print (f'HECHO {nombre}')



path= os.getcwd()+'/'
listadi = LISTADO(path)

#TRADUCIR(listadi)

#-----------------



def LISTADOTRAD(path):    #entrega lista de 'TRAD_PAIS.txt'
	return [obj for obj in listdir(path) if isfile(path + obj) and obj[-4:]=='.txt' and obj[:4] == 'TRAD']


listatrad=LISTADOTRAD(path)


def CREAR_SEQS(listatrad):
	textoSEQ=''
	
	for archiv in listatrad:
		nombre = archiv[:-4]
		txt = open(archiv,'r').read()
		textoSEQ += f'>{nombre} \n'
		textoSEQ += f'{txt} \n\n'
		
	salida=open('SEQSALIDA.txt','w')
	
	salida.write(textoSEQ)
	
	
	
CREAR_SEQS(listatrad)


print ('TERMINE')

