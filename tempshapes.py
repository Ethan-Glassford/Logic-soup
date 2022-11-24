#Note:
# I am undure how closely we are able to follow Prof. Muise's code. I will preemtively create 
# these following his code in the interest of time.
#
# I also need help interpreting exactly what his code is doing

def gen_I():
    shapes = [] #create a list of possible orientations
    shapes.append("""
                    XXXX
    """)
    shapes.append("""
                    X
                    X
                    X
                    X
    """)
    return shapes
def gen_O():
    shapes = [] #create a list of possible orientations
    shapes.append("""
                    XX
                    XX
    """)
    return shapes
def gen_J():
    shapes = [] #create a list of possible orientations
    shapes.append("""
                    -X
                    -X
                    XX
    """)
    shapes.append("""
                    XXX
                    --X
    """)
    shapes.append("""
                    XX
                    X-
                    X-
    """)
    shapes.append("""
                    X--
                    XXX
    """)
    return shapes
def gen_L():
    shapes = [] #create a list of possible orientations
    shapes.append("""
                    X-
                    X-
                    XX
    """)
    shapes.append("""
                    XXX
                    x--
    """)
    shapes.append("""
                    XX
                    -X
                    -X
    """)
    shapes.append("""
                    --X
                    XXX
    """)
    return shapes
def gen_S():
    shapes = [] #create a list of possible orientations
    shapes.append("""
                    -XX
                    XX-
    """)
    shapes.append("""
                    X-
                    XX
                    -X
    """)
    return shapes
def gen_Z():
    shapes = [] #create a list of possible orientations
    shapes.append("""
                    XX-
                    -XX
    """)
    shapes.append("""
                    -X
                    XX
                    X-
    """)
    return shapes
def gen_T():
    shapes = [] #create a list of possible orientations
    shapes.append("""
                    XXX
                    -X-
    """)
    shapes.append("""
                    X-
                    XX
                    X-
    """)
    shapes.append("""
                    -X-
                    XXX
    """)
    shapes.append("""
                    -X
                    XX
                    -X
    """)
    return shapes

