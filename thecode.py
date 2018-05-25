#!/usr/bin/env python
from mpi4py import MPI
import sys
import fileinput
import pprint
# ################# funciones para manejo de libros ####################

""" funcion: countWords 
    descripcion: dadas las palabras en el chunk correspondiente, las parsea y cuenta para escribir en un archivo de salida
    entrada: 
    searchFile: str - la ruta y el nombre del archivo de busqueda
    bookFile: str - la ruta y nombre del libro txt """
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

""" funcion: getWordsOrDefinitions
    descripcion: retorna en una lista las palabras o las definiciones dadas en el archivo de busqueda
    entrada: 
    searchFile: str - la ruta y el nombre del archivo de busqueda
    param: int - 0 para obtener las palabras y 1 para obtener las definiciones """
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
    return copy

def run(searchFile, book, book2):
    comm = MPI.COMM_WORLD
    numnodos = comm.Get_size()
    my_id = comm.Get_rank()
    name = MPI.Get_processor_name()
    final = []
    if (my_id==0):
        filedata=read(book)
        write(book2,filedata)  
        chunk = open(searchFile,"r").readlines() 
        parts = getChunks(searchFile, numnodos-1)
        i = 0
        while (i < (numnodos - 1)):
            comm.send(parts[i], dest = i+1, tag = 11)
 	    i = i+1
        #recibe la cantidad de palabras, ordenarlas y escribir en el archivo
        i=1
        while (i<= (numnodos-1)):
            numwords = comm.recv(source=i, tag =13)
	    for word in numwords:
	        final.append(word)
            i = i+1
	    final.sort()
#    	pprint.pprint(final.encode('utf-8'))
	i = 0
        print("CANTIDAD DE PALABRAS CONTADAS:: %d" % len(final))
        while (i<(len(final)-1)):
            print(final[i].decode('utf-8'))
            i = i+1      
        ring(my_id,book2,parts,comm,numnodos)
    else:
        parts = comm.recv(source = 0, tag =11)
        words = countWords(book, parts)
        print("Nodo %s realizo su CUENTA" % my_id)
        comm.send(words, dest = 0, tag =13) 
        ring(my_id,book2,parts,comm,numnodos)
#parts = MPI.COMM_WORLD.recv(numnodos-1,tag)

def getChunks(searchFile, numnodos):
    chunk = list(evenChunks(searchFile, numnodos))
    dif = len(chunk) - numnodos
    if (dif>0):
        chunk = unevenChunks(chunk, dif)
    return chunk
    

# ################# FIN funciones para manejo de libros #################


# ################# funciones para cambio de palabras #################

""" funcion: read
 descripcion: lee un archivo
 entrada:
   bookFile: str - la ruta y el nombre del archivo del libro """
def read(bookFile):
    with open(bookFile) as f:
        filedata = f.read()
        f.close()
    return filedata

""" funcion: write
 descripcion: escribe en un archivo
 entrada:
   bookFile: str - la ruta y el nombre del archivo del libro """
def write(bookFile,data):
    with open(bookFile,'w+') as f:
        f.write(data)
        f.close()

""" funcion: readList
 descripcion: lee en un archivo y lo coloca en lista por linea
 entrada:
   bookFile: str - la ruta y el nombre del archivo del libro """
def readList(bookFile):
    with open(bookFile) as f:
        filedata = f.readlines()
        f.close()
    return filedata

""" funcion: writeList
 descripcion: escribe una lista en un archivo
 entrada:
   bookFile: str - la ruta y el nombre del archivo del libro """
def writeList(bookFile,lista):
    with open(bookFile,'w+') as f:
        for item in lista:
            f.write(item)
    f.close()
    
""" funcion: getDefinitions
 descripcion: retorna las definiciones de una palabra dada en el archivo de busqueda
 entrada: 
   searchFile: str - la ruta y el nombre del archivo de busqueda
   palabra: str -  palabra de la cual se busca la definicion """
def getDefinitions(lista,palabra):
    definition = ""
    for i in lista:
       thisline = i.split(' "')
       if (thisline[0]==palabra):
           thisdef = thisline[1].split('"')
           definition = thisdef[0]
    return definition

""" funcion: subWords
 descripcion: cambia la primera aparicion de las palabras que se encuentren en la lista de palabras por su respectiva definicion
 entrada:
   bookFile: str - la ruta y el nombre del archivo del libro
   searchFile: str - la ruta y el nombre del archivo de busqueda
   palabras: list -  lista de palabras que se cambiaran en el libro """
def subWords(bookFile,lista,libro):
    for el in lista:
        word=el.split(' "')
        definition=word[1].split('"')
        for i in range(len(libro)):
            if (" "+word[0].lower()+" ") in libro[i].lower():
                libro[i] = libro[i].lower().replace(word[0].lower(),definition[0],1)
                break
    return libro

""" funcion: ring
 descripcion: realiza el recorrido en anillo para cambiar las palabras del libro en cada nodo
 entrada:
   bookFile: str - la ruta y el nombre del archivo del libro
   lista: list -  lista de palabras y definiciones que le toca al nodo cambiar en el libro """
def ring(my_id,bookFile, lista,comm,size):
    #coordinador solo recibe y escribe en el archivo
#    print(size)
    if (my_id)==0:
        data = comm.recv(source = (size-1), tag =12)
        writeList(bookFile,data)
        print("** Coordinador recibio libro con modificaciones **")
    #primer nodo solo modifica y envia al siguiente
    elif (my_id)==1:
        libro=readList(bookFile)
        filedata=subWords(bookFile,lista,libro)
        comm.send(filedata, dest = ((my_id)+1), tag = 12)
        print("Nodo %s realizo su modificacion" % my_id)
    #ultimo nodo recibe, modifica y envia al coordinador
    elif (my_id)==size-1:
        libro = comm.recv(source =((my_id)-1) , tag =12)
        filedata=subWords(bookFile,lista,libro)
        comm.send(filedata, dest = 0, tag = 12)
        print("Nodo %s realizo su modificacion" % my_id)
    #los demas nodos reciben, modifican y envian al siguiente
    else:
        libro = comm.recv(source =((my_id)-1) , tag =12)
        filedata=subWords(bookFile,lista)
        comm.send(filedata, dest = ((my_id)+1), tag = 12)
        print("Nodo %s realizo su modificacion" % my_id)

# ################# FIN funciones para cambio de palabras #################



############### MAIN CODE ################
#palabras = getWordsOrDefinitions("input.txt",0)
#prueba=getDefinitions("input.txt","software")
searchFile = 'palabras_libro_medicina.txt'
book = 'libro.txt'
bookm='libro_medicina.txt'
local_book = '/local_home/mnarguelles.14/libro.txt'
book2 = 'libro2.txt'
run(searchFile, bookm, book2)
#print(chunk[0])
#subWords("libro.txt",chunk[0])
#enviar chunk[my_id]
#chunk=getChunks(searchFile,7)
#subWords("libro.txt",chunk[0])
#filedata=readList("libro.txt")
#writeList("prueba.txt",filedata)
#final = countWords("libro.txt", chunk[0])
#print("PALABRAS Y REPETICIONES :: %s" % final)