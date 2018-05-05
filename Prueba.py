#!/usr/bin/env python
#from mpi4py import MPI
import sys
import fileinput

size = 3
rank = 8
name = "Prueba 1 Distribuidos"

sys.stdout.write(
    "HOLA MUNDO!!! soy process %d of %d on %s.\n" % (rank,size,name)
)

file = open("input.txt", "r")
lines = file.readlines()
for i in lines:
   thisline = i.split('"')
   print (thisline)

tempFile = open( "input.txt", 'r+' )

for line in fileinput.input( "input.txt" ):
    if "hardware" in line :
        print('Match Found')
    else:
        print('Match Not Found!!')
    tempFile.write( line.replace( "hardware", "logro" ) )

tempFile.close()

