

    #include "lidarLite.h"
    
    bool _dbg;
   
    // Initialize wiring I2C interface to LidarLite
    int lidar_init(bool dbg) {
            int fd;
            _dbg = dbg;
            if (_dbg) printf("LidarLite V0.1\n\n");
            fd = wiringPiI2CSetup(LIDAR_LITE_ADRS);
            if (fd != -1) {
                lidar_status(fd);  // Dummy request to wake up device
                delay (100);
                }
            return(fd);
            }        

    // Read distance in cm from LidarLite
    int lidar_read(int fd) {
           int hiVal, loVal, i=0;
          // wiringPiI2CWriteReg8(fd,SIG,0xff);
           // send "measure" command
           hiVal = wiringPiI2CWriteReg8(fd, MEASURE_REG, MEASURE_VAL);
           if (_dbg) printf("write res=%d\n", hiVal);
           
           delay(20);
       
           // Read second byte and append with first 
           loVal = _read_byteNZ(fd, DISTANCE_REG_LO) ;        
           if (_dbg) printf(" Lo=%d\n", loVal);
           
           // read first byte 
           hiVal = _read_byte(fd, DISTANCE_REG_HI) ;             
           if (_dbg) printf ("Hi=%d ", hiVal);
           
           return ( (hiVal << 8) + loVal);
    }
    
   unsigned char lidar_version(int fd) {
            return( (unsigned char) _read_byteNZ(fd, VERSION_REG) );
            }
         
    unsigned char lidar_status(int fd) {
            return( (unsigned char) wiringPiI2CReadReg8(fd, STATUS_REG) );
            }
            
    void lidar_status_print(unsigned char status) {
    if (status != 0) 
        printf("STATUS BYTE: 0x%x ", (unsigned int) status);

if (status & STAT_BUSY) printf("busy \n");              
if (status & STAT_REF_OVER) printf("reference overflow \n");            
if (status & STAT_SIG_OVER) printf("signal overflow \n");            
if (status & STAT_PIN) printf("mode select pin \n");                 
if (status & STAT_SECOND_PEAK) printf("second peak \n");         
if (status & STAT_TIME) printf("active between pairs \n");                
if (status & STAT_INVALID) printf("no signal \n");             
if (status & STAT_EYE) printf(" eye safety \n");                 
    }    
    
    // Read a byte from I2C register.  Repeat if not ready
unsigned char  _read_byte(int fd, int reg)
 {
 return _read_byte_raw(fd, reg, true);
 }
    
        // Read Lo byte from I2C register.  Repeat if not ready or zero
unsigned char  _read_byteNZ(int fd, int reg) {
return _read_byte_raw(fd, reg, false);
}
    
    // Read byte from I2C register.  Special handling for zero value
unsigned char  _read_byte_raw(int fd, int reg, bool allowZero) {
    int i;
    unsigned char val;
    delay(1);
         while (true) {
            val = wiringPiI2CReadReg8(fd, reg);
            
            // Retry on error
            if (val == ERROR_READ || (val==0 && !allowZero) ) {
                delay (20) ;		// ms
               // if (_dbg) printf(".");
                if (i++ > 50) {
                   // Timeout
                   printf("Timeout");
                   return (ERROR_READ);
                   }
              }
              else return(val);
         }   
    }
