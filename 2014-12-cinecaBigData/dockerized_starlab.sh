#!/bin/bash

# Create a docker container with devices and volumes and git it a name
docker create --name sltest -i -t 
				--device /dev/nvidia0:/dev/nvidia0 \
				--device /dev/nvidia1:/dev/nvidia1 \
				--device /dev/nvidiactl:/dev/nvidiactl \
				--device /dev/nvidia-uvm:/dev/nvidia-uvm \
				-v       ~/starlab-results:/starlab-results \
				brunetto/starlab-pub-cuda-340.46-6.0.37:20141221 bash

# Start the container
docker start sltest

# Exec commands to create ICs
docker exec sltest /slbin/makeking -n 100 -w 5 -i -u \
					| /slbin/makemass -f 8 -l 0.1 -u 40 \
					| /slbin/add_star -R 1 -Z 0.1 \
					| /slbin/scale -R 1 -M 1 > /starlab-results/testIC.txt

# Start kira
docker exec /slbin/kira -t 3 -d 1 -D 1 -f 0 -n 10 -e 0 -B -b 1 \
						< /starlab-results/testIC.txt \
						> /starlab-results/out.txt \
						2> /starlab-results/err.txt


