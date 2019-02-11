from cscore import CameraServer

def main():
    cs = CameraServer.getInstance()
    #server = cs.getServer()
    cs.enableLogging()

    #kKeepOpen = cs.VideoSource.ConnectionStrategy.kConnectionKeepOpen
    
    usb1 = cs.startAutomaticCapture(dev=0)
    usb2 = cs.startAutomaticCapture(dev=1)

    #cs.addServer("Server 1", 1181)

    #usb1.setConnectionStrategy(VideoSource.ConnectionStrategy.kKeepOpen)
    #usb2.setConnectionStrategy(VideoSource.ConnectionStrategy.kKeepOpen)

    cs.waitForever()
