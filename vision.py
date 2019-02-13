from cscore import CameraServer

def main():
    cs = CameraServer.getInstance()
    cs.enableLogging()

    usb1 = cs.startAutomaticCapture(name='cam1', path='/dev/v4l/by-path/platform-ci_hdrc.0-usb-0:1.1:1.0-video-index0')

    usb2 = cs.startAutomaticCapture(name='cam2', path='/dev/v4l/by-path/platform-ci_hdrc.0-usb-0:1.2:1.0-video-index0')

    cs.waitForever()
