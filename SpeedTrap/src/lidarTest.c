#include "lidarLite.h"
#include <time.h>


#define maxMPH_remember 3000 //After this number of ms the system will forget the max speed
//controls how fast we display. Too slow and it doesn't seem like it's responding.
#define LOOPTIME 50

int main(int argc,char *argv[])
{

    //variables
    long lastTime = 0;
    long lastReading = 0;
    long maxMPH_timeout = 0; //Forget the max speed after some length of time

    int lastDistance = 265;
    int deltaDistance =0;
    int maxMPH = 0; //Keeps track of what the latest fastest speed is

    float newDistance;
    float avgDeltas = 0.0;
    float instantMPH;

    const byte numberOfDeltas = 8;
    float deltas[numberOfDeltas];
    byte deltaSpot = 0; //Keeps track of where we are within the deltas array

    //DELETE AFTER!!!
    int fd, i, del;
    unsigned char status, ver;

    // First arg is delay in ms (default is 50)
    if (argc > 1) {
        del = atoi(argv[1]);
    }
    else {
        del=LOOPTIME; //delay 50ms between readings

        //initialize lidar
        fd = lidar_init(false);

        if (fd == -1) {
            printf("initialization error\n");
        } else {
            while (1) {
                //Take a reading every 50ms
                if (millis() - lastReading > (LOOPTIME-1)) // 49)
                {
                    newDistance = lidar_read(fd);
                    status = lidar_status(fd);

                    //Error checking
                    if(newDistance > 3000) {
                        newDistance = 0;
                    }

                    deltaDistance = lastDistance - newDistance;
                    lastDistance = newDistance;

                    //Scan delta array to see if this new delta is sane or not
                    boolean safeDelta = true;
                    for(int x = 0 ; x < numberOfDeltas ; x++)
                    {
                        //We don't want to register jumps greater than 30cm in 50ms
                        //But if we're less than 1000cm then maybe
                        //30 works well
                        if( abs(deltaDistance - deltas[x]) > 40){
                            safeDelta = false;
                        }
                    }

                    //Insert this new delta into the array
                    if(safeDelta)
                    {
                        deltas[deltaSpot++] = deltaDistance;
                        if (deltaSpot > numberOfDeltas) {
                            deltaSpot = 0; //Wrap this variable
                        }
                    }

                    //Get average of the current deltas array
                    for (byte x = 0 ; x < numberOfDeltas ; x++)
                        avgDeltas += (float)deltas[x];
                    avgDeltas /= numberOfDeltas;

                    //22.36936 comes from a big coversion from cm per 50ms to mile per hour
                    instantMPH = 22.36936 * (float)avgDeltas / (float)LOOPTIME;

                    instantMPH = abs(instantMPH); //We want to measure as you walk away

                    ceil(instantMPH); //Round up to the next number. This is helpful if we're not displaying decimals.

                    if(instantMPH > maxMPH)
                    {
                        //printf("%d MPH \n", instantMPH);
                        maxMPH = instantMPH;
                        maxMPH_timeout = millis();
                    }
                    else //maxMPH is king
                    {
                        //printf("%d MPH\n", maxMPH);
                    }

                    if(millis() - maxMPH_timeout > maxMPH_remember)
                    {
                        maxMPH = 0;
                    }

                    //print all the values for debug
                    printf("Raw: %d\n", newDistance);
                    printf("Delta %d\n", delta);
                    printf("Delta Distance %d cm\n, deltaDistance");
                    printf("Speed %d MPH\n, instantMPH");
                    lidar_status_print(status);
                }
            }

        }
    }
}
