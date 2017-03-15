import logging; logger = logging.getLogger("morse." + __name__)

import morse.core.actuator
 
from morse.core.services import service, async_service, interruptible
from morse.core import status
from morse.core import mathutils
from morse.helpers.components import add_data, add_property
from morse.helpers.morse_math import normalise_angle
import math
from pymorse import Morse
import numpy as np
import scipy.linalg






class Ruch(morse.core.actuator.Actuator):
    """Write here the general documentation of your actuator.
    It will appear in the generated online documentation.
    """
    _name = "Ruch"
    _short_desc = "poruszanie sie segwaya"

    # define here the data fields required by your actuator
    # format is: field name, initial value, type, description

    
#
#    add_data('v', 0.0, 'float',
#             'linear velocity in x direction (forward movement) (m/s)')
#    add_data('w', 0.0, 'float', 'angular velocity (rad/s)')

    add_property('_type', 'Velocity', 'ControlType', 'string',
                 "Kind of control, can be one of ['Velocity', 'Position']")
                 
    add_data('F', '0.0', "float",
                    'Sila')
    add_data('Reset', False, "bool",
                    'Reset')
    add_data('Debug', False, "bool",
                    'Wyswietlanie wszystkich macierzy')
    
    add_property('_speed', float('inf'), 'speed', 'float',
                 'Rotation speed, in radian by sec')
    add_property('_tolerance', 0.02, 'tolerance', 'float',
                 'Tolerance in radian to decide if the robot has reached the goal')
    add_property('_type', 'Velocity', 'ControlType', 'string',
                 "Kind of control, can be one of ['Velocity', 'Position']")
                 
    def lqr(self,A,B,Q,R):
        """Solve the continuous time lqr controller.
         
        dx/dt = A x + B u
         
        cost = integral x.T*Q*x + u.T*R*u
        """
        #ref Bertsekas, p.151
     
        #first, try to solve the ricatti equation
        X = np.matrix(scipy.linalg.solve_continuous_are(A, B, Q, R))
         
        #compute the LQR gain
        K = np.matrix(scipy.linalg.inv(R)*(B.T*X))
         
        eigVals, eigVecs = scipy.linalg.eig(A-B*K)
         
        return K  #, X, eigVals
    
    def macierzeStanu(self):
        
        M = 2.1 
        m = 1.0 
        C = 1.5*0.0980  
        g = 9.8 
        l = 0.3 
        r = 0.02 
        
        #variables
        X=(1/3)*((M*(M+6*m)*l)/(M+(3/2)*m))
        Y=(M/((M+(3/2)*m)*r))+1/l 
        A23=g*(1-(4/3)*l*(M/l)) 
        A43=g*M/l 
        
        B1=0
        B2=((4*l*Y/3*X)-(1/M*l)) 
        B3=0
        B4=-(Y/X) 
        
        
        
        
        #testy
        B1=0
        B2=0
        B3=1
        B4=0
        
        
        #A, B, C and D matrices
        A=np.array([[0, 1, 0, 0],
        [0, 0, A23, 0], 
        [0, 0, 0, 1], 
        [0, 0, A43, 0]] )
        B_1=np.array([[B1], 
        [B2], 
        [B3], 
        [B4]]) 
        B_2=C+C
        B=B_1*B_2 
     
        
#        x=10000
#        y=500
#        Q=np.array([[x, 0, 0, 0],
#        [0, 0, 0.0, 0],
#        [0, 0, y, 0],
#        [0, 0, 0, 0]])
        
        
        #macierz wag
        Q=np.array([[0, 0, 0, 0],
        [0, 0, 0.0, 0],
        [0, 0, 100, 0],
        [0, 0, 0, 0]])
        
        
        
        
        R = [[1.0]]
        K = self.lqr(A,B,Q,R)
        Ac = (A - B*K)
        Bc = B


#        return (X+(np.dot(Ac,X)+Bc*U))/self.frequency
        return (Ac,Bc)

    def __init__(self, obj, parent=None):
        logger.info("%s initialization" % obj.name)
        # Call the constructor of the parent class
        morse.core.actuator.Actuator.__init__(self, obj, parent)

        # Do here actuator specific initializations
        
        self.orientation = self.bge_object.orientation.to_euler('XYZ')
        self.wychylenie=self.orientation.y
        
        self.X=np.array([[0.0],[0.0],[0.3],[0.0]])
        
        (self.A, self.B) = self.macierzeStanu()
        
        #self.X=np.transpose(self.X)        
        
        #ze sterownikiem
