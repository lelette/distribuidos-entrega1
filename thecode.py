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

def evenChunks(searchFile, numnodos):
    chunk = open(searchFile,"r").readlines()
    n = len(list(chunk)) / numnodos
    for i in range(0, len(chunk), int(n)):
        yield chunk[int(i):int(i+n)] 
    return

def unevenChunks(chunk, dif):
    copy = chunk
    i=0
    while (i<dif):
        for elm in chunk[len(chunk)-1 -i]:
            copy[i].append(elm)
        copy.remove(chunk[len(chunk)-1 -i])
        i = i + 1
    #pprint.pprint(copy)
    return copy


def run():
    size
    my_id
    MPI_Comm_size(comm, size)
    MPI_Comm_rank(comm, my_id)
    searchWords = open('input.txt', 'r').readlines()

    #MPI.Comm.bcast()
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
def getDefinitions(lista,palabra):
    definition = ""
    for i in lista:
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
def subWords(bookFile,lista):
    for el in lista:
        f = open("libro.txt",'r')
        filedata = f.read()
        f.close()
        word=el.split(' "')
        definition=word[1].split('"')
        for line in fileinput.FileInput( bookFile ):
            newdata = filedata.replace(word[0],definition[0],1)
            f = open(bookFile,'w')
            f.write(newdata)
            f.close()
            if el in line :
                break
    return newdata

def ring(bookFile, lista):
    #coordinador solo recibe y escribe en el archivo
    if (my_id)==0:
    #   MPI_Recv(data,data.length,)
        f = open(bookFile,'w')
        f.write(data)
        f.close()
    #primer nodo solo modifica y envia al siguiente
    if (my_id)==1:
        subWords(bookFile,lista)
        f = open(bookFile,'r')
        filedata = f.read()
        f.close()
        MPI_Send(filedata, filedata.length, MPI_CHAR, (my_id+1), MPI_ANY_TAG, MPI_COMM_WORLD)
    #ultimo nodo recibe, modifica y envia al coordinador
    if (my_id)==size-1:
    #   MPI_Recv(data,data.length,)
        f = open(bookFile,'w')
        f.write(data)
        f.close()
        subWords(bookFile,lista)
        f = open(bookFile,'r')
        filedata = f.read()
        f.close()
        MPI_Send(filedata, filedata.length, MPI_CHAR,0, MPI_ANY_TAG, MPI_COMM_WORLD)
    #los demas nodos reciben, modifican y envian al siguiente
    else:
    #   MPI_Recv(data,data.length,)
        f = open(bookFile,'w')
        f.write(data)
        f.close()
        subWords(bookFile,lista)
        f = open(bookFile,'r')
        filedata = f.read()
        f.close()
        MPI_Send(filedata, filedata.length, MPI_CHAR,(my_id+1), MPI_ANY_TAG, MPI_COMM_WORLD)

# ################# FIN funciones para cambio de palabras #################

palabras = getWordsOrDefinitions("input.txt",0)
#prueba=getDefinitions("input.txt","software")
searchFile = 'input.txt'
#length/numnodos = chunksize
numnodos = 7
chunk = list(evenChunks(searchFile, numnodos))
dif = len(chunk) - numnodos
if (dif>0):
    chunk = unevenChunks(chunk, dif)
print("CANTIDAD DE PARTES A ENVIAR :: %d" % len(chunk))
print(chunk[0])
subWords("libro.txt",chunk[0])
#enviar chunk[my_id]
#final = countWords("libro.txt", chunk[0])
#print("PALABRAS Y REPETICIONES :: %s" % final)
############################################################################################

