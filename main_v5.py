"""
CMSC 129 - Programming Exercise: Syntax Analyzer

This program is a portion of the Programming Project, a working compiler.
The program is a simple parser for a custom programming language. 
The parser performs syntax analysis and semantic analysis of 
source codes written using the custom programming language. 
The program is a partial implementation of the compiler to 
be developed for a custom programming language (PL) and is 
an update to the lexical analyzer program previously developed 
for the same custom PL.

Group members and their respective roles:
Lumontod - File saving and file opening functionalities. Error-checking and documentation.
Suico - Part of lexical analysis. Error checking and documentation.
Tadle - Part of lexical analysis. Documentation, program execution funtions.
Warain - Lexical, syntax and semantic analysis for the integer-oriented language (IOL) and error-checking of the program. Created frontend design and UI. Documentation.
"""

from faulthandler import disable
from pickle import TRUE
import PySimpleGUI as sg        # library used to create the front-end of program
import os
from dynamic_multiline import Multiline
from expression_evaluation import evaluation
import copy

from re import X

settings = {'filename': None}

def get_file_name(filepath):            # function for acquiring file name
    # filename = os.path.basename(filepath)
    return filepath
        
def save_file_as(window, values):       # function for saving another file; opens dialog box
    try: 
        filename = sg.popup_get_file('Save File', file_types=[("iol (*.iol)", "*.iol"),], save_as=True, no_window=True)
    except:
        return
    if filename not in (None,''):
        with open(filename,'w') as f:
            f.write(values['-code-'])
        settings.update(filename = filename)
        window["-filepath-"].update("File Path: "+filename) 

def matching_keyword(string, list):     # gets two arguments to compare keywords on a list and determine similarity; returns bool value
    for j in list:
        if string == j:
            return True
    return False

def remove_sublist(lst, sub):           # removes a sublist within a list; returns the remaining of that list
    i = 0
    out = []
    while i < len(lst):
        if lst[i:i+len(sub)] == sub:        # if list[from i to i + length of sub[]] is equal to sub[]
            i += len(sub)                   # then it will go to the next portion, or else... 
        else:
            out.append(lst[i])              # it will append it to the out[] list
            i += 1
    return out

