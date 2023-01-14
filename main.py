"""
CMSC 129 - Programming Project

This program is a serves as the Programming Project, a working compiler.
The program is a simple parser for a custom programming language. 
The parser performs lexical, syntax, semantic analysis of 
source codes and program test execution written using the custom programming language. 
The program is the compiler for a Integer-Only Language (IOL)

"""

from faulthandler import disable
from pickle import TRUE
import PySimpleGUI as sg        # library used to create the front-end of program
import os
from os.path import exists
from dynamic_multiline import Multiline
from expression_evaluation import evaluation
import lexical_analyzer as la
import syntax_analyzer as syn_a
import semantic_analyzer as sem_a
import copy

from re import X

settings = {'filename': None}

def delete_file(file_name):     # function for deleting generated text files
    file_exists = exists(file_name)
    if file_exists:  
        os.remove(file_name)

def get_file_name(filepath):            # function for acquiring file name
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

def matching_keyword(string, list):     # function for getting two arguments to compare keywords on a list and determine similarity; returns bool value
    for j in list:
        if string == j:
            return True
    return False

def remove_sublist(lst, sub):           # function for removing a sublist within a list; returns the remaining of that list
    i = 0
    out = []
    while i < len(lst):
        if lst[i:i+len(sub)] == sub:        # if list[from i to i + length of sub[]] is equal to sub[]
            i += len(sub)                   # then it will go to the next portion, or else... 
        else:
            out.append(lst[i])              # it will append it to the out[] list
            i += 1
    return out

def main():     # function for the main program

    def openWindow(symbolTable, q):  # function for opening window for BEG operation in code execution

        layoutWindow = [     # layout for the dialog window
        [sg.Text(key='-varType-')],
        [sg.InputText(pad = ((0,0), (0, 5)))],
        [sg.Submit()]
        ]
        
        if symbolTable[q][0] == 'INT':      # if variable type is INT, ask for integer input from user

            window = sg.Window('TYPE INT', layoutWindow, font=font, finalize=True)
            window['-varType-'].update('Enter INT value for '+symbolTable[q][1]+':')
            event, inputExpression = window.read()
            window.close()

            if inputExpression == None:     # return an error if empty input was detected
                sg.Popup("Empty input detected for INT variable.", font = font, button_type = 5, title = "Error!")
                return(True, None)

            elif str(inputExpression[0]).isnumeric():      # if input value is valid, then update variable's value in symbol table
                symbolTable[q][2] = inputExpression[0]
                outputLine = str('Input for '+symbolTable[q][1]+': '+ inputExpression[0]+'\n')
                return(False, outputLine)

            else:       # return an error if invalid input was detected
                sg.Popup("Invalid input detected for INT variable.", font = font, button_type = 5, title = "Error!")
                return(True, None)

        if symbolTable[q][0] == 'STR':     # if variable type is STR, ask for string input from user

            window = sg.Window('TYPE STR', layoutWindow, font=font, finalize=True)   
            window['-varType-'].update('Enter STR value for '+symbolTable[q][1]+':')
            event, inputExpression = window.read()
            window.close()

            if inputExpression == None:     # return an error if empty input was detected
                sg.Popup("Empty input detected for STR variable.", font = font, button_type = 5, title = "Error!")
                return(True, None)

            elif inputExpression[0] == '':      # if input value is empty, then update variable's value in symbol table-
                                                # as an empty string
                symbolTable[q][2] = ''
                outputLine = str('Input for '+symbolTable[q][1]+': '+ inputExpression[0]+'\n')                    
                return(False, outputLine)

            else:           # if input value is empty, then update variable's value in symbol table
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

    # for keyboard shortcuts
    window.bind("<Control_L><s>", "Ctrl-S")                 # Ctrl-S for 'Save'
    window.bind("<Control_L><Shift-S>", "Ctrl-Shift-S")     # Ctrl-Shift-S for 'Save As'
    window.bind("<Control_L><n>", "Ctrl-N")                 # Ctrl-N for 'New File'
    window.bind("<Control_L><o>", "Ctrl-O")                 # Ctrl-O for 'Open File'
    window.bind("<Control_L><Shift-X>", "Ctrl-Shift-X")     # Ctrl-Shift-X for 'Exit'
    window.bind("<Control_L><Alt_L><c>", "Ctrl-Alt-C")      # Ctrl-Alt-C for 'Compile Code'
    window.bind("<Control_L><Alt_L><t>", "Ctrl-Alt-T")      # Ctrl-Alt-T for 'Show Tokenized Code'
    window.bind("<Control_L><Alt_L><e>", "Ctrl-Alt-E")      # Ctrl-Alt-E for 'Execute Code'

    filepath = "" # user starts with an empty file path and file name
    filename = "" 

    while True:    # event loop that will capture any actions/events done in the window
        event, values = window.read()
    
        if event in (sg.WIN_CLOSED, 'Exit', 'Ctrl-Shift-X'):
            break

        elif event == '-code-':    # action for updating line numbers
            ml.reset()

        elif event in ("Save", "Ctrl-S"):   # save event
            filename = settings.get('filename')
            if filename not in (None, ''):
                with open(filename,'w') as f:
                    f.write(values['-code-'])
            else:
                save_file_as(window, values)
                open_file_key = 0

        elif event in ("Save As", "Ctrl-Shift-S"):        # save as event
            save_file_as(window, values)
            open_file_key = 0

        elif event in ("New File", "Ctrl-N"):       # new file event
            clear_string = ''
            window["-console-"].update(clear_string)
            window["-code-"].update(clear_string)
            values["-console-"] = ''
            values["-code-"] = ''
            save_file_as(window, values)
            open_file_key = 0

        elif event in ("Open File", "Ctrl-O"):      #  open file event
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

        elif event in ("Compile Code", "Ctrl-Alt-C"):       # when user selects compile code, code blocks for lexical, syntax and semantic analysis will run

            filename = settings.get('filename')

            if(filename is None):
                filename = ''

            if(filename != ''):
                with open(filename) as inputFile:
                    checkIfEmpty = inputFile.read()
        
            if (filename == '' or len(checkIfEmpty) == 0 ):      # don't compile if user doesn't select a file, or opens an empty file
                sg.Popup("Please open a non-empty file before proceeding to code compilation.", font = font, button_type = 5, title = "Error!")

