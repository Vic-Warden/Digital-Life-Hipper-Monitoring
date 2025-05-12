# Documentation plan - Activity Monitoring Algorithm

## Introduction

- Aim of the algorithm : tracking physical activity using an accelerometer

- Execution: daily activity score, health tracking

## Functioning :

- Data reading (X, Y, Z)

- Digital filtering

- Intensity signal calculation

- Step detection

- Assignment to steps

- Calculation of PamScore

## Inputs / Outputs

- Inputs

    - Raw data X, Y, Z 

    - Sampling frequency 

- Outputs :

    - Steps

    - PamScore

    - Time spent by activity

## Algorithm details

- Initialization: AM_Init_v, AM_ResetDay_v

- Filtering: DC_Filter_u16

    - Double high-pass filter to eliminate signal drift

    - Motion vector norm calculation

    - Noise threshold (NOISE_THRESHOLD)

- Step counting: peak detection in step_s16 with step_timeout

- Accumulation per second: AM_EachSecond_v

- Correction: AM_CalibrationCorrection_u16, AM_RunCorrection_u16

- Zone allocation: AM_AllocateZone_v

## Utility functions

- SQ_AP3: weighted square root approximation

- Getters/Setters to access score, steps, minutes by zone

## Complexity 

- Low complexity

## Most important functions

- Activity calculation

```c
u8 AM_Calculate_Activity_v(s16 X_Axis_s16, s16 Y_Axis_s16, s16 Z_Axis_s16)
{
    u16 AbsR_u16;
    
	prev_step_count_u32=step_count_u32;
       
    AbsR_u16 = DC_Filter_u16(X_Axis_s16, Y_Axis_s16, Z_Axis_s16); // Pam algorithm
    sum_second_u16 += AbsR_u16;
   
    u8 smpCnt = 25; 
    if (AS_SPI_GetSamplingRate_v() < 10)
       smpCnt = 2;

    //call the function every two seconds
    //static u8 secondCount;
    if (++secondCount >= smpCnt) //after 10 times for 10 Hz, or after 1 time for 1 Hz
    {
        AM_EachSecond_v();
        secondCount = 0;
    }
    return 0;
}
```
- Filtering + Step detection

```c
u16 DC_Filter_u16(s16 X_Axis_s16, s16 Y_Axis_s16, s16 Z_Axis_s16)
{
    s16 X_old_old_s16 = X_old_s16;
	X_old_s16 = X_s16;
    s16 X1_old_s16 = X1_s16;
    s16 X2_old_s16 = X2_s16;
    s16 Y_old_s16 = Y_s16;
    s16 Y1_old_s16 = Y1_s16;
    s16 Y2_old_s16 = Y2_s16;
    s16 Z_old_s16 = Z_s16;
    s16 Z1_old_s16 = Z1_s16;
    s16 Z2_old_s16 = Z2_s16;
    //s16 Xf_s16;
    //s16 Yf_s16;
    //s16 Zf_s16;
    //s32 dummy_s32;
    u16 AbsR_u16;
    u8  F_u8;

	step_old_old_s16 = step_old_s16;
	step_old_s16 = step_s16;
    
    if (step_timeout_u8>0)
        step_timeout_u8--;
    
	step_s16 = SQ_AP3(X_Axis_s16,Y_Axis_s16,0);


	if ((step_old_s16 < step_s16) && (step_old_s16 < step_old_old_s16) )
    {
        max_step_s16 = step_old_s16;
    }
	if ((step_old_s16 > step_s16) && (step_old_s16 > step_old_old_s16) && (step_timeout_u8==0) && (abs(max_step_s16-step_old_s16)>50))
    {
        step_count_u32++;
        step_timeout_u8=5;
    }		

   
    //next block added by Rosty 28.08.2022
    if (AS_SPI_GetSamplingRate_v() >= 10)
    	F_u8 = 4;
    else F_u8 = 1;

 // the digital filter method: high pass filter with f_low
 // pi*f_low*t_sample = 1/(2^F_u8)   or f_low = sample_frequency/(pi * (2^F_u8) )
 // sample_frequency = 8 Hz, F_u8 = 4 => f_low =  0.16 Hz
 // sample_frequency = 1 Hz, F_u8 = 1 => f_low =  0.16 Hz
 
    X_s16 = X_Axis_s16;
    Y_s16 = Y_Axis_s16;
    Z_s16 = Z_Axis_s16;


// Put in recursive formula
    X1_s16 = (((X_s16 - X_old_s16 + X1_old_s16)<<F_u8) - X1_old_s16)>>F_u8;  // first order DC-filter for X-axis
    Y1_s16 = (((Y_s16 - Y_old_s16 + Y1_old_s16)<<F_u8) - Y1_old_s16)>>F_u8;  // first order DC-filter for Y-axis
    Z1_s16 = (((Z_s16 - Z_old_s16 + Z1_old_s16)<<F_u8) - Z1_old_s16)>>F_u8;  // first order DC-filter for Z-axis

    X2_s16 = (((X1_s16 - X1_old_s16 + X2_old_s16)<<F_u8) - X2_old_s16)>>F_u8;  // second order DC-filter for X-axis
    Y2_s16 = (((Y1_s16 - Y1_old_s16 + Y2_old_s16)<<F_u8) - Y2_old_s16)>>F_u8;  // second order DC-filter for Y-axis
    Z2_s16 = (((Z1_s16 - Z1_old_s16 + Z2_old_s16)<<F_u8) - Z2_old_s16)>>F_u8;  // second order DC-filter for Z-axis
    
// now take the vector length

    AbsR_u16 = SQ_AP3(X2_s16,Y2_s16,Z2_s16)/2; // factor of two is due to G Range and other corrections in connection with sensor choice

// if the absolute value is below the noise threshold, convert it to zero
    
   if (AbsR_u16 < NOISE_THRESHOLD)
         AbsR_u16 = 0;
    
    return AbsR_u16;
}
```

