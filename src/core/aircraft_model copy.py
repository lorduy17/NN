from src.domain.aircraft_parameter import AircraftParameters
from src.core.operations import Operations as op
import numpy as np

class AircraftModel:

    def __init__(self):
        self.yml_path
        self.ac = AircraftParameters(self.yml_path)

    def xdot(self,x,u):
        """
        Calculate the next state of the A/C.

        Inputs:
        -------

        ***x, Vector State:***
       
        - Body Speed, (m/s): `[u,v,w] = [x1,x2,x3]`.
        - Angle Rates, (rad/s): `[p,q,r] = [x4, x5, x6]`.
        - Euler Angles, (rad): `[phi, theta, psi]  = [x7,x8,x9]`.
       
        ***u, Control Vector:***
        - `delta_aleron = u1`, deg.
        - `delta_eletavor = u2`, deg.
        - `delta_rudder = u3`, deg.
        - `throttle_1`: Estimate the thurst of engine in percent.
        - `throttle_2`. _(If be eg2)_

        Output:
        -------
        
        ***x_dot, Future State:***
        
        - Aceleration:
            - Body, m/s² `[u_dot,v_dot,w_dot]`
            - Angles rad/s² `[p_dot,q_dot,r_dot]`

        - Euler Angles Ratea, rad/s: `[phi_dot, theta_dot, psi_dot]`

        All in same vector like `x`
        """
        # -- Utilities
        sin = lambda x: np.sin(x)
        cos = lambda x: np.cos(x)
        
        # -- Obtain States
        x1,x2,x3,x4,x5,x6,x7,x8,x9 = x

        # -- Obtain Control Inputs
        u1,u2,u3,u4,u5 = u

        # ---- Limit Control
        # ------ Deflection Angles
        u1 = np.clip(u1,np.radians(-25),np.radians(25))
        u2 = np.clip(u2,np.radians(-25),np.radians(10))
        u3 = np.clip(u3,np.radians(-30),np.radians(30))
        # ------ Engine
        u4 = np.clip(u4,np.radians(0.5),np.radians(10))
        u5 = np.clip(u5,np.radians(0.5),np.radians(10))

        # -- Define Vectors
        body_speed = np.asarray([x1,x2,x3],dtype=float)
        angle_rates = np.asarray([x4,x5,x6],dtype=float)
        euler_angles = np.asarray([x7,x8,x9],dtype=float)

        # -- Define Norm of Speed
        Va = np.linalg.norm(body_speed)
        Va = 1e-6 if Va < 1e-6 else Va

        # -- Dynamic Presure 
        rho = 1.225 # SEA LEVEL
        Q = 0.5*rho*Va**2

        # -- Obtain Aerodynamic Angles
        alpha = np.arctan2(x3,x1)
        alpha_wing = alpha - self.ac.alpha_diff
        beta = np.arcsin(np.clip(x2/Va,-1,1))

        # -- Normalize Angle Rates
        p_ad = (x4 * self.ac.b) / (2 * Va)
        q_ad = (x5 * self.ac.mac) / (2 * Va)
        r_ad = (x6 * self.ac.b) / (2 * Va)

        # -- Wind Frame
        # ---- Non Dimension Forces
        # ------ CL
        if alpha_wing <= self.ac.alpha_max:
            CL_w = self.ac.n*(alpha_wing-self.ac.alpha_0)
        else:
            CL_w = (self.ac.a1
                    +self.ac.a2*alpha_wing
                    +self.ac.a3*alpha_wing**2
                    +self.ac.a4*alpha_wing**3)
        # ------ CL tail
        CL_t = (self.ac.n_t*(1-self.ac.deda)*alpha
                +self.ac.n_t*(self.ac.incidence_t-self.ac.epsilon_0)
                +self.ac.CL_n_e*u2)
        CL = CL_w + self.ac.area_ratio_t*CL_t
        # ------ CD
        k = 1/(np.pi*self.ac.AR*self.ac.e)
        CD_i = CL**2*k
        CD = self.ac.cd0 + CD_i
        # ------ Side Force
        CY = (self.ac.n_v*self.ac.side_wash_factor*beta+self.ac.CY_n_r*u3)

        # ---- Aero Forces
        non_dimesion_forces = np.asarray([-CD,CY,-CL],dtype=float)
        aero_forces = self.s*Q*non_dimesion_forces

        # ---- Non Dimension Moments
        # ------ Cl
        Cl = (self.ac.Cl_beta * beta + 
              self.ac.Cl_p * p_ad + 
              self.ac.Cl_r * r_ad + 
              self.ac.Cl_n_a * u1)
        # ------ Cm
        Cm = (self.ac.Cm_0 + 
              CL_w * self.ac.static_margin - 
              self.ac.V_H_t * CL_t + 
              self.ac.Cm_q * q_ad + 
              self.ac.Cm_n_e * u2)
        # ------ Cn
        cn_beta_wing = CL**2*self.ac.cb_beta_wing_factor
        Cn_beta = self.ac.cn_beta_tail+self.ac.cn_beta_fus+cn_beta_wing
        Cn = (Cn_beta * beta + 
              self.ac.Cn_p * p_ad + 
              self.ac.Cn_r * r_ad + 
              self.ac.Cn_n_r * u3 + 
              self.ac.Cn_da * u1)
        
        # ---- Aero Mometns
        l_moment,n_moment = Cl*Q*self.ac.s*self.ac.b,Cn*Q*self.ac.s*self.ac.b
        m_moment = Cm*Q*self.ac.s*self.ac.mac

        aero_moments = np.asarray([l_moment,m_moment,n_moment],dtype=float)

        # -- Gravity
        g = 9.81    # m/s²
        gravity_force = np.asarray([-self.ac.m*g*sin(x8),
                                    self.ac.m*g*cos(x8)*sin(x7),
                                    self.ac.m*g*cos(x8)*cos(x7)],
                                    dtype=float)

        # -- Propulsive
        # ---- Forces
        f1 = self.ac.m*g*u4
        f2 = self.ac.m*g*u5
        engine_force = np.asarray([f1+f2,0,0],dtype=float)
        # ---- Moments
        engine_moment = (np.cross(self.ac.eg1,np.asarray([f1,0,0],dtype=float)),
                         np.cross(self.ac.eg2,np.asarray([f2,0,0],dtype=float)))

        # -- Body Frame
        aero_forces = op.c_wb*aero_forces
        aero_moments = op.c_wb*aero_moments

        forces = aero_forces+engine_force+gravity_force
        moments = aero_moments+engine_moment
        

    

        

        
#%%

# ---- INTEACTIVE TESTING

from pathlib import Path
import sys

root = Path.cwd().resolve().parents[1]
sys.path.insert(0,str(root))

from src.domain.aircraft_parameter import AircraftParameters
from src.service.loader import LoadFiles
# %%