def main():     # function for the whole program

    def expressionSyntaxEvaluation(formOfOperation):  # function for expression evaluation; checks if expression follows correct syntax

        errorFlag = 0
        validExpression = True  

        if (intOrVarFlag != operationFlag+1): # checks if number of operations is higher than one (1) than the combined number of integers and int variables to-
            validExpression = False           # ensure that the numerical expression is valid
            fileout.write("^Error in line "+str(x+1)+": Invalid expression detected for "+formOfOperation+" statement."+"\n")
            errorFlag = 1
            return errorFlag

        while(validExpression):     # proceeds if numerical expression is valid

            breakLoop = True
            for o in range(len(lengthOfExpression)):
                for p in range(len(numOperations)):
                    if (lengthOfExpression[o] == numOperations[p]):
                        breakLoop = False

            m=0
            while(m < len(lengthOfExpression)):
                if (lengthOfExpression[m] in numOperations):
                    try:
                        if(lengthOfExpression[m+1] in intOrVar):
                            try:
                                if(lengthOfExpression[m+2] in intOrVar):
                                    lengthOfExpression[m] = 'IDENT'
                                    del lengthOfExpression[m+1]
                                    del lengthOfExpression[m+1]
                            except:
                                fileout.write("^Error in line "+str(x+1)+": Invalid numerical expression detected for "+formOfOperation+" statement."+"\n")
                                errorFlag = 1 
                                breakLoop = True
                                break
                    except:
                        fileout.write("^Error in line "+str(x+1)+": Invalid numerical expression detected for "+formOfOperation+" statement."+"\n")
                        errorFlag = 1 
                        breakLoop = True
                        break

                if(m < len(listOfTokens[x])):   # proceed to the next interation in the loop
                    m = m + 1
                else:
                    break
            
            if breakLoop:
                return errorFlag

    def expressionEvaluation(m, formOfOperation):

        expressionHelperFunction = evaluation()
        
        if( ( (expressionHelperFunction.checkIfInteger(numericalExpression[m+1]) or 
                expressionHelperFunction.checkIfVariable(numericalExpression[m+1])) and 
                not matching_keyword(numericalExpression[m+1], keywords) ) 
        
        and
        
        ( (expressionHelperFunction.checkIfInteger(numericalExpression[m+2]) or 
            expressionHelperFunction.checkIfVariable(numericalExpression[m+2])) and 
            not matching_keyword(numericalExpression[m+2], keywords) ) 

        ):

            if( expressionHelperFunction.checkIfInteger(numericalExpression[m+1]) ):
                firstIntegerLiteral = float(numericalExpression[m+1])
                
            if( expressionHelperFunction.checkIfVariable(numericalExpression[m+1]) and 
                not matching_keyword(numericalExpression[m+1], keywords) ):
                
                firstIntegerLiteral = 0
                for q in range(len(symbolTable)):
                    if (numericalExpression[m+1] == symbolTable[q][1]):
                        firstIntegerLiteral = float(symbolTable[q][2])
                
            if( expressionHelperFunction.checkIfInteger(numericalExpression[m+2]) ):
                secondIntegerLiteral = float(numericalExpression[m+2])  
                
            if( expressionHelperFunction.checkIfVariable(numericalExpression[m+2]) and  
                not matching_keyword(numericalExpression[m+2], keywords) ):
                
                secondIntegerLiteral = 0
                for q in range(len(symbolTable)):
                    if (numericalExpression[m+2] == symbolTable[q][1]):
                        secondIntegerLiteral = float(symbolTable[q][2])

            if formOfOperation == 'ADD':
                numericalExpression[m] = float(firstIntegerLiteral + secondIntegerLiteral)

            if formOfOperation == 'SUB':
                numericalExpression[m] = float(firstIntegerLiteral - secondIntegerLiteral) 

            if formOfOperation == 'MULT':
                numericalExpression[m] = float(firstIntegerLiteral * secondIntegerLiteral)

            if formOfOperation in ['MULT', 'SUB', 'ADD']:
                del numericalExpression[m+1]
                del numericalExpression[m+1]

            if formOfOperation == 'DIV':
                if (secondIntegerLiteral != 0):
                    numericalExpression[m] = float(firstIntegerLiteral / secondIntegerLiteral)
                    del numericalExpression[m+1]
                    del numericalExpression[m+1] 

                elif (secondIntegerLiteral == 0):
                    errorDuringEvaluation.append('DIV')

            if formOfOperation == 'MOD':
                if (secondIntegerLiteral != 0):
                    numericalExpression[m] = float(firstIntegerLiteral % secondIntegerLiteral)
                    del numericalExpression[m+1]
                    del numericalExpression[m+1] 
                    
                elif (secondIntegerLiteral == 0):
                    errorDuringEvaluation.append('MOD')

    def openWindow(symbolTable, q):
        layoutWindow = [
        [sg.Text(key='-varType-')],
        [sg.InputText(pad = ((0,0), (0, 5)))],
        [sg.Submit()]
        ]
        
        if symbolTable[q][0] == 'INT':

            window = sg.Window('TYPE INT', layoutWindow, font=font, finalize=True)
            window['-varType-'].update('Enter INT value for '+symbolTable[q][1]+':')
            event, inputExpression = window.read()
            window.close()

            if inputExpression == None:
                sg.Popup("Empty input detected for INT variable.", font = font, button_type = 5, title = "Error!")
                return(True, None)

            elif str(inputExpression[0]).isnumeric():
                symbolTable[q][2] = inputExpression[0]
                outputLine = str('Input for '+symbolTable[q][1]+': '+ inputExpression[0]+'\n')
                return(False, outputLine)

            else:
                sg.Popup("Invalid input detected for INT variable.", font = font, button_type = 5, title = "Error!")
                return(True, None)

        if symbolTable[q][0] == 'STR':

            window = sg.Window('TYPE STR', layoutWindow, font=font, finalize=True)
            window['-varType-'].update('Enter STR value for '+symbolTable[q][1]+':')
            event, inputExpression = window.read()
            window.close()
            print(inputExpression)

            if inputExpression == None:
                sg.Popup("Empty input detected for STR variable.", font = font, button_type = 5, title = "Error!")
                return(True, None)

            elif inputExpression[0] == '':
                symbolTable[q][2] = ''
                outputLine = str('Input for '+symbolTable[q][1]+': '+ inputExpression[0]+'\n')                    
                return(False, outputLine)

            else:
                symbolTable[q][2] = inputExpression[0]
                outputLine = str('Input for '+symbolTable[q][1]+': '+ inputExpression[0]+'\n') 
                return(False, outputLine)
                

    sg.theme('DarkGrey8')       # theme and font style of the program
    font = ("Arial", 11)

    heading = ['Type', 'Variable Name', ]       # initial values for table
    empty = [[' ', ' ']]

    menu_def = [          # menu bar widget
            ['&File', ['&Save', '&Save As', '&New File', '&Open File',  'E&xit']],
            ['&Compile', ['&Compile Code','&Show Tokenized Code']],
            ['&Execute', ['&Execute Code']]
    ]

    file_viewer_column = [          # column widgets to display code from .iol files
            [sg.Text("File Path: ", key="-filepath-", size=(100, 0), p=((3, 0), (5, 0)))],

            [Multiline('',   size=(40, 20), justification='left', focus=True, pad=(0, 0),
            background_color='#404040', text_color='white', expand_x=True,
            expand_y=True, enable_events=True, horizontal_scroll=True, sbar_width=15,
            sbar_arrow_width=15, key='-code-')],

            [sg.Multiline(size=(150, 20), key="-console-", p=((5, 0), (10, 0)), horizontal_scroll=True, disabled=True)],
    ]
            
    second_column = [       # table widget for displaying the variable table
            [sg.Table        
                (
                    headings=heading[:],
                    values=empty[:],
                    max_col_width=15,
                    def_col_width=15,
                    header_border_width=2,
                    auto_size_columns=False,
                    justification="left",
                    vertical_scroll_only=False,
                    enable_events=True,
                    key='-TABLE-',
                    size = (50, 42),
                )
            ]
    ]

    layout = [                 # layout settings for the window
            [sg.Menu(menu_def, pad=(0,0), key='-menubar-', font = font)],
            [
                sg.Column(file_viewer_column, vertical_alignment='top',
                    p=((0, 0), (0, 50))),
                sg.Column(second_column, vertical_alignment='center',
                    p=((0, 0), (26, 50)))
            ]
    ]
    

    location = sg.Window.get_screen_size()
    
    # display the window of the program
    window = sg.Window("Integer-Only Language", layout, font = font, resizable = True, size=(1650, 750), finalize=True, location=location,  margins=(0, 0))
    ml = window['-code-']
    ml.initial(window, width=5, bg='#202020', fg='#808080', font=font)

    filepath = "" # user starts with an empty file path and file name
    filename = "" 

    while True:    # event loop that will capture any actions/events done in the window
        event, values = window.read()
    
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        elif event == '-code-':    # action for updating line numbers
            ml.reset()

        elif event == 'Save':   # save event
            filename = settings.get('filename')
            if filename not in (None, ''):
                with open(filename,'w') as f:
                    f.write(values['-code-'])
            else:
                save_file_as(window, values)
                open_file_key = 0

        elif event == 'Save As':        # save as event
            save_file_as(window, values)
            open_file_key = 0

        elif event == 'New File':       # new file event
            clear_string = ''
            window["-console-"].update(clear_string)
            window["-code-"].update(clear_string)

        elif event == 'Open File':      #  open file event
            filepath = sg.popup_get_file(file_types=  # these are the only file types that the user can select
                [
                    ("iol (*.iol)", "*.iol"),  # .tkn format
                ],
                no_window=True, message="")

            if (filepath != ""):
                window["-filepath-"].update("File Path: "+filepath) 
                settings.update(filename = filepath)
                filename = get_file_name(filepath)          # get the filename

                if (filepath.split(".")[1] == "iol"):       # check if the file is an .iol file
                    with open(filepath) as g:
                        input_string = g.read()  # read the input 

                    window["-code-"].update(input_string)
            
                    # clear info in table and editor area ( 0 means a new opened file)
                    window['-TABLE-'].update(values='')
                    window['-console-'].update('')

                    # user has to compile code from an opened file before showing tokenized code ( 0 means a new opened file)
                    open_file_key = 0

        elif event == 'Compile Code':       # when user selects compile code, code blocks for lexical, syntax and semantic analysis will run

            filename = settings.get('filename')

            if(filename is None):
                filename = ''
            
            if (filename == ''):      # do nothing if user doesn't select a file
                pass

