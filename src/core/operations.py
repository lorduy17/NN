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

    @staticmethod
    def c_wb(alpha,beta):
        """
        Calculate the body yo eart rotation matrix from aerodynamic angles.
        """
        cos = lambda x : np.cos(x)
        sin = lambda x : np.sin(x)
        R = np.array([
            [ cos(alpha) * cos(beta), -cos(alpha) * sin(beta), -sin(alpha)],
            [         sin(beta),          cos(beta),    0.0],
            [ sin(alpha) * cos(beta), -sin(alpha) * sin(beta),  cos(alpha)]
        ], dtype=float)
        return R
    @staticmethod
    def c_be(phi,theta,psi):
        """
        Calculate the body to earth rotation matrix from Euler angles.
        """
        a_11 = np.cos(theta)*np.cos(psi)
        a_12 = np.cos(theta)*np.sin(psi)
        a_13 = -np.sin(theta)
        a_21 = np.sin(phi)*np.sin(theta)*np.cos(psi) - np.cos(phi)*np.sin(psi)
        a_22 = np.sin(phi)*np.sin(theta)*np.sin(psi) + np.cos(phi)*np.cos(psi)
        a_23 = np.sin(phi)*np.cos(theta)
        a_31 = np.cos(phi)*np.sin(theta)*np.cos(psi) + np.sin(phi)*np.sin(psi)
        a_32 = np.cos(phi)*np.sin(theta)*np.sin(psi) - np.sin(phi)*np.cos(psi)
        a_33 = np.cos(phi)*np.cos(theta)
        return np.asarray([[a_11,a_12,a_13],
                           [a_21,a_22,a_23],
                           [a_31,a_32,a_33]],dtype=float)
