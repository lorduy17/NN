#%%

from domain.aircraft_parameter import AircraftParameters
from domain.simulation_config import SimulationParameters
import numpy as np
import jstyleson
import pandas as pd
import pyvista  as pv
class LoadFiles:
    """
    Load files
    """
    @staticmethod
    def ac_parameters(data):
        supported_units = ["SI"]
        # Check units system
        unit_system = data.get("unit_sys")
        if unit_system not in supported_units:
            raise ValueError(f'{unit_system} NOT IS SUPPORTED')
        else:
            fields = [
            "m", "inertia_matrix", "s", "mac", "x_apt1", "y_apt1", "z_apt1", 
            "x_apt2", "y_apt2", "z_apt2", "alpha_0", "n", "s_t", "l_t"
            ]
            values = {}
            # Load parameters
            for i in fields:
                if i == "inertia_matrix":
                    values[i] = np.array(data[i])
                else:
                    values[i] = data[i]
            return AircraftParameters(**values)

    @staticmethod
    def simulation_parameters(data):
        supported_units = ["SI"]
        # Check units system
        unit_system = data.get("units_sys")
        if unit_system not in supported_units:
            raise ValueError(f'{unit_system} NOT IS SUPPORTED')
        else:
            fields = ["X","U","time","dt","da","da_start","da_end","eg","show"]
            values = {}
            for i in fields:
                if i == "X" or i == "U":
                    values[i] = np.array(data[i])
                else:
                    values[i] = data[i]
            return SimulationParameters(**values)
    @staticmethod
    def _load_states(path):
        """
        Load states from csv file
        """
        df = pd.read_csv(path)
        states = df.values
        return states
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
        return mesh
    @staticmethod
    def _read_jsonc(path):
        # Read parameters
        with open(path,'r') as f:
            data = jstyleson.load(f)
        return data

