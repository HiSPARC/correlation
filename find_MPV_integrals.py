from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy import array
from query_yes_no import query_yes_no

from get_number_of_plates import get_number_of_plates
from units import units

def func(x, a, b, c):
    return a * (x - b) ** 2 + c

# pulseintegral_list = [array_day1(p_plate_1, p_plate_2, p_plate_3, p_plate_4), arrayday2(...) etc.]
# plot_variable = [('pulseheights','data_s501_2011,12,7 - 2011,12,8.h5','501','events')]
# MPV_list, number_of_plates = find_MPV_integrals(pulseintegral_list, plot_variable)

def find_MPV_integrals(pulseintegral_list, plot_variable):

    print ''
    show_plot = query_yes_no('Do you want to see a plot of every individual fit for every plate?')
    MPV_list = []

    for pi in pulseintegral_list:

        print 'Time interval %d of %d.' % (pulseintegral_list.index(pi) + 1, len(pulseintegral_list))
        print ''

        MPV_MIPs = []
        number_of_plates = get_number_of_plates(pi[0])

        for i in range(number_of_plates):

            print ''
            print 'plate ', i + 1

            p_plate_total = array(pi[:, i])

            hist = plt.hist(p_plate_total, 750)
            binsize = hist[0]
            value = hist[1]
            del hist
            plt.clf()

            binsize_sort = sorted(binsize)

            photon_bin = 0

            for g in range(len(binsize)):
                if binsize[g] == binsize_sort[-1]:
                    photon_bin = g
                    break

            for h in range(len(binsize)):
                if h > photon_bin and binsize[h + 1] > binsize[h]:
                    lowest_bin = h
                    lowest_p = value[h]
                    break

            binsize = binsize[lowest_bin:]
            value = value[lowest_bin:]
            binsize_sort = sorted(binsize)
            MPV_bin = binsize_sort[-1]

            for j in range(len(binsize)):
                if binsize[j] == MPV_bin:
                    MPV_value = (value[j] - value[j - 1]) / 2 + value[j]

            #print 'MPV = ', MPV_value

            extra = [1500, 1250, 1000, 750, 500]

            list = []
            success = False

            for k in extra:

                p_red = filter(lambda x: x < MPV_value + k and x > MPV_value - k, p_plate_total)

                plo = plt.hist(p_red, 500)
                del p_red

                values = plo[0]
                #print values
                bins = plo[1]
                del plo
                bin_centers = (bins[:-1] + bins[1:]) / 2
                del bins
                #print bin_centers

                plt.clf()


                try:
                    popt, pcov = curve_fit(func, bin_centers, values)
                    del pcov
                    a = popt[0]
                    b = popt[1]
                    c = popt[2]

                    deviation = abs(MPV_value - b)

                    #print 'THE VALUES deviation,a,b,c,k:  ', deviation,a,b,c,k

                    if a < 0 and deviation < 500:
                        success = True
                        #print success
                        list.append([deviation, a, b, c, k])

                except RuntimeError:
                    print 'Error'

            if success:
                list = sorted(list)
                MPV_MIPs.append(list[0][2])

                print ''
                afw = "Deviation  = %g" % list[0][0]
                print afw
                ap = "a = %g" % list[0][1]
                print ap
                bp = "b = %g" % list[0][2]
                print bp
                cp = "c = %g" % list[0][3]
                print cp
                kp = "k = %g" % list[0][4]
                print kp
                print ''

                if show_plot:
                    hist = plt.hist(p_plate_total, 750)
                    plt.yscale('log')
                    plt.axvline(list[0][2])
                    print 'Close plot to continue...'
                    print ''
                    plt.show()

                print 'MPV value = %.2f %s ' % (list[0][2], units[plot_variable[0][0]])
                print ''

            else:
                MPV_MIPs.append(MPV_value)
                print ''
                print 'WARNING: Bad fit'
                print ''

                print ''
                print 'MPV value = %.2f %s ' % (MPV_value, units[plot_variable[0][0]])
                print ''

                if show_plot:
                    hist = plt.hist(p_plate_total, 750)
                    plt.yscale('log')
                    plt.axvline(MPV_value)
                    print ''
                    print 'Close plot to continue...'
                    plt.show()

            #print MPV_MIPs

        MPV_list.append(MPV_MIPs)

    return MPV_list, number_of_plates
