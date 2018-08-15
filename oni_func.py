from openni import openni2 as OP
from openni import _openni2


def getVideo(file_name):
    OP.initialize()
    framesColor = []
    framesDepth = []

    file = OP.Device(file_name)
    file.set_depth_color_sync_enabled
    cStream = OP.VideoStream(file,OP.SENSOR_COLOR)
    dStream = OP.VideoStream(file, OP.SENSOR_DEPTH)

    cStream.start()
    dStream.start()
    for i in range(cStream.get_number_of_frames()):
        framesColor.append(cStream.read_frame())
        framesDepth.append(dStream.read_frame())
        print(framesDepth[len(framesDepth)-1]._frame)
    cStream.stop()
    dStream.stop()
    return framesColor, framesDepth