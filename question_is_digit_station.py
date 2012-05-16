def question_is_digit_station(question,stations):
    while True:
        answer = raw_input(question)
        if str.isdigit(answer) and answer in stations:
            break
        else:
            print "Oops!  That was not a valid station_ID.  Choose from the station(s) listed above."
    return answer

