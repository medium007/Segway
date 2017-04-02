from morse.builder.creator import ActuatorCreator

class Ruch(ActuatorCreator):
    _classpath = "projekt.actuators.ruch.Ruch"
    _blendname = "ruch"

    def __init__(self, name=None):
        ActuatorCreator.__init__(self, name)

