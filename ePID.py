#-------------------------------------------------------------------------------
# Name:         ePID
# Purpose:      closed-loop error control
#
# Author:       Ethan
#
# Created:      02/05/2016
# Copyright:    (c) Ethan 2016
#-------------------------------------------------------------------------------
import time

class Timer:
    def __init__(self):
        self.startTime = 0;
        self.accumulatedTime = 0;

    def Start(self):
        self.startTime = time.time();

    def Reset(self):
        self.startTime = time.time();
        self.accumulatedTime = 0;

    def Get(self):
        return time.time() - self.startTime;

class ePID(object):
    def __init__(self, p = 0, i = 0, d = 0, errorEpsilon = 0):
        self.m_p = p;
        self.m_i = i;
        self.m_d = d;
        self.m_errorEpsilon = errorEpsilon;
        self.m_errorSum = 0;
        self.m_errorIncrement = 1;
        self.m_oldDesiredValue = 0;
        self.m_desiredValue = 0;
        self.m_originaldDesiredValue = 0;
        self.m_maxOutput = 1.0;
        self.m_output = 0;
        self.m_rampRate = 1;
        self.m_rampSum = 0;
        self.m_isRamping = True;
        self.m_error = 0;
        self.m_firstCycle = True;
        self.previousValue = 0;
        self.velocityTime = Timer();

    def setConstants(self, p, i, d):
        self.m_p = p;
        self.m_i = i;
        self.m_d = d;

    def setErrorIncrement(self, inc):
        self.m_errorIncrement = inc;

    def setErrorEpsilon(self, epsilon):
        self.m_errorEpsilon = epsilon;

    def setMaxOutput(self, max):
        self.m_maxOutput = max;

    def resetErrorSum(self):
        self.m_errorSum = 0;

    def setRampRate(self, rampRate):
        self.m_rampRate = rampRate;

    def setDesiredValue(self, desiredValue):
        self.m_desiredValue = desiredValue;

    def isDone(self):
        if (self.m_error <= self.m_errorEpsilon):
            return True
        else:
            return False

    def calcPID(self, currentValue):
        pVal = 0;
        iVal = 0;
        dVal = 0;

        if (self.m_firstCycle):
            self.m_previousValue = currentValue;
            self.m_firstCycle = False;
            self.velocityTime.Start();
            self.velocityTime.Reset();
            self.m_originaldDesiredValue = self.m_desiredValue;
            self.m_isRamping = True;
            self.m_rampSum = (self.m_maxOutput / self.m_rampRate)

        if (self.m_oldDesiredValue != self.m_desiredValue):
            self.m_firstCycle = True;

        #calculate Error
        self.m_error = self.m_desiredValue - currentValue;

        #calculate P value
        pVal = self.m_error * self.m_p;

        #calculate I value
    	if (self.m_error >= self.m_errorEpsilon):
            if (self.m_errorSum < 0):
                self.m_errorSum = 0;
            if (self.m_error < self.m_errorIncrement):
    			self.m_errorSum += self.m_error;
            else:
                self.m_errorSum += self.m_errorIncrement;

    	elif (self.m_error <= -self.m_errorEpsilon) :
            if (self.m_errorSum > 0):
                self.m_errorSum = 0;
    		if (self.m_error > -self.m_errorIncrement):
    			self.m_errorSum += self.m_error;
    		else:
    			self.m_errorSum -= self.m_errorIncrement;
        else:
    		self.m_errorSum = 0;

    	iVal = self.m_i * float(self.m_errorSum);

        #calculate D value
        if(not self.m_firstCycle and self.velocityTime.Get() != 0):
            velocity = ((currentValue - self.m_previousValue) / float(self.velocityTime.Get()));
            dVal = self.m_d * float(velocity);
    	else:
    		dVal = 0;

        #calculate output
        if(self.m_isRamping):
            self.m_output = self.m_maxOutput - (self.m_rampRate * self.m_rampSum);
            if (self.m_rampSum == 0 or self.m_error <= (self.m_originaldDesiredValue / 2)):
                self.m_isRamping = False;
            else:
                self.m_rampSum -= 1;
        else:
            self.m_output = pVal + iVal - dVal;


        #ensure the value is inside the max_output
        if (self.m_output > self.m_maxOutput):
            self.m_output = self.m_maxOutput;
        elif (self.m_output < -self.m_maxOutput):
            self.m_output = -self.m_maxOutput;

        #store values for next cycle
        self.m_previousValue = currentValue;
        self.velocityTime.Reset();
        self.m_oldDesiredValue = self.m_desiredValue;
        #return the calculated value
        return self.m_output;
