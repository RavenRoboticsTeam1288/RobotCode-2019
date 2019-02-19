self.armEncoder = wpilib.Encoder(2,3)

self.wristMotor = wpilib.Talon(1)
self.armMotor1 = wpilib.Talon(2)
self.armMotor2 = wpilib.Talon(3)

self.gamepad = wpilib.Joystick(3)
self.position = ''

#Code teleop
if self.stick1.getRawButton(1): #Hold the button for it to work or it will just keep going 
    #To bring the arm and hand from starting position
    self.position = 'num1'
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

if self.position == 'num1':
