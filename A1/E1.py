import time
import ntplib
from datetime import datetime

# Liste von Zeitservern
servers = ['ptbtime1.ptb.de']


# Funktion zur Abfrage der Zeitabweichung
def query_time_difference(server):
    c = ntplib.NTPClient()
    response = c.request(server, version=3)
    server_time = datetime.fromtimestamp(response.tx_time)
    local_time = datetime.utcnow()
    time_difference = (local_time - server_time).total_seconds()
    return local_time, server_time, time_difference


# Schreiben der Daten in CSV-Datei
with open('time_measurements.csv', 'w') as f:
    f.write("Server,Local_Time_UTC,Server_Time_UTC,Time_Difference\n")
    for _ in range(10):  # Messungen alle 5 Minuten für eine Stunde
        for server in servers:
            local_time, server_time, time_diff = query_time_difference(server)
            line = f"{server},{local_time},{server_time},{time_diff}\n"
            f.write(line)
        time.sleep(1)
