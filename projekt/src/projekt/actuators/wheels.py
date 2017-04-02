import logging; logger = logging.getLogger("morse." + __name__)

import morse.core.actuator

from morse.core.services import service, async_service, interruptible
from morse.core import status
from morse.helpers.components import add_data, add_property
from morse.core import mathutils
from morse.builder import *

class Wheels(morse.core.actuator.Actuator):
    """Write here the general documentation of your actuator.
    It will appear in the generated online documentation.
    """
    _name = "Wheels"
    _short_desc = "obracanie kol"

    # define here the data fields required by your actuator
    # format is: field name, initial value, type, description

    add_data('v', 0.0, 'float', 'Velocity')
    add_data('w', 0.0, 'float', 'angular speed')
    left=0.0
    right=0.0
    def __init__(self, obj, parent=None):
        logger.info("%s initialization" % obj.name)
        # Call the constructor of the parent class
        morse.core.actuator.Actuator.__init__(self, obj, parent)




        # Do here actuator specific initializations

        self.left_wheel = parent.bge_object.children["left_wheel"]
        self.right_wheel = parent.bge_object.children["right_wheel"]

        logger.info('Component initialized')

  
    def default_action(self):
        """ Main loop of the actuator.

        Implements the component behaviour
        """
        v=self.local_data['v']
        w=self.local_data['w']
        self.left+=0.05*v-0.05*w
        if self.left > 6.28:
           self.left=0
        if self.left <0:
           self.left=6.28

        self.right+=0.05*v+0.05*w
        if self.right > 6.28:
           self.right=0
        if self.right <0:
           self.right=6.28

        l_orientation = mathutils.Euler([1.57, self.left, 0.0])
        self.left_wheel.orientation = l_orientation.to_matrix()

        r_orientation = mathutils.Euler([1.57, self.right, 0.0])
        self.right_wheel.orientation = r_orientation.to_matrix()
