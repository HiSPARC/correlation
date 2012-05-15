def question_is_digit_station(question,stations):
    dummy = True
    while dummy:
        answer = raw_input(question)
        if str.isdigit(answer) and answer in stations:
            dummy=False
        else:
            print "Oops!  That was not a valid station_ID.  Choose from the station(s) listed above."
    return answer

