from matplotlib import pyplot as plt

def plot_mean_and_std_spectrum(mean_spectrum, std_spectrum, sample_rate):
    """Plot the mean spectrum and standard deviation spectrum."""
    # Calculate frequencies for the FFT bins
    freqs = np.fft.fftfreq(len(mean_spectrum), 1 / sample_rate)

    plt.figure(figsize=(10, 6))

    # Plotting the standard deviation spectrum as error bars
    plt.errorbar(freqs[:len(freqs) // 2], mean_spectrum[:len(freqs) // 2], yerr=std_spectrum[:len(freqs) // 2],
                 fmt='o', markersize=1, capsize=3, label='Standard Deviation', color='red')
    # Plotting the mean spectrum
    plt.plot(freqs[:len(freqs) // 2], mean_spectrum[:len(freqs) // 2], label='Mean Spectrum', color='blue')
    plt.xscale('log')

    plt.title('Mean Spectrum and Standard Deviation')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.legend()
    plt.grid(True)
    plt.show()
