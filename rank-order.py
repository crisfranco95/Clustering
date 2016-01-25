# -*- coding: utf-8 -*-
import string
import sys,os
from collections import defaultdict

# GLOBAL CONFIGURATION VARIABLES
tab = "\t"
space = " "
newline = os.linesep

def getColumns(inFile, delim=tab, header=True):
    """
    Get columns of data from inFile. The order of the rows is respected
    
    :param inFile: column file separated by delim
    :param header: if True the first line will be considered a header line
    :returns: a tuple of 2 dicts (cols, indexToName). cols dict has keys that 
    are headings in the inFile, and values are a list of all the entries in that
    column. indexToName dict maps column index to names that are used as keys in 
    the cols dict. The names are the same as the headings used in inFile. If
    header is False, then column indices (starting from 0) are used for the 
    heading names (i.e. the keys in the cols dict)
    
    Sample File:
    Heading 1    Heading 2    Heading 3
    row1value1   row1value2   row1value3
    row2value1   row2value2   row2value3
    
    Sample usage on sample file:
    cols, i2n = getColumns(sampleFile)
    cols["Heading 1"] == cols[i2n[0]]
    cols["Heading 2"] == cols[i2n[1]]
    cols["Heading 3"][0] == "row1value3"
    set(cols["Heading 1"]).union(set(cols["Heading 3"]) 
    """
    cols = {}
    indexToName = {}
    for lineNum, line in enumerate(inFile):
        if lineNum == 0:
            headings = line.strip().split(delim)
            k = 0
            for heading in headings:
                heading = heading.strip()
                if header:
                    cols[heading] = []
                    indexToName[k] = heading
                else:
                    # in this case the heading is actually just a cell
                    cols[k] = [heading]
                    indexToName[k] = k
                k += 1
        else:
            cells = line.strip().split(delim)
            k = 0
            for cell in cells:
                cell = cell.strip()
                cols[indexToName[k]] += [cell]
                k += 1
                
    return cols, indexToName

#files
matrix_file = "/Users/lauricdd/Documents/Github/Clustering/matrix.txt"
temporal_file = "/Users/lauricdd/Documents/Github/Clustering/temp.txt"
ordered_matrix_file = "/Users/lauricdd/Documents/Github/Clustering/ordered_matrix.txt"
final_matrix_file = "/Users/lauricdd/Documents/Github/Clustering/final_matrix.txt"
students_file = "/Users/lauricdd/Documents/Github/Clustering/students.txt"
final_students_file = "/Users/lauricdd/Documents/Github/Clustering/final_students.txt"
items_file = "/Users/lauricdd/Documents/Github/Clustering/items.txt"
final_items_file = "/Users/lauricdd/Documents/Github/Clustering/final_items.txt"
students_and_pows = "/Users/lauricdd/Documents/Github/Clustering/students_and_pows.txt"

open_matrix_file = open(matrix_file, "r")

#read the opened file
open_matrix_file_data = open_matrix_file.read()

#print "\nfile\n", open_matrix_file_data

#number of elements of the file
elements = string.split(open_matrix_file_data)
elements_number = len(elements)
print "elements =", elements_number

#file lines number
#lines = len(open(file).readlines())
lines_number = 0
with open(matrix_file) as open_final_items_file:
    for students_file_lines in open_final_items_file:
       if students_file_lines.strip():
          lines_number += 1
print "lines =", lines_number

#number of elements per line : elements = lines*columns then columns = elements/lines
columns_number = elements_number/lines_number
print "columns =", columns_number
open_matrix_file.close()

#split file by lines and save on matrix
matrix = [[0 for col in range(columns_number)] for row in range(lines_number)] #fill matrix with 0
i = 0
open_matrix_file = open(matrix_file, "r")
for students_file_lines in open_matrix_file:
    x = students_file_lines.split()
    matrix[i] = x
    #print "x", x
    #print "i", i
    i+=1
        
print "\nmatrix"
for i in range(lines_number):
    for j in range(columns_number):
        print matrix[i][j],
    print 
open_matrix_file.close()

print

#RANK-ORDER ALGORITHM
binary_array = [0 for i in range(0, columns_number)] #fill array with 0
for i in range(0, columns_number):
        binary_array[i] = 2**(columns_number-i-1) #pows 2^4, 2^3, 2^2...

print "\nbinary_array"
for i in range(columns_number):
    print binary_array[i],
      
