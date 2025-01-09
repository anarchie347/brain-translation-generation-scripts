# See bottome for code that is actually run to start

SET_ZERO = "[-]"

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

def copy_Dx_to_W0(x): # starts and ends at W0
    to_W0 = x + 1 # account for least significant is col 0
    copy_code = SET_ZERO
    copy_code += ptr_W0_to_Dx(x)
    copy_code += move_patterned([to_W0,5]) # move to W0,W1
    copy_code += ptr_Dx_to_W0(x)
    copy_code += ">>>>>" # to W1
    copy_code += move_patterned([-(to_W0 + 5)]) # move W1 to Dx
    copy_code += "<<<<<" # back to W0

    return copy_code

def translation_add_full(): # starts and ends W0
    add_code = "<+<+<+<+>>>>" # add 1 to all D, return to W0
    add_code += copy_Dx_to_W0(0)
    add_code += "[<<->>" # if W0(=D0) != 0, undo D1 carry
    add_code += copy_Dx_to_W0(1)
    add_code += "[<<<->>>" # if W0(=D1) != 0 (and prev condition), undo D2 carry
    add_code += copy_Dx_to_W0(2)
    add_code += "[<<<<->>>>" # if W0(=D2) != 0 (and prev conditions), undo D3 carry
    add_code += SET_ZERO # zero W0 so loops exit
    add_code += "]]]" # exit on W0

ADVANCE_COLON = ">>>>>>>>>>>>>>:<<<<<<<<<<<<<<"
AROUND_COLON = ">>>>>>>:<<<<<<<"

# actual code


with open("output.bf", "w") as file:
    file.write(result)

print(result)