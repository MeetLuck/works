g = -99
def outer():
    g = +99
    def inner():
        global g
        g += 1
        return g
    return inner()
outer()