lines_weight_array = [0 for i in range(0, lines_number)] #fill array with 0
for i in range(lines_number):
    weight = 0 
    for j in range(columns_number):
        weight += binary_array[j] * int(matrix[i][j]) #convert string to int
    lines_weight_array[i] = weight #save weight of each line

print "\nlines_weight_array"
for i in range(lines_number):
    print lines_weight_array[i],

#create lines_weight_array copy
lines_weight_array_copy = [0 for i in range(0, lines_number)] #fill array with 0
for i in range(0, lines_number):
        lines_weight_array_copy[i] = lines_weight_array[i]

print "\nlines_weight_array_copy"
for i in range(lines_number):
    print lines_weight_array_copy[i],

#calculate ordered_lines_weight
value = 1
ordered_lines_weight_array = [0 for i in range(0, lines_number)]  #fill array with 0

while value < lines_number+1:
    aux = 0 
    exp = 2**(lines_number+2)
    lower = exp
    for i in range(0, lines_number):
        #print i, lines_weight_copy[i]
        if lines_weight_array_copy[i] < lower:
            lower = lines_weight_array_copy[i]
            #print "lower", lower
            aux = i 
    #print "lower", lower, "i", aux 
    #print "lines_weight_copy[aux]", lines_weight_copy[aux]
    lines_weight_array_copy[aux] = exp
    ordered_lines_weight_array[aux] = value
    value += 1

print "\nordered_lines_weight"
for i in range(lines_number):
    print ordered_lines_weight_array[i],

#sort weights in decreasing order
value = 1
flag = 0
ordered_matrix = [[0 for col in range(columns_number)] for row in range(lines_number)] #fill matrix with 0
temp = [0 for col in range(columns_number)]

#read students_final file
open_final_students_file = open(final_students_file, "r")
open_final_students_file_readlines = open_final_students_file.readlines()

while value < lines_number+1:
    aux = 0 
    upper = 0
    for i in range(0, lines_number):
        if ordered_lines_weight_array[i] > upper:
            upper = ordered_lines_weight_array[i]
            aux = i 
    
    #print "upper", upper, "i=", aux  
    #print temp
    
    ordered_lines_weight_array[aux] = 0
    
    #read matrix file
    open_matrix_file = open(matrix_file, "r")
    open_matrix_file_readlines = open_matrix_file.readlines()
    temp = open_matrix_file_readlines[aux]
    #temp[aux] = l[aux]
    #print "temp", temp
        
    #read students file  
    open_students_file = open(students_file, "r")
    students_file_lines = open_students_file.readlines()
    #print "line[" + aux + "]" + students_file_lines[aux]
       
    #override final_students file
    open_final_students_file_readlines[flag] = students_file_lines[aux]
                
    #write temp file
    open_final_items_file = open(temporal_file, "w")
    open_final_items_file.write(str(temp.replace(' ', '').split()))
    #f.write(str(temp[aux].replace(' ','').split()))
    open_final_items_file.close()
        
    open_final_items_file = open(temporal_file, "r")
    for students_file_lines in open_final_items_file:
        #print "file:", line[2], line[3], line[4], line[5], line[6]   
        i = 0
        while i <= columns_number-1:
            ordered_matrix[flag][i] = students_file_lines[i+2]
            i += 1
    open_final_items_file.close()

    value += 1
    flag += 1
    open_matrix_file.close()
    open_students_file.close()
    

#write back on students_final file
open_final_students_file = open(final_students_file, "w")
#open_final_students_file.writelines(open_final_students_file_readlines)
#open_final_students_file_readlines size
count = open_final_students_file_readlines.__len__()
for i in range(0, count):
    open_final_students_file.write(open_final_students_file_readlines[i].replace('\r\n','') + '\n')
open_final_students_file.close()

#for i in range(lines_number):
 # for j in range(columns_number):
  #  print ordered_matrix[i][j],
   # print

#write ordered_matrix on a file
open_ordered_matrix_file = open(ordered_matrix_file, "w")
i = 0
while i < columns_number:
    open_ordered_matrix_file.write("col"+str(i) + "\t")
    i += 1
open_ordered_matrix_file.write("\n")
for i in range(lines_number):
    for j in range(columns_number):
        open_ordered_matrix_file.write(ordered_matrix[i][j]+"\t")
    open_ordered_matrix_file.write("\n")
open_ordered_matrix_file.close()

binary2_array = [0 for i in range(0, lines_number)] #fill array with 0
for i in range(0, lines_number):
        binary2_array[i] = 2**(lines_number-i-1) #pows 2^4, 2^3, 2^2...

print "\nbinary2_array"
for i in range(lines_number):
    print binary2_array[i],
      
