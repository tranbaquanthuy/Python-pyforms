import pyforms
from pyforms          import BaseWidget
from pyforms.controls import ControlText,ControlFile,ControlButton,ControlList,ControlDir,ControlCheckBoxList
#import tkinter to use messagebox to show dialog
from tkinter import messagebox
import tkinter as tk
#import funtion from Xu_Ly_Heap_Sort
from Xu_Ly_Heap_Sort import heap_sort
#import variable from Xu_Ly_Excel
from Xu_Ly_Excel import  values,fsqc,sqc,numberofcols,values_name
from Xu_Ly_Excel import   valuesimport,numberofcolsimport,fsqcimport,sqcimport,values_nameimport
#import funtion from Xu_Ly_Excel
from Xu_Ly_Excel import read,importexcel,write
#import for validating file name and path 
import os
from pathlib import Path

class SimpleExample1(BaseWidget):
    
    def __init__(self):
        super(SimpleExample1,self).__init__(' Thực Tập Cơ Sở ')
    
    #main menu
        self.mainmenu = [
            {'File': [
                {'Open Excel': self.__open, 'icon' : 'img/folder_open.png'},
                '-',
                {'Import': self.__import, 'icon' : 'img/import_icon.png'}
            ]
            }
        ]
    
    #tkinler for messagebox
        root = tk.Tk()
        root.withdraw()
    
    #list
        self._list = ControlList('Danh sách')
        self._list.readonly = True
    
    #1.open file excel và heap sort
        self._file = ControlFile('Chọn file Excel')
        self._butheapsort  = ControlButton('Heap Sort')
        self._butheapsort.icon = 'img/sort_icon.png'
        self._butheapsort.value = self.__heapsort
        self._butloadexcel = ControlButton('Load')
        self._butloadexcel.icon = 'img/load_icon.png'
        self._butloadexcel.value = self.__load
        self._butremoveloadexcel = ControlButton('Hủy bỏ')
        self._butremoveloadexcel.icon = 'img/remove_icon.png'
        self._butremoveloadexcel.value = self.__removeloadexcel
    
    #2.thêm thửa đất
        self._diachi = ControlText('Địa chỉ')
        self._dientich = ControlText('Diện tích')
        self._chusohuuhientai =  ControlText('Chủ sở hữu hiện tại')
        self._loainha = ControlText('Loại nhà')
        self._mucdichsudung = ControlText('Mục đích Sử dụng')
        self._giatien = ControlText('Giá tiền')
        self._but1 = ControlButton('Thêm thửa đất')
        self._but1.value = self.__add
        self._but1.icon = 'img/add_icon.png'
    
    #3.tìm kiếm thử đất và xóa
        #tìm kiếm       
        self._butsearch = ControlButton('Tìm kiếm')
        self._butsearch.icon = 'img/search_icon.png'
        self._butsearch.value = self.__search
        self._timkiem = ControlText('Tìm Kiếm')
        self._checklisttimkiem = ControlCheckBoxList('Chọn tiêu chí tìm kiếm:')
        self._checklisttimkiem.hide()
        self._buttonhideshowtimkiem = ControlButton('Hiển thị tiêu chí')
        self._buttonhideshowtimkiem.value = self._buthideshowtimkiem
        self._buttonhideshowtimkiem.icon = 'img/show.png'
        self._buthuybo = ControlButton('Hủy bỏ')
        self._buthuybo.icon = 'img/remove_icon.png'
        self._buthuybo.value = self._huybo
        #xóa
        self._textxoa = ControlText('Nhập nội dung cần xóa') 
        self._butxoa = ControlButton('Xoá')
        self._butxoa.icon = 'img/delete_icon.png'
        self._butxoa.value = self.__xoa
        self._checklistxoa = ControlCheckBoxList('Chọn tiêu chí xóa:')
        self._checklistxoa.hide()
        self._buttonhideshowxoa = ControlButton('Hiển thị tiêu chí')
        self._buttonhideshowxoa.value = self._buthideshowxoa
        self._buttonhideshowxoa.icon = 'img/show.png'
    
    #4.xuất
        self._directory = ControlDir('Chọn chỗ xuất file excel')
        self._tenfilexuat = ControlText('Tên file xuất')
        self._butxuat = ControlButton('Xuất')
        self._butxuat.icon = 'img/export_icon.png'
        self._butxuat.value = self.__xuat
    
    #5.merge
        self._filemerge = ControlFile('Chọn file Excel cần merge')
        self._butimport = ControlButton('Import')
        self._butimport.icon = 'img/import2_icon.png'
        self._butimport.value = self._import
        self._butmerge = ControlButton('Gộp')
        self._butmerge.icon = 'img/merge_icon'
        self._butmerge.value = self._merge
        self._butmerge.hide()
        self._listmerge = ControlList('Danh sách import')
        self._listmerge.readonly = True
        self._buttonhideshow =  ControlButton('Hiển thị tùy chọn')
        self._buttonhideshow.value = self._buthideshow
        self._buttonhideshow.hide()
        self._buttonhideshow.icon = 'img/show.png'
        self._checklist =  ControlCheckBoxList('Chọn tiêu chí giữ trong danh sách import:')
        self._checklist.hide()
        self._buttonremovemerge =  ControlButton('Hủy bỏ')
        self._buttonremovemerge.value = self._remove
        self._buttonremovemerge.icon = 'img/remove_icon.png'
        self._buttonremovemerge.hide()
    
    #formset as layout
        self.formset = [
            {
                '1.Mở File và Heap Sort': [' ','_file',' ',
                (' ','_butloadexcel','_butremoveloadexcel','_butheapsort',' '),' '],
                
                '2.Thêm': [' ','_diachi', '_dientich', '_chusohuuhientai',
                 '_loainha', '_mucdichsudung', '_giatien',' ',(' ', '_but1', ' '),' '],
                
                '3.Tìm kiếm và Xóa': [' ', '_textxoa',' ',(' ', '_butxoa','_buttonhideshowxoa','_checklistxoa', ' '),
                 ' ','_timkiem', ' ', (' ', '_butsearch','_buttonhideshowtimkiem','_checklisttimkiem','_buthuybo',' '), ' '],
                
                '4.Xuất': [' ','_directory',' ', '_tenfilexuat',' ', (' ', '_butxuat', ' '),' '],
                
                '5.Merge danh sách': ['_filemerge',(' ','_butimport','_butmerge','_buttonremovemerge',
                                                 '_buttonhideshow','_checklist',' '),'_listmerge'],
            }
            , '', '', '_list'
            ]
 
 #event for mainmenu 
    def __open(self): 
        self._file.click()
    def __import(self): 
        self._filemerge.click()
 
 #event tab 1
    #event for _butremoveloadexcel
    def __removeloadexcel(self):
        if not values :
          messagebox.showwarning("Warning", "Không có thông tin cần loại bỏ")
        else :
         values.clear()
         fsqc.clear()
         self._refresh()
    #event for _butheapsort
    def __heapsort(self): 
     if self._list.rows_count <= 1 :
         messagebox.showwarning("Warning","không có list để sort")
     else :
       heap_sort()
       self._refresh()
    #event for load button
    def __load(self): 
     if not self._file.value  :
         tk.messagebox.showwarning("Warning", "Đường dẫn trống" )
     else:
        try:
          if self._file.value != '' :
             path = self._file.value
             read(path)
             self._list.value = [values_name]
             n = 0
             for i in range(int(len(values) / numberofcols[0])):
                 self._list.__add__(values[n:n + numberofcols[0]])
                 n = n + numberofcols[0]
             if self._checklistxoa.count < 1:
                 for s in range(0, len(values_name)):
                     self._checklistxoa.__add__((values_name[s]))
             if self._checklisttimkiem.count < 1:
                 for s in range(0, len(values_name)):
                     self._checklisttimkiem.__add__((values_name[s]))
        except:
          tk.messagebox.showwarning("Warning", "Không thể đọc file khác excel hoặc đường dẫn không đúng")
  
  #event tab 2
    #event for thêm button
    def __add(self): 
      var = str(self._diachi.value).strip().split(',')
      var2 = var[0].split('/')
      var3 = var2[0]
      if self._list.rows_count < 1  :
          messagebox.showwarning("Warning", "Không có list để thêm vào")
      elif len(var3) == 0 \
              or (not var3[0].isdigit() and len(var3)  == 1 ) \
              or ( not var3[0:(len(var3) -1 )].isdigit() and len(var3) > 1 ) :
          messagebox.showwarning("Warning", "Địa chỉ không hợp lệ" )
      elif not str(self._dientich.value).strip().isnumeric()  :
          messagebox.showwarning("Warning", "Diện tích không hợp lệ")
      elif not str(self._chusohuuhientai.value).strip()  :
          messagebox.showwarning("Warning", "Chủ sở hữu trống")
      elif not str(self._loainha.value).strip():
          messagebox.showwarning("Warning", "loại nhà trống")
      elif not str(self._mucdichsudung.value).strip() :
          messagebox.showwarning("Warning", "mục đích sử dụng trống")
      elif not str(self._giatien.value).strip() :
          messagebox.showwarning("Warning", "giá tiền trống")
      else :
        index = self._list.rows_count
        values.append(index)
        values.append(str(self._diachi.value))
        values.append(str(self._dientich.value))
        values.append(str(self._chusohuuhientai.value))
        values.append(str(self._loainha.value))
        values.append(str(self._mucdichsudung.value))
        values.append(str(self._giatien.value))
        if var3.isdigit():
         fsqc.append(int(var3[0:(len(var3))]))
        else :
         fsqc.append(int(var3[0:(len(var3) - 1)]))
        heap_sort()
        self._refresh()
 
 #event tab 3
    #search  :
    def __search(self): 
     if self._list.rows_count <= 1:
            messagebox.showwarning("Warning", "Danh sách rỗng")
     elif not self._timkiem.value:
            messagebox.showwarning("Warning", "Vui lòng nhập nội dung tìm kiếm")
     elif self._checklisttimkiem.selected_row_index  == -1 :
         messagebox.showwarning("Warning", "Vui lòng chọn tiêu chí cần xóa")
         self._checklisttimkiem.show()
         self._buttonhideshowtimkiem.icon = 'img/hide_icon.png'
         self._buttonhideshowtimkiem.label = 'Ẩn tiêu chí'
     else :
      self._refresh()
      s = 1
      while s < self._list.rows_count:
       if not (str(self._timkiem.value).strip()) in str(self._list.get_value(self._checklisttimkiem.selected_row_index,s)) : 
          self._list.__sub__(s)
          s = s -1
       s = s + 1
    def _huybo(self):
        self._refresh()
    def _buthideshowtimkiem(self):
        if not values_name :
            tk.messagebox.showwarning("Warning", "Không có list để chọn tiêu chí")
        elif   str(self._buttonhideshowtimkiem.label) == 'Ẩn tiêu chí':
            self._checklisttimkiem.hide()
            self._buttonhideshowtimkiem.icon = 'img/show.png'
            self._buttonhideshowtimkiem.label = 'Hiển thị tiêu chí'
        elif  str(self._buttonhideshowtimkiem.label) == 'Hiển thị tiêu chí' :
            self._checklisttimkiem.show()
            self._buttonhideshowtimkiem.icon = 'img/hide_icon.png'
            self._buttonhideshowtimkiem.label = 'Ẩn tiêu chí'
    #delete
    def __xoa(self): 
     if self._list.rows_count <= 1:
            messagebox.showwarning("Warning", "Danh sách rỗng")
     elif not self._textxoa.value :
         messagebox.showwarning("Warning", "Vui lòng nhập nội dung cần xóa")
     elif self._checklistxoa.selected_row_index  == -1 :
         messagebox.showwarning("Warning", "Vui lòng chọn tiêu chí cần xóa")
         self._checklistxoa.show()
         self._buttonhideshowxoa.icon = 'img/hide_icon.png'
         self._buttonhideshowxoa.label = 'Ẩn tiêu chí'
     else :
      result = messagebox.askokcancel('Warning', 'Bạn có chắc muốn xóa?')
      startvaluescount = len(values)
      if result == 1:
        s = 1
        while s < len(values):
           if (str(self._textxoa.value).strip()) in str(values[s + self._checklistxoa.selected_row_index - 1]):            
               del fsqc[s//7]
               del values[(s - 1):(s  + 6)]
               s = s - 7
           s = s + 7
        self._refresh()
      if startvaluescount > len(values) :
          messagebox.showinfo("Sucess!!", "Đã xóa dữ liệu thành công")
          self._checklistxoa.hide()
          self._buttonhideshowxoa.icon = 'img/show.png'
          self._buttonhideshowxoa.label = 'Hiển thị tiêu chí'
      else :
          messagebox.showinfo("Opps", "Nội dung cần xóa không có trong cột tiêu chí trong danh sách")
    def _buthideshowxoa(self):
        if not values_name :
            tk.messagebox.showwarning("Warning", "Không có list để chọn tiêu chí")
        elif   str(self._buttonhideshowxoa.label) == 'Ẩn tiêu chí':
            self._checklistxoa.hide()
            self._buttonhideshowxoa.icon = 'img/show.png'
            self._buttonhideshowxoa.label = 'Hiển thị tiêu chí'
        elif  str(self._buttonhideshowxoa.label) == 'Hiển thị tiêu chí' :
            self._checklistxoa.show()
            self._buttonhideshowxoa.icon = 'img/hide_icon.png'
            self._buttonhideshowxoa.label = 'Ẩn tiêu chí'
  #event tab 4
    #event _butxuat
    def __xuat(self): 
     # kiểm tra đường dẫn
     if not os.path.isdir(self._directory.value): 
            messagebox.showwarning("Warning", "đường dẫn ko có")
     elif not self._tenfilexuat.value:
            messagebox.showwarning("Warning", "tên file rỗng")
     elif not values and not values_name:
            messagebox.showwarning("Warning", "không có dữ liệu để xuất")
     else:
        try:
            os.makedirs(self._tenfilexuat.value)
            os.rmdir(self._tenfilexuat.value)
            if os.path.isfile(self._directory.value + '/' + self._tenfilexuat.value + '.xls'):
                result = messagebox.askokcancel('Warning', 'File đã tồn tại bạn có muốn ghi đè lên  ?')
                if result == 1:
                    write(self._directory.value, self._tenfilexuat.value)
                    myfile = Path(self._directory.value + '/' + self._tenfilexuat.value + '.xls')
                    if myfile.is_file():
                        messagebox.showinfo("Sucess!!", "Đã xuất file thành công")
            else:
                result = messagebox.askokcancel('Warning', 'Bạn có chắc muốn xuất?')
                if result == 1:
                    write(self._directory.value, self._tenfilexuat.value)
                    myfile = Path(self._directory.value + '/' + self._tenfilexuat.value + '.xls')
                    if myfile.is_file():
                        messagebox.showinfo("Sucess!!", "Đã xuất file thành công")
        except OSError:
            messagebox.showwarning("Warning", "Tên file không hợp lệ hoặc đang được mở bởi ứng dụng khác")
 
 #event tab 5
    #event _butmerge
    def _merge(self): 
        if self._list.rows_count < 1:
            messagebox.showwarning("Warning", "Danh sách rỗng")
        else :
          result = messagebox.askokcancel('Warning', 'Bạn có chắc muốn gộp?')
          if result == 1:
            for i in range(1,len(valuesimport) ,7):
               n = False
               for s in range(1,len(values),7) :
                 if valuesimport[i] == values[s] :
                     f = self._checklist.checked_indexes
                     for c in range(0,len(f),1):
                         values[s + int(f[c]) -1 ] = valuesimport[i + int(f[c]) -1]
                     n = True
               if not n :
                   fsqc.append(fsqcimport[int(i/7)])
                   for s in range(i-1,i+6) :
                     values.append(valuesimport[s])
            self._refresh()
            for i in range(0, self._listmerge.rows_count):
                self._listmerge.__sub__(i)
                for j in range(0, self._listmerge.rows_count):
                    self._listmerge.__sub__(j)
            self._clearimportdata()
            self._checklist.hide()
            self._buttonhideshow.icon = 'img/show.png'
            self._buttonhideshow.label = 'Hiển thị tùy chọn'
            self._buttonremovemerge.hide()
            self._butmerge.hide()
            self._buttonhideshow.hide()
            tk.messagebox.showinfo("Success", "Đã merge thành công")
    #event _buttonremovemerge
    def _remove(self):
     if self._listmerge.rows_count < 1 :
         tk.messagebox.showwarning("Warning", "Đã xóa hết!")
     else:
        for i in range(0, self._listmerge.rows_count):
            self._listmerge.__sub__(i)
            for j in range(0, self._listmerge.rows_count):
                self._listmerge.__sub__(j)
        self._clearimportdata()
        self._checklist.clear()
        self._buttonremovemerge.hide()
        self._buttonhideshow.hide()
        self._checklist.hide()
        self._butmerge.hide()
    #event  _buttonhideshow
    def _buthideshow(self):
        if   str(self._buttonhideshow.label) == 'Ẩn tùy chọn':
            self._checklist.hide()
            self._buttonhideshow.icon = 'img/show.png'
            self._buttonhideshow.label = 'Hiển thị tùy chọn'
        elif  str(self._buttonhideshow.label) == 'Hiển thị tùy chọn' :
            self._checklist.show()
            self._buttonhideshow.icon = 'img/hide_icon.png'
            self._buttonhideshow.label = 'Ẩn tùy chọn'
    #event _buttonimport
    def _import(self): 
        if not self._filemerge.value:
            tk.messagebox.showwarning("Warning", "Đường dẫn trống")
        else:
                path = self._filemerge.value
                try:
                    importexcel(path)
                    self._listmerge.value = [values_nameimport]
                    n = 0
                    for i in range(int(len(valuesimport) / numberofcolsimport[0])):
                        self._listmerge.__add__(valuesimport[n:n + numberofcolsimport[0]])
                        n = n + numberofcolsimport[0]
                    if self._checklist.count < 1:
                        for s in range(0, len(values_nameimport)):
                            self._checklist.__add__((values_nameimport[s], True))
                    if self._listmerge and not self._buttonhideshow.visible:
                        if str(self._buttonhideshow.label) == 'Ẩn tùy chọn':
                            self._buttonhideshow.icon = 'img/show.png'
                            self._buttonhideshow.label = 'Hiển thị tùy chọn'
                    self._buttonhideshow.show()
                    self._buttonremovemerge.show()
                    self._butmerge.show()
                except:
                    tk.messagebox.showwarning("Warning", "Không thể đọc file khác excel hoặc đường dẫn không đúng")
 #reusable function
    def _refresh(self):
        for i in range(1, self._list.rows_count):
            self._list.__sub__(i)
            for j in range(1, self._list.rows_count):
                self._list.__sub__(j)
        n = 0
        for i in range(int(len(values) / numberofcols[0])):
            self._list.__add__(values[n:n + numberofcols[0]])
            n = n + numberofcols[0]
        # update STT
        for s in range(1, self._list.rows_count):  
            values[(s - 1) * 7] = s
            self._list.set_value(0, s, s)
    def _clearimportdata(self):
            fsqcimport.clear()
            valuesimport.clear()
            sqcimport.clear()
            numberofcolsimport.clear()
            values_nameimport.clear()
            self._checklist.clear()
if __name__ == "__main__":   pyforms.start_app(SimpleExample1)