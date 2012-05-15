from question_is_variable import question_is_variable
import tables

def select_variable(kind_of_data_in_table,stations):
	stationID = str(stations) 
	filename = kind_of_data_in_table[0][0]
	variables = [] # needed for module 'question_is_variable'
	variable = []
	
	for j in kind_of_data_in_table:
		if variable:
			break
		if not variable:
			filename = j[0]
			if stationID in filename:
				data = tables.openFile(filename, 'r')
				if j[1] == True:
					shower_var = eval('data.root.s' + stationID + '.events.colnames')
					# Remove for novice students useless shower variables
					if 'event_id' in shower_var:
						index = shower_var.index('event_id')
						del shower_var[index]
					if 'data_reduction' in shower_var:
						index = shower_var.index('data_reduction')
						del shower_var[index]	
					if 'trigger_pattern' in shower_var:
						index = shower_var.index('trigger_pattern')
						del shower_var[index]	
					if 'traces' in shower_var:
						index = shower_var.index('traces')
						del shower_var[index]
					
					variables.extend(shower_var) 
					print ''
					print 'SHOWER variables:'
					print ''
					for k in shower_var:
					    print '-' + k
				else:
					pass
				
				if j[2] == True:
					weather_var = eval('data.root.s' + stationID + '.weather.colnames')
					
					if 'event_id' in weather_var:
						index = weather_var.index('event_id')
						del weather_var[index]
					
					variables.extend(weather_var)
					print ''
					print 'WEATHER variables:'
					print ''
					        
					for l in weather_var:
					    print '-' + l
				else:
					pass
				data.close()
				   
				if j[1] == True | j[2] == True: 
					print ''
					print 'The variables from station ' + str(stationID) + ' are shown above.'      
					var = question_is_variable('Enter the variable from station ' + stationID + " that you want to use in your analysis ( e.g. 'event_rate' ) : ", variables)
					variable.append(var)
					returnvar = variable[0]
			else:
				pass
		else:
			break
	return returnvar

"""    
stations = [502,501]
a = kind_of_data_in_table = [('data_s502_2011,6,30 - 2011,6,30.h5', True, False),('data_s502_2011,7,1 - 2011,7,31.h5', True, False),('data_s502_2011,8,1 - 2011,8,3.h5', True, False),('data_s501_2011,6,30 - 2011,6,30.h5', True, True),('data_s501_2011,7,1 - 2011,7,31.h5', True, True),('data_s501_2011,8,1 - 2011,8,3.h5', True, True)]

print a


stations = [501]
kind_of_data_in_table = [('data_s501_2011,6,30 - 2011,6,30.h5', True, True),('data_s501_2011,7,1 - 2011,7,31.h5', True, True),('data_s501_2011,8,1 - 2011,8,3.h5', True, True)]

var = select_variable(kind_of_data_in_table,stations[0])
print var
"""