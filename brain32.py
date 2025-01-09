# See bottome for code that is actually run to start

def ptr_W0_to_Dx(x):
    match x:
        case 0: return "<"
        case 1: return "<<"
        case 2: return "<<<"
        case 3: return "<<<<"

def ptr_Dx_to_W0(x):
    match x:
        case 0: return ">"
        case 1: return ">>"
        case 2: return ">>>"
        case 3: return ">>>>"

def move_patterned(offsets): # takes list of offsets, each relative to the previous
    move_code = "["
    for o in offsets:
        dir = "<" if o < 0 else ">"
        move_code += dir * abs(o)
        move_code += "+" # traverse to all cells and add 1
    
    return_dist = - sum(offsets)
    dir = "<" if return_dist < 0 else ">"
    move_code += dir * abs(return_dist) # get back to start
    move_code += "-]" # decrement starting cell

    return move_code


# actual code
result = ""


with open("output.bf", "w") as file:
    file.write(result)

print(result)