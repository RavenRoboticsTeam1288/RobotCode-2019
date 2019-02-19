#Put all utility functions here so they do not pollute the space
#in the main file. Put functions such as "Drive for X Time", etc. here.


#Raven Robotics 2019 Deep Space
import wpilib
from wpilib import RobotDrive

class UtilityFunctions():
    #Function to handle the gyro and turning the robot num degrees from the current heading
    #As long as this function returns false, we are not done turning
    #When this function returns true we are done turning
    def turnNumDegrees(robot, num): #-num means turn left (0 to -179), +num means turn right (1 to 180)
        robot.initialHeading = UtilityFunctions.getAnInitialHeading(robot, robot.initialHeading, robot.autoSafeToGetHeading)
        robot.autoSafeToGetHeading = False
        
        angle = robot.gyro.getAngle()
        angle = angle % 360
        if angle < 0:
            angle = angle + 360
            
        # Give an output so we can check if the gyro is working
        print(angle)
                
        desired_heading = robot.initialHeading + (1*num)#ADXRS450 gyro is backwards from previous gyro
        print('Desired: ' + str(desired_heading))
        
        if desired_heading < 0:
            desired_heading = desired_heading + 360
        elif desired_heading > 360:
            desired_heading = desired_heading - 360
            
        #desired_degrees = angle - desired_heading
        #value = current - desired
        #if value < 0 and |value| < 180 or value > 0 and |value| > 180 turn right
        #if value < 0 and |value| > 180 or value >0 and |value| < 180 turn left
        value = angle - desired_heading
        print('Value: ' + str(value))
        
        if ((value <= 0 and abs(value) <= 180) or (value >= 0 and abs(value) >= 180)): #TURN RIGHT
            if abs(value) <= robot.acceptable_heading_error:
                robot.leftFrontMotor.set(0)
                robot.leftBackMotor.set(0)
                robot.rightFrontMotor.set(0)
                robot.rightBackMotor.set(0)
                robot.autoSafeToGetHeading = True
                return True
            elif abs(value) <= robot.slower_speed_band:
                robot.leftFrontMotor.set(-1*robot.autoSlowTurnSpeed)
                robot.leftBackMotor.set(-1*robot.autoSlowTurnSpeed)
                robot.rightFrontMotor.set(-1*robot.autoSlowTurnSpeed)
                robot.rightBackMotor.set(-1*robot.autoSlowTurnSpeed)
                return False
            else:
                robot.leftFrontMotor.set(-1*robot.autoNormalTurnSpeed)
                robot.leftBackMotor.set(-1*robot.autoNormalTurnSpeed)
                robot.rightFrontMotor.set(-1*robot.autoNormalTurnSpeed)
                robot.rightBackMotor.set(-1*robot.autoNormalTurnSpeed)
                return False
        elif ((value < 0 and abs(value) > 180) or (value > 0 and abs(value) < 180)): #TURN LEFT
            if abs(value) <= robot.acceptable_heading_error:
                robot.leftFrontMotor.set(0)
                robot.leftBackMotor.set(0)
                robot.rightFrontMotor.set(0)
                robot.rightBackMotor.set(0)
                robot.autoSafeToGetHeading = True
                return True
            elif abs(value) <= robot.slower_speed_band:    
                robot.leftFrontMotor.set(1*robot.autoSlowTurnSpeed)
                robot.leftBackMotor.set(1*robot.autoSlowTurnSpeed)
                robot.rightFrontMotor.set(1*robot.autoSlowTurnSpeed)
                robot.rightBackMotor.set(1*robot.autoSlowTurnSpeed)
                return False
            else:
                robot.leftFrontMotor.set(1*robot.autoNormalTurnSpeed)
                robot.leftBackMotor.set(1*robot.autoNormalTurnSpeed)
                robot.rightFrontMotor.set(1*robot.autoNormalTurnSpeed)
                robot.rightBackMotor.set(1*robot.autoNormalTurnSpeed)
                return False
        else:
            #hopefully we never get here
            return False
            
    #function meant to get the current heading only once to be used as the starting point for a gyro turn
    def getAnInitialHeading(robot, initHeading, safeToGetHeading):
        if safeToGetHeading:
            #return the current gyro provided angle
            angle = robot.gyro.getAngle()
            angle = angle % 360
            if angle < 0:
                angle = angle + 360
            return angle
        else:
            return initHeading #we don't want to remove the heading from the variable if we keep calling this function
            
        
    # Returns an initial timestamp in seconds (need to multiply getMsClock() by 1000)
    def getAnInitialTimeStamp(robot, initTime, safeToGetTime):
        if safeToGetTime:
            time = robot.timer.getMsClock() / 1000
            return time
        else:
            return initTime
            
    def resetEncoderValue(robot, myEncoder, safeToResetEncoder):
        if safeToResetEncoder:
            myEncoder.reset()
        else:
            pass
            
    #Drive a motor a certain num seconds at the specified speed and direction        
    #Direction of 1 means FORWARD, -1 means BACKWARDS
    def driveNumSeconds(robot, motor, direction, speed, num, initTime):
        time = robot.timer.getMsClock() / 1000
        if time - initTime < num:
            motor.set(speed * direction)
            return False
        else:
            motor.set(0)
            return True
            
    #Drive motors a certain num seconds at the specified speed and direction        
    #motors list: motorName, Speed (INCLUDES direction)
    def driveMotorsNumSeconds(robot, motors, num, initTime):
        time = robot.timer.getMsClock() / 1000
        if time - initTime < num:
            for motor in motors:
                motor[0].set(motor[1])
            return False
        else:
            for motor in motors:
                motor[0].set(0)
            return True
            
    #Function to handle the digital encoder for driving forward num inches
    # Direction will either be 1 (FORWARD) or -1 (REVERSE)
    def driveNumInches(robot, num, direction, speed):
        UtilityFunctions.resetEncoderValue(robot, robot.encoder, robot.autoSafeToResetEncoder)
        inches_distance = abs(robot.encoder.get()) * .087 # (100 ticks ~ 10.188 inches)
        #print(abs(robot.encoder.get()))
        if inches_distance < num:
            #not there yet, keep going and return false (FORWARD)
            robot.leftFrontMotor.set(-direction * speed)
            robot.leftBackMotor.set(-direction * speed)
            robot.rightFrontMotor.set(direction * speed)
            robot.rightBackMotor.set(direction * speed)
            robot.autoSafeToResetEncoder = False
            print("DRIVING NUM INCHES")
            #print(inches_distance)
            return False
        else:
            #reached the end, stop and return true (STOP)
            robot.leftFrontMotor.set(0)
            robot.leftBackMotor.set(0)
            robot.rightFrontMotor.set(0)
            robot.rightBackMotor.set(0)
            robot.autoSafeToResetEncoder = True
            print("FINISHED DRIVE NUM INCHES")
            return True

    def liftAllNumInches(robot, motors, num, speed):
        UtitlityFunctions.resetEncoderValue(robot,robot.encoder, robot.autoSafeToResetEncoder)
        inches_distance = abs(robot.encoder.get()) *.087 # (100 ticks ~ 10.188 inches)
        if inches_distance < num:
            robot.climberRight.set(direction * speed)
            robot.climberLeft.set(direction * speed)
            robot.climberBack.set(direction * speed)
            robot.autoSafeToResetEncoder = False
            return False
        else:
            robot.climberRight.set(0)
            robot.climberLeft.set(0)
            robot.climberBack.set(0)
            return True

    def liftFrontNumInches(robot, num, direction, speed):
        UtitlityFunctions.resetEncoderValue(robot,robot.encoder, robot.autoSafeToResetEncoder)
        inches_distance = abs(robot.encoder.get()) *.087 # (100 ticks ~ 10.188 inches)
        if inches_distance < num:
            robot.climberRight.set(direction * speed)
            robot.climberLeft.set(direction * speed)
            robot.autoSafeToResetEncoder = False
            return False
        else:
            robot.climberRight.set(0)
            robot.climberLeft.set(0)
            return True

    def liftBackNumInches(robot, num, direction, speed):
        UtitlityFunctions.resetEncoderValue(robot,robot.encoder, robot.autoSafeToResetEncoder)
        inches_distance = abs(robot.encoder.get()) *.087 # (100 ticks ~ 10.188 inches)
        if inches_distance < num:
            robot.climberBack.set(direction * speed)
            robot.autoSafeToResetEncoder = False
            return False
        else:
            robot.climberBack.set(0)
            return True

            
    #Use the values from networkTables from the camera to determine which direction to turn the robot to align
    #to the goal. 
    def getDirectionToGoal(robot):
        #keep track of the last value we got. If either COG is 0, then we do not see a target and should just
        #use the last valid value (assuming we will occasionally drop sight of the target)
        #If too much time passes without getting a valid target, then assume we are not looking in the right
        #direction and stop trying
        
        direction = robot.ERROR
        #print(robot.sd.getValue('COG_X'))
        #Get the COG_X (and maybe COG_Y) network table values. X is what is important, we want X to be close to 80 (160 x 120 images) to be center
        if robot.sd.containsKey('COG_X'):
            x = robot.sd.getValue('COG_X')
            
            #make sure we can see a target, otherwise use last valid value
            if x == 0:
                if robot.lastCOG_X == 0:
                    #there is nothing we can do, no target, don't do anything!
                    direction = robot.ERROR
                else:
                    x = robot.lastCOG_X
            else:
                robot.lastCOG_X = x
                
            #check the direction
            #TODO: Update Target COG Location
            if x >= 1 and x <= 75: #Guessing
                direction = robot.GO_RIGHT
            elif x > 75 and x <= 85:
                direction = robot.ON_TARGET
            elif x > 85 and x <= 160:
                direction = robot.GO_LEFT
            else:
                direction = robot.ERROR
                
        else:
            #no keys, can't look for the target
            direction = robot.ERROR
           
        #Lets NOT use this for now. we can enable it if necessary
        #if direction == robot.ERROR:
        #    robot.noGoalFoundCount += 1
        #    
        #if robot.noGoalFoundCount >= 300:
        #    robot.noGoalFoundCount = 0
        #    robot.lastCOG_X = 0
        #    robot.lastCOG_Y = 0
        
        return direction
        
    def driveForTime(robot, speed, time):
        done = False
        robot.initialTime = UtilityFunctions.getAnInitialTimeStamp(robot, robot.initialTime, robot.autoSafeToGetTime)
        #Create the list of motors to command
        motorsList = []
        motorsList.append((robot.leftBackMotor, -speed))
        motorsList.append((robot.leftFrontMotor, -speed))
        motorsList.append((robot.rightFrontMotor, speed))
        motorsList.append((robot.rightBackMotor, speed))
        
        #Command the motors to turn for some time
        if UtilityFunctions.driveMotorsNumSeconds(robot, motorsList, time, robot.initialTime) == False:
            robot.autoSafeToGetTime = False
        else:
            robot.autoSafeToGetTime = True
            robot.leftBackMotor.set(0)
            robot.leftFrontMotor.set(0)
            robot.rightBackMotor.set(0)
            robot.rightFrontMotor.set(0)
            done = True
        return done

    def waitForTime(robot, time):
        done = False
        robot.initialTime = UtilityFunctions.getAnInitialTimeStamp(robot, robot.initialTime, robot.autoSafeToGetTime)
        
        if UtilityFunctions.waitNumSeconds(robot, time, robot.initialTime) == False:
            robot.autoSafeToGetTime = False
        else:
            robot.autoSafeToGetTime = True
            done = True
        return done
            
    def waitNumSeconds(robot, num, initTime):
        time = robot.timer.getMsClock() / 1000
        if time - initTime < num:
            return False
        else:
            return True

    '''
    def encoderCompare(robot, encoders, motorMove):
        for E in encoders:
            Evalue = E.get()
            for e in encoders:
                evalue = e.get()
                if Evalue - evalue > 0:
                    motorMove.update(E=False)
                else:
                    motorMove.update(E=True)
            print(motorMove)'''

    def encoderCompareUp(robot, encoder, encoderList):
        print(encoder)
        for e in encoderList:
            if e != encoder:
                if encoder.get() - e.get() > 5000:
                    print("Stop Motor: " + str(e))
                    return False
                else:
                    return True
                    
    def encoderCompareDown(robot, encoder, encoderList):
        print(encoder)
        for e in encoderList:
            if e != encoder:
                if e.get() - encoder.get() > 5000:
                    print("Stop Motor: " + str(e))
                    return False
                else:
                    return True

    def getHeight(robot, targetHeight):
        targetHeightHigh = targetHeight + 100
        targetHeightLow = targetHeight - 100
        if self.armEncoder.get() <= targetHeightHigh:
            self.drivingArm = True
            self.armMotor1.set(.1)
            self.armMotor2.set(.1)
            elif self.armEncoder.get() >= targetHeightLow:
                self.armMotor1.set(0)
                self.armMotor2.set(0)
                self.drivingArm = False
                return False
        elif self.armEncoder.get() >= targetHeightHigh:
            self.drivingArm = True
            self.armMotor1.set(-.1)
            self.armMotor2.set(-.1)
            elif self.armEncoder.get() <= targetHeightHigh:
                self.armMotor1.set(0)
                self.armMotor2.set(0)
                self.drivingArm = False
                return False
        else:
            return True
