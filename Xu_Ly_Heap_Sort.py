from Xu_Ly_Excel import fsqc,values,numberofcols
def swap(i, j):
    fsqc[i], fsqc[j] = fsqc[j], fsqc[i]
    #swap element of value and then use values list to fill list on GUI
    for k in range(1,numberofcols[0]) :
     values[numberofcols[0] * j + k], values[numberofcols[0] * i + k] = values[numberofcols[0] * i  + k], values[numberofcols[0] * j + k]
def heapify(end,i):
    l= 2 * i + 1
    r =  2 * i + 2
    maxnum = i
    if l < end and fsqc[i] < fsqc[l]:
        maxnum = l
    if r < end and fsqc[maxnum] < fsqc[r]:
        maxnum = r
    if maxnum != i:
        swap(i, maxnum)
        heapify(end, maxnum)
def heap_sort():
    end = len(fsqc)
    begin = end // 2 - 1
    for i in range(begin, -1, -1):
        heapify(end, i)
    for i in range(end-1, 0, -1):
        swap(i,0)
        heapify(i,0)