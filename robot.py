import wpilib
from wpilib import RobotDrive
from networktables import NetworkTables
#from Utilities import UtilityFunctions
import vision

class MyRobot(wpilib.TimedRobot):

    def autonomousInit(self):
        pass
    
    def robotInit(self):

        self.sd = NetworkTables.getTable('SmartDashboard')
        wpilib.CameraServer.launch('vision.py:camSrv1')
        wpilib.CameraServer.launch('vision.py:camSrv2')

        #Joystick/gamepad setup
        self.stick1 = wpilib.Joystick(1) #Right
        self.stick2 = wpilib.Joystick(2) #Left
        self.gamepad = wpilib.Joystick(3) #Operator Controller

        #Servo setup
        self.rightServo = wpilib.Servo(1) #Right
        self.leftServo = wpilib.Servo(2) #Left

        #Drive Train Motor Setup
        self.rightFrontMotor = wpilib.Talon(7) #Right front
        self.rightBackMotor = wpilib.Talon(6) #Right back
        self.leftFrontMotor = wpilib.Talon(8) #Left front
        self.leftBackMotor = wpilib.Talon(9) #Left back

        #Ball Fly Wheel Setup
        #self.rightFly = wpilib.Talon(0) #Right Fly Wheel
        #self.leftFly = wpilib.Talon(16) #Left Fly Wheel

        #Arm Elevator Setup
        #self.bottomLiftRight = wpilib.Talon(0) #Arm Lifter Right
        #self.bottomLiftLeft = wpilib.Talon(16) #Arm Lifter Left
        self.topLift = wpilib.Talon(0) #Wrist Lifter

        #Limit Switch Setup
        #self.limit = wpilib.DigitalInput(1)

        #Climber Setup
        #self.climberRight = wpilib.Talon(x)
        #self.climberLeft = wpilib.Talon(x)
        #self.climberBack = wpilib.Talon(x)
        #self.climberWheel = wpilib.Talon(x)


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
        '''if self.stick2.getRawButton(1):# and not self.limit.get():
            self.rightFly.set(self.intakeSpeed)
            self.leftFly.set(-self.intakeSpeed)
        elif self.stick1.getRawButton(1):
            self.rightFly.set(self.spitSpeed)
            self.leftFly.set(-self.spitSpeed)
        else:
            self.rightFly.set(0)
            self.leftFly.set(0)'''

        #Arm Elevation
        if self.gamepad.getRawButton(6): #Up
            #self.bottomLiftLeft.set(.1)
            #self.bottomLiftRight.set(-.1)
            self.topLift.set(-1)
        elif self.gamepad.getRawButton(5): #Down
            #self.bottomLiftLeft.set(-.1)
            #self.bottomLiftRight.set(.1)
            self.topLift.set(1)
        else: #Stop
            #self.bottomLiftLeft.set(0)
            #self.bottomLiftRight.set(0)
            self.topLift.set(0)

        #Hatch servos
        '''if self.gamepad.getRawButton(*):
            self.rightServo.setAngle(180) #Extended
            self.leftServo.setAngle(180) #Extended
        elif self.gamepad.getRawButton(*):
            self.rightServo.setAngle(0) #Retracted
            self.leftServo.setAngle(0) #Retracted'''

        #Climbing Controls
        if self.stick1.getRawButton(8):
            self.climberLeft


            
if __name__ == '__main__':
    wpilib.run(MyRobot)
