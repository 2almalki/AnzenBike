    #include "lidarLite.h"
    #include "Lider_run.h"
    #include <stdlib.h>
	#include <stdio.h>
	#define ERange 2000 // error range 2m
    #define SAMPLERATE 20 // set the sample rate in ms
	#define OUT_PIN_ZONE1 6
	#define OUT_PIN_ZONE2 4
	#define ZONE1L 1500
	#define ZONE1U 3600
	#define ZONE2L 600
	#define ZONE2U 1500



struct LData input ={0,0,0};

void to_sensor(int data1, int data2 , struct LData *(in))
{
	
	// determine range
	if((data1-ERange)> (data2+ERange))
	{
		if(data1> ZONE1L && data1 < ZONE1U)
		{
			in->zone1 = 1;
			in->zone2 = 0;
		}
		else if (data1> ZONE2L && data1 < ZONE2U)
		{
			in->zone1 = 0;
			in->zone2 = 1;
		}
		else 
		{
			in->zone1 = 0;
			in->zone2 = 0;
		}

	}
	else if((data1+ERange)< (data2-ERange))
	{
		in->zone1 = 0;
		in->zone2 = 0;
	}
	in->lastDistance=data2;
}


 
void run(int carry1)
{
	int fd,del,res1=0, res2=0;
	int first_run =1;
    unsigned char st;
	del = SAMPLERATE;
    res1=input.lastDistance;
	fd = lidar_init(false);
	if ( wiringPiSetup () == -1)
	{
		return; 
	}
	pinMode (OUT_PIN , OUTPUT);
	if (fd == -1) 
	{
		printf("initialization error\n");
	}
	else 
	{
		while(true)
		{
			
				if(!res1 && !res2 && first_run )
				{
					res1=lidar_read(fd);
					first_run =0;
				}
				else if (!first_run)
				{
					res1=res2;
					res2=lidar_read(fd);
					tosensor(res1,res2,input);
				}
			
			//*
			if (input.zone1 == 1 && input.zone2 ==0)
			{
				digitalWrite(OUT_PIN_ZONE1,1);
			}
			else if (input.zone1 == 0 && input.zone2 == 1)
			{
				digitalWrite(OUT_PIN_ZONE2,1);
			}
			delay(200);

		}
			//*/

	}
}