CC = mpicc

test_mcast: hello_world_mcast.c
	gcc hello_world_mcast.c -std=c99 -O2 -libverbs -libumad -o test_mcast

