#%%
from src.domain.aircraft_parameter import AircraftParameters
# import pyvista as pv

class LoadFiles:
    """
    Load files
    """
    @staticmethod
    def load_ac(path):
        """
        Load Aircraft Parameters 
        """
        return AircraftParameters.from_yml(path)
    """
    @staticmethod
    def _load_mesh(path):
        mesh = pv.read(path)
        center = mesh.center
        bounds = mesh.bounds
        scale = max(
            bounds[1] - bounds[0],
            bounds[3] - bounds[2],
            bounds[5] - bounds[4]
        )
        mesh.points -= center
        mesh.points /= scale
        return mesh """

# %%
