import numpy as np
from dataclasses import dataclass
@dataclass
class SimulationParameters:
    x: np.ndarray
    u:np.ndarray
    time:float
    dt:float
    da:float
    da_start:float
    da_end:float
    eg:float
    show:float
    