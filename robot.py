import wpilib
from wpilib import RobotDrive
from networktables import NetworkTables
from Utilities import UtilityFunctions

class MyRobot(wpilib.TimedRobot):

    def autonomousInit(self):
        pass
    
    def robotInit(self):

        self.sd = NetworkTables.getTable('SmartDashboard')
        #wpilib.CameraServer.launch('vision.py:main')

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
        self.backEncoder = wpilib.Counter(2)
        self.leftEncoder = wpilib.Counter(4)
        self.rightEncoder = wpilib.Counter(0)
        self.armEncoder = wpilib.Encoder(0, 1)

        self.backEncoder.reset()
        self.leftEncoder.reset()
        self.rightEncoder.reset()
        self.armEncoder.reset()

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
        
        

        #initialize the gyro (ANALOG INPUT)
        #self.gyro = wpilib.ADXRS450_Gyro()

        
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
        if self.stick2.getRawButton(2):# and not self.limit.get():
            self.rightFly.set(self.intakeSpeed)
            self.leftFly.set(-self.intakeSpeed)
        elif self.stick1.getRawButton(1):
            self.rightFly.set(self.spitSpeed)
            self.leftFly.set(-self.spitSpeed)
        else:
            self.rightFly.set(0)
            self.leftFly.set(0)

        #Arm Elevation
        if self.gamepad.getRawButton(8): #Up
            self.armMotor1.set(self.armSpeed)
            self.armMotor2.set(self.armSpeed)
        elif self.gamepad.getRawButton(7): #Down
            self.armMotor1.set(-self.armSpeed)
            self.armMotor2.set(-self.armSpeed)
        elif self.gamepad.getRawButton(8) == False and self.gamepad.getRawButton(7) == False: #Stop
            self.armMotor1.set(0)
            self.armMotor2.set(0)


        #Hook
        if self.gamepad.getRawButton(5):
            self.wristMotor.set(.1)
        elif self.gamepad.getRawButton(6):
            self.wristMotor.set(-.1)
        elif self.gamepad.getRawButton(5) == False and self.gamepad.getRawButton(6) == False:
            self.wrist.set(0)
        
        #Climbing Controls
        if self.stick1.getRawButton(8):
            if UtilityFunctions.encoderCompare(self, self.backEncoder, self.encoderMotor) == True and self.backEncoder.get() <= 247000:
                self.climberBack.set(0.35)
            else:
                self.climberBack.set(0)
            if UtilityFunctions.encoderCompare(self, self.leftEncoder, self.encoderMotor) == True and self.leftEncoder.get() <= 247000:
                self.climberLeft.set(-0.35)
            else:
                self.climberLeft.set(0)
            if UtilityFunctions.encoderCompare(self, self.rightEncoder, self.encoderMotor) == True and self.rightEncoder.get() <= 247000:
                self.climberRight.set(0.35)
            else:
                self.climberRight.set(0)

        elif self.stick2.getRawButton(8):
            if UtilityFunctions.encoderCompare(self, self.backEncoder, self.encoderMotor) == True and self.backEncoder.get() <= 247000:
                self.climberBack.set(-0.25)
            else:
                self.climberBack.set(0)
            if UtilityFunctions.encoderCompare(self, self.leftEncoder, self.encoderMotor) == True and self.backEncoder.get() <= 247000:
                self.climberLeft.set(0.25)
            else:
                self.climberLeft.set(0)
            if UtilityFunctions.encoderCompare(self, self.rightEncoder, self.encoderMotor) == True and self.backEncoder.get() <= 247000:
                self.climberRight.set(-0.25)
            else:
                self.climberRight.set(0)
        else:
            self.climberRight.set(0)
            self.climberLeft.set(0)
            self.climberBack.set(0)

        if self.stick1.getRawButton(11):
            print('RESET')
            self.backEncoder.reset()
            self.leftEncoder.reset()
            self.rightEncoder.reset()

        if self.stick2.getRawButton(11):
            print('Back: ' + str(self.backEncoder.get()))
            print('Left: ' + str(self.leftEncoder.get()))
            print('Right: ' + str(self.rightEncoder.get()))

        if self.stick1.getRawButton(1): #Hold the button for it to work or it will just keep going 
            #To bring the arm and hand from starting position
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
                        self.armMotor1.set(0)
                        self.armMotor2.set(0)

            #if the height is higher than first position
            elif self.armEncoder.get() >= 13000:
                self.armMotor1.set(-.1)
                self.armMotor2.set(-.1)
            elif self.armEncoder.get() <= 13000:
                self.armMotor1.set(0)
                self.armMotor2.set(0)

        if self.stick2.getRawButton(1):
            self.armEncoder.reset()
            print(str(self.armEncoder.get()))
    
        '''if self.stick1.getRawButton(1):
            print('Foward: ' + str(self.randomEncoder.get()))'''

       
        #motor is reverse so -1 is clockwise and +1 is counter clockwise
        

            

        #Climb 2 Electric Boogaloo
        '''
        if self.stick1.getRawButton(*):
            
        '''


        #Two modes
            #if self.gamepad.getRawButton(3):
            #angle = robot.gyro.getAngle()
            #angle = angle % 360
            


            
if __name__ == '__main__':
    wpilib.run(MyRobot)

