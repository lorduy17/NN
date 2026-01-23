import numpy as np
from io import StringIO
from datetime import datetime
import trimesh
from tkinter import filedialog
import os
import time


class SaveLoadFiles:
    def __init__(self):
        self.mesh = None
           
    def load_stl(self):
        route = filedialog.askopenfilename(
            title="Select STL file",
            filetypes=(("STL files","*.stl"),("All files","*.*"))
        )

        if route == "":
            print("No file selected")
            return
        
        # Load STL file
        try:
            self.mesh = trimesh.load(route)
            self.mesh.apply_translation(-self.mesh.centroid)
            self.mesh.apply_scale(1/np.max(self.mesh.extents))
            return self.mesh.apply_scale(2)
            
        
        except Exception as e:
            print(f"Error loading STL file: {e}")
            return None
        
    def load_states(self):
        file_path = filedialog.askopenfilename(
            title="Select simulation states file",
            filetypes=(("STL files","*.txt"),("All files","*.*"))
        )
        if file_path:
            print(f"txt file loaded: {file_path}")
            states = np.loadtxt(file_path,delimiter=",",skiprows=1)
            states = np.asarray(states,dtype=float)
            time.sleep(3)
            return  states, states[1,8], file_path
        else:
            print("No file selected")
            time.sleep(3)
            return None

    @staticmethod 
    def save_simulation(states):
        """
        Input:
          states: Matrix with A/C in each dt.
            states, size: [time/dt,14]
        
            
        Output:
            .txt with states simulation.
        """

        if states.size != 0: # Check if states is not empty
            states_to_save = np.zeros((states.shape[0],10))
            states_to_save[:, 0:3] = states[:, 0:3]         # Save u,v,w
            states_to_save[:, 3:6] = states[:, 6:9]         # Save phi,theta,psi 
            states_to_save[:, 6:9] = states[:, 9:12]        # Save alpha,beta,gamma
            states_to_save[:, 9] = states[:,12]             # Save time_current
      

            os.makedirs('issues', exist_ok=True)
                
            timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
            filename_states = f'states_simulated/simulation_data_{timestamp}.txt'
            
            np.savetxt(
                filename_states,
                states_to_save,
                header="u,v,w,phi,theta,psi,alpha,beta,gamma,time",
                delimiter=","
            )
            print(f"States saved as: {filename_states}")
            time.sleep(3)
        else:
            print("No states to save")
            return


        