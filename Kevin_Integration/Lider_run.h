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
    int LidarTriger;
    int lastDistance;
};

void to_sensor(int data1, int data2 , struct LData *in);
void run(int carry1);




#endif /* Lider_run_h */
