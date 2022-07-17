
import sys
from os import listdir
from os.path import isfile, isdir
import os, subprocess

import pandas as pd
import numpy as np


#CARPETAS ARCHIVOS

CONST='CONSTITUCIONES_TXT/'
CONSTRAD='CONSTITUCIONES_TRAD/'


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
		print (f'CONVIRTIENDO = {CONST}{archivo}')
		
		txt = open(f'{CONST}{archivo}','r').read()
		nombre = archivo[:-4]

		trad = TRADUCE(txt)

		salida = open(f'{CONSTRAD}TRAD_{nombre}.txt','w')

		salida.write(trad)
		print (f'HECHO {nombre}')


def LISTADOTRAD(path):    #entrega lista de 'TRAD_PAIS.txt'
	return [obj for obj in listdir(path) if isfile(path + obj) and obj[-4:]=='.txt' and obj[:4] == 'TRAD']




def CREAR_SEQS(listatrad):
	textoSEQ=''
	
	for archiv in listatrad:
		nombre = archiv[:-4]
		txt = open(archiv,'r').read()
		textoSEQ += f'>{nombre} \n'
		textoSEQ += f'{txt} \n\n'
		
	salida=open('SEQSALIDA.txt','w')
	
	salida.write(textoSEQ)
	
	

def PASO1():
		
	path1= os.getcwd()+'/'+CONST

	print (path1)
	listadi = LISTADO(path1)

	print (listadi)
	TRADUCIR(listadi)


def PASO2():
	path2= os.getcwd()+'/'+CONSTRAD
	print (f'PATH = {path2}')
	
	
	listatrad = LISTADOTRAD(path2)
	print (f' LISTADO TRAD = {listatrad}')


	#CREAR_SEQS(listatrad)
	
	
#PASO1()
PASO2()



print ('TERMINE')

