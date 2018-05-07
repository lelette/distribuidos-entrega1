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


final = countWords("input.txt", "libro.txt")
print("PALABRAS Y REPETICIONES :: %s" % final)


#tempFile = open( "input.txt", 'r+' )

#for line in fileinput.input( "input.txt" ):
 #   if "hardware" in line :
  #      print('Match Found')
   # else:
    #    print('Match Not Found!!')
    #tempFile.write( line.replace( "hardware", "logro" ) )

#tempFile.close()
############################################################################################

