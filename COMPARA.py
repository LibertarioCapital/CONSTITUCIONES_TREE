
import sys
from os import listdir
from os.path import isfile, isdir
import os, subprocess

import pandas as pd
import numpy as np


#CARPETAS ARCHIVOS

CONST='CONSTITUCIONES_TXT/'
CONSTRAD='CONSTITUCIONES_TRAD/'
CONSTFASTA='CONSTITUCIONES_FASTA/'
CONSTNUBE='CONSTITUCIONES_NUBE/'


#crea diccionario desde CODIGOS.xls

BASE = pd.read_excel('CODIGOS.xls') 
BASEnp= BASE.to_numpy()
filas,cols = BASEnp.shape


#crea diccionario 
DICC = {' ':'AAA'}
for fila in range(filas):
	DICC[BASEnp[fila][0]] = BASEnp[fila][4]



def LISTADO(path):   #entrega lista de archivos .txt , no 'TRAD_PAIS.txt' 
	return [obj for obj in listdir(path) if isfile(path + obj) and obj[-4:]=='.txt' and obj[:4] != 'TRAD']


def SIMPLIFICA(txt):
	txt=txt.lower()
	txt=txt.replace('á','a')
	txt=txt.replace('é','e')
	txt=txt.replace('í','i')
	txt=txt.replace('ó','o')
	txt=txt.replace('ú','u')
	txt=txt.replace(',',' ')
	txt=txt.replace('.',' ')
	txt=txt.replace(';',' ')
	
	return txt
	

def TRADUCE(txt):
	
	txt=SIMPLIFICA(txt)
	
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
	


def FRECUENCIA(palabra,text):
		
	#text = open(f'{archivo}','r').read()
	text=SIMPLIFICA(text)

	total_occurrences = text.count(palabra)
	
	return [palabra, total_occurrences]
	
def LISTAFRECUENCIA(archivo):
	text = open(f'{archivo}','r').read()
	text=SIMPLIFICA(text)
	
	textosplit = text.split()
	
	textoset = set(textosplit)
	
	LISTAFREC=[]
	for palabra in textoset:
		if len(palabra)>3:
			
			frec = FRECUENCIA(palabra, text)
			LISTAFREC.append(frec)
	
	LISTAFREC.sort(key=lambda x: x[1], reverse=True)
	return LISTAFREC


def COINCIDENCIAS(txt1, txt2):
	
	txt1=SIMPLIFICA(txt1)
	txt2=SIMPLIFICA(txt2)
	
	txt1SET= set(txt1.split())
	txt2SET= set(txt2.split())

	return len(txt1SET & txt2SET)
	

def PASO1():  #transforma txt -> codones
		
	path1= os.getcwd()+'/'+CONST

	print (path1)
	listadi = LISTADO(path1)

	print (listadi)
	TRADUCIR(listadi)


	
def PASO2(N=100):  # obtiene fast con N letras
	path2= os.getcwd()+'/'+CONSTFASTA
	
	#print (f'PATH = {path2}')
	
	TRADFASTA= open('TRADFASTA.txt','w')
	listatrad = LISTADOTRAD(path2)
	
	#print (f' LISTADO TRAD = {listatrad}')
	
	acumula=''
	
	for archiv in listatrad:
		print(archiv)
		
		texto = open(f'{path2}{archiv}','r').read()
		textoN = texto[0:N]
		#print(texto)
		
		NOMBRE= archiv[:-4]
		#print(archiv[:-4])#
		
		#textprimero = archiv[0:N]
		
		#print (textprimero)
		
		TEXTOFAST= f'''
>{NOMBRE}
{textoN}
		
		'''
		acumula += TEXTOFAST
	TRADFASTA.write(acumula)
	
	#CREAR_SEQS(listatrad)
	
	
def PASO3():
	path3= os.getcwd()+'/'+CONSTNUBE
	listadi = LISTADO(path3)

	#print (listadi)
	
	for archiv in listadi:
		
		#print(archiv)
		texto = open(f'{path3}{archiv}','r').read()
		
		#print(texto)
		textosplit = texto.split()
		textoset = set(textosplit)
		
		#print(textosplit)
		
		
		for palabra in textoset:
			print (palabra)
	

def PASO4():  #ordena palabras por frecuencia
	
	ruta = f'{CONSTNUBE}CHILE2021.txt'

	#print (LISTAFRECUENCIA(ruta))

	for i in LISTAFRECUENCIA(ruta):
		print (i)



def PASO5():
	path= os.getcwd()+'/'+CONSTNUBE
	listadi = LISTADO(path)
	n=len(listadi)
	
	
	SALIDA=[]
	k=0
	for i in range(n):
		text1 = open(f'{path}{listadi[i]}','r').read()
		text1=SIMPLIFICA(text1)
		
		for j in range(i+1,n):
			k+=1
			text2 = open(f'{path}{listadi[j]}','r').read()
			text2=SIMPLIFICA(text2)
			
			
			
			
			pais1 = listadi[i][:-4]
			pais2 = listadi[j][:-4]
			coinciden =COINCIDENCIAS(text1, text2)
			numeropalabras1 = len(text1.split())
			numeropalabras2 =len(text2.split())
			n1 = round (coinciden / numeropalabras1 *100, 2)
			n2 = round (coinciden / numeropalabras2 *100, 2)
			
			coinci= [pais1, pais2, coinciden,numeropalabras1,numeropalabras2, n1, n2]
			
			 
			SALIDA.append(coinci)
			print (k, listadi[i][:-4],listadi[j][:-4])
	
	
	ENCABEZADO = ['PAIS 1','PAIS 2','# COINCIDENCIAS','#PALABRAS PAIS 1','#PALABRAS PAIS 2','% COINCIDENCIAS 1', '% COINCIDENCIAS 2']
			
	SALIDA.sort(key=lambda x: x[1], reverse=True)
	SALIDA.insert(0, ENCABEZADO)
	
	df1 = pd.DataFrame(SALIDA)
	df1.to_excel("output.xlsx")
		


#PASO1()  #transforma txt -> codones
#PASO2(N=15000)  # obtiene fast con N letras
#PASO3()
#PASO4() # ordena palabras por frecuencia

PASO5()  # compara todasXtodas coicindencias palabras






print ('')
print ('TERMINE')
