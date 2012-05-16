def question_is_variable(question,variable_list):
    dummy = True
    while dummy:
        answer = raw_input(question)
        if answer in variable_list:
            dummy=False
        else:
            print "Oops!  You misspelled your variable name.  Try again..."
    return answer