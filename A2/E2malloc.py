import wave
import numpy as np
import matplotlib.pyplot as plt
import tracemalloc


def load_wav_file(file_path):
    """Load a WAV file and return the audio data and sampling rate."""
    with wave.open(file_path, 'rb') as wav_file:
        # Get the audio parameters
        params = wav_file.getparams()
        num_channels, sample_width, frame_rate, num_frames = params[:4]

        # Read audio data
        audio_data = np.frombuffer(wav_file.readframes(num_frames), dtype=np.int16)

        # If the audio has more than one channel, take only the first one
        if num_channels > 1:
            audio_data = audio_data[::num_channels]

        # Normalize audio data to range [-1, 1]
        audio_data = audio_data / (2 ** 15)

        return audio_data, frame_rate


def calculate_windowed_fft(audio_data, malloc: list, window_size, offset):
    """Calculate windowed Fourier transforms for the given audio data."""
    # Create a Hamming window of the specified size
    window = np.hamming(window_size)

    # List to store all windowed FFT results
    fft_results = []


    tracemalloc.start()
    # Perform sliding window Fourier transform
    start = 0
    while start + window_size <= len(audio_data):
        end = start + window_size
        # Apply window to the audio data segment
        segment = audio_data[start:end] * window

        # Compute the Fourier transform (magnitude spectrum)
        spectrum = np.abs(np.fft.fft(segment))

        # Append the spectrum to the results list
        fft_results.append(spectrum)

        malloc.append([start, tracemalloc.get_traced_memory()])
        # Slide the window
        start = start + offset

    tracemalloc.stop()

    return np.array(fft_results)


def calculate_statistics(fft_results):
    """Calculate mean and standard deviation for each frequency across all windows."""
    # Calculate mean and standard deviation for each frequency bin
    mean_spectrum = np.mean(fft_results, axis=0)
    std_spectrum = np.std(fft_results, axis=0)

    return mean_spectrum, std_spectrum


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


def main():
    file_path = '../A1/nicht_zu_laut_abspielen.wav'  # Update with your actual file path

    # Load the WAV file
    audio_data, sample_rate = load_wav_file(file_path)

    # Parameters for windowing and Fourier transform
    window_size = 44000  # Window size in samples
    offset = 1000  # Overlap size in samples

    malloc = []
    # Calculate windowed Fourier transforms
    fft_results = calculate_windowed_fft(audio_data, malloc, window_size, offset)

    # Calculate mean and standard deviation for each frequency bin
    mean_spectrum, std_spectrum = calculate_statistics(fft_results)

    # Plot the mean spectrum and standard deviation spectrum
    plot_mean_and_std_spectrum(mean_spectrum, std_spectrum, sample_rate)

    input()


if __name__ == "__main__":
    main()
