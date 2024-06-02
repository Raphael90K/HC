import wave
from collections import Counter

import numpy as np
import matplotlib.pyplot as plt


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


def calculate_windowed_fft(audio_data, sample_rate, window_size, offset):
    """Calculate windowed Fourier transforms for the given audio data."""
    # Create a Hamming window of the specified size
    window = np.hamming(window_size)

    # List to store all windowed FFT results and additional information
    fft_results = []

    # Perform sliding window Fourier transform
    start = 0
    while start + window_size <= len(audio_data):
        end = start + window_size

        # Apply window to the audio data segment
        segment = audio_data[start:end] * window

        # Compute the Fourier transform (magnitude spectrum)
        spectrum = np.abs(np.fft.fft(segment))

        # Only take the first half of the spectrum (real signals)
        spectrum = spectrum[:window_size // 2]

        # Find the 10 most prominent frequencies
        freq_indices = np.argsort(spectrum)[-10:][::-1]  # Indices of the 10 largest magnitudes
        prominent_freqs = freq_indices * sample_rate / window_size  # Convert indices to frequencies
        prominent_freqs = [round(x) for x in prominent_freqs]

        # Append the start, end, and prominent frequencies to the results list
        fft_results.append({
            "start_frame": start,
            "end_frame": end,
            "prominent_frequencies": prominent_freqs
        })

        # Slide the window
        start = start + offset

    return fft_results


def find_top_frequencies(fft_results):
    """Find the 10 most frequently occurring frequencies across all windows."""
    # Collect all prominent frequencies from each window
    all_frequencies = []
    for result in fft_results:
        all_frequencies.extend(result["prominent_frequencies"])

    # Count the frequency of each unique frequency
    frequency_counter = Counter(all_frequencies)

    # Find the 10 most common frequencies
    most_common_frequencies = frequency_counter.most_common(10)

    return most_common_frequencies


def main():
    file_path = '../Audios/nicht_zu_laut_abspielen.wav'  # Update with your actual file path

    # Load the WAV file
    audio_data, sample_rate = load_wav_file(file_path)

    # Parameters for windowing and Fourier transform
    window_size = 44000  # Window size in samples
    offset = 2200  # Overlap size in samples

    # Calculate windowed Fourier transforms
    fft_results = calculate_windowed_fft(audio_data, sample_rate, window_size, offset)

    top_frequencies = find_top_frequencies(fft_results)

    print(top_frequencies)


if __name__ == "__main__":
    main()