#--------------------------------------------------------------------- Lexical analysis is done at the code block below ---------------------------------------------------------------------

            # check if the file is an .iol file
            elif (filename.split(".")[1] == "iol"):

                with open('console.txt', 'w') as empty:    # initialize the file console.txt that is used to print the errors of lexical and syntax analysis
                    empty.write("")                        
                empty.close()

                keywords = ["INT", "STR", "INTO", "IS", "BEG",
                            "PRINT", "ADD", "SUB", "MOD", "DIV", "MULT", "NEWLN", "LOI", "IOL"]
                            
                keyword = []
                KeyW_Var_List = []
                ERR_LEX = []
                ERR_LOC = []
                tokens = []
                OUTPUT_TOKENS = []
                err_lex_counter = 0
                
                filename = settings.get('filename')

                with open(filename) as h:
                    with open('output.tkn', 'w') as fileout: # creates output.tkn for syntax analysis
                        text = h.readlines()

                        for x in range(len(text)):
                            OUTPUT_TOKENS = OUTPUT_TOKENS + [' '] # create a list based on the number of lines in the .iol file

                        for x in range(len(text)):

                            # read input per line and strip of \n characters
                            input_string = text[x].strip().split()

                            # reset all token lists per input line
                            tokens.clear()
                            keyword.clear()
                            tokenized_string = ""

                            for i in input_string:

                                # checking for keywords and variables
                                if i.isupper():
                                    if i in keywords:
                                        keyword.append(i)
                                        KeyW_Var_List.append(i)
                                        tokens.append(i)
                                        tokenized_string += str(i)+" "
                                    else:
                                        KeyW_Var_List.append(i)
                                        tokens.append("IDENT")
                                        tokenized_string += "IDENT "
                                        continue

                                # checking for integers
                                elif i.isnumeric():
                                    
                                    tokens.append("INT_LIT")
                                    tokenized_string += "INT_LIT "

                                # checking for variables
                                elif ( i.isalnum() and i[0].isalpha() ):
                                    
                                    KeyW_Var_List.append(i)
                                    tokens.append("IDENT")
                                    tokenized_string += "IDENT "

                                # everything else not mentioned, these include symbols
                                else:
                                    ERR_LEX.append(i)
                                    ERR_LOC.append(x+1)
                                    tokens.append("ERR_LEX")
                                    tokenized_string += "ERR_LEX "

                            # check if there are errors
                            if bool(ERR_LEX):   
                                for a in range(len(ERR_LOC)):
                                    if (x+1 == ERR_LOC[a]):
                                        with open('console.txt', 'a+') as lexError:
                                            lexError.write("^ERR_LEX detected in line " + str(ERR_LOC[a]) +": "+ str(ERR_LEX[err_lex_counter]) +"\n")
                                            err_lex_counter += 1
                                        lexError.close()

                            OUTPUT_TOKENS[x] = tokenized_string

                        for i in range(len(OUTPUT_TOKENS)):
                            fileout.write(OUTPUT_TOKENS[i]+"\n")

                    # INT and STR variables will then be collected for the display of the variable table
                    keyW_Var = []
                    keyW_Var_Table = [[]]   

                    # Checks on the variable after the INT/STR keyword
                    get_variable = False
                    for x in KeyW_Var_List:
                        if (x == "INT" or x == "STR"):
                            keyW_Var.append((x))
                            get_variable = True
                        else:
                            if (get_variable):
                                keyW_Var.append((x))
                                get_variable = False
                    # the list will always pair the INT/STR keyword with its variable
                    # after that, a 2d table will the pairs for the display of the variable table

                    try:
                        keyW_Var_Table = [[keyW_Var[i], keyW_Var[i + 1]]
                                        for i in range(0, len(keyW_Var), 2)]
                    except:
                        pass
                    
                    # this will update the table with the variables
                    window['-TABLE-'].update(values='')
                    window['-TABLE-'].update(values=keyW_Var_Table[:][:])

                    fileout.close()
                h.close()

