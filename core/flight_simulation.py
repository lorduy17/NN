import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation
from operations import Operations as ops
import matplotlib.colors as mcolors
import time

class FlightSimulation:


    def __init__(self,states,mesh,dt,interval,background_color=None):
        self.states = states
        self.mesh = mesh
        self.dt = dt
        self.interval = interval
        self.vertices = mesh.vertices
        self.faces = mesh.faces

        self.background_color = self._validate_color(background_color)

    def _validate_color(self,color):
        if color is None:
            return "white"
        
        if not color in mcolors.cnames.keys():
            if not self._hex_color(color):
                raise ValueError("Invalid color format. Use named colors or hex format (e.g., #RRGGBB).")
 
        else:
            return color
    
    def _hex_color(self,color):
        if not isinstance(color,str):
            return False
        if not color.startswith("#"):
            return False
        
        hex_part = color[1:]

        if len(hex_part) not in [3,6,8]:
            return False
        
        try:
            int(hex_part,16)
            return True
        except ValueError:
            return False
        

    def animation(self):

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim(-1,1)
        ax.set_ylim(-1,1)
        ax.set_zlim(-1,1)
        ax.set_axis_off()

        try:
            fig.patch.set_facecolor(self.background_color)
            ax.set_facecolor(self.background_color)
        except:
            ValueError("Invalid background color. Using default.")
            time.sleep(5)
    
        vert0 = self.vertices
        faces = self.faces

        poly = Poly3DCollection(vert0[faces], alpha=0.8, edgecolor='k')
        ax.add_collection3d(poly)

        # Plot static NED axes
        ax.quiver(0, 0, 0,  1, 0, 0, color='r', length=1.5, arrow_length_ratio=0.1)   # N
        ax.quiver(0, 0, 0,  0, -1, 0, color='g', length=1.5, arrow_length_ratio=0.1)   # E
        ax.quiver(0, 0, 0,  0, 0, -1, color='b', length=1.5, arrow_length_ratio=0.1)  # D

        wind_quiver = [ax.quiver(
            0,0,0 ,0,0,0,
            color="steelblue",arrow_length_ratio=0.1,pivot="tip"
        )]

        def update(num):
            """
            Doc
            """
            
            # Body rotation
            phi,theta,psi = self.states[num,3:6]
            nose = np.asarray([vert0[:,0].max(), 0, 0], dtype=float)
            R = ops.body_rotation_matrix(phi,theta,psi)
            mesh_rotated = (R@vert0.T).T
            nose_rotated = R@nose
            poly.set_verts(mesh_rotated[faces])


            # Wind vector
            u,v,w = self.states[num,:3]
            alpha,beta = self.states[num,6:8]
            v_rel = -np.asarray([u,v,w],dtype=float)
            wind_vector = R@v_rel

            # Wind vector in nose
            center = nose_rotated
            wind_quiver[0].remove()
            wind_quiver[0] = ax.quiver(
                center[0],center[1],center[2],
                wind_vector[0],wind_vector[1],wind_vector[2],
                color="steelblue",arrow_length_ratio=0.1,pivot="tip",
                normalize=True,length=0.75
            )
        
            
            
            time = num*self.dt
            ax.set_title(f"Flight Simulation at t={time:.2f} s")

            return [poly,wind_quiver[0]]

        if self.interval is None:
            self.interval = self.dt*1000
            
        anim = FuncAnimation(fig, update, frames=len(self.states), interval=self.interval, blit=False)

        plt.show()

