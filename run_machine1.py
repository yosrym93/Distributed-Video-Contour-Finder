import subprocess
import os
import signal
import config


n = config.n
producer_port = config.producer_port
collector_port_rec = config.collector_stage1_port_rec
collector_port_send = config.contour_finder_port_start

# Create the producer
subprocess.Popen(['python', 'producer.py', str(producer_port)])

for i in range(n):
    # create otsu converter n times
    subprocess.Popen(['python', 'otsu_converter.py', str(collector_port_rec), str(producer_port)])
    if i % 2 == 1:
        # create 1 collectors for every 2 otsu collectors
        subprocess.Popen(['python', 'collector_stage1.py', str(collector_port_send), str(collector_port_rec)])
        collector_port_rec += 1
        collector_port_send += 1

if n % 2 == 1:
    # if n is odd create 1 collector for 1 otsu converter
    subprocess.Popen(['python', 'collector_stage1.py', str(collector_port_send), str(collector_port_rec)])

# press any key to kill processes
input('press any key to exit .. \n')
os.killpg(0,signal.SIGKILL)
