#!/usr/bin/env python
#from mpi4py import MPI
import sys
import fileinput
############################################################################################

# Region de funciones
# ################# funciones para manejo de libros #################


# funcion: contarPalabras 
# descripcion: dadas las palabras en el chunk correspondiente, las parsea y cuenta para escribir en un archivo de salida
def contarPalabras(searchFile, bookFile):
    file = open(searchFile, "r")
    lines = file.readlines()
    words = []
    for i in lines:
        thisline = i.split('"')
        words.append(thisline[0])
        print (words)
    libro = open(bookFile, "r")
    lineas = libro.readlines()
    for word, _ in words:
        for line  in enumerate(lineas):
            if lineas[line:line + len(word)] == word:
                print(word)
            #if word in line : print("holaa %s" % (word))  
    return


#contarPalabras("input.txt", "libro.txt")


#sys.stdout.write(
#    "HOLA MUNDO!!! soy process %d of %d on %s.\n" % (rank,size,name)
#)



tempFile = open( "input.txt", 'r+' )

for line in fileinput.input( "input.txt" ):
    if "hardware" in line :
        print('Match Found')
    else:
        print('Match Not Found!!')
    tempFile.write( line.replace( "hardware", "logro" ) )

tempFile.close()
############################################################################################

