import subprocess
import config
import os
import signal

n = config.n
collector_port = config.collector_port
contour_finder_port_start = config.contour_finder_port_start
consumers_address = config.consumers_address

# Create the collector
subprocess.Popen(['python', 'collector.py', str(collector_port)])

# Create contour finders
port = contour_finder_port_start
for i in range(n):
    subprocess.Popen(['python', 'contour_finder.py', consumers_address, str(port), str(collector_port)])
    if i % 2 == 1:
        port += 1

input('Press any key to exit..\n')
os.killpg(0, signal.SIGKILL)
