    #include "lidarLite.h"
    //#include <time.h>
    #include <stdlib.h>
#include <stdio.h>
#include <sys/time.h>
    #define Test  1 
    
    struct timevaln
    {
    time_t      tv_sec;     /* seconds */
    suseconds_t tv_usec;    /* microseconds */
    };

double time_diff(struct timevaln x , struct timevaln y);



    int main(int argc,char *argv[])
    {
    int fd, res, i, del;
    unsigned char st, ver;
    FILE *ofp;
    char *mode = "w";
    char outputFilename[] = "out.txt";
    int outputF=1;
     struct timevaln before , after;
    
// First arg is delay in ms (default is 1000)
if (argc > 1) 
   del = atoi(argv[1]);
else del=100;
    
    del = 20;
    fd = lidar_init(false);
   
    if (fd == -1) {
        printf("initialization error\n");
        }

    else {

  if(Test==1)
  {
    ofp = fopen(outputFilename, "w");

if (ofp == NULL) {
  fprintf(stderr, "Can't open output file %s!\n",outputFilename);
  outputF=0;
}

    gettimeofday(&before , NULL);
}
        for(i=0 ; i<1000;i++) {
            
            res = lidar_read(fd);
            st = lidar_status(fd);
            //ver = lidar_version(fd);
            gettimeofday(&after , NULL);
            printf("TIME : %3.0f , DIST : %3.0d  \n",time_diff(before , after),res);
            if(outputF & Test==1)
            fprintf(ofp,"%3.0f , %3.0d  \n", time_diff(before , after),res);
          //  lidar_status_print(st);
           // fclose(ofp);
            delay(del);
            }
            fclose(ofp);
        }
    }




double time_diff(struct timevaln x , struct timevaln y)
{
    double x_ms , y_ms , diff;
     
    x_ms = (double)x.tv_sec*1000000 + (double)x.tv_usec;
    y_ms = (double)y.tv_sec*1000000 + (double)y.tv_usec;
     
    diff = (double)y_ms - (double)x_ms;
     
    return diff;
}