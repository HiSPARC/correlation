def question_is_digit_plate(question,number_of_plates):
    dummy = True
    while dummy:
        answer = raw_input(question)
        if str.isdigit(answer) and int(answer) in range(1,number_of_plates+1):
            dummy=False
        else:
            print "Oops!  That was no valid number.  Try again..."
    return answer