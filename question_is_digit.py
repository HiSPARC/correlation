def question_is_digit(question):
    dummy = True
    while dummy:
        answer = raw_input(question)
        answer_without_comma = answer.replace(',','')
        if str.isdigit(answer_without_comma):
            dummy=False
        else:
            print "Oops!  That was no valid number.  Try again..."
    return answer