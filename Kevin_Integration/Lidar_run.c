    #include "lidarLite.h"
    #include "Lider_run.h"
    #include <stdlib.h>
	#include <stdio.h>
	#define ERange 2000 // error range 2m
    #define SAMPLERATE 20 // set the sample rate in ms




struct LData input ={0 ,0};

void to_sensor(int data1, int data2 , struct LData *(in))
{
	
	// determine range
	if((data1-ERange)> (data2+ERange))
	{
		in->LidarTriger=1;
		in->lastDistance=data2;
	}
	else if((data1+ERange)< (data2-ERange))
	{
		in->LidarTriger=0;
		in->lastDistance=data2;
	}
}

 
void run(int carry1)
{
	int fd,del,res1=0, res2=0;
    unsigned char st;
	del = SAMPLERATE;
    res1=input.lastDistance;
	fd = lidar_init(false);
	if (fd == -1) 
	{
		printf("initialization error\n");
	}
	else 
	{
		int count =0;
		while(count<2)
		{
			count++;
			if(res1==0 && res2==0 )
			{
				res1=lidar_read(fd);
			}
			else if ((res1)&& !res2)
			{
				res2=lidar_read(fd);
			}
		}
		tosensor(res1,res2,input);

	}
}