

#include <stdio.h>
#include <wiringPiI2C.h>
#include <stdbool.h>

#define LIDAR_LITE_ADRS 0x62

#define MEASURE_VAL 0x04
#define MEASURE_REG 0x00
#define STATUS_REG  0x47
#define DISTANCE_REG_HI 0x0f
#define DISTANCE_REG_LO 0x10  
#define VERSION_REG 0x41

#define ERROR_READ -1

// Status Bits
#define STAT_BUSY               0x01
#define STAT_REF_OVER           0x02
#define STAT_SIG_OVER           0x04
#define STAT_PIN                0x08
#define STAT_SECOND_PEAK        0x10
#define STAT_TIME               0x20
#define STAT_INVALID            0x40
#define STAT_EYE                0x80

int lidar_init(bool);
int lidar_read(int);
unsigned char  _read_byte(int, int);
unsigned char  _read_byteNZ(int, int);
unsigned char  _read_byte_raw(int, int, bool);
unsigned char lidar_version(int) ;
unsigned char lidar_status(int);
