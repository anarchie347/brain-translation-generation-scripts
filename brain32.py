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
    copy_code += ">>>>>" + SET_ZERO + "<<<<<" # set W1 = 0
    copy_code += ptr_W0_to_Dx(x)
    copy_code += move_patterned([to_W0,5]) # move to W0,W1
    copy_code += ptr_Dx_to_W0(x)
    copy_code += ">>>>>" # to W1
    copy_code += move_patterned([-(to_W0 + 5)]) # move W1 to Dx
    copy_code += "<<<<<" # back to W0

    return copy_code

# problem is carry is undone just before check is done
def translation_add_full_old(): # starts and ends W0
    add_code = "<+<+<+<+>>>>" # add 1 to all D, return to W0
    add_code += copy_Dx_to_W0(0) + "?"
    add_code += "[<<->>" # if W0(=D0) != 0, undo D1 carry
    add_code += copy_Dx_to_W0(1) + "?"
    add_code += "[<<<->>>" # if W0(=D1) != 0 (and prev condition), undo D2 carry
    add_code += copy_Dx_to_W0(2) + "?"
    add_code += "[<<<<->>>>" # if W0(=D2) != 0 (and prev conditions), undo D3 carry
    add_code += SET_ZERO # zero W0 so loops exit
    add_code += "]]]" # exit on W0
    return add_code

# problem with carrys still. this involves carry check before carry is undone which means if a 255 exists anywhere it WILL cause a carry to its right
def translation_add_full_2(): # starts and ends W0
    #add_code = "<-<+<+<+>>>>" # add 1 to all D, return to W0
    add_code = "<+>"
    add_code += copy_Dx_to_W0(0)
    add_code += "[" # if W0(=D0) != 0, undo D1 carry
    add_code += copy_Dx_to_W0(1)
    add_code += "[" # if W0(=D1) != 0 (and prev condition), undo D2 carry
    add_code += copy_Dx_to_W0(2)
    add_code += "[" # if W0(=D2) != 0 (and prev conditions), undo D3 carry
    add_code += SET_ZERO # zero W0 so loops exit
    add_code += "<<<<->>>>]<<<->>>]<<->>]" # exit on W0
    return add_code

def translation_add_full_3():
    # need OR not AND
    # Worst case scenario, code for 8 separate cases, so use extra + or - that will be cancelled out by the scenario also matching a later case
    add_code = "<+<+<+<+>>>>"
    add_code += copy_Dx_to_W0(0)
    add_code += "["
    add_code += "<<-<-<->>>>"
    add_code += SET_ZERO
    add_code += "]"
    add_code += copy_Dx_to_W0(1)
    add_code += "["
    add_code += "<<<-<->>>>"
    add_code += SET_ZERO
    add_code += "]"
    add_code += copy_Dx_to_W0(2)
    add_code += "["
    add_code += "<<<<->>>>"
    add_code += SET_ZERO
    add_code += "]"
    return add_code


def translation_add_full_4():
    # could add perf improvement by using W[-1] instead of W2 or maybe make it so W is on left
    add_code = "<+<+<+<+>>>>" # default carry
    add_code += ">>>>>>>>>>" + SET_ZERO + "+<<<<<<<<<<" # W2 = 1, stores 1 if no undo-carries have been done
    add_code += copy_Dx_to_W0(0)
    add_code += "["
    add_code += "<<-<-<->>>>"
    add_code += SET_ZERO
    add_code += ">>>>>>>>>>" + SET_ZERO + "<<<<<<<<<<"
    add_code += "]"

    add_code += copy_Dx_to_W0(1)
    add_code += "[>>>>>>>>>>[<<<<<<<<<<"
    add_code += "<<<-<->>>>"
    add_code += ">>>>>>>>>>"
    add_code += SET_ZERO
    add_code += "]<<<<<<<<<<"
    add_code += SET_ZERO
    add_code += "]"

    add_code += copy_Dx_to_W0(2)
    add_code += "[>>>>>>>>>>[<<<<<<<<<<"
    add_code += "<<<<->>>>"
    add_code += ">>>>>>>>>>"
    add_code += SET_ZERO
    add_code += "]<<<<<<<<<<"
    add_code += SET_ZERO
    add_code += "]"


    return add_code

def translation_sub_full(): # ive forgotten how loops work
    sub_code = copy_Dx_to_W0(0)
    sub_code += "["
    sub_code += copy_Dx_to_W0(1)
    sub_code += "["
    sub_code += copy_Dx_to_W0(2)
    sub_code += "["
    sub_code += "<<<<->>>>"
    sub_code += SET_ZERO
    sub_code += "]"
    sub_code += "<<<->>>"
    sub_code += SET_ZERO
    sub_code += "]"
    sub_code += "<<->>"
    sub_code += SET_ZERO
    sub_code += "]"
    sub_code += "-"
    return sub_code

ADVANCE_COLON = ">>>>>>>>>>>>>>:<<<<<<<<<<<<<<"
AROUND_COLON = ">>>>>>>:<<<<<<<"



# actual code
result = ">>>>" + translation_sub_full() + AROUND_COLON



with open("output.bf", "w") as file:
    file.write(result)

print(result)