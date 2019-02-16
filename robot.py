import wpilib
from wpilib import RobotDrive
from networktables import NetworkTables
#from Utilities import UtilityFunctions

class MyRobot(wpilib.TimedRobot):

    def autonomousInit(self):
        pass
    
    def robotInit(self):

        self.sd = NetworkTables.getTable('SmartDashboard')
        wpilib.CameraServer.launch('vision.py:main')
        
        #Encoder
        self.encoder1 = wpilib.counter(1)
        self.encoder2 = wpilib.counter(2)
        self.encoder3 = wpilib.counter(3)
        self.encoder4 = wpilb.counter(4)
        self.encoder5 = wpilib.counter(5)
        self.encoder6 = wpilib.counter(6)
        
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
        self.leftFly = wpilib.Talon(16) #Left Fly Wheel

        #Arm Elevator Setup
        self.bottomLiftRight = wpilib.Talon(3) #Arm Lifter Right
        self.topLift = wpilib.Talon(2) #Wrist Lifte

        #Docker Setup
        self.climberRight = wpilib.Talon(1)
        self.climberLeft = wpilib.Talon(12)
        self.climberBack = wpilib.Talon(17)
        self.climberWheel = wpilib.Talon(18)


        #Robot Drive Setup
        self.robotDrive = wpilib.RobotDrive(self.leftFrontMotor, 
                                            self.leftBackMotor, 
                                            self.rightFrontMotor, 
                                            self.rightBackMotor)

        #Misc Variables Setup
        self.intakeSpeed = 0.1
        self.spitSpeed = -0.1
        
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
        if self.gamepad.getRawButton(8): #Up
            self.bottomLift.set(.1)
            #self.topLift.set(-1)
        elif self.gamepad.getRawButton(7): #Down
            self.bottomLift.set(-.1)
            #self.topLift.set(1)
        else: #Stop
            self.bottomLiftLeft.set(0)
            #self.topLift.set(0)

        #Hook
        if self.gamepad.getRawButton(5):
            self.topLift.set(.3)
        elif self.gamepad.getRawButton(6):
            self.topLift.set(-.3)
        else:
            self.topLift.set(0)
        
        #Climbing Controls
        if self.stick1.getRawButton(8):
            liftAllNumInches(MyRobot, 6, 1, .1) 
        elif self.stick1.getRawButton(9):
            self.climberWheel.set(.1)
        elif self.stick2.getRawButton(8):
            liftFrontNumInches(MyRobot, 6, -1, .1)
        elif self.stick2.getRawButton(9):
            liftBackNumInches(MyRobot, 6, -1, .1)
        else:
            self.climberWheel.set(0)

        if self.stick1.getRawButton(6):
            liftAllNumInches(MyRobot, 19, 1, .1) 
        elif self.stick1.getRawButton(5):
            self.climberWheel.set(.1)
        elif self.stick2.getRawButton(6):
            liftFrontNumInches(MyRobot, 19, -1, .1)
        elif self.stick2.getRawButton(5):
            liftBackNumInches(MyRobot, 19, -1, .1)
        else:
            self.climberWheel.set(0)


        #Two modes
            #if self.gamepad.getRawButton(3):
            #angle = robot.gyro.getAngle()
            #angle = angle % 360


            
if __name__ == '__main__':
    wpilib.run(MyRobot)
