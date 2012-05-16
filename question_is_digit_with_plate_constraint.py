def question_is_digit_with_plate_constraint(question):
    while True:
        answer = raw_input(question)
        if str.isdigit(answer) and int(answer) <= 4:
            break
        else:
            print "Oops!  That was no valid number.  Try again..."
    return answer
