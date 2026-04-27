import numpy as np
from dataclasses import dataclass
@dataclass
class AircraftParameters:
    """
    Aircrafts parameters
    """
    m: float
    inertia_matrix: np.ndarray
    s: float
    mac: float
    x_apt1: float
    y_apt1: float
    z_apt1: float
    x_apt2: float
    y_apt2: float
    z_apt2: float
    alpha_0: float
    n: float
    s_t: float
    l_t: float