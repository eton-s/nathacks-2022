# functions to clean raw brain data into power band data. see PythonIII workshop
# Ethan Santos, nathacks2022

import numpy as np
import matplotlib.pyplot as plt

# convert raw csv braindata (prefixed name) to returned list of
# lists of delta-gamma bands, one per channel
def rawToBands(name, channels):
    bands_lists = []
    for n in range(channels):
        bands = channelToBands(name, n)
        bands_lists += [bands]
    return bands_lists

# returns bands for channel chan_num of raw csv prefixed name
def channelToBands(name, chan_num):
    
    # reads data in to channel as list
    channel = []
    with open(name + ".csv", "r") as data:
        for line in data:
            line = line.split(",")
            channel += [float(line[chan_num])]
            
    # cancel out inverse wave
    for point in range(len(channel)):
        if(point%2 != 0):
            channel[point] = channel[point-1]
            
    # Fourier transform
    fftData = np.fft.fft(channel)
    freq = np.fft.fftfreq(len(channel))*250

    # Remove unnecessary negative reflection
    fftData = fftData[1:int(len(fftData)/2)]
    freq = freq[1:int(len(freq)/2)]

    # Recall FFT is a complex function
    fftData = np.sqrt(fftData.real**2 + fftData.imag**2)
    
    # Plot for sanity check
    # plt.plot(freq, fftData)
    # plt.xlabel("Frequency (Hz)")
    # plt.ylabel("Magnitude")
    # plt.show()
    # plt.clf()
    
    bands = fftBands(fftData, freq)
    return bands

# returns bands corresponding to fourier transform data and frequency
def fftBands(data, freq):
    bandTotals = [0,0,0,0,0]
    bandCounts = [0,0,0,0,0]

    for point in range(len(freq)):
        if(freq[point] < 4):
            bandTotals[0] += data[point]
            bandCounts[0] += 1
        elif(freq[point] < 8):
            bandTotals[1] += data[point]
            bandCounts[1] += 1
        elif(freq[point] < 12):
            bandTotals[2] += data[point]
            bandCounts[2] += 1
        elif(freq[point] < 30):
            bandTotals[3] += data[point]
            bandCounts[3] += 1
        elif(freq[point] < 100):
            bandTotals[4] += data[point]
            bandCounts[4] += 1
    
    return list(np.array(bandTotals)/np.array(bandCounts))

# plots bands, using given title
def plotBands(bands, title):
    binNames = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]
    plt.ylabel("Amplitude")
    plt.bar(binNames, bands, color="#7967e1")
    plt.title(title)
    plt.show()
    plt.clf()    

if __name__ == "__main__":
    ret = rawToBands("util/testData", 16)
    for n in range(len(ret)):
        plotBands(ret[n], "Channel " + str(n + 1))
