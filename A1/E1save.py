import wave
import numpy as np
import tracemalloc

import h5py


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

def calculate_windowed_fft(audio_data, malloc: list, window_size, offset, output_file):
    """Calculate windowed Fourier transforms for the given audio data and store results in a file."""
    # Create a Hamming window of the specified size
    window = np.hamming(window_size)

    # Open an HDF5 file for storing the results
    with h5py.File(output_file, 'w') as f:
        # Dataset to store FFT results
        dset = f.create_dataset('fft_results', (0, window_size), maxshape=(None, window_size), dtype=np.float32)

        tracemalloc.start()
        start = 0
        fft_index = 0
        while start + window_size <= len(audio_data):
            end = start + window_size
            # Apply window to the audio data segment
            segment = audio_data[start:end] * window

            # Compute the Fourier transform (magnitude spectrum)
            spectrum = np.abs(np.fft.fft(segment))

            # Resize dataset to accommodate new result
            dset.resize((fft_index + 1, window_size))
            dset[fft_index, :] = spectrum

            malloc.append([start, tracemalloc.get_traced_memory()])

            # Slide the window
            start = start + offset
            fft_index += 1

        tracemalloc.stop()


def calculate_statistics(fft_results):
    """Calculate mean and standard deviation for each frequency across all windows."""
    # Calculate mean and standard deviation for each frequency bin
    mean_spectrum = np.mean(fft_results, axis=0)
    std_spectrum = np.std(fft_results, axis=0)

    return mean_spectrum, std_spectrum


def main():
    file_path = '../Audios/nicht_zu_laut_abspielen.wav'  # Update with your actual file path

    # Load the WAV file
    audio_data, sample_rate = load_wav_file(file_path)

    # Parameters for windowing and Fourier transform
    window_size = 88000  # Window size in samples
    offset = 2200  # Overlap size in samples

    malloc = []
    output_file = 'fft_results.h5'

    # Calculate windowed Fourier transforms and save the windows
    calculate_windowed_fft(audio_data, malloc, window_size, offset, output_file)


if __name__ == "__main__":
    main()
