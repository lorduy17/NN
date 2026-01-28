import numpy as np
import matplotlib.pyplot as plt
from aircraft_model import AircraftModel as amodel

class Simulate:

    def __init__(self,model,x,u,time,dt,da=None,da_start=None,da_end=None,eg=None):
        self.model = model
        self.x = x
        self.u = u
        self.time = time
        self.dt = dt
        self.da = da
        self.da_start = da_start
        self.da_end = da_end
        self.eg = eg

    

    def simulate(self,da=None,da_start=None,da_end=None,eg=None,show=None):
        """

        The function simnulate the behavior of the A/C (aircraft) with
        cases like if the pilot deflect aleron, shut off a any engine

        Input:
            X: state variables.
            X = [u, v, w, p, q, r, phi, theta, psi]
            U: control variables
            U = [delta_e, delta_a, delta_r, delta_t1, delta_t2]
            time: Time that the user wanna simulate
            dt: How many each do calculate the behavior
            da: Aleron deflection, degs
            eg: shutoff the engine. 1: shut off engine 1 , 2: shut off engine 2.

        Output:
            states: Matrix with A/C in each dt.
            states = size: [time/dt,14] 
            
            states = [
            u0, v0, w0, p0, q0, r0, phi0, theta0, psi0, alpha0, beta0, gamma0, time_current0
            u1, v1, w1, p1, q1, r1, phi1, theta1, psi1, alpha1, beta1, gamma1, time_current1
            u2, v2, w2, p2, q2, r2, phi2, theta2, psi2, alpha3, beta3, gamma3, time_current3
            u3, v3, w3, p3, q3, r3, phi3, theta3, psi3, alpha4, beta4, gamma4, time_current4
            .
            .
            .
            ]
        
        """

        def calc_abgVa(x,time_current):
            """
            This function is used for calculate the aerondynamics angles aditional add
            the moment the calc.

            PRINCIPLY WAS USE IN SIMULATE. So the redaction be focused in how is used in simulate

            INPUT:
        
                x: State vector,
                    x = [u,v,w,phi,theta,psi]
                time_current: Time correspond to calc time
                    time_current = type: float

            OUTPUT:
                aerodynamic angles
                    aerodynamic angles = [alpha,beta,gamma,time_current], type = float

            """
            u,v,w,phi,theta,psi = x[0],x[1],x[2],x[6],x[7],x[8]

            if  np.sqrt(u**2 + v**2 + w**2) < 1e-6:
                Va = 1e-6
            else:
                Va = np.sqrt(u**2 + v**2 + w**2) 

            alpha = np.arctan2(w,u)
            beta = np.arcsin(np.clip(v/Va, -1, 1))
            gamma = theta - alpha
            return np.asarray([alpha,beta,gamma,time_current],dtype=float)

        X = self.x
        U = self.u
        time = self.time
        dt = self.dt
        da = self.da
        da_sta = self.da_start
        da_end = self.da_end
        eg = self.eg
        iter_counter = 0
        counter_time = 0


        deg2rad = np.pi/180

        
        u1,u2,u3 = U[0:3]
        U = np.array([u1,u2,u3,U[3],U[4]])
        
        # Save initial moment
        states = [X]
        states_abg = [calc_abgVa(X,counter_time)]
        time_vector = [0]

        iter_counter =+ 1
        counter_time =+ dt
        
        # Save x,U for start simulation.
        x_current = X.copy()
        U_initial = U.copy()


        iter_fail = None ## If simulation tend to infinite -> Show warning in the terminal

        while counter_time <= time:
            U = U_initial.copy()

            # If the user wanna case simulate with aleron deflection 
            if da is not None and da != 0.0:
                if da_sta <= counter_time <= da_end:
                    U[0] += da*deg2rad # rad
            
            # If the user wanna case simulate with engine fail 
            if eg == 1:
                U[3] = 0 # shut off engine 1
            elif eg == 2:
                U[4] = 0 # shut off engine 2
            

            # Euler explicit integration
            x_dot_current = amodel.xdot(x_current,U,self.model)
            x_next = x_current + x_dot_current*dt
            

            # Conditions for active warning
            Va = np.sqrt(x_next[0]**2 + x_next[1]**2 + x_next[2]**2)
            if Va > 300 or np.any(np.abs(x_next[6:9]) > np.pi/2):
                iter_fail = True

            states_abg.append(calc_abgVa(x_next,counter_time))
            states.append(x_next) # Add X to state
            time_vector.append(counter_time)

            x_current = x_next # Fresh x_current
            counter_time += dt
            iter_counter += 1
            

            if show is True: # Show simulate progress
                progress = counter_time/time
                if progress < 1:
                    if progress * 100 % 5 == 0:
                        print(
                            f"{counter_time/time*100:.f2}%      Iteration N°{iter_counter}"
                        )

            if iter_fail is not None: # Print state if will not converge
                if iter_counter%2500 == 0:
                    print(50*"*")
                    print(2*"\t","WARNING")
                    print("Simulation can not converge for")
                    print(f"Iteration:{iter_counter}","\twith\t",f"time: {round(counter_time,0)}s")
                    print(50*"*")
    
        states = np.asarray(states,dtype=float)
        time_vector = np.asarray(time_vector,dtype=float)
        
        ## Plotter
        fig, axs = plt.subplots(9, 1, figsize=(10, 15), sharex=True)
        labels_y = ["u, m/s", "v, m/s", "w, m/s", "p, rad/s", "q, rad/s", "r, rad/s", "phi, rad", "theta, rad", "psi, rad"]
        
        for i in range(9):
            axs[i].plot(time_vector, states[:,i], label=labels_y[i],)
            axs[i].legend()
            axs[i].grid(True)
            if i == 8:  # Last subplot
                axs[i].set_xlabel('Time (s)')
        
        plt.tight_layout()
        plt.show(block=False)

        states = np.hstack((states,states_abg))
      


        return states

    
#%%
    