#--------------------------------------------------------------------- Syntax analysis is done at the code block below --------------------------------------------------------------------------

                # Important lists for the determining of certain groups of keywords
                keywords = ["INT", "STR", "INTO", "IS", "BEG",
                            "PRINT", "ADD", "SUB", "MOD", "DIV", "MULT", "NEWLN", "LOI", "IOL"]

                dataTypes = ['STR', 'INT']
                inputOperation = ['BEG']
                outputOperation = ['PRINT']
                numOperations = ['ADD', 'SUB', 'MULT', 'DIV', 'MOD']
                intOrVar = ['INT_LIT', 'IDENT']
                startKeyword = 'IOL'
                endKeyword = 'LOI'

                # Will open 'output.tkn' for the extraction of inputs
                with open('output.tkn') as h:
                    with open('console.txt', 'a+') as fileout:
                        text = h.readlines()    # text is now a list, with each point containing one or more keys
                        listOfTokens = []   # 'listOfTokens' is used for separating each points with keys into a list of its own
                        modifiedList = []   # 'modifiedList' is reserved for error checking, for leftover keys that may not be part of the grammar
                        
                        for x in range(len(text)):
                            listOfTokens.append(text[x].strip().split())    # 'listOfTokens' will separate lines of text into a list

                        if ((len(listOfTokens[0])) != 1 or listOfTokens[0][0] != startKeyword ):    # checks if 'IOL' is included in the input
                            fileout.write("^Error in line 1: IOL should only be at the start of the file."+"\n")     # or else, analysis will not execute

                        elif ((len(listOfTokens[len(listOfTokens)-1])) != 1 or listOfTokens[(len(listOfTokens)-1)][0] != endKeyword ):
                            fileout.write("^Error in last line: LOI should only be at the end of the file."+"\n") # same is true if 'LOI' is not included in the input
                        
                        else:   # if above conditions satisfy, the program can now proceed checking for syntax analysis
                            for x in range(1, len(listOfTokens)-1):
                                y = 0
                                errorFlag = 0
                                copyOfExpression = []

                                while (y < len(listOfTokens[x])):
                                    if matching_keyword(listOfTokens[x][y], dataTypes):     # Syntax analysis for Data Types
                                        if(y < len(listOfTokens[x])-1 and listOfTokens[x][y+1] != 'IDENT'):
                                            fileout.write("^Error in line "+str(x+1)+": "+listOfTokens[x][y]+" is missing IDENT"+"."+"\n")
                                            errorFlag = 1
                                        elif(y == len(listOfTokens[x])-1):
                                            fileout.write("^Error in line "+str(x+1)+": "+listOfTokens[x][y]+" is missing IDENT"+"."+"\n")
                                            errorFlag = 1

                                    if matching_keyword(listOfTokens[x][y], ['INT']):   # Syntax analysis to check if user declared INT IDENT IS (INT_LIT or IDENT) statement
                                        try:
                                            if (listOfTokens[x][y+1] == 'IDENT'):   # checks order of input if syntax is correct 
                                                if (listOfTokens[x][y+2] == 'IS'):
                                                    try:
                                                        if (listOfTokens[x][y+3] != 'INT_LIT'): 
                                                            fileout.write("^Error in line "+str(x+1)+": A literal "
                                                            "should be after IS keyword for INT."+"\n")
                                                            errorFlag = 1
                                                    except:
                                                        fileout.write("^Error in line "+str(x+1)+": A INT_LIT "
                                                        "should be after IS keyword for INT."+"\n")
                                                        errorFlag = 1
                                        except:
                                            pass

                                    if matching_keyword(listOfTokens[x][y], ['STR']):    # Syntax analysis to check if user declared incorrect STR IDENT IS INT_LIT statement
                                        try:
                                            if (listOfTokens[x][y+1] == 'IDENT'):   # checks order of input if syntax is correct 
                                                
                                                try:
                                                    if (listOfTokens[x][y+2] == 'IS'):
                                                        if (listOfTokens[x][y+3] == 'INT_LIT'):
                                                            fileout.write("^Error in line "+str(x+1)+": STR IDENT IS INT_LIT is an invalid operation."+"\n")
                                                            errorFlag = 1
                                                except:
                                                    pass
                                        except:
                                            pass
                                    
                                    if matching_keyword(listOfTokens[x][y], inputOperation):     # Syntax analysis for BEG operation                    
                                        if(y < len(listOfTokens[x])-1 and listOfTokens[x][y+1] != 'IDENT'): # checks order of input if syntax is correct 
                                            fileout.write("^Error in line "+str(x+1)+": "+listOfTokens[x][y]+" is missing IDENT"+"."+"\n")
                                            errorFlag = 1
                                        elif(y == len(listOfTokens[x])-1):
                                            fileout.write("^Error in line "+str(x+1)+": "+listOfTokens[x][y]+" is missing IDENT"+"."+"\n")
                                            errorFlag = 1
                                    
                                    if matching_keyword(listOfTokens[x][y], outputOperation):     # Syntax analysis for PRINT operation  
                                        matchOperation = False                                    # checks order of input if syntax is correct
                                        if(y < len(listOfTokens[x])-1):
                                            matchOperation = matching_keyword(listOfTokens[x][y+1], numOperations)  
                                          
                                            if (listOfTokens[x][y+1] != 'INT_LIT' and listOfTokens[x][y+1] != 'IDENT' and matchOperation == False):
                                                
                                                fileout.write("^Error in line "+str(x+1)+": Missing IDENT, INT_LIT or numerical expression after PRINT."+"\n")
                                                errorFlag = 1 

                                        elif(y == len(listOfTokens[x])-1):
                                            fileout.write("^Error in line "+str(x+1)+": Missing IDENT, INT_LIT or numerical expression after PRINT."+"\n")
                                            errorFlag = 1     
                                        
                                        if(matchOperation == True):          # if PRINT involves a NUMERICAL OPERATION, the code is as follows
                                            lengthOfExpression = ['PRINT', listOfTokens[x][y+1] ]       # 'lengthOfExpression' is storage for numerical expressions
                                            counter = 0                                                 # 'counter' for scanning through the list
                                            operationFlag = 1                                           # 'operationFlag' for checking number of operators used
                                            intOrVarFlag = 0                                            # 'intOrVarFlag' for checking number of INT_LIT and IDENT as operands  
                                            
                                            try:
                                                # this will check through the 'PRINT' keyword's operations and append into-
                                                # 'lengthOfExpression' list whenever operators and operands appear 
                                                while(True):
                                                    if (listOfTokens[x][y+2+counter] in numOperations):
                                                        operationFlag = operationFlag + 1
                                                        lengthOfExpression.append(listOfTokens[x][y+2+counter])

                                                    elif (listOfTokens[x][y+2+counter] in intOrVar):
                                                        intOrVarFlag = intOrVarFlag + 1
                                                        lengthOfExpression.append(listOfTokens[x][y+2+counter])

                                                    else:
                                                        break

                                                    counter += 1
                                            except:
                                                pass

                                            copyOfExpression.append(list(lengthOfExpression))   # copy of the expression will be created for later use
                                            errorFlag = expressionSyntaxEvaluation('PRINT')   # this will then check for errors in those operations

                                    if matching_keyword(listOfTokens[x][y], ['INTO']):   # Syntax analysis to check if user declared assignment operation
                                        matchOperation = False
                                            
                                        try:                                    # checks order of input if syntax is correct
                                            if (listOfTokens[x][y+1] == 'IDENT'):
                                                try:
                                                    if (listOfTokens[x][y+2] == 'IS'):
                                                        try:
                                                            matchOperation = matching_keyword(listOfTokens[x][y+3], numOperations)
                                                            if (listOfTokens[x][y+1] != 'INT_LIT' and listOfTokens[x][y+1] != 'IDENT' and matchOperation == False):
                                                                fileout.write("^Error in line "+str(x+1)+": Missing IDENT, INT_LIT or numerical expression after INTO IDENT IS."+"\n")
                                                                errorFlag = 1 
                                                
                                                        except:
                                                            fileout.write("^Error in line "+str(x+1)+": Missing "
                                                            "expression after INTO IDENT IS keyword."+"\n")
                                                            errorFlag = 1
                                                            
                                                    elif (listOfTokens[x][y+2] != 'IS'):
                                                        fileout.write("^Error in line "+str(x+1)+": IS "
                                                                "should be after INTO IDENT."+"\n")
                                                        errorFlag = 1
                                                except:
                                                    fileout.write("^Error in line "+str(x+1)+": Missing IS "
                                                            "after INTO IDENT keyword."+"\n")
                                                    errorFlag = 1

                                            elif (listOfTokens[x][y+1] != 'IDENT'):
                                                fileout.write("^Error in line "+str(x+1)+": IDENT "
                                                            "should be after INTO keyword."+"\n")
                                                errorFlag = 1
                                        except:
                                            fileout.write("^Error in line "+str(x+1)+": Missing "
                                                            "IDENT IS and expression after INTO."+"\n")
                                            errorFlag = 1
                                            pass

                                        if(matchOperation == True):             # if INTO IDENT IS involves a NUMERICAL OPERATION, the code is as follows
                                            assignmentExpression = ['INTO', 'IDENT', 'IS', listOfTokens[x][y+3] ]
                                            lengthOfExpression = assignmentExpression               # 'lengthOfExpression' is storage for numerical expressions
                                            counter = 0                                             # 'counter' for scanning through the list
                                            operationFlag = 1                                       # 'operationFlag' for checking number of operators used
                                            intOrVarFlag = 0                                        # 'intOrVarFlag' for checking number of INT_LIT and IDENT as operands
                                            
                                            
                                            try:
                                                # this will check through the 'INTO IDENT IS' keyword's operations and append into 
                                                # 'lengthOfExpression' list whenever operators and operands appear                             
                                                while(True):
                                                    if (listOfTokens[x][y+4+counter] in numOperations):
                                                        operationFlag = operationFlag + 1
                                                        lengthOfExpression.append(listOfTokens[x][y+4+counter])

                                                    elif (listOfTokens[x][y+4+counter] in intOrVar):
                                                        intOrVarFlag = intOrVarFlag + 1
                                                        lengthOfExpression.append(listOfTokens[x][y+4+counter])

                                                    else:
                                                        break

                                                    counter += 1
                                            except:
                                                pass

                                            copyOfExpression.append(list(lengthOfExpression))
                                            errorFlag = expressionSyntaxEvaluation('INTO IDENT IS')
                                            
                                    if(y < len(listOfTokens[x])):   # proceed to the next interation in the loop
                                        y = y + 1
                                    else:
                                        break
                                        
                                if errorFlag != 1: # to check if there are other violations, the line will have its correct statements removed
                                                   # and check if there are remaining keywords that do not fit in the grammar of the PL
                                                   # All of this will be stored in the 'modifiedList' list
                                    modifiedList = remove_sublist(listOfTokens[x], ['INT', 'IDENT', 'IS', 'INT_LIT'])
   
                                    modifiedList = remove_sublist(modifiedList, ['INT', 'IDENT'])
                                    modifiedList = remove_sublist(modifiedList, ['STR', 'IDENT'])
                                    modifiedList = remove_sublist(modifiedList, ['BEG', 'IDENT'])

                                    modifiedList = remove_sublist(modifiedList, ['PRINT', 'INT_LIT'])
                                    modifiedList = remove_sublist(modifiedList, ['PRINT', 'IDENT'])

                                    modifiedList = remove_sublist(modifiedList, ['INTO', 'IDENT', 'IS', 'IDENT'])
                                    modifiedList = remove_sublist(modifiedList, ['INTO', 'IDENT', 'IS', 'INT_LIT'])

                                    modifiedList = remove_sublist(modifiedList, ['NEWLN'])
                                    
                                    try:
                                        for z in range(len(copyOfExpression)):
                                            modifiedList = remove_sublist(modifiedList, copyOfExpression[z])
                                        
                                    except:
                                        pass
                                   

                                    errorTokens = ''
                                    for i in modifiedList:   
                                        errorTokens += (i+', ')
                                    errorTokens = errorTokens[:-2]
                                    
                                    if (len(modifiedList) > 0):     # this will be the output if errors of grammar violations exist in the input
                                        fileout.write("^Error in line "+str(x+1)+": Found token(s) "+errorTokens+" that violate rules of the grammar."+"\n")
                              
                    fileout.close()
                h.close()

                with open("console.txt") as g:      # output from the syntax analysis will then be shown in the GUI console
                    output_string = g.read()        # read the input 
                    window["-console-"].update(output_string)

                g.close()