#        self.A = np.array([[0,1,0,0],[-232.575,-34.1891,21.8774,0.5746],[0,0,0,1],[5017.5,737.5824,-783.9337,-12.3965]])
        
#        self.B = np.array([[0],[232.575],[0],[-5017.5]])
        
        #bez sterownika
#        self.A=np.array([[0,1,0,0],[0,0,-17.64,0],[0,0,0,1],[0,0,68.6,0]])
#        self.B=np.array([[0],[0.7355],[0],[-15.8667]])
        
        #testy
#        self.A = np.array([[0,1,0,0],[-232.575,-34.1891,21.8774,0.5746],[0,0,0,1],[5017.5,737.5824,-783.9337,-12.3965]])
        #self.B = np.array([[0],[0],[0],[-5017.5]])


        logger.info('Component initialized')

    @service


    def default_action(self):
        """ Main loop of the actuator.

        Implements the component behaviour
        """
               
        if self.local_data['Debug']:
            print("X:\n",self.X)
            print("A:\n",self.A)
            print("B:\n",self.B)
            print("F:\n",self.local_data['F'])
            
            print("A*X:\n",np.dot(self.A,self.X))
            print("B*U:\n",np.multiply(self.B,float(self.local_data['F'])))
            print("dX:\n",np.add(np.dot(self.A,self.X),np.dot(self.B,float(self.local_data['F']))))
        if self.local_data['Reset']:
            self.X=np.array([[0.0],[0.0],[0.0],[0.0]])
        
        self.X+=np.add(np.dot(self.A,self.X),np.dot(self.B,float(self.local_data['F'])))/float(self.frequency)
#        self.X=(self.X+(np.dot(self.A,self.X)+self.B*U))/self.frequency        
        
        
#        if self.X[0,2]>0.35:
#            self.X[0.2]=0.35
#        if self.X[0,2]<-0.35:
#            self.X[0.2]=-0.35
        
        
        # check if we have an on-going asynchronous tasks...
        if self._speed == float('inf'):
            # New parent orientation
            orientation = mathutils.Euler([self.position_3d.roll,
                                           self.X[2],
                                           self.position_3d.yaw])

            self.robot_parent.force_pose(None, orientation.to_matrix())
        else:
            goal = [self.position_3d.roll, self.X[2], self.position_3d.yaw]
            current_rot = [self.position_3d.roll, self.position_3d.pitch, self.position_3d.yaw]
            cmd = [0.0, 0.0, 0.0]
            for i in range(0, 3):
                diff = goal[i] - current_rot[i]
                diff = normalise_angle(diff)
                diff_abs = abs(diff)
                if diff_abs < self._tolerance:
                    cmd[i] = 0.0
                else:
                    sign = diff_abs / diff
                    if diff_abs > self._speed / self._frequency:
                        cmd[i] = sign * self._speed
                    else:
                        cmd[i] = diff_abs * self._frequency
                if self._type == 'Position':
                    cmd[i] /= self._frequency 

            self.robot_parent.apply_speed(self._type, [0.0, 0.0, 0.0], cmd)

        # implement here the behaviour of your actuator
        vx, vy, vz = 0.0, 0.0, 0.0
        rx, ry, rz = 0.0, 0.0, 0.0
        
        try:
           # vself.+=9.81*math.tan(self.local_data['pitch'])/ self.frequency
            if self._type == 'Position':
                vx = self.X[1]/ self.frequency
                rz = 0/ self.frequency
            elif self._type == 'Velocity':
                vx = self.X[1] 
                rz = 0
        # For the moment ignoring the division by zero
        # It happens apparently when the simulation starts
        except ZeroDivisionError:
            pass
        


        orientation = mathutils.Euler([self.position_3d.roll,
                                           self.X[2],
                                           self.position_3d.yaw])

#        self.robot_parent.force_pose([self.X[0], self.position_3d.y,self.position_3d.y], orientation.to_matrix())
        self.robot_parent.force_pose([-self.X[0],self.position_3d.y,self.position_3d.z], orientation.to_matrix())
        #self.robot_parent.apply_speed(self._type, [-vx, vy, vz], [rx, ry, rz])
