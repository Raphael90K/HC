import json
import matplotlib.pyplot as plt

dir = 'logs/cumulated/'
file_name = 'windows_44100_441.json'

with open(f'{dir}{file_name}', 'r') as file:
    data = json.load(file)

start_indices = [entry[0] for entry in data]
memory_usage = [entry[1] / (10 ** 6) for entry in data]

plt.figure(figsize=(10, 6))
plt.plot(start_indices, memory_usage, linestyle='-')
plt.title('Speicherbedarf über die Startindizes')
plt.xlabel('Start Sample')
plt.ylabel('Speicherbedarf (Megabyte)')
plt.grid(True)
plt.savefig(f'{file_name[:-5]}.png')
plt.show()
