from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

from query_yes_no import query_yes_no
from get_number_of_variable_values import get_number_of_variable_values
from units import units


def func(x, a, b, c):
    return a * (x - b) ** 2 + c

# pulseheights_list = [array_day1(p_plate_1, p_plate_2, p_plate_3, p_plate_4), arrayday2(...) etc.]
# plot_variable = [('pulseheights','data_s501_2011,12,7 - 2011,12,8.h5','501','events')]
# time = [t0,t1,t2...]
# MPV_list, number_of_plates, timing = find_MPV_pulseheights(pulseheights_list, plot_variable, time, number_of_plates)

def find_MPV_pulseheights(pulseheights_list, plot_variable, time, number_of_plates):

    print ''
    show_plot = query_yes_no('Do you want to see a plot of every individual fit for every plate?')
    MPV_list = []
    timing = []

    for p in range(len(pulseheights_list)):
        #print 'Time interval %d of %d.' % (pulseheights_list.index(p) + 1, len(pulseheights_list))

        MPV_MIPs = []

        for i in range(number_of_plates):

            print 'plate ', i + 1

            p_plate_total = pulseheights_list[p][:, i] # select for this time interval the data of plate i

            # this histogram is for finding pulseheight value corresponding to the MPV bin (the highest bin besides the first photon bin)
            hist = plt.hist(p_plate_total, 150) # make a histogram from the pulseheights of plate i

            binsize = hist[0] # array with the number of pulseheights in each bin
            value = hist[1] # array with the pulseheight value corresponding to the left side of each bin.
            del hist
            plt.clf()

            # sort the bins on the number of pulseheights in each bin
            binsize_sort = sorted(binsize)

            # Here we select the the 'photon bin': the bin with the most pulseheights
            photon_bin = 0

            for g in range(len(binsize)):
                if binsize[g] == binsize_sort[-1]:

                    photon_bin = g
                    break

            # Here the minimum after the photon bin is selected
            skip = False
            for h in range(len(binsize)):
                try:
                    if h > photon_bin and binsize[h + 1] > binsize[h]:    # the bin that is more to the right than the photon bin and if the histogram is rising again.
                        lowest_bin = h
                        break   # if the lowest bin is found stop searching
                except IndexError:
                    skip = True

                    """
                    plt.hist(p_plate_total,150)
                    plt.show()

                    print 'h = ',h
                    print 'len(binsize) = ', len(binsize)
                    print 'photon_bin = ', photon_bin
                    print 'p = ',p
                    print 'time[p] = ', time[p]
                    """
            if skip == False:
                # throw away that part of the histogram left from the lowest bin
                binsize = binsize[lowest_bin:] #array with number of pulseheights in each bin from the lowest bin to the right of the histogram
                value = value[lowest_bin:] #array with the pulseheight value corresponding to the left side of each bin. from the lowest bin to the right of the histogram
                binsize_sort = sorted(binsize) # sort this selection of the bins on the number of pulseheights in each bin
                MPV_bin = binsize_sort[-1] # the largest bin of this selection is the best guess for the MPV bin.

                # calculate pulseheight value of the centre of the MPV-bin.
                for j in range(len(binsize)):
                    if binsize[j] == MPV_bin:
                        MPV_value = (value[j] - value[j - 1]) / 2 + value[j]

                interval = [100, 80, 60, 40, 30]   # we fit the data in the range (MPV_value - interval[i], MPV_value + interval[i])

                fit_values_list = []
                success = False

                # fit for every interval
                for k in interval:

                    # select the fit data that is within the interval
                    ph_red = [p for p in p_plate_total if (MPV_value - k < p < MPV_value + k)]

                    plo = plt.hist(ph_red, 40)
                    del ph_red

                    values = plo[0]
                    #print values
                    bins = plo[1]
                    del plo
                    bin_centers = (bins[:-1] + bins[1:]) / 2

                    # bins = [0,500,1000,1500] i.e. the x-value for the LEFT side of each bin
                    # bins[:-1] = [0  ,500 ,1000]
                    # bins[1:]  = [500,1000,1500]
                    # Therefore (bins[:-1] + bins[1:])/2 = [(0+500)/2 , (500+1000)/2, (1000+1500)/2]
                    #                                    = [ 250      ,  750        , 1250 ] i.e. the x-value for the CENTER side of each bin

                    del bins
                    #print bin_centers

                    plt.clf()

                    try:
                        popt, pcov = curve_fit(func, bin_centers, values, [1, MPV_value, 1])
                        del pcov
                        a = popt[0]
                        b = popt[1]
                        c = popt[2]

                        deviation = abs(MPV_value - b)

                        #print 'THE VALUES deviation,a,b,c,k:  ', deviation,a,b,c,k

                        if a < 0 and deviation < 60:
                            success = True
                            #print success
                            fit_values_list.append([deviation, a, b, c, k])

                    except RuntimeError:
                        print 'Error'

                if success:
                    fit_values_list = sorted(fit_values_list)
                    MPV_MIPs.append(fit_values_list[0][2])

                    """

                    print ''
                    afw = "Deviation  = %g" % fit_values_list[0][0]
                    print afw
                    ap = "a = %g" % fit_values_list[0][1]
                    print ap
                    bp = "b = %g" % fit_values_list[0][2]
                    print bp
                    cp = "c = %g" % fit_values_list[0][3]
                    print cp
                    kp = "k = %g" % fit_values_list[0][4]
                    print kp
                    """

                    if show_plot:

                        hist = plt.hist(p_plate_total, 150)
                        plt.yscale('log')
                        plt.axvline(fit_values_list[0][2])
                        print 'Close plot to continue...'
                        print ''
                        plt.show()
                    print 'MPV value = %.2f %s ' % (fit_values_list[0][2], units[plot_variable[0][0]])
                    print ''
                    success = False

                else:
                    MPV_MIPs.append(MPV_value)
                    print ''
                    print 'WARNING: Bad fit'
                    print ''

                    print ''
                    print 'MPV value = %.2f %s ' % (MPV_value, units[plot_variable[0][0]])
                    print ''

                    if show_plot:
                        hist = plt.hist(p_plate_total, 150)
                        plt.yscale('log')
                        plt.axvline(MPV_value)
                        print ''
                        print 'Close plot to continue...'
                        plt.show()

            elif skip == True:
                MPV_MIPs.append(None)
        print '------------------------------------------------------------'
        MPV_list.append(MPV_MIPs)
        timing.append(time[p])

    return MPV_list, number_of_plates, timing
