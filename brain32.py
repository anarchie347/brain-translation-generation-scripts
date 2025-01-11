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

def translation_add_full(): # starts W0, ends W0
    add_code = "<+<+<+<+" # default carry on all D because conditions can only be done based on NOT zero
    add_code += "<" + SET_ZERO + "+>>>>>" # set W[-1] = 1, stores 1 if no undo-carries have been done. Prevents undoing multiple times
    add_code += copy_Dx_to_W0(0)
    add_code += "[" # if W0(=D0) != 0 then undo carries on W1,2,3
    add_code += "<<-<-<-"
    add_code += "<" + SET_ZERO + ">>>>>" + SET_ZERO # set W[-1] = 0 so no more undo-carries done, sets W0 = 0 to exit loop
    add_code += "]"

    add_code += copy_Dx_to_W0(1)
    add_code += "[<<<<<[>>>>>" # W0(=D1) != 0 and W[-1] != 0 then undo carries in D2,3
    add_code += "<<<-<-"
    add_code += "<" + SET_ZERO # set W[-1] = 0 so no more undo-carries done (and exit loop)
    add_code += "]" # exit W[-1]
    add_code += ">>>>>" + SET_ZERO
    add_code += "]" # exit W0

    add_code += copy_Dx_to_W0(2)
    add_code += "[<<<<<[>>>>>" # W0(=D2) != 0 and W[-1] != 0 then undo carries in D3
    add_code += "<<<<-"
    add_code += "<" + SET_ZERO # set W[-1] = 0 so no more undo-carries done (and exit loop)
    add_code += "]" # exit W[-1]
    add_code += ">>>>>" + SET_ZERO
    add_code += "]" # exit W0


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
result = ""


with open("output.bf", "w") as file:
    file.write(result)

print(result)