import xlwt as xl
from helper import get_fibs,get_prediction,compute_percent

def get_style(name='Arial',height=210, color='black',bold=False,pattern='solid',fgcolor='gray25', vertical='center', horizontal='right'):
    font = 'font: name {}, height {}, color {}, bold {};'.format(name,str(height),color,bold)
    pattern = 'pattern: pattern {pattern}, fore_color {fgcolor};' .format(pattern=pattern,fgcolor=fgcolor)
    align = 'align: vertical {vertical}, horizontal {horizontal};'.format(vertical=vertical,horizontal=horizontal)
    return font+pattern+align

def get_sheetname(wavename2):
    literal = '[]{}()<>'
    sheetname = wavename2[:]
    for ch in literal:
        sheetname = sheetname.replace(ch,'')
    return sheetname

START_ROW = 2
DEFAULT_STYLE = xl.easyxf( get_style() )

class WaveToXls(object):

    def __init__(self,book,wave):
        '''*** one sheet for wave and subwaves ***'''
        sheetname = get_sheetname(wave.name2)
        self.sheet = book.add_sheet(sheetname,True)
        self.sheet.show_grid = False
        self.row_no = START_ROW
        self.init_sheet()
        #self.create(wave)
        #book.save(name)

    def nextline(self,no=1):
        self.row_no += no

    def init_sheet(self):
        for r in range(80*2):
            for c in range(20):
                self.sheet.row(r).write(c,'',DEFAULT_STYLE)
                self.sheet.col(c).width = 275*12
    def overview(self,wave):
        def write(row,wave,style):
            sp = ' '
            row.write(1,str(wave.name) + sp, style)
            row.write(2,str(wave.start), style)
            row.write(3,str(wave.end) + sp*2 , style )
            row.write(4,str(wave.size) + sp, style)
            row.write(5,str(wave.percent)+ sp, style)
            self.nextline()
        # printing title
        row_title = self.sheet.row(self.row_no)
        row_title.write(3,wave.name2,xl.easyxf(get_style(height=240,color='dark_red',bold=True,horizontal='center')) )
        self.nextline()
        # main wave 
        style = xl.easyxf( get_style(height=210,bold=True) + 'borders: bottom thin;')
        write(self.sheet.row(self.row_no),wave,style)
        # subwave 1,2,3,4,5
        if not wave.has_subwaves: return
        for subwave in wave.subwaves:
            write(self.sheet.row(self.row_no),subwave,DEFAULT_STYLE)

    def fibs(self,wave):
        style = xl.easyxf( get_style(height=210,color='green',bold=True,horizontal='center') )
        if not wave.has_subwaves:
            self.sheet.row(self.row_no).write(3,'No subwaves, Fibonacci rato not avaiable for wave',style)
            return 
        row_title = self.sheet.row(self.row_no)
        row_title.write(3, 'Fibonacci ratio for wave {}'.format(wave.name), style)
        self.nextline()
        def write(row,li,style):
            for i,value in enumerate(li):
                row.write(i+1, value,style)
            self.nextline()
        row_head = self.sheet.row(self.row_no)
        row_data = self.sheet.row(self.row_no+1)
        style = xl.easyxf( get_style(height=210,bold=True,horizontal='center') + 'borders: bottom thin;')
        data =  'II/I', ' III/I', 'IV/III', 'V/I','fib2.0','fib2.38'
        write(row_head,data,style)
        style = xl.easyxf( get_style(horizontal='center') )
        write(row_data,get_fibs(wave),style)

    def predict(self,wave):
        style = xl.easyxf( get_style(height=210,color='green',bold=True,horizontal='center') )
        if not wave.has_subwaves:
            self.sheet.row(self.row_no).write(3,'No subwaves, cannot predict waves for wave',style)
            return 
        row_title = self.sheet.row(self.row_no)
        row_title.write(3, 'Predict p3 and p5 for {}'.format(wave.name), style)
        self.nextline()
        p31,p51,p52,p53,p54,p54s = get_prediction(wave)
        style_n = xl.easyxf( get_style(bold=False,horizontal='center'))# + 'borders: bottom thin;')
        style_hl = xl.easyxf( get_style(bold=True,horizontal='center'))# + 'borders: bottom thin;')
        def write(title1,title2,price1,price2,price3,style=style_n):
            row = self.sheet.row(self.row_no)
            row.write(1,title1,style); row.write(2,title2,style); row.write(3,price1,style); row.write(4,price2,style)
            row.write(5,price3,style)
            self.nextline()
        style_20 = xl.easyxf( get_style(bold=True,horizontal='center') + 'borders: bottom thin;')
        write('p3','2.0*i',     p31,p31-wave.ii.end,compute_percent(wave.ii.end,p31),style=style_20)
        write('p5','2.382*i',   p51,p51-wave.start,compute_percent(wave.start,p51))
        write('p5','p3+(p2-p0)',p52,p52-wave.start,compute_percent(wave.start,p52))
        write('p5','p3+0.382*i',p53,p53-wave.start,compute_percent(wave.start,p53),style=style_hl)
        write('p5','p4+1.0*i',  p54,p54-wave.start,compute_percent(wave.start,p54))
        write('p5','p4+0.618*iii',  p54s,p54s-wave.start,compute_percent(wave.start,p54s))
