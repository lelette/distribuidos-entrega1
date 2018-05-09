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

def deleteFile(filename):
    try:
        os.remove(filename)
    except OSError:
        pass

    try:
        os.remove(filename)
    except OSError:
        pass

def run():
    size
    my_id
    MPI_Comm_size(comm, size)
    MPI_Comm_rank(comm, my_id)
    searchWords = open('input.txt', 'r').readlines()

    MPI.Comm.bcast()
    if (my_id==0):
        print("cao")
        #do coordinator stuff
    else:
        print("hola")
        #do standard-node stuff

    

# ################# FIN funciones para manejo de libros #################


# ################# funciones para cambio de palabras #################

# funcion: getDefinitions
# descripcion: retorna las definiciones de una palabra dada en el archivo de busqueda
# entrada: 
#   searchFile: str - la ruta y el nombre del archivo de busqueda
#   palabra: str -  palabra de la cual se busca la definicion
def getDefinitions(searchFile,palabra):
    file = open(searchFile, "r")
    lines = file.readlines()
    definition = ""
    for i in lines:
       thisline = i.split(' "')
       if (thisline[0]==palabra):
           thisdef = thisline[1].split('"')
           definition = thisdef[0]
    return definition

# funcion: subWords
# descripcion: cambia la primera aparicion de las palabras que se encuentren en la lista de palabras por su respectiva definicion
# entrada:
#   bookFile: str - la ruta y el nombre del archivo del libro
#   searchFile: str - la ruta y el nombre del archivo de busqueda
#   palabras: list -  lista de palabras que se cambiaran en el libro
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

# ################# FIN funciones para cambio de palabras #################

final = countWords("input.txt", "libro.txt")
palabras = getWordsOrDefinitions("input.txt",0)
prueba=getDefinitions("input.txt","software")
subWords("libro.txt",palabras,"input.txt")
print("PALABRAS Y REPETICIONES :: %s" % final)
############################################################################################

