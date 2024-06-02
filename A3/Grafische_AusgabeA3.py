import json
import matplotlib.pyplot as plt
import os

import numpy as np
directory = ''

# Initialisieren Sie die Figur für das Plotten
plt.figure(figsize=(10, 6))


# Iterieren durch alle Dateien im Verzeichnis
for filename in os.listdir():
    if filename.endswith('.json'):
        json_file_path = os.path.join(directory, filename)

        # JSON-Daten aus der Datei einlesen
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Start-Indizes und Speicherbedarf extrahieren
        start_indices = [entry[0] for entry in data]
        memory_usage = [entry[1] / (10 ** 6) for entry in data]

        # Datei-Basename ohne Verzeichnis und Dateiendung
        base_name = os.path.basename(filename)
        legend_name = base_name.split('_')[0]

        # Plot für jede Datei hinzufügen
        plt.plot(start_indices, memory_usage, linestyle='-', label=legend_name)

# Titel, Achsenbeschriftungen und Gitter hinzufügen
plt.title('Arbeitsspeicherbedarf')
plt.xlabel('Start Sample')
plt.ylabel('Speicherbedarf (Megabyte)')
plt.grid(True)

# Legende hinzufügen
plt.legend(title='Platform')

# Diagramm speichern
plt.savefig(f'{directory}combined_plot.png')

# Diagramm anzeigen
plt.show()
