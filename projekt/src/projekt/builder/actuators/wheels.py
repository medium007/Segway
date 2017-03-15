from morse.builder.creator import ActuatorCreator

class Wheels(ActuatorCreator):
    _classpath = "projekt.actuators.wheels.Wheels"
    _blendname = "wheels"

    def __init__(self, name=None):
        ActuatorCreator.__init__(self, name)

