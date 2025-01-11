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
    add_code += "[<<<<<[" # W0(=D1) != 0 and W[-1] != 0 then undo carries in D2,3
    add_code += ">>-<-"
    add_code += "<" + SET_ZERO # set W[-1] = 0 so no more undo-carries done (and exit loop)
    add_code += "]" # exit W[-1]
    add_code += ">>>>>" + SET_ZERO
    add_code += "]" # exit W0

    add_code += copy_Dx_to_W0(2)
    add_code += "[<<<<<[" # W0(=D2) != 0 and W[-1] != 0 then undo carries in D3
    add_code += ">-"
    add_code += "<" + SET_ZERO # set W[-1] = 0 so no more undo-carries done (and exit loop)
    add_code += "]" # exit W[-1]
    add_code += ">>>>>" + SET_ZERO
    add_code += "]" # exit W0


    return add_code

def translation_sub_full():
    sub_code = "<<<<<" + SET_ZERO + "+>>>>>" # set W[-1] = 1, used so only 1 undo carry block is run
    sub_code += copy_Dx_to_W0(0)
    sub_code += "[" # if W0(=D0) != 0 then undo carry on D1,2,3
    sub_code += "<<+<+<+"
    sub_code += "<" + SET_ZERO + ">>>>>" # set W[-1] = 0 to prevent future undos
    sub_code += SET_ZERO
    sub_code += "]" # exit W0

    sub_code += copy_Dx_to_W0(1)
    sub_code += "[<<<<<[" # if W0(=D1) !=0 and havent already undone, undo carry on D2,3
    sub_code += ">>+<+<"
    sub_code += SET_ZERO # set W[-1] = 0 to prevent future carries
    sub_code += "]"
    sub_code += ">>>>>" + SET_ZERO # zero W0 to exit loop
    sub_code += "]" # exit on W0

    sub_code += copy_Dx_to_W0(2)
    sub_code += "[<<<<<[" # if W0(=D2) !=0 and havent already undone, undo carry on D3
    sub_code += ">+<"
    sub_code += SET_ZERO # zero W[-1] to exit loop
    sub_code += "]"
    sub_code += SET_ZERO + ">>>>>" # zero W0 to exit loop
    sub_code += "]" # exit W0

    sub_code += "<-<-<-<->>>>" # do actual subtraction. Has to be done after undo-carries because special case is when value is 0 BEFORE subtracting
    return sub_code

ADVANCE_COLON = ">>>>>>>>>>>>>>:<<<<<<<<<<<<<<"
AROUND_COLON = ">>>>>>>:<<<<<<<"

def gen_add_tests():
    result = ">"
    result += ">>>>"
    for i in range(0,16):
        result += "<<<<"
        for place in range (0,4):
            if ((i >> place) & 1):
                result += "->"
            else:
                result += "+" * 5 + ">"
        result += AROUND_COLON
        result += translation_add_full()
        result += AROUND_COLON
        result += "<[-]" * 4 + ">" * 4 + "\\"
    return result

# actual code
result = gen_add_tests()


with open("output.bf", "w") as file:
    file.write(result)

print(result)