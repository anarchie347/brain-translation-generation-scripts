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
    add_code += "[" # if W0(=D0) != 0 then undo carries on D1,2,3
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

def translation_add_1(): #start W0, end W0
    add_code = "<<+<+<+" # default carry D2,3, increment D1
    add_code += "<" + SET_ZERO + "+>>>>>" # set W[-1] = 1, stores 1 if no undo carries have been done, prevents undoing multiple times
    add_code += copy_Dx_to_W0(1)
    add_code += "[" #if W0(=D1) != 0 then undo carries on D2,3
    add_code += "<<<-<-"
    add_code += "<" + SET_ZERO + ">>>>>" + SET_ZERO # set W[-1] = 0 so no more undo carries, sets W0 = 0 to exit loop
    add_code += "]"

    add_code += copy_Dx_to_W0(2)
    add_code += "[<<<<<[" #W0(=D2) != 0 and W[-1] != 0 then undo carries in D3
    add_code += ">-"
    add_code += "<" + SET_ZERO # set W[-1] = 0 so no more undo carries done (and exit loop)
    add_code += "]" #exit W[-1]
    add_code += ">>>>>" + SET_ZERO # to exit loop at W0
    add_code += "]" #exit W0

    return add_code

def translation_add_2(): # starts W0, ends W0
    add_code = "<<<+<+" #default carry on D3, increment D2
    add_code += ">>>>" #return W0
    add_code += copy_Dx_to_W0(2)
    add_code += "[" #if W0(=D2) != 0, then undo D3 carry
    add_code += "<<<<->>>>" # undo D3 carry, return W0
    add_code += "]" # exit W0

    return add_code

# add_3 is not needed as no carry logic is required

def translation_sub_full(): # starts W0, ends W0
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
    sub_code += SET_ZERO # set W[-1] = 0 to prevent future undos
    sub_code += "]"
    sub_code += ">>>>>" + SET_ZERO # zero W0 to exit loop
    sub_code += "]" # exit on W0

    sub_code += copy_Dx_to_W0(2)
    sub_code += "[<<<<<[" # if W0(=D2) !=0 and havent already undone, undo carry on D3
    sub_code += ">+<"
    sub_code += SET_ZERO # zero W[-1] to exit loop
    sub_code += "]"
    sub_code += ">>>>>" + SET_ZERO # zero W0 to exit loop
    sub_code += "]" # exit W0

    sub_code += "<-<-<-<->>>>" # do actual subtraction. Has to be done after undo-carries because special case is when value is 0 BEFORE subtracting
    return sub_code

def translation_sub_1():
    sub_code = "<<<<<" + SET_ZERO + ">>>>>" # Set W[-1] = 1, used so only 1 undo carry block is run
    sub_code += copy_Dx_to_W0(1)
    sub_code += "[" # if W0(=D0) != 0 then undo carry on D2,3
    sub_code += "<<<+<+" # undo carries
    sub_code += "<" + SET_ZERO + ">>>>>" # set W[-1] = to prevent future undos
    sub_code += SET_ZERO
    sub_code += "]" # exit on W0

    sub_code += copy_Dx_to_W0(2)
    sub_code += "[<<<<<[" # if W0(=D2) != 0 and havent already undone, undo carry on D3
    sub_code += ">+<" # undo D3 carry, return to W[-1]
    sub_code += SET_ZERO # set W[-1] = 0 to prevent future undos
    sub_code += "]" # exit on W[-1]
    sub_code += ">>>>>" + SET_ZERO # set W0 to exit loop
    sub_code += "]" # exit on W0

    sub_code += "<<-<-<->>>>" # do actual subtraction. has to be done after undo-carries because special case is when value is 0 BEFORE subtracting

    return sub_code

def translation_sub_2():
    sub_code = copy_Dx_to_W0(2)
    sub_code += "[" # if W0(=D0) != 0 then undo carry on D3
    sub_code += "<<<<+>>>>" # undo D3 carry
    sub_code += SET_ZERO # zero W0 for loop exit
    sub_code += "]" # exit loop on W0

    sub_code += "<<<-<-" # do actual subtraction. has to be done after undo-carries because special case is whenvalue is 0 BEFORE subtracting

    return sub_code

# Like addition, sub_3 is trivial as no carry logic is needed


def single_cell_zero_check(x):
    check_code = copy_Dx_to_W0(x)
    check_code += "[<<<<<+>>>>>" + SET_ZERO + "]" # if W0(=Dx) != 0, increment W[-1], then zero W0 to exit loop
    return check_code

def translation_open_full(): # starts W0, ends W0 for inside loop. If loop is skipped, pointer is at W[-1]
    open_code = "<<<<<" + SET_ZERO + ">>>>>" # zero W[-1]

    open_code += single_cell_zero_check(0)
    open_code += single_cell_zero_check(1)
    open_code += single_cell_zero_check(2)
    open_code += single_cell_zero_check(3)

    open_code += "<<<<<[>>>>>" # go to W[-1] to run loop condition, then return to W0
    return open_code

def translation_close_full(): # starts W0 if in loop, else W[-1]. exits W0
    close_code = "<<<<<" + SET_ZERO + ">>>>>" # zero W[-1]

    close_code += single_cell_zero_check(0)
    close_code += single_cell_zero_check(1)
    close_code += single_cell_zero_check(2)
    close_code += single_cell_zero_check(3)

    # checks have to also be done just before the ] becausein the resulting brainfuck, the loop jump is to the corresponding *brainfuck* [ which is after the logic to work with the multiple cells representing one brain32 cell, so the logic must also be present here

    close_code += "<<<<<]>>>>>" # go to W[-1] to run condition, return to W0 after loop exit
    return close_code

def translation_open_custom(D3 : int, D2 : int, D1 : int, D0 : int):
    open_code = "<<<<<" + SET_ZERO + ">>>>>"
    if D0 == 1:
        open_code += single_cell_zero_check(0)
    if D1 == 1:
        open_code += single_cell_zero_check(1)
    if D2 == 2:
        open_code += single_cell_zero_check(2)
    if D3 == 3:
        open_code += single_cell_zero_check(3)
    open_code += "<<<<<[>>>>>"

    return open_code

def translation_close_custom(D3: int, D2 : int, D1 : int, D0 : int):
    close_code = "<<<<<" + SET_ZERO + ">>>>>"
    if D0 == 1:
        close_code += single_cell_zero_check(0)
    if D1 == 1:
        close_code += single_cell_zero_check(1)
    if D2 == 1:
        close_code += single_cell_zero_check(2)
    if D3 == 1:
        close_code += single_cell_zero_check(3)

    close_code += "<<<<<]>>>>>"

    return close_code


ADVANCE_COLON = ">>>>>>>>>>>>>>:<<<<<<<<<<<<<<"
AROUND_COLON = ">>>>>>>:<<<<<<<"

# actual code
result = translation_sub_2()


with open("output.bf", "w") as file:
    file.write(result)

print(result)