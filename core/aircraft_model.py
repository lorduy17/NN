import numpy as np

class AircraftModel:
    def __init__(self, ac_params):
        self.ac_params = ac_params

    def xdot(self, state_var, control_var):
        """
        Inputs:
        -------
        control_vars: Variables of control, like:

        control_var = [u1,u2,u3,u4,u5]

        u1: delta_aleron, rad
        u2: delta_elevator, rad
        u3: delta_rudder, rad
        u4: thurst 1
        u5: thurst 2

        state_var: Variables of state, define the state of the A/C.

        state_var = [x1,x2,x3,x4,x5,x6,x7,x8,x9]

        x1: u
        x2: v
        x3: w
        x4: p
        x5: q
        x6: r
        x7: phi
        x8: theta
        x9: psi

        where body speed, m/s: x1,x2,x3  and angle rates, rad/s: x4,x5,x6

        m: mass
        s: surface wing
        mac: mean aerodynamic chord
        (x,y,z)_apt(1,2): distance since c.g to engine poss
        alpha_0: alpha value when CL = 0
        n : cl-alpha curve slope
        s_t: surface tail
        l_t: distance between wing and tail ac's
        
        Output:
        -------
        xdot = [accel_body,accel_angles,euler_rates_rate]

        accel_body = [u_dot,v_dot,w_dot] m/s**2
        accel_angles = [p_dot,q_dot,r_dot] rad/s**2
        euler_rates_rate = [phi_dot,theta_dot,psi_dot] rad/s
        """
        ### deg2rad
        deg2rad = np.pi/180
        # STEP 1
        # Control limits
        for i in range(len(control_var)):
            if i < 3:
                control_var[i] = np.clip(control_var[i],-25*deg2rad,25*deg2rad)
            else:
                control_var[i] = np.clip(control_var[i],0,1)
        u1,u2,u3,u4,u5 = control_var
        # STEP 2
        ## Variables intermedias
        x1,x2,x3,x4,x5,x6,x7,x8,x9 = state_var

        body_speed = np.array([x1,x2,x3])
        angle_rates = np.array([x4,x5,x6])
        euler_angles = np.array([x7,x8,x9])

        Va = np.sqrt(x1**2 + x2**2 + x3**2)
        if Va < 1e-6:
            Va = 1e-6

        alpha = np.arctan2(x3,x1)
        beta = np.arcsin(np.clip(x2/Va, -1, 1))
        rho = 1.225
        Q = 0.5*rho*Va**2
        g = 9.80665 # m/s2
        

        # Aircraft parameters, calcs from self.ac_params
        innertia_body = self.ac_params.m*self.ac_params.inertia_matrix

        # STEP 3
        ## Nondimensional Aero Forces coefficientes in Fs
        if alpha <= 14.5/180*np.pi:  
            cl_wb = self.ac_params.n*(alpha-self.ac_params.alpha_0) # 
        else:  ## Stall region
            a1 = -155.2 
            a2 = 609.2  
            a3 = -768.5 
            a0 = 15.212 
            cl_wb = a0 + a1*alpha + a2*alpha**2 + a3*alpha**3

        # Tail
        deda = 0.25 
        epsilon = deda*(alpha -self.ac_params.alpha_0)
        alpha_t = alpha-epsilon+u2+1.3*x5*self.ac_params.l_t/Va
        cl_t = self.ac_params.s_t/self.ac_params.s*3.1*alpha_t 
        
        # Forces
        cl = cl_wb+cl_t
        c_d = 0.13+0.0061*(self.ac_params.n*alpha+0.645)**2 
        c_y = -1.6*beta+0.24*u3
        
        ## Aerodynamic Force in Fb
        non_dim_forces = [-c_d,c_y,-cl]

        c_ws = np.array([[np.cos(beta),np.sin(beta),0],
                        [-np.sin(beta),np.cos(beta),0],
                        [0,0,1]])

        # STEP 4
        forces_s = Q*self.ac_params.s*np.array(non_dim_forces)
        c_bs = np.array([
            [np.cos(alpha),0,-np.sin(alpha)],
            [0,1,0],
            [np.sin(alpha),0,np.cos(alpha)]
        ])
        forces_a = c_bs@forces_s

        # STEP 5
        ## Nondimensional Aero Moment Coefficient about AC in Fb
        # Defube parametters for calc cm
        n_bar = np.array([
            -1.4*beta,
            -0.59-(3.1*self.ac_params.s_t*self.ac_params.l_t)/(self.ac_params.s*self.ac_params.mac)*(alpha-epsilon),
            (1-alpha*180/(np.pi*15))*beta
        ])
        cm_x = self.ac_params.mac/Va*np.array([
            [-11,0,5],
            [0,-4.03*self.ac_params.s_t*self.ac_params.l_t**2/(self.ac_params.s*self.ac_params.mac**2),0],
            [1.7,0,-11.5]
        ])
        cm_u = np.array([
            [-0.6,0,0.22],
            [0,-3.1*(self.ac_params.s_t*self.ac_params.l_t/(self.ac_params.s*self.ac_params.mac)),0],
            [0,0,-0.63]
        ])


        cm_ac = n_bar +cm_x@(angle_rates)+cm_u@[u1,u2,u3]
        moments_ac = self.ac_params.mac*cm_ac*Q*self.ac_params.s
        
        # STEP 7
        ## Aero moment about cg in Fb
        """
        Define parammetters (r_cg,r_ac) for calculate mmoment cg in Fb
        """
        r_cg = np.array([0.23*self.ac_params.mac,0,0.1*self.ac_params.mac])
        r_ac = np.array([0.12*self.ac_params.mac,0,0])
        moments_cg = moments_ac+np.cross(forces_a,(r_cg-r_ac))

        # STEP 8
        ## Propulsion effects
        f1 = min(u4*self.ac_params.m*g, 0.175*self.ac_params.m*g) 
        f2 = min(u5*self.ac_params.m*g, 0.175*self.ac_params.m*g)

        """Define parammetters (u_bar1,u_bar2) for the propulsion effects"""
        f_e = f1+f2
        u_bar1 = np.array([
            self.ac_params.x_apt1,
            self.ac_params.y_apt1,
            self.ac_params.z_apt1
    ])
        u_bar1 = u_bar1 - r_cg
        u_bar2 = np.array([
            self.ac_params.x_apt2,
            self.ac_params.y_apt2,
            self.ac_params.z_apt2
        ])
        u_bar2 = u_bar2 - r_cg

        m_ecg = np.cross(u_bar1,[f1,0,0]) + np.cross(u_bar2,[f2,0,0])

        # STEP 9
        ## Gravity effects
        fg_bar = self.ac_params.m*np.array([
            -g*np.sin(x8),
            g*np.cos(x8)*np.sin(x7),
            g*np.cos(x8)*np.cos(x7)
        ]) 

        # STEP 10
        forces = forces_a + fg_bar +[f_e,0,0]
        moments =  m_ecg + moments_cg

        accel_body = forces/self.ac_params.m-np.cross(angle_rates,body_speed)

        innertia_body_inv = np.linalg.inv(innertia_body)
        accel_angles = innertia_body_inv@(moments-np.cross(angle_rates,innertia_body@angle_rates))
        euler_derivate = np.array([
            [1,np.sin(x7)*np.tan(x8),np.cos(x7)*np.tan(x8)],
            [0,np.cos(x7),-np.sin(x7)],
            [0,np.sin(x7)/np.cos(x8),np.cos(x7)/np.cos(x8)]
        ])@angle_rates

        x_dot_r = np.hstack((accel_body,accel_angles,euler_derivate))
    
        x_dot_r = np.array(x_dot_r,dtype=float)
        return x_dot_r