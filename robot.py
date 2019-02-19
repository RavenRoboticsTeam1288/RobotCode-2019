import wpilib
from wpilib import RobotDrive
from networktables import NetworkTables
from Utilities import UtilityFunctions

class MyRobot(wpilib.TimedRobot):

    def autonomousInit(self):
        pass
    
    def robotInit(self):

        self.sd = NetworkTables.getTable('SmartDashboard')
        wpilib.CameraServer.launch('vision.py:main')

        #Joystick/gamepad setup
        self.stick1 = wpilib.Joystick(1) #Right
        self.stick2 = wpilib.Joystick(2) #Left
        self.gamepad = wpilib.Joystick(3) #Operator Controller

        #Drive Train Motor Setup
        self.rightFrontMotor = wpilib.Talon(7) #Right front
        self.rightBackMotor = wpilib.Talon(6) #Right back
        self.leftFrontMotor = wpilib.Talon(8) #Left front
        self.leftBackMotor = wpilib.Talon(9) #Left back

        #Ball Fly Wheel Setup
        self.rightFly = wpilib.Talon(10) #Right Fly Wheel
        self.leftFly = wpilib.Talon(11) #Left Fly Wheel

        #Arm Elevator Setup
        self.armMotor1 = wpilib.Talon(12) #Arm Lifter Bottom
        self.armMotor2 = wpilib.Talon(14)#Arm Lifter Top
        self.wristMotor = wpilib.Talon(13) #Wrist Lifter

        #Climber Setup
        self.climberRight = wpilib.Talon(4)
        self.climberLeft = wpilib.Talon(3)
        self.climberBack = wpilib.Talon(2)
        self.climberWheel = wpilib.Talon(18)


        #Robot Drive Setup
        self.robotDrive = wpilib.RobotDrive(self.leftFrontMotor, 
                                            self.leftBackMotor, 
                                            self.rightFrontMotor, 
                                            self.rightBackMotor)

        #Encoders Setup
        self.backEncoder = wpilib.Encoder(2, 3)
        self.leftEncoder = wpilib.Encoder(4, 5)
        self.rightEncoder = wpilib.Encoder(0, 1)
        self.armEncoder = wpilib.Encoder(6, 7)
        self.wristEncoder = wpilib.Encoder(8,9)

        self.backEncoder.reset()
        self.leftEncoder.reset()
        self.rightEncoder.reset()
        self.armEncoder.reset()
        self.wristEncoder.reset()

        #Misc Variables Setup
        self.intakeSpeed = 0.1
        self.spitSpeed = -0.1
        self.armSpeed = 0.1
        self.wristSpeed = 0.1
        self.encoderMotor = {self.backEncoder : self.climberBack, self.rightEncoder : self.climberRight, self.leftEncoder : self.climberLeft}
        self.actuatorMove = {self.climberBack : True, self.climberRight : True, self.climberLeft : True}
        self.armHeight1LowS = 14500
        self.armHeight1HighS = 14600
        self.armHeightLowG = 1800
        self.armHeightHighG = 1900
        self.armHeightHigh2 = 23700
        self.armHeightLow2 = 23600
        self.armHeightHigh3 = 32700
        self.armHeightLow3 = 32800
        self.extend19 = 247000
        self.extend6 = 78000
        self.fullRetract = 0
        self.extendSpeed = .35
        self.retactSpeed = -.25
        self.climbWheelSpeed = .1
        self.positionWrist = 'Start'
        self.position = 'Start'
        #The position the arm/wrist is currently in. Either that being start, 1st, 2nd, 3rd, or manual
        self.drivingArm = False
        #When the arm isn't driving then the value is False but when the robot is driving then the value is true
        self.drivingWrist = False

        
    def autonomousPeriodic(self):
            self.robotDrive.setSafetyEnabled(False)

    def disabledInit(self):
        pass

    def disabledPeriodic(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):

        self.robotDrive.setSafetyEnabled(True)

        #Joystick Axis Setup
        stick1_X = self.stick1.getX()
        stick2_Y = self.stick2.getY()
        stick2_X = self.stick2.getX()

        #Joystick Deadzone Setup
        if stick1_X > -0.05 and stick1_X < 0.05:
            stick1_X = 0
        if stick2_Y > -0.05 and stick2_Y < 0.05:
            stick2_Y = 0
        if stick2_X > -0.05 and stick2_X < 0.05:
            stick2_X = 0

        #Mecanum Drive Setup
        self.robotDrive.mecanumDrive_Cartesian(-stick2_X, -stick2_Y, -stick1_X, 0)

        #Ball intake/outtake
        if self.stick2.getRawButton(1):# and not self.limit.get():
            self.rightFly.set(self.intakeSpeed)
            self.leftFly.set(-self.intakeSpeed)
        elif self.stick1.getRawButton(1):
            self.rightFly.set(self.spitSpeed)
            self.leftFly.set(-self.spitSpeed)
        else:
            self.rightFly.set(0)
            self.leftFly.set(0)

        #Arm Elevation
        if self.gamepad.getRawButton(5): #Up
            self.drivingArm = True
            self.armMotor1.set(self.armSpeed)
            self.armMotor2.set(self.armSpeed)
            self.position = 'Manual'
            self.setPointArm = self.armEncoder.get()
        elif self.gamepad.getRawButton(6): #Down
            self.drivingArm = True
            self.armMotor1.set(-self.armSpeed)
            self.armMotor2.set(-self.armSpeed)
            self.position = 'Manual'
            self.setPointArm = self.armEncoder.get()
        elif self.gamepad.getRawButton(5) == False and self.gamepad.getRawButton(6) == False: #Stop
            self.armMotor1.set(0)
            self.armMotor2.set(0)
            self.drivingArm = False

        #Arm Stablizer
        if self.position == 'Manual' and self.drivingArm == False: 
            self.error = self.setPointArm - self.armEncoder.get()
            self.speed = self.error * .005 #.005 is the z. If the hand/arm is moving more up and down then lower the Z
            #If it is still dropping then increase z
            #Eqaution: speed = error * z
            self.armMotor1(self.speed)
            self.armMotor2(self.speed)


        #Hook
        if self.gamepad.getRawButton(7):
            self.drivingWrist = True
            self.wristMotor.set(.1)
            self.setPointWrist = self.wristEncoder.get()
            self.positionWrist = 'Manual'
        elif self.gamepad.getRawButton(8):
            self.drivingWrist = True
            self.wristMotor.set(-.1)
            self.setPointWrist = self.wristEncoder.get()
            self.positionWrist= 'Manual'
        elif not self.gamepad.getRawButton(7) and self.gamepad.getRawButton(8):
            self.wristMotor.set(0)
            self.drivingWrist = False

        #Hook Stablizer
        if self.positionWrist == 'Manual' and self.drivingWrist == False:
            self.error2 = self.setPointWrist - self.wristEncoder.get()
            self.speed2 = self.error2 * .005
            self.wristMotor.set(speed2)
        
        #Climbing Controls
        
        if self.stick1.getRawButton(8):
            if UtilityFunctions.encoderCompareUp(self, self.backEncoder, self.encoderMotor) == True and self.backEncoder.get() <= self.fullExtend:
                self.climberBack.set(self.extendSpeed)
            else:
                self.climberBack.set(0)
            if UtilityFunctions.encoderCompareUp(self, self.leftEncoder, self.encoderMotor) == True and self.leftEncoder.get() <= self.fullExtend:
                self.climberLeft.set(self.extendSpeed)
            else:
                self.climberLeft.set(0)
            if UtilityFunctions.encoderCompareUp(self, self.rightEncoder, self.encoderMotor) == True and self.rightEncoder.get() <= self.fullExtend:
                self.climberRight.set(self.extendSpeed)
            else:
                self.climberRight.set(0)
                
        elif self.stick2.getRawButton(8):
            '''if UtilityFunctions.encoderCompareDown(self, self.backEncoder, self.encoderMotor) == True and self.backEncoder.get() >= self.fullRetract:
                self.climberBack.set(self.retactSpeed)
            else:
                self.climberBack.set(0)'''
            if UtilityFunctions.encoderCompareDown(self, self.leftEncoder, self.encoderMotor) == True and self.backEncoder.get() >= self.fullRetract:
                self.climberLeft.set(self.retactSpeed)
            else:
                self.climberLeft.set(0)
            if UtilityFunctions.encoderCompareDown(self, self.rightEncoder, self.encoderMotor) == True and self.backEncoder.get() >= self.fullRetract:
                self.climberRight.set(self.retactSpeed)
            else:
                self.climberRight.set(0)
                
        elif self.stick2.getRawButton(9):
            if self.backEncoder.get() >= self.fullRetract:
                self.climberBack.set(self.retactSpeed)
            else:
                self.climberBack.set(0)
                
        else:
            self.climberRight.set(0)
            self.climberLeft.set(0)
            self.climberBack.set(0)
            
        if self.stick1.getRawButton(9):
            self.climberWheel.set(self.climbWheelSpeed)
        else:
            self.climberWheel.set(0)
            
        if self.stick1.getRawButton(11):
            print('RESET')
            self.backEncoder.reset()
            self.leftEncoder.reset()
            self.rightEncoder.reset()
            
        if self.stick2.getRawButton(11):
            print('Back: ' + str(self.backEncoder.get()))
            print('Left: ' + str(self.leftEncoder.get()))
            print('Right: ' + str(self.rightEncoder.get()))


        if self.gamepad.getRawButton(1): #Hold the button for it to work or it will just keep going 
            #To bring the arm and hand from starting position
            self.driving = True
            if self.armEncoder.get() <= self.armHeightHighG:
                self.armMotor1.set(.1)
                self.armMotor2.set(.1)
            elif self.armEncoder.get() >= self.armHeightLowG:
                self.armMotor1.set(0)
                self.armMotor2.set(0)
                if self.wristEncoder.get() <= 14300: #bring the hand up 
                    self.wristMotor.set(.1)
                elif self.wristEncoder.get() >= 14200:
                    self.wristMotor.set(0.09)
                    if self.armEncoder.get() >= self.armHeightHighS: #lower the arm to 1st position
                        self.armMotor1.set(-.1)
                        self.armMotor2.set(-.1)
                    elif self.armEncoder.get() <= self.armHeightHighS:
                        self.position = 'First'
                        self.setPoint = self.armEncoder.get()
                        self.armMotor1.set(0)
                        self.armMotor2.set(0)
                        self.driving = False

            #if the height is higher than first position
            elif self.armEncoder.get() >= 13000:
                self.armMotor1.set(-.1)
                self.armMotor2.set(-.1)
            elif self.armEncoder.get() <= 13000:
                self.position = 'First'
                self.setPoint = self.armEncoder.get()
                self.armMotor1.set(0)
                self.armMotor2.set(0)
                self.driving = False

        if self.driving == False and self.position == 'First':
            self.error = self.setPoint - self.armEncoder.get()
            self.speed = self.error * .005 #.005 is the z. If the hand/arm is moving more up and down then lower the Z
            #If it is still dropping then increase z
            #Eqaution: speed = error * z
            self.armMotor1(self.speed)
            self.armMotor2(self.speed)
       
        #motor is reverse so -1 is clockwise and +1 is counter clockwise
        
        #Climb 2 Electric Boogaloo
        '''
        if self.stick1.getRawButton(*):
            
        '''


            
if __name__ == '__main__':
    wpilib.run(MyRobot)
