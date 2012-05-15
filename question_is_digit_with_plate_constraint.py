def question_is_digit_with_plate_constraint(question):
    dummy = True
    while dummy:
        answer = raw_input(question)
        if str.isdigit(answer) and int(answer) <= 4:
            dummy=False
        else:
            print "Oops!  That was no valid number.  Try again..."
    return answer