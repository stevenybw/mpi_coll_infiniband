#!/usr/bin/env python

import os
#from subprocess import *
import subprocess
import time
import random

TEST_ITEMS = [#"MCAST",
              "NORMAL",
              "MCAST"]
HOSTS = ['node1', 'node2', 'node3', 'node4', 'node5', 'node6', 'node7', 'node8',
         'node9', 'node10']
PREFIX = {"NORMAL": "",
          "MCAST": "MV2_USE_MCAST=1 MV2_MCAST_NUM_NODES_THRESHOLD=1"}
BCAST_GET_TRHOUGHPUT_EXEC = "./get_throughput"

MAX_MESSAGE_BYTES_IDX = 30
MAX_PROCESSES = len(HOSTS)
BCAST_TIMES = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, #1024
               100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
               64,  32,  32,  32,  32,  32,  16,  8,   4,   3, 2, 2]
RETRY_TIMES = 4

#MAX_PROCESSES = len(HOSTS)
#BCAST_TIMES = 100
#RETRY_TIMES = 1

OUTFILENAME_PREFIX = "bcast_benchmark_out"

if not os.path.exists(BCAST_GET_TRHOUGHPUT_EXEC):
    raise IOError('get_thoughput executable not found.')

print("Benchmarking Broadcast Performance...")
print("Process from 2 to %d" % MAX_PROCESSES)
print("Message length per Bcast from 4 to: 2**%d" % MAX_MESSAGE_BYTES_IDX)
print("Bcast time per test item: %s" % str(BCAST_TIMES))
print("Output file: %s.<MODE>.<TIMESTAMP>" % OUTFILENAME_PREFIX)
print("*************************************\n\n")


def random_choose_host_and_generate(num_host_to_aquire):
    random.shuffle(HOSTS)
    ret = str()
    for i in range(num_host_to_aquire-1):
        ret += HOSTS[i]
        ret += ','
    ret += HOSTS[num_host_to_aquire-1]
    return ret

TIMESTAMP = int(time.time())

for mode in TEST_ITEMS:
    print("Testing mode: " + mode)
    output_file = open('%s.%s.%d' % (OUTFILENAME_PREFIX, mode, TIMESTAMP), "w")
    output_file.write("# Row: msg_bytes, from 4 to 2**%d\n" % MAX_MESSAGE_BYTES_IDX + '\n')
    output_file.write("# Column: processes, " + str(range(2, MAX_PROCESSES + 1, 1)) + '\n')
    output_file.write('# Bcast times per test item: MAX=%d, MIN=%d\n' %
                      (max(BCAST_TIMES), min(BCAST_TIMES)))
    output_file.write('# Test items per test unit: %d\n' % RETRY_TIMES)
    prefix = PREFIX[mode]
    for msg_bytes_idx in range(2,MAX_MESSAGE_BYTES_IDX+1):
        CURRENT_BCAST_TIMES = BCAST_TIMES[msg_bytes_idx]
        msg_bytes = 2**msg_bytes_idx
        for num_process in range(2, MAX_PROCESSES+1, 1):
            results = list()
            for retry_time in range(RETRY_TIMES):
                cmd = prefix+((' mpiexec -n %d -host %s %s %d %d')
                            % (num_process,
                                random_choose_host_and_generate(min(len(HOSTS),num_process)),
                                BCAST_GET_TRHOUGHPUT_EXEC,
                                msg_bytes,
                                CURRENT_BCAST_TIMES))
                print(" Executing: " + cmd)
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                pipe_result = proc.communicate()
                pipe_stdout = pipe_result[0]
                print("Output: " + pipe_stdout)
                items = pipe_stdout.split('\n')
                print("Result: "),
                nsum = 0.0
                n = 0.0
                for item in items:
                    if(len(item) > 0):
                        #print(items),
                        nsum += float(item)
                        n += 1.0
                avg_bandwitdh = nsum/n
                print("(%d,%d) -> %.2d" % (msg_bytes, num_process, avg_bandwitdh))
                results.append(avg_bandwitdh)
            result = sorted(results)[len(results)/2]
            print(str(results) + " ==> " + str(result))
            output_file.write(str(result) + ' ')
        output_file.write('\n')
    output_file.close()
