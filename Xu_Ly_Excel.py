from xlrd import open_workbook
import xlwt

#list hold data
values = [] 

# list hold column name
values_name = [] 

# first part of sqc ex  : 12 of 12/3A
fsqc = [] 

# first part of address ex :  12/3A  
sqc = []    

#number of column 
numberofcols = [] 

# for import excel
valuesimport = []
fsqcimport =  []
sqcimport = []
numberofcolsimport = []
values_nameimport = []
def read(path) :
 fsqc.clear()
 values.clear()
 values_name.clear()
 sqc.clear()
 numberofcols.clear()
 addsqc = []
 wb = open_workbook(path)
 first_sheet = wb.sheet_by_index(0)
 numberofcols.append(first_sheet.ncols)
 for s in wb.sheets():
    for row in range(1, s.nrows):
      for column in range(0, s.ncols):
       #handle  when a row in rectangle is null will make crash when fill controllist
       if not first_sheet.cell(row, column).value :
        #set cell  = ' ' 
        particular_cell_value = ' '  
       else :
        particular_cell_value = first_sheet.cell(row, column).value
       #values is a list that hold data from excel
       values.append(particular_cell_value) 
       # getcolumnvalues = 'Địa chỉ' and split address  
       if  str(first_sheet.cell(0, column).value).strip() == "Địa chỉ": 
          addsqc.append(particular_cell_value)
          #split a data of addresss and then the first part is the number of address
          address = str(particular_cell_value).split(",") 
          sqc.append(address[0])
    #get column name
    for column in range(0, s.ncols): 
        col_names = first_sheet.cell(0, column).value
        values_name.append(col_names)
 if sqc  :
  for i in range(len(sqc)) :
    faddress = sqc[i].split("/")
    fpaddress = faddress[0]
    if not fpaddress.isdigit():
        fpaddress = fpaddress[0:int(len(fpaddress) - 1)]
    if fpaddress :
     fsqc.append(int(fpaddress))
def importexcel(path) :
    fsqcimport.clear()
    valuesimport.clear()
    sqcimport.clear()
    addsqc = []
    wb = open_workbook(path)
    first_sheet = wb.sheet_by_index(0)
    numberofcolsimport.append(first_sheet.ncols)
    for s in wb.sheets():
        for row in range(1, s.nrows):
            for column in range(0, s.ncols):
                if not first_sheet.cell(row,column).value:  
                    particular_cell_value = ' '  
                else:
                    particular_cell_value = first_sheet.cell(row, column).value
                valuesimport.append(particular_cell_value)
                if column == 1:  
                    addsqc.append(particular_cell_value)
                    
                    address = str(particular_cell_value).split( ",")  
                    sqcimport.append(address[0])
        for column in range(0, s.ncols):  
            col_names = first_sheet.cell(0, column).value
            values_nameimport.append(col_names)
    if sqcimport:
        for i in range(len(sqcimport)):
            faddress = sqcimport[i].split("/")
            fpaddress = faddress[0]
            if not fpaddress.isdigit():
                fpaddress = fpaddress[0:int(len(fpaddress) - 1)]
            if fpaddress:
                fsqcimport.append(int(fpaddress))
def write(path,filename) :
    book = xlwt.Workbook()
    sh = book.add_sheet("Sheet 1")
    for s in range(0,len(values_name)):
      sh.write(0, s , values_name[s])
    for col in range(0, numberofcols[0]):
     for row in range(0,int(len(values) / numberofcols[0])):
        sh.write(row + 1, col , values[row *7 + col])
    book.save(path+'/'+filename+'.xls')
