#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/time.h>

char buf[1024*1024*1024 + 1024*1024];

double currentTime()
{
	struct timeval tv;
	gettimeofday(&tv, NULL);
	return (double)tv.tv_sec + (double)tv.tv_usec/1000000.0;
}


int main(int argc, char* argv[])
{
	MPI_Init(&argc, &argv);
	int rank;
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	if(argc!=3)
	{
		fprintf(stderr, "Usage: %s <MessageLength> <SendTimes>\nReturns: Bandwidth(Bcasts/s)\n", argv[0]);
		return -1;
	}
	int messageLength = atoi(argv[1]);
	int sendTimes = atoi(argv[2]);
	if(messageLength<=0 || sendTimes<=0 || messageLength>1024*1024*1024)
	{
		fprintf(stderr, "Usage: %s <MessageLength<=1024*1024*1024> <SendTimes>\nReturns: Bandwidth(Bcasts/s)\n", argv[0]);
		return -1;
	}
	for(int i=0; i<messageLength; i++)
	{
		buf[i]=i;
	}
	double begin_time = currentTime();
	for(int i=0; i<sendTimes; i++)
	{
		if(MPI_Bcast(buf, messageLength, MPI_CHAR, 0, MPI_COMM_WORLD))
		{
			fprintf(stderr, "%d> Bcast failed.", rank);
			return -1;
		}
	}
	double end_time = currentTime();
	printf("%lf\n", (double)sendTimes/(end_time-begin_time));

	MPI_Finalize();
	return 0;
}