- Updated every second

```c
void AM_EachSecond_v(void)
{
#ifndef DBG_NOIMAGE
    smoothed_second_u16 = (smoothed_second_u16 * 3 + sum_second_u16/2) >> 2;  // We devide sum_second by 2 to correct for the fact that we do this each TWO seconds
    sum_second_u16 = AM_CalibrationCorrection_u16(smoothed_second_u16);         // So sum_second is now really the sum of ONE second (two seconds of sampling devided by 2)
    sum_second_u16 = AM_RunCorrection_u16(sum_second_u16);
    sum_day_u32 += sum_second_u16*2;  // And here we correct back again to make sure that the total sum of the day is correct
    //sum_epoch_u32 += sum_second_u16;
    AM_AllocateZone_v(sum_second_u16,smoothed_second_u16);    // Because sum_second is still like the old sum_second, all other functions stay the same
    sum_second_last_u16 = sum_second_u16;
    sum_second_u16 = 0;
    PamScore = sum_day_u32 >> 12;  // OUTCOME OF ACTIVITY IN Pam Points
#else
    // only for debugging, to have constant increasing of PAM
    sum_day_u32 += 1;
    PamScore = sum_day_u32 >> 2;  // OUTCOME OF ACTIVITY IN Pam Points
#endif
}
```

- Allocation to activity zones

```c
void AM_AllocateZone_v(u16 x, u16 sx)
{
    if (x > ((125 * THRESHOLD_CONVERSION)>>5))
    {
        SportMinutes++; SportMinutes++;   //we have to add TWO seconds to each zone and not one as before
    }
    else if (x > ((50 * THRESHOLD_CONVERSION)>>5))
    {
        HealthMinutes++; HealthMinutes++;   //we have to add TWO seconds to each zone and not one as before
    }
    else if (x > ((20 * THRESHOLD_CONVERSION)>>5))
    {
        LivZoneMinutes++; LivZoneMinutes++;   //we have to add TWO seconds to each zone and not one as before
    }
    
    //change frequency - only if it is not 100 Hz, no workout started
    //if (!IsMonitoringStarted())
    {
        if (sx > ((125 * THRESHOLD_CONVERSION)>>5))
        {
            //ActiveZone = 3;
            AS_SPI_SetSamplingRate_v(12);
        }
        else if (sx > ((50 * THRESHOLD_CONVERSION)>>5))
        {
            //ActiveZone = 2;
            AS_SPI_SetSamplingRate_v(12);
        }
        else if (sx > ((20 * THRESHOLD_CONVERSION)>>5))
        {
            //ActiveZone = 1;
            AS_SPI_SetSamplingRate_v(12);
        }
        else if (sx <= ((20 * THRESHOLD_CONVERSION)>>5))
        {
            //ActiveZone = 0;
            AS_SPI_SetSamplingRate_v(2);
        }
    }
    //u16 l_u16 = (u16) (((u32) LivZoneMinutes *273) >> 14);  // convert from seconds to minutes
    //u16 m_u16 = (u16) (((u32) HealthMinutes *273) >> 14);   // convert from seconds to minutes
    //u16 h_u16 = (u16) (((u32) SportMinutes *273) >> 14);    // convert from seconds to minutes
}
```

- Approximation function

```c
u16 SQ_AP3(s16 a,s16 b,s16 c)
{
    u16 fa;
    u32 sq;
    fa = abs(a)+abs(b)+abs(c);
    sq = (s32) a*a + (s32) b*b + (s32) c*c;
    if (fa>0)
    {
        sq = (sq/fa+fa)/2;
        fa = sq;
    }
    else
        fa=0;
    return fa;
}
```