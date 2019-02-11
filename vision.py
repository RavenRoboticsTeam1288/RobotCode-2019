from cscore import CameraServer

def main():
    cs = CameraServer.getInstance()
    #server = cs.getServer()
    cs.enableLogging()

    #kKeepOpen = cs.VideoSource.ConnectionStrategy.kConnectionKeepOpen
    
    usb1 = cs.startAutomaticCapture(name="cam1", path='/dev/v4l/by-id/some-path-here')
    usb2 = cs.startAutomaticCapture(name="cam2", path='/dev/v4l/by-id/some-other-path-here')

    #cs.addServer("Server 1", 1181)

    #usb1.setConnectionStrategy(VideoSource.ConnectionStrategy.kKeepOpen)
    #usb2.setConnectionStrategy(VideoSource.ConnectionStrategy.kKeepOpen)

    cs.waitForever()
