from core.operations import Operations as ops
import numpy as np
import pyvista as pv

class FlightSimulation:
    def __init__(self,mesh,dt):
        self.mesh = mesh
        self.dt = dt
    def animation(self,states):
        og_points = self.mesh.copy().points # Save original body
        plotter = pv.Plotter()
        plotter.add_mesh(self.mesh,opacity=0.8)
        axis = [[1,0,0], [0,-1,0], [0,0,-1]]
        axs_colors = ["red", "green", "blue"]
        for i in range(len(axis)):
            arrow = pv.Arrow(
                start=[0,0,0],
                direction = axis[i],
                scale = 0.5,
                shaft_radius = 0.005,
                tip_radius   = 0.02,
                tip_length   = 0.15,
            )
            plotter.add_mesh(arrow, color=axs_colors[i])
        plotter.show(interactive_update=True,auto_close=False) # Open the plotter window
        for idx,_ in enumerate(states,0):
            phi,theta,psi = states[idx,6:9]
            R = ops.body_rotation_matrix(phi,theta,psi)
            self.mesh.points = (R@og_points.T).T
            plotter.update()
        plotter.close()