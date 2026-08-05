import numpy as np


class Operations:

    def __init__(self):
        pass
    
    @staticmethod
    def body_rotation_matrix(phi, theta, psi):
        """
        Calculate the body rotation matrix from Euler angles.
        """
        R_roll = np.array([
            [1, 0, 0],
            [0, np.cos(phi), -np.sin(phi)],
            [0, np.sin(phi), np.cos(phi)]
        ])

        R_pitch = np.array([
            [np.cos(theta), 0, np.sin(theta)],
            [0, 1, 0],
            [-np.sin(theta), 0, np.cos(theta)]
        ])

        R_yaw = np.array([
            [np.cos(psi), -np.sin(psi), 0],
            [np.sin(psi), np.cos(psi), 0],
            [0, 0, 1]
        ])

        R = R_yaw @ R_pitch @ R_roll
        return R
    @staticmethod
    def wind_rotation_matrix(alpha, beta):
        """
        Calculate the wind rotation matrix from angles of attack and sideslip.
        """
        R_alpha = np.array([
            [np.cos(alpha), 0, -np.sin(alpha)],
            [0, 1, 0],
            [np.sin(alpha), 0, np.cos(alpha)]
        ])

        R_beta = np.array([
            [np.cos(-beta), np.sin(-beta), 0],
            [-np.sin(-beta), np.cos(-beta), 0],
            [0, 0, 1]
        ])

        R = R_beta @ R_alpha
        return R
