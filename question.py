

def variable(question, variable_list):
    while True:
        answer = raw_input(question)
        if answer in variable_list:
            break
        else:
            print "Oops! You misspelled your variable name. Try again..."
    return answer


def digit(question):
    while True:
        answer = raw_input(question)
        answer_without_comma = answer.replace(',', '')
        if str.isdigit(answer_without_comma):
            break
        else:
            print "Oops! That was no valid number. Try again..."
    return answer


def digit_and_date(question):
    while True:
        answer = raw_input(question)
        answer_without_whitespace = answer.replace(' ', '')
        answer_without_comma = answer_without_whitespace.replace(',', '')
        if str.isdigit(answer_without_comma) and answer.count(',') == 2:
            break
        else:
            print "That was no valid input. Follow the example and try again..."
    return answer_without_whitespace


def digit_plate(question, number_of_plates):
    while True:
        answer = raw_input(question)
        if str.isdigit(answer) and int(answer) in range(1, number_of_plates + 1):
            break
        else:
            print "Oops! That was no valid number. Try again..."
    return answer


def digit_station(question, stations):
    while True:
        answer = raw_input(question)
        if str.isdigit(answer) and answer in stations:
            break
        else:
            print "Oops! That was not a valid station_ID. Choose from the station(s) listed above."
    return answer


def digit_with_constraint(question):
    while True:
        answer = raw_input(question)
        answer_without_comma = answer.replace(',', '')
        if str.isdigit(answer_without_comma) and int(answer_without_comma) <= 2:
            break
        else:
            print "Oops! That was no valid number. Try again..."
    return answer


def digit_with_plate_constraint(question):
    while True:
        answer = raw_input(question)
        if str.isdigit(answer) and int(answer) <= 4:
            break
        else:
            print "Oops! That was no valid number. Try again..."
    return answer
