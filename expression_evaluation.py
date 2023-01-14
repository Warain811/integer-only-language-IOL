# Module for Expression Evaluation

import numpy as np

def matching_keyword(string, list):     # gets two arguments to compare keywords on a list and determine similarity; returns bool value
    for j in list:
        if string == j:
            return True
    return False

class evaluation(): # class for helping evaluate numerical expressions
    
    def __init__(self): # intialization of variable with object scope
        self.conditionPassed = False
    
    def checkIfInteger(self, inputExpression):  # method to check if the lexeme is an integer
        self.conditionPassed = False
        if(str(inputExpression).lstrip("-").split('.')[0].isnumeric()):
            self.conditionPassed = True
        return self.conditionPassed

    def checkIfVariable(self, inputExpression):     # method to check if the lexeme is a variable
        self.conditionPassed = False
        if(str(inputExpression).isalnum() and not str(inputExpression).lstrip("-").split('.')[0].isnumeric() ):
            self.conditionPassed = True
        return self.conditionPassed        
    
    def evaluateVariableValue(self, variableName, symbolTable, integerValue):     # method to get the integer value of a given variable
        for q in range(len(symbolTable)):
            if (variableName == symbolTable[q][1]):
                symbolTable[q][2] = integerValue
    
    def expressionSyntaxEvaluation(intOrVarFlag, operationFlag, lengthOfExpression, numOperations, x, listOfTokens, formOfOperation):  # method for expression evaluation; checks if expression follows correct syntax

        errorFlag = 0
        validExpression = True
        intOrVar = ['INT_LIT', 'IDENT']

        with open('console.txt', 'a+') as fileout:
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
                            breakLoop = False       # don't break loop if numerical operations still exist within the expression

                m=0
                while(m < len(lengthOfExpression)):     
                    if (lengthOfExpression[m] in numOperations): # for every numerical operation, check if the two elements in the expression-
                        try:                                     # are operands
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
        fileout.close()

    def expressionEvaluation(self, m, symbolTable, errorDuringEvaluation, numericalExpression):  # method for evaluating expression into a numeric value when user executes code
        formOfOperation = numericalExpression[m]
        keywords = ["INT", "STR", "INTO", "IS", "BEG", "PRINT", "ADD", 
                    "SUB", "MOD", "DIV", "MULT", "NEWLN", "LOI", "IOL"]
        
        if( ( (self.checkIfInteger(numericalExpression[m+1]) or 
                self.checkIfVariable(numericalExpression[m+1])) and 
                not matching_keyword(numericalExpression[m+1], keywords) ) 
        
        and
        
        ( (self.checkIfInteger(numericalExpression[m+2]) or 
            self.checkIfVariable(numericalExpression[m+2])) and 
            not matching_keyword(numericalExpression[m+2], keywords) ) 

        ):

            if( self.checkIfInteger(numericalExpression[m+1]) ):        # if lexeme is an integer, set it as first operand
                firstIntegerLiteral = int(numericalExpression[m+1])
                
            if( self.checkIfVariable(numericalExpression[m+1]) and      # if  lexeme is a variable, get its value from the symbol, and set it as first operand
                not matching_keyword(numericalExpression[m+1], keywords) ):
                
                firstIntegerLiteral = 0
                for q in range(len(symbolTable)):
                    if (numericalExpression[m+1] == symbolTable[q][1]):
                        firstIntegerLiteral = int(symbolTable[q][2])
                
            if( self.checkIfInteger(numericalExpression[m+2]) ):        # if lexeme is an integer, set it as second operand
                secondIntegerLiteral = int(numericalExpression[m+2])  
                
            if( self.checkIfVariable(numericalExpression[m+2]) and          # if  lexeme is a variable, get its value from the symbol, and set it as second operand
                not matching_keyword(numericalExpression[m+2], keywords) ):
                
                secondIntegerLiteral = 0
                for q in range(len(symbolTable)):
                    if (numericalExpression[m+2] == symbolTable[q][1]):
                        secondIntegerLiteral = int(symbolTable[q][2])

            if formOfOperation == 'ADD':          # ADD operator
                numericalExpression[m] = (firstIntegerLiteral + secondIntegerLiteral)

            if formOfOperation == 'SUB':          # SUB operator
                numericalExpression[m] = (firstIntegerLiteral - secondIntegerLiteral) 

            if formOfOperation == 'MULT':         # MULT operator
                numericalExpression[m] = (firstIntegerLiteral * secondIntegerLiteral)

            if formOfOperation in ['MULT', 'SUB', 'ADD']:      
                del numericalExpression[m+1]
                del numericalExpression[m+1]

            if formOfOperation == 'DIV':        # DIV operator
                if (secondIntegerLiteral != 0):     
                    numericalExpression[m] = int(np.floor(firstIntegerLiteral / secondIntegerLiteral))
                    del numericalExpression[m+1]
                    del numericalExpression[m+1] 

                elif (secondIntegerLiteral == 0): # if second operand is zero (0),- 
                                                  # halt program execution since division by zero is invalid
                    errorDuringEvaluation.append('DIV')

            if formOfOperation == 'MOD':        # MOD operator
                if (secondIntegerLiteral != 0):     
                    numericalExpression[m] = int(np.floor(firstIntegerLiteral % secondIntegerLiteral))
                    del numericalExpression[m+1]
                    del numericalExpression[m+1] 
                    
                elif (secondIntegerLiteral == 0):   # if second operand is zero (0),- 
                                                    # halt program execution since modulo by zero is invalid 
                    errorDuringEvaluation.append('MOD')