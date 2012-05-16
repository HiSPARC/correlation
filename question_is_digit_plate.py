def question_is_digit_plate(question,number_of_plates):
    while True:
        answer = raw_input(question)
        if str.isdigit(answer) and int(answer) in range(1, number_of_plates+1):
            break
        else:
            print "Oops!  That was no valid number.  Try again..."
    return answer
