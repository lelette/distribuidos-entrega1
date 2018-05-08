#!/usr/bin/env python
#from mpi4py import MPI
import sys
import fileinput
############################################################################################


# ################# funciones para manejo de libros ####################

# funcion: contarPalabras 
# descripcion: dadas las palabras en el chunk correspondiente, las parsea y cuenta para escribir en un archivo de salida
# entrada: 
#   searchFile: str - la ruta y el nombre del archivo de busqueda
#   bookFile: str - la ruta y nombre del libro txt
def countWords(searchFile, bookFile):
    words = getWordsOrDefinitions(searchFile, 0)  
    lineas = open(bookFile, "r").readlines()
    final = ''
    index = 0
    for word in words:
        veces = 0
        for linea in lineas:
            veces = veces + linea.count(word)
        index = index + 1
        final = final + word + ";" + str(veces) + "|"
    return final

# funcion: getWordsOrDefinitions
# descripcion: retorna en una lista las palabras o las definiciones dadas en el archivo de busqueda
# entrada: 
#   searchFile: str - la ruta y el nombre del archivo de busqueda
#   param: int - 0 para obtener las palabras y 1 para obtener las definiciones
def getWordsOrDefinitions(searchFile, param):
    file = open(searchFile, "r")
    lines = file.readlines()
    words = []
    for i in lines:
       thisline = i.split(' "')
       words.append(thisline[param])
    return words
# ################# FIN funciones para manejo de libros #################

def getDefinitions(searchFile,palabra):
    file = open(searchFile, "r")
    lines = file.readlines()
    definition = ""
    for i in lines:
       thisline = i.split(' "')
       if (thisline[0]==palabra):
           definition = thisline[1]
    return definition

def subWords(bookFile,palabras,searchFile):
    for el in palabras:
        f = open(bookFile,'r')
        filedata = f.read()
        f.close()
        for line in fileinput.FileInput( bookFile ):
            newdata = filedata.replace(el,getDefinitions(searchFile,el),1)
            f = open(bookFile,'w')
            f.write(newdata)
            f.close()
            if el in line :
                break
    return 0

final = countWords("input.txt", "libro.txt")
palabras = getWordsOrDefinitions("input.txt",0)
prueba=getDefinitions("input.txt","lelita")
subWords("libro.txt",palabras,"input.txt")
print("PALABRAS Y REPETICIONES :: %s" % final)
############################################################################################

