#from xlwt import Workbook,easyxf
import xlwt as xl
# ---------------------------------------------------------------------------------#
# sheet.write_merge(r1, r2, c1, c2, label='', style=<xlwt.Style.XFStyle object>)   #
# ---------------------------------------------------------------------------------#

style = xl.easyxf( 'pattern: pattern solid,fore_color green;'
                   'font: name Arial, color red;'
                   'borders: left thick, right thick, top thick, bottom thick;'
                   'align: vertical center, horizontal center;' )
wb = xl.Workbook()
ws = wb.add_sheet('Merged',True)
ws.write_merge(1,3,1,5,'Merged',style)
ws.show_grid = False
wb.save('merged.xls')
