# Module for Semantic Analysis

import main

def semantic_analysis(filename):
    keywords = ["INT", "STR", "INTO", "IS", "BEG",
                "PRINT", "ADD", "SUB", "MOD", "DIV", "MULT", "NEWLN", "LOI", "IOL"]
    numOperations = ['ADD', 'SUB', 'MULT', 'DIV', 'MOD']
    listOfLexemes = []      
    keywordVariablePairs = []

    with open("console.txt") as g:      # output from the syntax analysis will then be shown in the GUI console
                    output_string = g.read()        # read the input 
    g.close()

    if output_string == '':   # if no errors from analysis were found in console.txt, proceed to semantic analysis 

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
                        
                        if main.matching_keyword(listOfLexemes[x][y], ['INTO']):     # semantic analysis for INTO keyword

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
                        if main.matching_keyword(listOfLexemes[x][y], ['IS']):       # semantic analysis for IS keyword

                            if(str(listOfLexemes[x][y+1]).isalnum() and not str(listOfLexemes[x][y+1]).isnumeric() and 
                            not main.matching_keyword(listOfLexemes[x][y+1], keywords)):

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

                        if main.matching_keyword(listOfLexemes[x][y], ['BEG']):  # semantic analysis for BEG keyword

                            matched = 0
                            for i in range(len(keywordVariablePairs)):
                                
                                if(keywordVariablePairs[i][1] == listOfLexemes[x][y+1]):
                                    matched = 1

                            if (matched == 0):                      # if variable for BEG keyword is not yet declared, print an error on console
                                fileout.write("^Error in line "+str(x+1)+": "+listOfLexemes[x][y+1]+" is undeclared."+"\n")
                        
                        if main.matching_keyword(listOfLexemes[x][y], ['PRINT']):    # semantic analysis for PRINT keyword

                            if(str(listOfLexemes[x][y+1]).isalnum() and not str(listOfLexemes[x][y+1]).isnumeric() and
                            not main.matching_keyword(listOfLexemes[x][y+1], keywords)):

                                matched = 0
                                for i in range(len(keywordVariablePairs)):
                                    
                                    if(keywordVariablePairs[i][1] == listOfLexemes[x][y+1]):
                                        matched = 1

                                if (matched == 0):                  # if variable for PRINT keyword is not yet declared, print an error on console
                                    fileout.write("^Error in line "+str(x+1)+": "+listOfLexemes[x][y+1]+" is undeclared."+"\n")
                        
                        if (main.matching_keyword(listOfLexemes[x][y], ['PRINT']) or main.matching_keyword(listOfLexemes[x][y], ['IS'])) and main.matching_keyword(listOfLexemes[x][y+1], numOperations):
                            # semantic analysis for numerical expressions that come after PRINT and IS

                            numericalExpression = []        # 'numericalExpression' is storage for numerical expressions
                            counter = 0                     # 'counter' for scanning through the list
                            
                            try:
                                # this will check through the keyword's operations and append into 
                                # 'numericalExpression' list whenever operators and operands appear 
                                while(True):
                                    if (listOfLexemes[x][y+1+counter] in numOperations):
                                        numericalExpression.append(listOfLexemes[x][y+1+counter])
                                    
                                    elif ( (str(listOfLexemes[x][y+1+counter]).isalnum() or str(listOfLexemes[x][y+1+counter]).isnumeric() ) and
                                        not main.matching_keyword(listOfLexemes[x][y+1+counter], keywords)):
                                        numericalExpression.append(listOfLexemes[x][y+1+counter])
                                    else:
                                        break
                                    counter += 1
                            except:
                                pass
                            
                            for i in range(len(numericalExpression)):   # loop through the 'numericalExpression' list
                            
                                if (str(numericalExpression[i]).isalnum() and (not str(numericalExpression[i]).isnumeric() and
                                    not main.matching_keyword(numericalExpression[i], keywords))):

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
    return listOfLexemes, keywordVariablePairs