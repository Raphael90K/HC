import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QFileDialog, QSlider, QCheckBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import wave
import pyqtgraph as pg


class AudioAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__(None)
        self.setWindowTitle("Audio Analyzer")
        self.setGeometry(100, 100, 1200, 800)  # Increased window size

        # Widgets
        self.filename_input = QLineEdit()
        self.load_button = QPushButton("Load WAV")
        self.sample_width_label = QLabel("Sample Width (ms):")
        self.sample_width_input = QLineEdit()
        self.sample_width_input.setText("1000")  # Default sample width
        self.plot_fft = pg.PlotWidget()
        self.canvas = FigureCanvas(plt.figure())  # Matplotlib canvas
        self.slider = QSlider()
        self.log_scale_checkbox = QCheckBox("Logarithmic Scale")

        # Layouts
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Top layout for file selection and sample width input
        file_layout = QHBoxLayout()
        main_layout.addLayout(file_layout)

        file_layout.addWidget(QLabel("Select WAV File:"))
        file_layout.addWidget(self.filename_input)
        file_layout.addWidget(self.load_button)
        file_layout.addWidget(self.sample_width_label)
        file_layout.addWidget(self.sample_width_input)

        # Plot layouts for FFT and audio visualization
        plot_layout = QHBoxLayout()
        main_layout.addLayout(plot_layout)

        plot_layout.addWidget(self.plot_fft)
        plot_layout.addWidget(self.canvas)  # Add matplotlib canvas to layout

        # Slider layout
        slider_layout = QHBoxLayout()
        main_layout.addLayout(slider_layout)

        slider_layout.addWidget(self.slider)

        # Checkbox layout
        slider_layout.addWidget(self.log_scale_checkbox)

        # Configure slider
        self.slider.setOrientation(1)  # Horizontal orientation
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)

        # Signals and Slots
        self.load_button.clicked.connect(self.select_wav_file)
        self.slider.valueChanged.connect(self.update_plots)
        self.sample_width_input.textChanged.connect(self.update_plots)  # Update plots on sample width change
        self.log_scale_checkbox.stateChanged.connect(self.update_plots)  # Update plots when checkbox state changes

    def select_wav_file(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open WAV File", "", "WAV Files (*.wav)", options=options)
        if filename:
            self.filename_input.setText(filename)
            self.load_wav_file()

    def load_wav_file(self):
        filename = self.filename_input.text()

        try:
            with wave.open(filename, 'rb') as wav_file:
                self.slider.setMaximum(wav_file.getnframes())
                # Initial plots
                self.update_plots()

        except Exception as e:
            print(f"Error loading WAV file: {e}")

    def update_plots(self):
        filename = self.filename_input.text()
        try:
            with wave.open(filename, 'rb') as wav_file:
                frames = wav_file.readframes(-1)
                audio_data = np.frombuffer(frames, dtype=np.int16)

                sample_rate = wav_file.getframerate()
                sample_width_ms = int(self.sample_width_input.text())
                sample_width = int(sample_rate * (sample_width_ms / 1000.0))  # Convert ms to samples

                # Calculate number of samples to display
                num_samples = len(audio_data)

                # Calculate start index based on slider value
                start_index = self.slider.value()
                end_index = start_index + sample_width

                if end_index > num_samples:
                    end_index = num_samples

                # Extract the selected sample width section
                section = audio_data[start_index:end_index]

                # Perform Fourier transformation
                spectrum = np.fft.fft(section)
                freq = np.fft.fftfreq(len(section), d=(1.0 / sample_rate))

                # Update FFT plot
                self.plot_fft.clear()
                self.plot_fft.plot(freq, np.abs(spectrum), pen='g')  # Plot absolute values only
                self.plot_fft.setLogMode(x=self.log_scale_checkbox.isChecked())

                # Update audio visualization plot (matplotlib)
                self.canvas.figure.clear()  # Clear previous plot
                ax = self.canvas.figure.add_subplot()
                ax.plot(np.linspace(start_index, end_index, len(section)), section, color='g')  # Plot audio waveform
                ax.set_xlabel('Sample Index')
                ax.set_ylabel('Amplitude')
                self.canvas.draw()  # Redraw canvas

        except Exception as e:
            print(f"Error updating plots: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioAnalyzer()
    window.show()
    sys.exit(app.exec_())
