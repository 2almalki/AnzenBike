//
//  Lider_run.h
//  Project
//
//  Created by Kevin on 2016-02-03.
//  Copyright © 2016 Kevin. All rights reserved.
//
#ifndef Lider_run_h
#define Lider_run_h
struct LData
{
    int zone1;
    int zone2;
    int lastDistance;
};

void to_sensor(int data1, int data2 , struct LData *in);
void run(struct LData *(input));




#endif /* Lider_run_h */