columns_weight_array = [0 for i in range(0, columns_number)] #fill array with 0
for j in range(columns_number):
    weight2 = 0 
    for i in range(lines_number):
        weight2 += binary2_array[i] * int(ordered_matrix[i][j]) #convert string to int
    columns_weight_array[j] = weight2 #save weight of each line

print "\ncolumns_weight_array"
for i in range(columns_number):
    print columns_weight_array[i],

#create copy
columns_weight_copy_array = [0 for i in range(0, columns_number)] #fill array with 0
for i in range(0, columns_number):
        columns_weight_copy_array[i] = columns_weight_array[i]

print "\ncolumns_weight_copy_array"
for i in range(columns_number):
    print columns_weight_copy_array[i],

#calculate ordered_lines_weight
value2 = 1
ordered_columns_weight = [0 for i in range(0, columns_number)] #fill array with 0

while value2 < columns_number+1:
    aux2 = 0 
    exp2 = 2**500 #REVISARRR PORQUE LA MATRIZ VERDADERA ES MUY GRANDE Y SE QUEDAN CORTOS ESOS EXPONENTES
    lower2 = exp2
    for i in range(0, columns_number):
        if columns_weight_copy_array[i]<lower2:
            lower2 = columns_weight_copy_array[i]
            aux2 = i 
    columns_weight_copy_array[aux2] = exp2
    ordered_columns_weight[aux2] = value2
    value2 += 1

print "\nordered_columns_weight"
for i in range(columns_number):
    print ordered_columns_weight[i],

#sort weights in decreasing order
value3 = 1
flag2 = 0
upper2 = 0
final_items_array = ["Al0" for col in range(columns_number)] #fill array with 0
final_matrix = [[0 for col in range(columns_number)] for row in range(lines_number)] #fill matrix with 0
while value3 < columns_number+1:
    aux3 = 0 
    upper2 = 0
    for i in range(0, columns_number):
        if ordered_columns_weight[i]>upper2:
            upper2 = ordered_columns_weight[i]
            aux3 = i 
        
    #print "upper", upper2, "i=", aux3
    
    ordered_columns_weight[aux3] = 0
    
    open_matrix_file = open(ordered_matrix_file, "r")
    cols, indexToName = getColumns(open_matrix_file)
    col = cols["col"+str(aux3)]
    
    #print "aux3",aux3,"columna", cols["col"+str(aux3)]  
    
    j = 0
    while j <= lines_number-1:
        final_matrix[j][flag2] = cols["col"+str(aux3)][j]
        j += 1
    
    #print "elemento",cols["col"+str(aux3)][0] 
    
    open_students_file = open(items_file, "r")
    cols, indexToName = getColumns(open_students_file)
    col2 = cols["col"+str(aux3)]
    final_items_array[flag2] = col2
    value3 += 1
    flag2 += 1

open_matrix_file.close()
open_students_file.close()

print "\nfinal_items_array"
for i in range(columns_number):
    print final_items_array[i],

#write final_items in the corresponding file
open_final_items_file = open(final_items_file, "w")
open_final_items_file.write(str(final_items_array))
open_final_items_file.close()


print "\nfinal_matrix"
for i in range(lines_number):
    for j in range(columns_number):
        print final_matrix[i][j],
    print   

#write final_matrix on a file
open_final_matrix_file = open(final_matrix_file, "w")
for i in range(lines_number):
    for j in range(columns_number):
        open_final_matrix_file.write(final_matrix[i][j]+" ")
    open_final_matrix_file.write("\n")
open_final_matrix_file.close()


#Calculate new weights from pows of 2
num = 0
sum_num = 0
sum_lines_pow = [0 for i in range(0, lines_number)]
for i in range(lines_number):
    for j in range(columns_number):
        sum_num += int(final_matrix[i][j])*(2**num)
        num += 1
    sum_lines_pow[i] = sum_num
    sum_num = 0
    num = 0

print "sum_lines_pow", sum_lines_pow
print "sum_lines_pow size", sum_lines_pow.__len__()

#Write students and new weights on a file, separated by tab
open_final_students = open(final_students_file, "r")
students_file_lines = open_final_students.readlines()
open_students_and_pows = open(students_and_pows, "w")

count = lines_number #open_final_students_file_readlines.__len__()
for i in range(0, count):
    open_students_and_pows.write(students_file_lines[i].replace('\n','') + '\t' + str(sum_lines_pow[i]) + '\n')

open_final_students.close()
open_students_and_pows.close()