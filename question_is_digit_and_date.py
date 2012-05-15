def question_is_digit_and_date(question):
    dummy = True
    while dummy:
        answer = raw_input(question)
        answer_without_whitespace = answer.replace(' ','')
        answer_without_comma = answer_without_whitespace.replace(',','')
        if str.isdigit(answer_without_comma) and answer.count(',') == 2:
            dummy=False
        else:
            print "That was no valid input. Follow the example and try again..."
    return answer_without_whitespace