def get_instruction():
    instructions = [
            'Propery initialize the screen',
            'Begin color support'
            ]
    codes = [None]*2
    codes[0] = [
            'screen = curses.initscr()',
            'curses.noecho()',
            'curses.cbreak()',
            'curses.curs_set(0)' ]
    codes[1] = [
            'if curses.has_colors():',
            '   curses.start_color()' ]
    return zip(instructions,codes)

if __name__ == '__main__':
    t = get_instruction()
    print t
    for instruction, code in t:
        print instruction
        print '\n'.join(code)
        print


