	#include <Python/Python.h>
    #include <stdlib.h>
	#include <stdio.h>
	#include <pthread.h>
	#include "Lider_run.h"
    // define statment
    #define LIDAR 0
    #define SMC 1
    #define USC 2
    #define DISPLAY 3
    #define MAX_THREAD 5
    #define DATASIZEMAX 6
    // struct
    struct Read_data{
        int * Lidar ;
        int * UCS;
    };

    // global / extern
    extern struct LData input;
    int poweroff=0;
    pthread_mutex_t LidarLock;
    pthread_mutex_t UCSLock;
    void *lidar_Thread(void * out);
    void *smc_thread(void *);
    void *ucs_thread(void * out);
    void *display_Thread(void * out);

    int main(void) //int argc,char *argv[])
    {
        // data array
        int LidarTrigger;
        int UltrsonicSensor;
        
        // thread veriable and checks

        pthread_t thread[MAX_THREAD]; // create number of threads
        int check_thread[MAX_THREAD];
        struct Read_data output ;
        output.Lidar =& LidarTrigger;
        output.UCS =&UltrsonicSensor;
        
     //   pthread_t Lidar,Camera,Ultrsonic,Display,Lane,lights;
	//int DE_Lidar,DE_Camera,DE_Ultrsonic,DE_Display,DE_Lane,DE_lights;
        
    check_thread[LIDAR] =   pthread_create(&thread[LIDAR], NULL,lidar_Thread, (void*)& LidarTrigger);
    check_thread[SMC]=      pthread_create(&thread[SMC], NULL,smc_thread, NULL);
    check_thread[USC]=      pthread_create(&thread[USC], NULL,ucs_thread, (void*)& UltrsonicSensor);
    check_thread[DISPLAY]=  pthread_create(&thread[DISPLAY], NULL,display_Thread,(void*)& output);
	// // camera
	//// US
	//// display and or out back
	int temp=1;
	for(int i=0 ; i<MAX_THREAD ; i++)
	{
		temp=temp*check_thread[i];
        if (!temp)
        {
            // exit?
        }
	}


	pthread_mutex_destroy(&LidarLock);
}


void *lidar_Thread(void * out)
{
	int value=(int)out ;
	
	while(!poweroff==0)
	{
        run(input.lastDistance);
		// call and run lidar
		pthread_mutex_lock(&LidarLock);
		value= input.lastDistance;
		pthread_mutex_unlock(&LidarLock);
	}
    return 0;
}


void *smc_thread(void * out)
{
    
    while(!poweroff==0)
    {
        Py_SetProgramName("richard add the program name here");
        Py_Initialize();
        Py_Finalize();
        
        // delay 200 // might need this ???
    }
    
    return 0;
}

void *ucs_thread(void * out)
{
    while(!poweroff==0)
    {
        Py_SetProgramName("allen add the program name here");
        Py_Initialize();
        Py_Finalize();
        
        // delay 200 // might need this ???
    }
    return 0;
}

void *display_Thread(void * out)
{
    while(!poweroff==0)
    {
        
    }
    return 0;
}