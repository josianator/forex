import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
import time

totalStart = time.time()

# fun large globals - here for easy access...
date, bid, ask = np.loadtxt('GBPUSD1d.txt', unpack = True,
                            delimiter = ',',
                            converters = { 0 : mdates.strpdate2num('%Y%m%d%H%M%S')})
               
avgLine = ((bid + ask) / 2)   
patternAr = []
performanceAr = []
patForRec = []
              
MAXIMUM = 1e12
              
def percentChange(startPoint, currentPoint):
    try:
        return (100.00 * (float(currentPoint) - float(startPoint)) / float(abs(startPoint)))
    except:
        return MAXIMUM
    
    
def patternStorage():
    patStartTime = time.time()
    x = len(avgLine)
    
    y = 11
    while y < x:
        pattern = []
    
        # I <3 magic numbers!
        p1  = percentChange(avgLine[y - 10], avgLine[y - 9])
        p2  = percentChange(avgLine[y - 10], avgLine[y - 8])
        p3  = percentChange(avgLine[y - 10], avgLine[y - 7])
        p4  = percentChange(avgLine[y - 10], avgLine[y - 6])
        p5  = percentChange(avgLine[y - 10], avgLine[y - 5])
        p6  = percentChange(avgLine[y - 10], avgLine[y - 4])
        p7  = percentChange(avgLine[y - 10], avgLine[y - 3])
        p8  = percentChange(avgLine[y - 10], avgLine[y - 2])
        p9  = percentChange(avgLine[y - 10], avgLine[y - 1])
        p10 = percentChange(avgLine[y - 10], avgLine[y - 0])


        outcomeRange = avgLine[y + 20 : y + 30]
        currentPoint = avgLine[y]
        # avoid -infinity
        try:
            avgOutcome =  reduce(lambda x, y: x + y, outcomeRange) / len(outcomeRange)
        except Exception, e:
            print str(e)
            avgOutcome = 0
            
        futureOutcome = percentChange(currentPoint, avgOutcome)
        pattern.append(p1 )
        pattern.append(p2 )
        pattern.append(p3 )
        pattern.append(p4 )
        pattern.append(p5 )
        pattern.append(p6 )
        pattern.append(p7 )
        pattern.append(p8 )
        pattern.append(p9 )
        pattern.append(p10)
        
        patternAr.append(pattern)
        performanceAr.append(futureOutcome)
        
        y += 1
        
    patEndTime = time.time()    
    print len(patternAr)
    print len(performanceAr)
    print 'Pattern storage took:', patEndTime - patStartTime, 'seconds'
    
    
def currentPattern():
    
    cp1  = percentChange(avgLine[-11], avgLine[-10])
    cp2  = percentChange(avgLine[-11], avgLine[-9])
    cp3  = percentChange(avgLine[-11], avgLine[-8])
    cp4  = percentChange(avgLine[-11], avgLine[-7])
    cp5  = percentChange(avgLine[-11], avgLine[-6])
    cp6  = percentChange(avgLine[-11], avgLine[-5])
    cp7  = percentChange(avgLine[-11], avgLine[-4])
    cp8  = percentChange(avgLine[-11], avgLine[-3])
    cp9  = percentChange(avgLine[-11], avgLine[-2])
    cp10 = percentChange(avgLine[-11], avgLine[-1])
    
    patForRec.append(cp1)
    patForRec.append(cp2)
    patForRec.append(cp3)
    patForRec.append(cp4)
    patForRec.append(cp5)
    patForRec.append(cp6)
    patForRec.append(cp7)
    patForRec.append(cp8)
    patForRec.append(cp9)
    patForRec.append(cp10)
    
    print patForRec
    
def patternRecognition():
    for eachPattern in patternAr:
    
        sim1  = 100.00 - abs(percentChange(eachPattern[0], patForRec[0]))
        sim2  = 100.00 - abs(percentChange(eachPattern[1], patForRec[1]))
        sim3  = 100.00 - abs(percentChange(eachPattern[2], patForRec[2]))
        sim4  = 100.00 - abs(percentChange(eachPattern[3], patForRec[3]))
        sim5  = 100.00 - abs(percentChange(eachPattern[4], patForRec[4]))
        sim6  = 100.00 - abs(percentChange(eachPattern[5], patForRec[5]))
        sim7  = 100.00 - abs(percentChange(eachPattern[6], patForRec[6]))
        sim8  = 100.00 - abs(percentChange(eachPattern[7], patForRec[7]))
        sim9  = 100.00 - abs(percentChange(eachPattern[8], patForRec[8]))
        sim10 = 100.00 - abs(percentChange(eachPattern[9], patForRec[9]))
        
        simSum = 0.0
        
        simSum += sim1 
        simSum += sim2 
        simSum += sim3 
        simSum += sim4 
        simSum += sim5 
        simSum += sim6 
        simSum += sim7 
        simSum += sim8 
        simSum += sim9 
        simSum += sim10
        
        howSim = simSum / 10
        
        if howSim > 80:
            patDex = patternAr.index(eachPattern)
        
            print '###########################'
            print '###########################'
            print patForRec
            print '==========================='
            print '==========================='
            print eachPattern            
            print '---------------------------'
            print 'predicted outcome', performanceAr[patDex]
            xp = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            fig = plt.figure()
            plt.plot(xp, patForRec)
            plt.plot(xp, eachPattern)
            plt.show()
            print '###########################'
            print '###########################'
        
def graphRawFX():

    fig = plt.figure(figsize = (10, 7))
    ax1 = plt.subplot2grid((40, 40), (0, 0), rowspan = 40, colspan = 40)
    
    ax1.plot(date, bid)
    ax1.plot(date, ask)
    
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
    
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
        
    ax1_2 = ax1.twinx()
    
    ax1_2.fill_between(date, 0, (ask - bid), facecolor = 'g', alpha = 0.3)    
        
    plt.subplots_adjust(bottom = 0.23)
    
    plt.grid(True)
    plt.show()
    
    
    
def main():
    # graphRawFX()

    patternStorage()
    
    currentPattern()

    patternRecognition()

    totalTime = time.time() - totalStart
    
    print 'Entire processing time took:', totalTime, 'seconds'
    
if __name__ == '__main__':

    main()
    
    # sys.exit(0)
    