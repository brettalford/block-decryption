#!/usr/bin/env python3
"""
=============================================================================
Title : Brett_Alford_R11700357_final_project.py
Description : This code decrypts a string
Author : Brett Alford R#11700357
Date : 12/04/2023
Version : 1.0
Usage : python3
Notes : This example script has no requirements.
Python Version: 3.x.x
=============================================================================
"""
import multiprocessing
import sys
import time
import argparse

def decryptletter(letter, rotationvalue):
    rotationstring = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ "
    currentposition = rotationstring.find(letter)
    return rotationstring[(currentposition + rotationvalue) % 95]


def detneighborval(neighbor):
    if neighbor == 'a':
        return 0
    elif neighbor == 'b':
        return 1
    else:
        return 2


def nextletter(currentletter, shift):
    if currentletter == 'a':
        if shift == 1:
            return 'b'
        else:
            return 'c'
    elif currentletter == 'b':
        if shift == 1:
            return 'c'
        else:
            return 'a'
    else:
        if shift == 1:
            return 'a'
        else:
            return 'b'


def getgroupval(groupnum, startarray, size):
    # put row values into a list called groupval
    groupval = []
    # list of primes, only need to be up to 13 because highest possible neighbor val is 16
    primes = [2, 3, 5, 7, 11, 13]
    start = 0
    for i in range(groupnum):
        start = start+size[i]
    end = start + size[groupnum]
    for n in range(start, end):
        neighborval = 0
        # if variable i isn't the furthest left column then it has a left
        if n % L != 0:
            neighborval = neighborval + detneighborval(startarray[n - 1])
        # if variable i isn't the furthest right
        if n % L != (L - 1):
            neighborval = neighborval + detneighborval(startarray[n + 1])
        # if variable i is greater than first row value it has an above
        if n >= L:
            neighborval = neighborval + detneighborval(startarray[n - L])
            # if i also isnt furthest left column then it has an upper left
            if n % L != 0:
                neighborval = neighborval + detneighborval(startarray[n - 1 - L])
                # if i also isnt furthest right
            if n % L != (L - 1):
                neighborval = neighborval + detneighborval(startarray[n + 1 - L])
            # if i is less than L*L-1-L it has a below
        if n < L * L - L:
            neighborval = neighborval + detneighborval(startarray[n + L])
            # if i also isnt furthest left column then it has an upper left
            if n % L != 0:
                neighborval = neighborval + detneighborval(startarray[n - 1 + L])
            # if i also isn't the furthest right
            if n % L != (L - 1):
                neighborval = neighborval + detneighborval(startarray[n + 1 + L])
        # check if prime
        if neighborval in primes:
            # do nothing
            groupval.append(startarray[n])
            pass
        else:
            # if value is even
            if neighborval % 2 == 0:
                # it is even make it the next letter
                groupval.append(nextletter(startarray[n], 1))
            # value is odd
            else:
                # it is odd so make it the previous letter
                groupval.append(nextletter(startarray[n], 0))
    return groupval


inputs = argparse.ArgumentParser()
inputs.add_argument('-i', type=str, required=True)
inputs.add_argument('-o', type=str, required=True)
inputs.add_argument('-s', type=str, required=True)
inputs.add_argument('-p', type=int, required=False)

# number of processes
processess = 1

inhold = inputs.parse_args()

if inhold.p is not None:
    processess = inhold.p
    if inhold.p < 1:
        print("Inappropriate processor count detected")
        sys.exit(1)


# input string
with open(inhold.i, 'r') as file:
    instring = file.read()

L = len(instring)
# how many rows will be left over if
remainder = L % processess
# size of the groups (in rows) without remainder aka standard size
groupsize = int((L * L - remainder * L) / processess)
rowsper = groupsize / L


def main():

    print("Project :: 11700357")
    # empty 2d array
    startarray = []
    start_time = time.time()
    abc = ['a', 'b', 'c']
    # distributing extra value to the other processes
    size = [groupsize] * processess
    for i in range(remainder):
        size[i] = size[i] + L
    # seed array for testing, will import from command line
    seedin = inhold.s
    for i in range(len(seedin)):
        if seedin[i] not in abc:
            print("Error: Not abc exclusive")
            sys.exit(1)

    seedarray = []
    s = len(seedin)
    for i in range(0, s):
        seedarray.append(seedin[i])

    # counts place in seed array, so you don't go over
    seedplacecount = 0

    # decrypted string
    decryptstr = ""

    # constructing array
    for i in range(L * L):
        if seedplacecount > len(seedarray) - 1:
            seedplacecount = 0
        # use .append for this
        startarray.append(seedarray[seedplacecount])
        seedplacecount = seedplacecount + 1
    # finding neighbor values, may separate this and the changing of character based on array,
    # both will be in a 100 for loop
    with multiprocessing.Pool(processess) as pool:
        for x in range(100):
            # okay so this part is the bit im doing multiprocessing on, what i plan to do is have a group of processes,
            # one for each of the user inputs. These processes will each get a different row value and then calculate
            # their respective rows neighbor values, continuing on until the block is finished at which point the
            # collection of row lists will be put into new startarray
            groupvals = pool.starmap(getgroupval, [(groupnum, startarray, size) for groupnum in range(processess)])
            startarray = []
            for i in range(processess):
                startarray.extend(groupvals[i])

    # initial values for columnvals
    columnvals = [0] * L
    # making sum of columns i=column j=row
    for i in range(0, L * L):
        # sets value of the total column val to 0 so every time it finishes one it resets and goes to the next
        columnval = 0
        if startarray[i] == 'b':
            # add one
            columnval = columnval + 1

        if startarray[i] == 'c':
            # add two
            columnval = columnval + 2

        # decide which column
        columnvals[i % L] = columnvals[i % L] + columnval
    # now the column value for that column should have been found so decrypt the 0th letter based on the
    # rotation of the columnval?
    for i in range(0, L):
        decryptstr += (decryptletter(instring[i], columnvals[i]))
    print(decryptstr)
    end_time = time.time()
    print("Execution time: {:.4f} seconds".format(end_time - start_time))

    with open(inhold.o, 'w') as fileout:
        fileout.write(decryptstr)


if __name__ == '__main__':
    main()