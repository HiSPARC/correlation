def question_is_digit(question):
    while True:
        answer = raw_input(question)
        answer_without_comma = answer.replace(',','')
        if str.isdigit(answer_without_comma):
            break
        else:
            print "Oops!  That was no valid number.  Try again..."
    return answer