#--------------------------------------------------------------------- Lexical analysis is done at the code block below ---------------------------------------------------------------------

            # check if the file is an .iol file
            elif (filename.split(".")[1] == "iol"):
                keyW_Var_Table = [[]] 
                OUTPUT_TOKENS = []
                keyW_Var_Table, OUTPUT_TOKENS = la.lexical_analysis(filename)
                
                # this will update the table with the variables
                window['-TABLE-'].update(values='')
                window['-TABLE-'].update(values=keyW_Var_Table[:][:])

#--------------------------------------------------------------------- Syntax analysis is done at the code block below --------------------------------------------------------------------------

                syn_a.syntax_analysis(filename)

                with open("console.txt") as g:      # output from the syntax analysis will then be shown in the GUI console
                    output_string = g.read()        # read the input 
                    window["-console-"].update(output_string)
                g.close()

#---------------------------------------------------------------------------- Semantic analysis is done at the code block below ------------------------------------------------------------------------------------
                
                listOfLexemes, keywordVariablePairs = sem_a.semantic_analysis(filename)
                
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
        elif event in ("Show Tokenized Code", "Ctrl-Alt-T"):       # event where user selects "Show Tokenized Code"
            
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
        elif event in ("Execute Code", "Ctrl-Alt-E"):       # event for expression evaluation after the user has compiled the input file
            
            keywords = ["INT", "STR", "INTO", "IS", "BEG",
                        "PRINT", "ADD", "SUB", "MOD", "DIV", "MULT", "NEWLN", "LOI", "IOL"]
            numOperations = ['ADD', 'SUB', 'MULT', 'DIV', 'MOD']
            executeCodeFlag = False
            codeLinesFromInput = []

            if ( (filename == "") or (open_file_key == 0) ):    # force user to recompile the code when opening another .iol file
                sg.Popup("Please compile code before executing code.", font = font, button_type = 5, title = "Error!")
            else:
                fileName = os.path.basename(filename)

                with open(filename) as h:       # read each line of input
                    text = h.readlines()
                h.close()

                with open('console.txt', 'r') as readAnalysis: # read console.txt
                    noErrorMessage = readAnalysis.readlines()
                readAnalysis.close()

                with open('execute.txt', 'w') as output:    # create execute.txt- this text file will show the output of the program test execution
                    output.close()

                with open('execute.txt', 'a+') as output:   # append the following messages to execute.txt

                    if(noErrorMessage[0] == "Lexical and syntax analysis of the code are successful. Proceeding with semantic analysis...\n" and
                        noErrorMessage[1] == "No errors have been detected during semantic analysis.\n"):

                        output.write(fileName+" was compiled without errors. Program test will now be executed.\n\n"    # if no errors during analysis, then-
                                        "IOL Execution:"+"\n")                                                          # program can proceed with test execution
                        executeCodeFlag = True

                    else:           # if there are errors during analysis, than halt program test execution
                        sg.Popup("Cannot execute program test because "+fileName+" contains errors during compilation.", font = font, button_type = 5, title = "Error!")
                    
                    if executeCodeFlag:
                        for x in range(len(text)):      
                            codeLinesFromInput.append(text[x].strip().split())

                        symbolTable = copy.deepcopy(keywordVariablePairs) # create the symbol table for execution
                        BEGErrorFlag = False

                        for x in range(len(symbolTable)):   # set the initial values of variables as zero (0) or empty string depending on datatype
                            if (symbolTable[x][0] == 'INT'):
                                symbolTable[x].append('0')
                            elif (symbolTable[x][0] == 'STR'):
                                symbolTable[x].append('')

                        errorDuringEvaluation = []
                        for x in range(len(codeLinesFromInput)):
                            
                            if (len(errorDuringEvaluation) != 0):      # halt program execution if error occurred during numerical expression evaluation
                                sg.Popup("Program execution terminated since "+fileName+ 
                                " contains division or modulo by zero.", font = font, button_type = 5, title = "Error!")
                                break
                            if BEGErrorFlag == True:    # halt program execution if error occurred during BEG operation
                                sg.Popup("Program execution terminated since invalid input for variable type" 
                                " in BEG operation has been detected.", font = font, button_type = 5, title = "Error!")
                                break

                            y=0
                            evaluateVariable = evaluation()
                            
                            while (y < len(codeLinesFromInput[x])):     
                                
                                if matching_keyword(codeLinesFromInput[x][y], ['INT']): # update INT variable when initialized with a specific integer value
                                    variableName = codeLinesFromInput[x][y+1]
                                    
                                    try:
                                        if matching_keyword(codeLinesFromInput[x][y+2], ['IS']):

                                            if str(codeLinesFromInput[x][y+3]).isnumeric():

                                                integerValue = codeLinesFromInput[x][y+3]
                                                evaluateVariable.evaluateVariableValue(variableName, symbolTable, integerValue)
                                    except:
                                        pass
                                            
                                if matching_keyword(codeLinesFromInput[x][y], ['NEWLN']):   # append newline symbol to execute.txt
                                    output.write("\n")
                                
                                if matching_keyword(codeLinesFromInput[x][y], ['PRINT']):   # PRINT operation to show integer or string

                                    if str(codeLinesFromInput[x][y+1]).isnumeric(): # append integer to execute.txt

                                        integerValue = codeLinesFromInput[x][y+1]
                                        output.write(str(integerValue))

                                    elif ( str(codeLinesFromInput[x][y+1]).isalnum() and not str(codeLinesFromInput[x][y+1]).isnumeric() and 
                                            not matching_keyword(listOfLexemes[x][y+1], keywords)):     # append variable's value to execute.txt

                                        checkVariableType = codeLinesFromInput[x][y+1]     
                                        for q in range(len(symbolTable)):
                                            if (checkVariableType == symbolTable[q][1]):
                                                output.write(str(symbolTable[q][2]))
                                    
                                    elif matching_keyword(codeLinesFromInput[x][y+1], numOperations):     # append value of numerical expression to execute.txt
                                        numericalExpression = []
                                        operationFlag = 0 
                                        counter = 0

                                        try:
                                            while(True):
                                                if (listOfLexemes[x][y+1+counter] in numOperations):  # get number of operations 
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
                                        
                                        for n in range(operationFlag):  # loop based on number of operations
                                            m = 0
                                            while(m < len(numericalExpression) ):
                                                
                                                if (numericalExpression[m] in numOperations):   # evaluate the numerical expression
                                                    evaluateVariable.expressionEvaluation(m, symbolTable, errorDuringEvaluation, numericalExpression)                                            

                                                if(m < len(numericalExpression)):   # proceed to the next iteration of the loop
                                                    m = m + 1
                                                else:
                                                    break
                                        
                                        integerValue = str(numericalExpression[0])
                                        output.write(str(integerValue))          # append the resulting integer value to execute.text                 
                                    
                                    
                                if matching_keyword(codeLinesFromInput[x][y], ['INTO']):   # INTO operations gets value of a INT variable only
                                    variableName = codeLinesFromInput[x][y+1]
                                    
                                    if matching_keyword(codeLinesFromInput[x][y+2], ['IS']):

                                        if str(codeLinesFromInput[x][y+3]).isnumeric():
                                            
                                            integerValue = codeLinesFromInput[x][y+3]
                                            evaluateVariable.evaluateVariableValue(variableName, symbolTable, integerValue)

                                        elif ( str(codeLinesFromInput[x][y+3]).isalnum() and not str(codeLinesFromInput[x][y+3]).isnumeric() and 
                                            not matching_keyword(listOfLexemes[x][y+3], keywords)):  # change value of the variable to the selected variable
                                            
                                            for q in range(len(symbolTable)):
                                                if (codeLinesFromInput[x][y+3] == symbolTable[q][1]):
                                                    integerValue = symbolTable[q][2]

                                            evaluateVariable.evaluateVariableValue(variableName, symbolTable, integerValue)
                                        
                                        elif (matching_keyword(codeLinesFromInput[x][y+3], numOperations)):  # evaluate value based from numerical expression
                                            
                                            numericalExpression = []
                                            operationFlag = 0 
                                            counter = 0

                                            try:
                                                while(True):
                                                    if (listOfLexemes[x][y+3+counter] in numOperations):   # get number of operations
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
                                            
                                            for n in range(operationFlag): # loop based on number of operations
                                                m = 0
                                                while(m < len(numericalExpression) ): 
                                                    
                                                    if (numericalExpression[m] in numOperations):
                                                        evaluateVariable.expressionEvaluation(m, symbolTable, errorDuringEvaluation, numericalExpression)   # evaluate the numerical-                                                  
                                                                                                                                            # expression
                                                    if(m < len(numericalExpression)):   # proceed to the next iteration of the loop
                                                        m = m + 1
                                                    else:
                                                        break
                                            
                                            integerValue = str(numericalExpression[0])       # update the variable value based from the resulting expression       
                                            evaluateVariable.evaluateVariableValue(variableName, symbolTable, integerValue)

                                if matching_keyword(codeLinesFromInput[x][y], ['BEG']):  # BEG operation serves as input operation
                                    outputLine = '' 
                                    evaluateExpression = codeLinesFromInput[x][y+1]
                                    for q in range(len(symbolTable)):
                                        if (evaluateExpression == symbolTable[q][1]):
                                            BEGErrorFlag, outputLine = openWindow(symbolTable, q)   # call function openWindow() to open dialog window for input
                                            output.write(str(outputLine))
                                            if BEGErrorFlag == True:  # if BEG operation contains error, then halt program text execution
                                                break
                                        

                                if (y < len(codeLinesFromInput[x]) and (len(errorDuringEvaluation) == 0)):   # proceed to the next string in the code line
                                    y = y + 1
                                else:
                                    break
                        
                        if((executeCodeFlag == True) and (len(errorDuringEvaluation) == 0) and (BEGErrorFlag == False)):    # if no error during program test execution,-
                            output.write("\nProgram terminated successfully...")                                            # append message for successful termination to execute.txt
                            
                        else:
                            output.close()
                            with open('execute.txt', 'w') as deleted:      # if error occurred during execution, append this error message to execute.txt
                                deleted.write(fileName+" was compiled without errors. Program test will now be executed.\n\n"+
                                "Program execution halted since an error was detected. Please try again.")

                with open('execute.txt') as g:         
                    output_string = g.read()  # read the input of execute.txt
                    if output_string != "":
                        window["-console-"].update(output_string)
                

    delete_file("console.txt")    
    delete_file("execute.txt")
  

    window.close()


if __name__ == '__main__':
    main()