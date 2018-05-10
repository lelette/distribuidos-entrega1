#!/usr/bin/env python
#from mpi4py import MPI
import sys
import fileinput
import pprint
############################################################################################


# ################# funciones para manejo de libros ####################

# funcion: contarPalabras 
# descripcion: dadas las palabras en el chunk correspondiente, las parsea y cuenta para escribir en un archivo de salida
# entrada: 
#   searchFile: str - la ruta y el nombre del archivo de busqueda
#   bookFile: str - la ruta y nombre del libro txt
def countWords(bookFile, lista):
    words = getWords(lista)
    lineas = open(bookFile, "r").readlines()
    final = []
    index = 0
    for word in words:
        veces = 0
        for linea in lineas:
            veces = veces + linea.count(word)
        index = index + 1
        final.append(word + "|" + str(veces))
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

def getWords(lista):
    words = []
    for i in lista:
       thisline = i.split(' "')
       words.append(thisline[0])
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

def chunks(n, searchFile):
    chunk = open(searchFile,"r").readlines()
    for i in range(0, len(chunk), n):
        yield chunk[i:i+n] 
    #verificar si la cantidad de sublistas (tamano de la lista padre) es mayor al numero de nodos, en ese caso, reasignar la diferencia a las primeras sublistas
    return

#input[i:i+n] for i in range(0, lenchunks (input), n)

def run():
    size
    my_id
    MPI_Comm_size(comm, size)
    MPI_Comm_rank(comm, my_id)
    searchWords = open('input.txt', 'r').readlines()

    MPI.Comm.bcast()
    if (my_id==0):
        print("cao COORDINADOR %d" % my_id)
        #do coordinator stuff
    else:
        print("hola NODO %d" % my_id)
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

#def ring():
    #if id=1 cambiar y enviar al siguiente, if id=size-1 recibir cambiar y enviar al coordinador, else recibir cambiar y enviar al siguiente
    #if (my_id)=1:
        

# ################# FIN funciones para cambio de palabras #################

palabras = getWordsOrDefinitions("input.txt",0)
#prueba=getDefinitions("input.txt","software")
subWords("libro.txt",palabras,"input.txt")
#print("PALABRAS Y REPETICIONES :: %s" % final)
searchFile = 'input.txt'
#length/numnodos = chunksize
numnodos = 7
chunksize = len(open(searchFile,"r").readlines()) / numnodos
chunk = list(chunks(chunksize, searchFile))
#enviar chunk[my_id]
#final = countWords("libro.txt", chunk[0])
#print(final)
############################################################################################

