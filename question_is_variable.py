def question_is_variable(question,variable_list):
    while True:
        answer = raw_input(question)
        if answer in variable_list:
            break
        else:
            print "Oops!  You misspelled your variable name.  Try again..."
    return answer
