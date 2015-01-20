# mpi_coll_infiniband
MPI Collective Operation optimized for InfiniBand fabric.

InfiniBand Multicast Benchmark Tool

1. Start the benchmark server

Before benchmarking, a server should be run at a node to infinitely
broadcasting data.

	mcast_benchmark server

2. Start the benchmark client

**** Notice: Each server or client should be run on different nodes. ****

There are two modes for benchmarking: performance and correctness.

For bandwitdh, the client joins the broadcast group and receives data,
it generate current average bandwitdh per time interval.

For correctness, the client will verify each package it receives using
per byte comparism. Output message if mistake happens.
