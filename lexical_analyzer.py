# Module for Lexical Analysis

def lexical_analysis(filename):

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

        fileout.close()
    h.close()

    return keyW_Var_Table, OUTPUT_TOKENS