import pandas as pd
import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt

# Set the default sample rate to 2000 Hz
sample_rate = 2000

# Read the Excel file
df = pd.read_excel('C:\\Users\\hoang\\workplace\\practice\\emg_data.xlsx')

# Define the smoothing window in seconds
smoothing_window = 0.5

# Define the notch frequency as 60 Hz
notch_frequency = 60

# Define the High-pass cutoff frequency
high_pass_cutoff = 20

# Define the Low-pass cutoff frequency
low_pass_cutoff = 500

# Apply a 2nd-order bandpass Butterworth filter
b, a = butter(2, [high_pass_cutoff / sample_rate, low_pass_cutoff / sample_rate], btype='bandpass', analog=False)
filtered_data = lfilter(b, a, df["EMG Data"])

# Apply a 2nd-order Butterworth notch filter
b, a = butter(2, [(notch_frequency - 1) / (sample_rate / 2), (notch_frequency + 1) / (sample_rate / 2)], btype='bandstop', analog=False)
notched_data = lfilter(b, a, df["EMG Data"])

# Apply a moving average smoothing
smoothed_data = np.convolve(filtered_data, np.ones(smoothing_window) / smoothing_window, mode='same')

# Create a dataframe to store the original, filtered, and smoothed data
data = pd.DataFrame({
    'Time': df[time_col],
    'Original': df[emg_col],
    'Filtered': filtered_data,
    'Smoothed': moving_average
})

# Create a plot with 3 lines: original data, filtered data, and smoothed data
plt.plot(data['Time'], data['Original'], label='Original Data')
plt.plot(data['Time'], data['Filtered'], label='Filtered Data')
plt.plot(data['Time'], data['Smoothed'], label='Smoothed Data')
plt.legend()
plt.xlabel('Time (seconds)')
plt.ylabel('EMG Data (microvolts)')
plt.title('EMG Data Analysis')
plt.show()

# Export the data to a CSV file
data.to_csv('output.csv', index=False)