#---------------------------------------------------------------------------- Semantic analysis is done at the code block below ------------------------------------------------------------------------------------

                if output_string == '':   # if no errors from analysis were found in console.txt, proceed to semantic analysis  

                    listOfLexemes = []      
                    keywordVariablePairs = []

                    with open(filename) as h:
                        with open('console.txt', 'a+') as fileout:     # semantic analysis should run only if lexixal and syntax analysis proceeded without any errors 
                            fileout.write("Lexical and syntax analysis of the code are successful. "
                                                    "Proceeding with semantic analysis..."+"\n")
                            text = h.readlines()

                            for x in range(len(text)):
                                listOfLexemes.append(text[x].strip().split())

                            for x in range(len(listOfLexemes)):
    
                                get_variable = False        
                                for wordOrVar in listOfLexemes[x]:      # store variables and their respective keywords in a list
                                    if (wordOrVar == "INT" or wordOrVar == "STR"):
                                        keyword = wordOrVar
                                        get_variable = True
                                    else:
                                        redeclarationError = 0
                                        if (get_variable):
                                            for pair in range(len(keywordVariablePairs)):
                                                if (keywordVariablePairs[pair][1] == wordOrVar):
                                                    redeclarationError = 1

                                            if redeclarationError == 0:
                                                keywordVariablePairs.append([keyword, wordOrVar])       # if a variable is being redeclared, don't append to the list-
                                            elif redeclarationError == 1:                               # and print and error on console
                                                fileout.write("^Error in line "+str(x+1)+": Redeclaration of variable "+wordOrVar+" detected."+"\n")    

                                            get_variable = False

                                y = 0
                                while (y < len(listOfLexemes[x])):
                                    
                                    if matching_keyword(listOfLexemes[x][y], ['INTO']):     # semantic analysis for INTO keyword

                                        matched = 0
                                        for i in range(len(keywordVariablePairs)):
                                            
                                            if(keywordVariablePairs[i][1] == listOfLexemes[x][y+1]):        # if variable for INTO keyword is not INT type, 
                                                matched = 1                                                 # print an error on console
                                                if(keywordVariablePairs[i][0] == 'STR'):
                                                    fileout.write("^Error in line "+str(x+1)+": "+listOfLexemes[x][y+1]+" is type STR."+"\n")
                                                elif(keywordVariablePairs[i][0] == 'INT'):
                                                    pass

                                        if (matched == 0):
                                            fileout.write("^Error in line "+str(x+1)+": "+listOfLexemes[x][y+1]+" is undeclared."+"\n") # if variable for INTO keyword is not yet declared-
                                                                                                                                        # but called, print and error on console
                                    if matching_keyword(listOfLexemes[x][y], ['IS']):       # semantic analysis for IS keyword

                                        if(str(listOfLexemes[x][y+1]).isalnum() and not str(listOfLexemes[x][y+1]).isnumeric() and 
                                        not matching_keyword(listOfLexemes[x][y+1], keywords)):

                                            matched = 0                             
                                            for i in range(len(keywordVariablePairs)):
                                                
                                                if(keywordVariablePairs[i][1] == listOfLexemes[x][y+1]):
                                                    matched = 1
                                                   
                                                    if(keywordVariablePairs[i][0] == 'STR'):         # if variable for IS keyword is not INT type, print an error on console
                                                        fileout.write("^Error in line "+str(x+1)+": "+listOfLexemes[x][y+1]+" is type STR."+"\n")
                                                    elif(keywordVariablePairs[i][0] == 'INT'):
                                                        pass

                                            if (matched == 0):                                          # if variable for INTO keyword is not yet declared, print an error on console
                                                fileout.write("^Error in line "+str(x+1)+": "+listOfLexemes[x][y+1]+" is undeclared."+"\n")

                                    if matching_keyword(listOfLexemes[x][y], ['BEG']):  # semantic analysis for BEG keyword

                                        matched = 0
                                        for i in range(len(keywordVariablePairs)):
                                            
                                            if(keywordVariablePairs[i][1] == listOfLexemes[x][y+1]):
                                                matched = 1

                                        if (matched == 0):                      # if variable for BEG keyword is not yet declared, print an error on console
                                            fileout.write("^Error in line "+str(x+1)+": "+listOfLexemes[x][y+1]+" is undeclared."+"\n")
                                    
                                    if matching_keyword(listOfLexemes[x][y], ['PRINT']):    # semantic analysis for PRINT keyword

                                        if(str(listOfLexemes[x][y+1]).isalnum() and not str(listOfLexemes[x][y+1]).isnumeric() and
                                        not matching_keyword(listOfLexemes[x][y+1], keywords)):

                                            matched = 0
                                            for i in range(len(keywordVariablePairs)):
                                                
                                                if(keywordVariablePairs[i][1] == listOfLexemes[x][y+1]):
                                                    matched = 1

                                            if (matched == 0):                  # if variable for PRINT keyword is not yet declared, print an error on console
                                                fileout.write("^Error in line "+str(x+1)+": "+listOfLexemes[x][y+1]+" is undeclared."+"\n")
                                    
                                    if (matching_keyword(listOfLexemes[x][y], ['PRINT']) or matching_keyword(listOfLexemes[x][y], ['IS'])) and matching_keyword(listOfLexemes[x][y+1], numOperations):
                                        # semantic analysis for numerical expressions that come after PRINT and IS

                                        numericalExpression = []        # 'numericalExpression' is storage for numerical expressions
                                        counter = 0                     # 'counter' for scanning through the list
                                        operationFlag = 0               # 'operationFlag' for checking number of operators used
                                        intOrVarFlag = 0                # 'intOrVarFlag' for checking number of INT_LIT and IDENT as operands  
                                        
                                        try:
                                            # this will check through the keyword's operations and append into 
                                            # 'numericalExpression' list whenever operators and operands appear 
                                            while(True):
                                                if (listOfLexemes[x][y+1+counter] in numOperations):
                                                    operationFlag = operationFlag + 1
                                                    numericalExpression.append(listOfLexemes[x][y+1+counter])
                                                
                                                elif ( (str(listOfLexemes[x][y+1+counter]).isalnum() or str(listOfLexemes[x][y+1+counter]).isnumeric() ) and
                                                    not matching_keyword(listOfLexemes[x][y+1+counter], keywords)):
                                                    intOrVarFlag = intOrVarFlag + 1
                                                    numericalExpression.append(listOfLexemes[x][y+1+counter])
                                                else:
                                                    break
                                                counter += 1
                                        except:
                                            pass
                                        
                                        for i in range(len(numericalExpression)):   # loop through the 'numericalExpression' list
                                           
                                            if (str(numericalExpression[i]).isalnum() and (not str(numericalExpression[i]).isnumeric() and
                                                not matching_keyword(numericalExpression[i], keywords))):

                                                matched = 0
                                                for keywordVarCounter in range(len(keywordVariablePairs)):
                                                    
                                                    if(keywordVariablePairs[keywordVarCounter][1] == numericalExpression[i]):
                                                        matched = 1
                                                                    # all operands should be declared as an INT datatype or should be an integer literal.
                                                                    # if not, display the respective error message on the console.
                                                        if(keywordVariablePairs[keywordVarCounter][0] == 'STR'): 
                                                            fileout.write("^Error in line "+str(x+1)+": "+numericalExpression[i]+" is type STR."+"\n")
                                                        elif(keywordVariablePairs[keywordVarCounter][0] == 'INT'):
                                                            pass

                                                if (matched == 0):
                                                    fileout.write("^Error in line "+str(x+1)+": "+numericalExpression[i]+" is undeclared."+"\n")
                                  
                                    if(y < len(listOfLexemes[x])):   # proceed to the next string in the code line
                                        y = y + 1
                                    else:
                                        break
              
                                    
                        fileout.close()
                    h.close()

                    with open("console.txt") as g:
                        output_string = g.read()  # read the input 
                        window["-console-"].update(output_string)
                    g.close()
                
                if len(output_string) == 93:        # if there are no errors found, then display in console that no errors were found
                    with open('console.txt', 'a+') as fileout:
                        fileout.write("No errors have been detected during semantic analysis."+"\n")
                    fileout.close()
                
                with open("console.txt") as g:
                    output_string = g.read()  # read the input 
                    window["-console-"].update(output_string)
                g.close()

                # allow user to show tokenized code or execute code after compiling a .iol file
                open_file_key = 1 
                
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        elif event == 'Show Tokenized Code':       # event where user selects "Show Tokenized Code"
            
            if ( (filename == "") or (open_file_key == 0) ):    # force user to recompile the code when opening another .iol file
                sg.Popup("Please compile code before showing the tokenized code.", font = font, button_type = 5, title = "Error!")
            else:               # every token created from the lexical analyzer will be displaed on the console

                if OUTPUT_TOKENS is not []:         
                    with open('output.tkn', 'w') as fileout:
                        for i in range(len(OUTPUT_TOKENS)):     # OUTPUT_TOKENS will be printed using for loop
                            fileout.write(OUTPUT_TOKENS[i]+"\n")
                    fileout.close()

                    with open("output.tkn") as g:         # output.tkn will then be read in order to display into the console
                        output_string = g.read()  # read the input
                        window["-console-"].update(output_string)
                    g.close()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        elif event == 'Execute Code':       # event for expression evaluation after the user has compiled the input file

            executeCodeFlag = False
            codeLinesFromInput = []

            if ( (filename == "") or (open_file_key == 0) ):    # force user to recompile the code when opening another .iol file
                sg.Popup("Please compile code before executing code.", font = font, button_type = 5, title = "Error!")
            else:
                fileName = os.path.basename(filename)

                with open(filename) as h:
                    text = h.readlines()
                h.close()

                with open('console.txt', 'r') as readAnalysis: 
                    noErrorMessage = readAnalysis.readlines()
                readAnalysis.close()

                with open('execute.txt', 'w') as output:
                    output.close()

                with open('execute.txt', 'a+') as output: 

                    if(noErrorMessage[0] == "Lexical and syntax analysis of the code are successful. Proceeding with semantic analysis...\n" and
                        noErrorMessage[1] == "No errors have been detected during semantic analysis.\n"):

                        output.write(fileName+" was compiled without errors. Program test will now be executed.\n\n"
                                        "IOL Execution."+"\n")
                        executeCodeFlag = True

                    else:
                        sg.Popup("Cannot execute program test because "+fileName+" contains errors during compilation.", font = font, button_type = 5, title = "Error!")
                    
                    if executeCodeFlag:
                        for x in range(len(text)):
                            codeLinesFromInput.append(text[x].strip().split())

                        symbolTable = copy.deepcopy(keywordVariablePairs)
                        BEGErrorFlag = False

                        for x in range(len(symbolTable)):
                            if (symbolTable[x][0] == 'INT'):
                                symbolTable[x].append('0')
                            elif (symbolTable[x][0] == 'STR'):
                                symbolTable[x].append('')

                        errorDuringEvaluation = []
                        for x in range(len(codeLinesFromInput)):
                            
                            if (len(errorDuringEvaluation) != 0):
                                sg.Popup("Program execution terminated since "+fileName+ 
                                " contains division or modulo by zero.", font = font, button_type = 5, title = "Error!")
                                break
                            if BEGErrorFlag == True:
                                sg.Popup("Program execution terminated since invalid input for variable type" 
                                " in BEG operation has been detected.", font = font, button_type = 5, title = "Error!")
                                break

                            y=0
                            evaluateVariable = evaluation()
                            
                            while (y < len(codeLinesFromInput[x])):
                                
                                if matching_keyword(codeLinesFromInput[x][y], ['INT']):
                                    variableName = codeLinesFromInput[x][y+1]
                                    
                                    try:
                                        if matching_keyword(codeLinesFromInput[x][y+2], ['IS']):

                                            if str(codeLinesFromInput[x][y+3]).isnumeric():

                                                integerValue = codeLinesFromInput[x][y+3]
                                                evaluateVariable.evaluateVariableValue(variableName, symbolTable, integerValue)
                                    except:
                                        pass
                                            
                                if matching_keyword(codeLinesFromInput[x][y], ['NEWLN']):
                                    output.write("\n")
                                
                                if matching_keyword(codeLinesFromInput[x][y], ['PRINT']):

                                    if str(codeLinesFromInput[x][y+1]).isnumeric():

                                        integerValue = codeLinesFromInput[x][y+1]
                                        output.write(str(integerValue))

                                    elif ( str(codeLinesFromInput[x][y+1]).isalnum() and not str(codeLinesFromInput[x][y+1]).isnumeric() and 
                                            not matching_keyword(listOfLexemes[x][y+1], keywords)):

                                        checkVariableType = codeLinesFromInput[x][y+1]
                                        for q in range(len(symbolTable)):
                                            if (checkVariableType == symbolTable[q][1]):
                                                output.write(str(symbolTable[q][2]))
                                    
                                    elif matching_keyword(codeLinesFromInput[x][y+1], numOperations):
                                        numericalExpression = []
                                        operationFlag = 0 
                                        counter = 0

                                        try:
                                            while(True):
                                                if (listOfLexemes[x][y+1+counter] in numOperations):
                                                    operationFlag += 1 
                                                    numericalExpression.append(listOfLexemes[x][y+1+counter])
                                                elif ( (str(listOfLexemes[x][y+1+counter]).isalnum() or str(listOfLexemes[x][y+1+counter]).isnumeric() ) and
                                                    not matching_keyword(listOfLexemes[x][y+1+counter], keywords)):
                                                    numericalExpression.append(listOfLexemes[x][y+1+counter])
                                                else:
                                                    break
                                                counter += 1
                                        except:
                                            pass
                                        
                                        for n in range(operationFlag):
                                            m = 0
                                            while(m < len(numericalExpression) ):
                                                
                                                if (numericalExpression[m] in numOperations):
                                                    expressionEvaluation(m, numericalExpression[m])                                                      

                                                if(m < len(numericalExpression)):   # proceed to the next interation in the loop
                                                    m = m + 1
                                                else:
                                                    break
                                        
                                        integerValue = str(numericalExpression[0])
                                        output.write(str(integerValue))                           
                                    
                                    
                                if matching_keyword(codeLinesFromInput[x][y], ['INTO']):
                                    variableName = codeLinesFromInput[x][y+1]
                                    
                                    if matching_keyword(codeLinesFromInput[x][y+2], ['IS']):

                                        if str(codeLinesFromInput[x][y+3]).isnumeric():
                                            
                                            integerValue = codeLinesFromInput[x][y+3]
                                            evaluateVariable.evaluateVariableValue(variableName, symbolTable, integerValue)

                                        elif ( str(codeLinesFromInput[x][y+3]).isalnum() and not str(codeLinesFromInput[x][y+3]).isnumeric() and 
                                            not matching_keyword(listOfLexemes[x][y+3], keywords)):
                                            
                                            for q in range(len(symbolTable)):
                                                if (codeLinesFromInput[x][y+3] == symbolTable[q][1]):
                                                    integerValue = symbolTable[q][2]

                                            evaluateVariable.evaluateVariableValue(variableName, symbolTable, integerValue)
                                        
                                        elif (matching_keyword(codeLinesFromInput[x][y+3], numOperations)):
                                            
                                            numericalExpression = []
                                            operationFlag = 0 
                                            counter = 0

                                            try:
                                                while(True):
                                                    if (listOfLexemes[x][y+3+counter] in numOperations):
                                                        operationFlag += 1 
                                                        numericalExpression.append(listOfLexemes[x][y+3+counter])
                                                    
                                                    elif ( (str(listOfLexemes[x][y+3+counter]).isalnum() or str(listOfLexemes[x][y+3+counter]).isnumeric() ) and
                                                        not matching_keyword(listOfLexemes[x][y+3+counter], keywords)):
                                                        numericalExpression.append(listOfLexemes[x][y+3+counter])
                                                    else:
                                                        break
                                                    counter += 1
                                            except:
                                                pass
                                            
                                            for n in range(operationFlag):
                                                m = 0
                                                while(m < len(numericalExpression) ):
                                                    
                                                    if (numericalExpression[m] in numOperations):
                                                        expressionEvaluation(m, numericalExpression[m])                                                      

                                                    if(m < len(numericalExpression)):   # proceed to the next interation in the loop
                                                        m = m + 1
                                                    else:
                                                        break
                                            
                                            integerValue = str(numericalExpression[0])
                                            evaluateVariable.evaluateVariableValue(variableName, symbolTable, integerValue)

                                if matching_keyword(codeLinesFromInput[x][y], ['BEG']): 
                                    outputLine = '' 
                                    evaluateExpression = codeLinesFromInput[x][y+1]
                                    for q in range(len(symbolTable)):
                                        if (evaluateExpression == symbolTable[q][1]):
                                            BEGErrorFlag, outputLine = openWindow(symbolTable, q)
                                            output.write(str(outputLine))
                                            if BEGErrorFlag == True:
                                                break
                                        

                                if(y < len(codeLinesFromInput[x]) and (len(errorDuringEvaluation) == 0)):   # proceed to the next string in the code line
                                    y = y + 1
                                else:
                                    break
                                    
                        print(len(errorDuringEvaluation))
                        print(symbolTable)

                        if((executeCodeFlag == True) and (len(errorDuringEvaluation) == 0) and (BEGErrorFlag == False)):
                            output.write("\n\nProgram terminated successfully…") 
                            
                        else:
                            output.close()
                            with open('execute.txt', 'w') as deleted:  
                                deleted.write(fileName+" was compiled without errors. Program test will now be executed.\n\n"+
                                "Program execution contains error. Please try again.")

                with open('execute.txt') as g:         
                    output_string = g.read()  # read the input
                    if output_string != "":
                        window["-console-"].update(output_string)
                

    # os.remove("console.txt")
    # os.remove("output.tkn")

    window.close()


if __name__ == '__main__':
    main()