
class evaluation():
    
    def __init__(self):
        self.conditionPassed = False
    
    def checkIfInteger(self, inputExpression):
        self.conditionPassed = False
        if(str(inputExpression).lstrip("-").split('.')[0].isnumeric()):
            self.conditionPassed = True
        return self.conditionPassed

    def checkIfVariable(self, inputExpression):
        self.conditionPassed = False
        if(str(inputExpression).isalnum() and not str(inputExpression).lstrip("-").split('.')[0].isnumeric() ):
            self.conditionPassed = True
        return self.conditionPassed        
    
    def evaluateVariableValue(self, variableName, symbolTable, integerValue):
        for q in range(len(symbolTable)):
            if (variableName == symbolTable[q][1]):
                symbolTable[q][2] = integerValue
    
    def getVariableType(self, variableName, symbolTable, integerValue):
        pass

