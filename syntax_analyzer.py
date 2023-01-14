# Module for Syntax Analysis

import main
from expression_evaluation import evaluation

def syntax_analysis(filename):
    
    # Important lists for the determining of certain groups of keywords

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
                        if main.matching_keyword(listOfTokens[x][y], dataTypes):     # Syntax analysis for Data Types
                            if(y < len(listOfTokens[x])-1 and listOfTokens[x][y+1] != 'IDENT'):
                                fileout.write("^Error in line "+str(x+1)+": "+listOfTokens[x][y]+" is missing IDENT"+"."+"\n")
                                errorFlag = 1
                            elif(y == len(listOfTokens[x])-1):
                                fileout.write("^Error in line "+str(x+1)+": "+listOfTokens[x][y]+" is missing IDENT"+"."+"\n")
                                errorFlag = 1

                        if main.matching_keyword(listOfTokens[x][y], ['INT']):   # Syntax analysis to check if user declared INT IDENT IS (INT_LIT or IDENT) statement
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

                        if main.matching_keyword(listOfTokens[x][y], ['STR']):    # Syntax analysis to check if user declared incorrect STR IDENT IS INT_LIT statement
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
                        
                        if main.matching_keyword(listOfTokens[x][y], inputOperation):     # Syntax analysis for BEG operation                    
                            if(y < len(listOfTokens[x])-1 and listOfTokens[x][y+1] != 'IDENT'): # checks order of input if syntax is correct 
                                fileout.write("^Error in line "+str(x+1)+": "+listOfTokens[x][y]+" is missing IDENT"+"."+"\n")
                                errorFlag = 1
                            elif(y == len(listOfTokens[x])-1):
                                fileout.write("^Error in line "+str(x+1)+": "+listOfTokens[x][y]+" is missing IDENT"+"."+"\n")
                                errorFlag = 1
                        
                        if main.matching_keyword(listOfTokens[x][y], outputOperation):     # Syntax analysis for PRINT operation  
                            matchOperation = False                                    # checks order of input if syntax is correct
                            if(y < len(listOfTokens[x])-1):
                                matchOperation = main.matching_keyword(listOfTokens[x][y+1], numOperations)  
                                
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
                                errorFlag = evaluation.expressionSyntaxEvaluation(intOrVarFlag, operationFlag, lengthOfExpression, numOperations, x, listOfTokens, 'PRINT')   # this will then check for errors in those operations

                        if main.matching_keyword(listOfTokens[x][y], ['INTO']):   # Syntax analysis to check if user declared assignment operation
                            matchOperation = False
                                
                            try:                                    # checks order of input if syntax is correct
                                if (listOfTokens[x][y+1] == 'IDENT'):
                                    try:
                                        if (listOfTokens[x][y+2] == 'IS'):
                                            try:
                                                matchOperation = main.matching_keyword(listOfTokens[x][y+3], numOperations)
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
                                errorFlag = evaluation.expressionSyntaxEvaluation(intOrVarFlag, operationFlag, lengthOfExpression, numOperations, x, listOfTokens, 'INTO IDENT IS')
                                
                        if(y < len(listOfTokens[x])):   # proceed to the next interation in the loop
                            y = y + 1
                        else:
                            break
                            
                    if errorFlag != 1: # to check if there are other violations, the line will have its correct statements removed
                                        # and check if there are reprimeing keywords that do not fit in the grammar of the PL
                                        # All of this will be stored in the 'modifiedList' list
                        modifiedList = main.remove_sublist(listOfTokens[x], ['INT', 'IDENT', 'IS', 'INT_LIT'])

                        modifiedList = main.remove_sublist(modifiedList, ['INT', 'IDENT'])
                        modifiedList = main.remove_sublist(modifiedList, ['STR', 'IDENT'])
                        modifiedList = main.remove_sublist(modifiedList, ['BEG', 'IDENT'])

                        modifiedList = main.remove_sublist(modifiedList, ['PRINT', 'INT_LIT'])
                        modifiedList = main.remove_sublist(modifiedList, ['PRINT', 'IDENT'])

                        modifiedList = main.remove_sublist(modifiedList, ['INTO', 'IDENT', 'IS', 'IDENT'])
                        modifiedList = main.remove_sublist(modifiedList, ['INTO', 'IDENT', 'IS', 'INT_LIT'])

                        modifiedList = main.remove_sublist(modifiedList, ['NEWLN'])
                        
                        try:
                            for z in range(len(copyOfExpression)):
                                modifiedList = main.remove_sublist(modifiedList, copyOfExpression[z])
                            
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
