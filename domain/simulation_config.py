import numpy as np
from dataclasses import dataclass
@dataclass
class SimulationParameters:
    """
    Simulation parameters
    """
    X: np.ndarray
    U:np.ndarray
    time:float
    dt:float
    da:float
    da_start:float
    da_end:float
    eg:float
    show:float
    