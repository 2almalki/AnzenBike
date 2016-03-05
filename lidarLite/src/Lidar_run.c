   	#include "lidarLite.h"
	#include <wiringPi.h>
	#include "Lidar_run.h"
	#include <stdlib.h>
	#include <stdio.h>


///	
	#define ERange 2000 // error range 2m
	#define SAMPLERATE 20 // set the sample rate in ms
	#define OUT_PIN_ZONE1 5
	#define OUT_PIN_ZONE2 4
	#define ZONE1L 1500
	#define ZONE1U 4600
	#define ZONE2L 600
	#define ZONE2U 1500
	#define test 1
	#define testrun 0

//struct LData input ={-1,-1,-1};
void to_sensor(int data1, int data2 , struct LData *(in))
{
	
	// determine range
//	if((data1-ERange)> (data2+ERange))
//	{
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
if (test==1)
printf("In values  %i \t %i " , in->zone1 ,in->zone2);
/*	}
	else if((data1+ERange)< (data2-ERange))
	{
		in->zone1 = 0;
		in->zone2 = 0;
	}
*/
	in->lastDistance=data2;
}


 
void run(struct LData *(input))
{
	int fd,del,res1=0, res2=0;
	int first_run =1;
   	unsigned char st;
	del = SAMPLERATE;
	res1=input->lastDistance;
	fd = lidar_init(false);

	int asdf=0;



	if(test==1)
		printf("2 ok \n");

	if ( wiringPiSetup () == -1)
	{
		if(test==1)
		printf("failed after 2 \n");
		return 0; 
	}
	pinMode (OUT_PIN_ZONE1,OUTPUT);
	pinMode (OUT_PIN_ZONE2 , OUTPUT);
	if(test==1)
{
		digitalWrite(OUT_PIN_ZONE1,1);
		digitalWrite(OUT_PIN_ZONE2,1);
		delay(1000);
		digitalWrite(OUT_PIN_ZONE1,0);
		digitalWrite(OUT_PIN_ZONE2,0);
		
		printf("3 ok \n");


}
	if (fd == -1) 
	{
		printf("initialization error\n");
		return 1;
	}
	else 
	{
		if(test==1)
		{

		printf("entering loop \n");
		}
		while(1)
		{
			
				if(!res1 && !res2 && first_run )
				{
					res1=lidar_read(fd);
						printf("Distance 1 : %i \n", res1);
					first_run =0;
				}
				else if (!first_run)
				{
					res1=res2;
					res2=lidar_read(fd);
						printf("Distance 2 : %i \n" , res2);
					to_sensor(res1,res2,input);
				}
						printf("count : \t %i Z1 : %i \t Z2  :%i \t " ,asdf,input->zone1,input->zone2);
		
		
			if (input->zone1 == 1 && input->zone2 ==0)
			{
				digitalWrite(OUT_PIN_ZONE1,1);
				delay(200);
				digitalWrite(OUT_PIN_ZONE1,0);
			}
			else if (input->zone1 == 0 && input->zone2 == 1)
			{
				digitalWrite(OUT_PIN_ZONE2,1);
				delay(200);
				digitalWrite(OUT_PIN_ZONE2,0);
			}
		//	delay(200);

		}
	}
}

int main (void)
{
	struct LData input ={0,0,0};
	wiringPiSetup();
	pinMode(OUT_PIN_ZONE1,OUTPUT);
	pinMode(OUT_PIN_ZONE2,OUTPUT);
	if(test==1)
		printf("1 ok \n");
	if (testrun ==1)
{
	delay(200);
	printf("test \n");
	delay(200);
	digitalWrite(OUT_PIN_ZONE1,1);
	digitalWrite(OUT_PIN_ZONE2,1);
	delay(200);
	digitalWrite(OUT_PIN_ZONE1,0);
	digitalWrite(OUT_PIN_ZONE2,0);
}
	run(&input);
	return 0;
}
