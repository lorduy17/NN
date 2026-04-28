from core.operations import Operations as ops
import pyvista as pv

class FlightSimulation:
    def __init__(self,mesh,dt):
        self.mesh = mesh
        self.dt = dt
    def animation(self,states):
        og_points = self.mesh.copy().points # Save original body
        plotter = pv.Plotter()
        plotter.add_mesh(self.mesh)
        plotter.show(interactive_update=True,auto_close=False) # Open the plotter window
        for idx,_ in enumerate(states,0):
            phi,theta,psi = states[idx,5:8]
            R = ops.body_rotation_matrix(phi,theta,psi)
            self.mesh.points = (R@og_points.T).T
            plotter.update()
        plotter.close()

            


