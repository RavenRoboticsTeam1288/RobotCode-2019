from cscore import CameraServer

### Oh my god, don't make it a global variable ###
#camSrv1 = CameraServer.addServer(name="camera1",port=1181)
#camSrv2 = CameraServer.addServer(name="camera2",port=1182)
### Seriously, please, don't f***ing do it ###

def camera1():
    camSrv1 = CameraServer.addServer(name="camera1",port=1181)
    #if you decided to be an a**hole and make it global, comment the line above and uncomment the line below#
    #instance1 = camSrv1.getInstance()
    camSrv1.enableLogging()
    usb1Src = camSrv1.startAutomaticCapture(name="cam1", path='/dev/v4l/by-id/some-path-here')
    showTime1 = camSrv1.getVideo()
    camSrv1.waitForever()

def camera2():
    camSrv2 = CameraServer.addServer(name="camera2",port=1182)
    #if you decided to be an a**hole and make it global, comment the line above and uncomment the line below#
    #instance2 = camSrv2.getInstance()
    camSrv2.enableLogging()
    usb2Src = camSrv2.startAutomaticCapture(name="cam2", path='/dev/v4l/by-id/some-other-path-here')
    showTime2 = camSrv2.getVideo()
    camSrv2.waitForever()
