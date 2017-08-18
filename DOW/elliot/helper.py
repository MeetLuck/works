import colorama
from colorama import Fore as fg, Back as bg, Style as stl
colorama.init(autoreset=True)

def compute_percent(start,end):
    if start is None or end is None: return None
    percent  = 100.0*(end-start)/start
    percent  = '{percent:2.1f}%'.format(percent=percent)
    return percent

def set_name(level,No): # <i> -> (i) -> i -> I -> (I) -> [I] -> {I}
    assert isinstance(No,int),'{No} must be 1,2,3,...8'.format(No=No)
    literals = 'unused','I','II','III','IV','V','A','B','C'
    if   level == +3: name = '{' + literals[No]+ '}'        # Cycle
    elif level == +2: name = '[' + literals[No]+ ']'        # Grand
    elif level == +1: name = '(' + literals[No]+ ')'        # Super
    elif level ==  0: name =       literals[No]             # Primary
    elif level == -1: name =       literals[No].lower()     # intermediate 
    elif level == -2: name = '('+literals[No].lower()+')'   # minor
    elif level == -3: name = '<'+literals[No].lower()+'>'   # minutes
    else:             name = 'Undefined'
    return name

def set_name2(level,No): 
    if   level == +3: name = 'Cycle wave '        + set_name(level,No)    # Cycle
    elif level == +2: name = 'Grand wave '        + set_name(level,No)    # Grand
    elif level == +1: name = 'Super wave '        + set_name(level,No)    # Super
    elif level ==  0: name = 'Primary wave '      + set_name(level,No)    # Primary
    elif level == -1: name = 'Intermediate wave ' + set_name(level,No)    # intermediate 
    elif level == -2: name = 'Minor wave '        + set_name(level,No)    # minor
    elif level == -3: name = 'Minute wave '       + set_name(level,No)    # minutes
    else:             name = 'Undefined wave'
    return name

def overview(wave):
    print wave
    if wave.has_subwaves:
        print fg.WHITE + '-'*70
        for subwave in wave.subwaves: print subwave
    else:
        pass
        #print '{:^10}'.format('N/A')
def get_fibs(wave):
    fibs = wave.fib(2,1), wave.fib(3,1), wave.fib(4,3), wave.fib(5,1), wave.fib20(), wave.fib238()
    fibs_list = list()
    for fib in fibs:
        fibs_list.append(round(fib,2))
    return fibs_list
def get_prediction(wave):
    p3_from_p1  = wave.predict_wave3(fib_ratio=2.0)
    p5_from_p1  = wave.predict_wave5from1(fib_ratio=2.382)
    p5_from_p2  = wave.predict_wave5from2()
    p5_from_p3  = wave.predict_wave5from3(fib_ratio=0.382)
    p5_from_p4  = wave.predict_wave5from4(fib_ratio=1.0)
    p5_from_p4s  = wave.predict_wave5from4s(fib_ratio=1.0)
    return int(p3_from_p1),int(p5_from_p1),int(p5_from_p2),int(p5_from_p3),int(p5_from_p4),int(p5_from_p4s)

def print_fibs(wave):
    if not wave.has_subwaves:
        print_subtitle(fg.GREEN,'No subwaves, Fibonacci rato not avaiable for wave',wave.name)
        return 
    print_subtitle(fg.GREEN,'Fibonacci rato for wave',wave.name)
    fib21,fib31,fib43,fib51,fib20,fib238 = get_fibs(wave)
    print '    II/I : {fib21:<9.2f} III/I : {fib31:<8.2f} IV/III : {fib43:<8.2f} V/I : {fib51:<8.2f}'\
          .format(fib31=fib31,fib21=fib21,fib43=fib43,fib51=fib51)
    print '    fib2.0 :{fib20:5.2f}    fib2.38 :{fib238:5.2f}'.format(fib20=fib20,fib238=fib238)

def print_fibs_interwaves(wave):
    print_subtitle(fg.GREEN,'Fibonacci ratio between inter-waves for', 'e.g. III.i/I.i') 
    sub_31to11 = wave.fibs_interwaves(3,1,1,1)
    sub_31to13 = wave.fibs_interwaves(3,1,1,3)
    sub_51to11 = wave.fibs_interwaves(5,1,1,1)
    sub_33to13 = wave.fibs_interwaves(3,3,1,3)
    sub_53to13 = wave.fibs_interwaves(5,3,1,3)
    print_data1(fg.WHITE,'III(1)/I(3)', sub_31to13)    
    print_data1(fg.WHITE,'III(1)/I(1)', sub_31to11)    
    print_data1(fg.WHITE,'V(1)/I(1)  ', sub_51to11)    
    print_data1(fg.WHITE,'III(3)/I(3)', sub_33to13)    
    print_data1(fg.WHITE,'V(3)/I(3)  ', sub_53to13)    

def print_predictions(wave):
    #--- predict wave 5 ---#
    if not wave.has_subwaves:
        print_subtitle(fg.YELLOW,'No subwaves, cannot predict waves for wave',wave.name)
        return
    print_subtitle(fg.YELLOW,'predict p3 and p5 for wave',wave.name)
    p3_from_p1,p5_from_p1,p5_from_p2,p5_from_p3,p5_from_p4,p5_from_p4s = get_prediction(wave)
    print_data2(fg.CYAN, 'p3 -> 2.0*i         ', p3_from_p1, 'p3-p2', p3_from_p1 - wave.ii.end,compute_percent(wave.ii.end,p3_from_p1) )
    print_data2(fg.WHITE,'p5 -> 2.382*i       ', p5_from_p1, 'p5-p0', p5_from_p1 - wave.start,compute_percent(wave.start, p5_from_p1) )
    print_data2(fg.CYAN, 'p5 -> p3 + (p2-p0)  ', p5_from_p2, 'p5-p0', p5_from_p2 - wave.start,compute_percent(wave.start, p5_from_p2) )
    print_data2(fg.WHITE,'p5 -> p3 + 0.382*i  ', p5_from_p3, 'p5-p0', p5_from_p3 - wave.start,compute_percent(wave.start, p5_from_p3) )
    print_data2(fg.CYAN, 'p5 -> p4 + 1.0*i    ', p5_from_p4, 'p5-p0', p5_from_p4 - wave.start,compute_percent(wave.start, p5_from_p4) )
    print_data2(fg.CYAN, 'p5 -> p4 + 0.618*iii    ', p5_from_p4s, 'p5-p0', p5_from_p4s - wave.start,compute_percent(wave.start, p5_from_p4s) )

def print_data1(fg,header1, data1):
    print fg + '    {} : {:5.2f}'.format(header1,data1)

def print_data2(fg,header1, data1,header2,data2,data3):
    print fg + '    {} : {:5.2f}   {} : {:>7.2f} {:>7}'.format(header1,data1,header2, data2, data3)

def print_title(fgcolor,title):
    print fgcolor + bg.WHITE +'\n{:^70}\n'.format(title)

def print_subtitle(color,title,name):
    print color + '\n{title} {name}'.format(title=title,name=name)
