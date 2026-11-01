#%%
import numpy as np
from dataclasses import dataclass
from dataclasses import field
import yaml
@dataclass
class AircraftParameters:
    """
    Aircrafts parameters
    """
    # -- Aircraft
    name : str
    m: float # Mass
    diameter_fus: float
    width_fus: float # Fuselage Width, m
    vol_fus: float # Fuselage Volume, m³
    cd0: float
    h_cg : float

    # -- Inertia 
    ixx: float # Innertia x axis
    iyy: float # Innertia x axis
    izz: float # Innertia x axis

    # -- Wing
    # ---- Geometry
    s: float
    mac: float
    AR: float
    taper_ratio_wing: float
    sweep_angle_wing: float
    incidence_wing: float
    twist_wing: float
    dihedral_angle: float
    b: float = field(init=False)
    h_ac : float
    # ---- Aerodynamic
    alpha_0: float
    n: float    # alpha slope
    e: float    # Oswald Eficiency
    # ------ CL curve
    CL_max: float
    CL_0: float
    alpha_max: float = field(init=False)
    # ---------- Stall Region
    a1: float
    a2: float
    a3: float
    a4: float

    # -- Tail
    # ---- Horizontal
    # ------ Geometry
    s_t: float
    l_t: float
    landa_t: float
    twist_t: float
    incidence_t: float
    # ------ Aerodynamic
    n_t : float
    eta_t: float
    alpha_0t: float
    # -------- Downdasg
    epsilon_0: float
    deda: float
    # ---- Vertical
    # -------- Geometry
    s_v: float
    l_v: float # 
    z_v: float # Normal (respect a endurance) distance between c_g A/C and Mean aerodynamic center
    # -------- Aerodynamic
    n_v: float
    side_wash_factor: float = field(init=False)

    # -- Surface Control
    Cl_n_a :float   # Aleron slope [1/deg]
    Cn_n_a: float   # Aleron slope [1/deg]
    CL_n_e : float  # Elavator [1/deg]
    Cm_n_e: float   # Elevator [1/deg] 
    Cn_n_r: float   # Rudder [1/deg]


    # -- Aerodynamic Derivates
    C_mq: float # Pitch Damping
    C_lp: float # Roll Damaping
    C_nr: float # Yaw Damping

   
    # -- Engine
    eg1: np.array = field(default_factory=lambda : np.asarray([0,0,0],dtype=float))
    eg2: np.array = field(default_factory=lambda : np.asarray([0,0,0],dtype=float))

    # Post_init method to calculate derived parameters

    # -- Static Margin
    static_margin: float = field(init=False)

    # -- Tail
    # ---- Horizontal
    V_H_t: float = field(init=False)
    area_ratio_t: float = field(init=False) 
    # ---- Vertical
    V_v: float = field(init=False)
    area_ratio_v: float = field(init=False)
    Z_bar: float = field(init=False)

    # -- INERTIA MATRIX
    inertia_matrix : np.ndarray = field(init=False)

    # -- Anothers calcs
    alpha_diff: float = field(init=False)

     # -- Moments Derivate Respect Beta
    Cl_beta: float = field(init=False)
    Cn_beta: float = field(init=False)
    
#%%
    def __post_init__(self):
        """
        Calculates all parameters can be calculated from the geometry of the aircraft.

        Characteristics params
        - Wing, Tail (VERTICAL AND HORIZONTAL):
            - Surface.
            - Span.
            - Mean aerodynamic chord.
            - Taper Ratio.
            - Sweep angle. (At c/4)
            - Aspect ratio.
        - Fuselage:
            - Length.
            - Diameter.
            - Lateral Area projection. 
            - X_distance from datum (nose) to c.g.
        """
        # -- Inertia matrix
        self.inertia_matrix = np.array([
            [self.ixx,0,0],
            [0,self.iyy,0],
            [0,0,self.izz]],
            dtype=float)*self.m

        # -- Calculate wing span
        self.b = np.sqrt(self.AR*self.s)
  
        # -- Calculate horizontal tail
        self.V_H_t = self.s_t * self.l_t/(  self.s * self.mac)
        self.area_ratio_t = self.s_t/self.s

        # -- Calculate vertical tail
        self.V_v = self.s_v *self.l_v/(self.s * self.b)
        self.area_ratio_v = self.s_v/self.s
        self.Z_bar = self.z_v/self.b    

        # -- Alpha diff
        self.alpha_diff = self.twist_wing+self.incidence_wing

        # -- alpha_max
        self.alpha_max = self.CL_max/self.n

        # -- Sidewash Factor
        self.side_wash_factor = 0.724+(3.06*self.s_v/self.s)/(1+np.cos(self.sweep_angle_wing))-0.4*self.z_v/self.diameter_fus+0.009*self.AR

        # -- Calculate Directional Derivates
        # ---- Roll
        # ------ Tail Contribution
        cl_beta_tail = self.n_v*self.side_wash_factor * self.area_ratio_v * self.Z_bar
        # ------ Wing Contribution (Dihedral Effect)
        gamma_rad = np.radians(self.dihedral_angle)
        lam = self.taper_ratio_wing
        factor_lam = (2 * (1 + 2 * lam)) / (3 * (1 + lam))
        cl_beta_gamma = - (self.n * gamma_rad / 4.0) * factor_lam
        # ------ Wing + Fuselage
        cl_beta_wf = -1.2 * (np.sqrt(self.AR) * self.z_wf * (self.diameter_fus + self.width_fus)) / (self.b**2)
        # ---- 
        self.Cl_beta = cl_beta_tail+cl_beta_gamma+cl_beta_wf
        # ---- Yaw
        # ------ Tail Contribution
        self.cn_beta_tail = self.n_v * self.side_wash_factor * self.area_ratio_v * (self.l_v / self.b)
        # ------ Fuselage Contribution
        self.cn_beta_fus = -1.3 * (self.vol_fus / (self.s * self.b)) * (self.diameter_fus / self.w_f) if self.w_f > 0 else 0.0
        # ------ Wing Contribution (Sweep Angle)
        sweep_rad = self.sweep_angle_wing
        cos = np.cos(sweep_rad)
        sin = np.sin(sweep_rad)
        tan = np.tan(sweep_rad)

        term1 = 1/(4*np.pi*self.AR)
        term2 = tan/(np.pi*self.AR*(self.AR+4*cos))
        term3 = cos-self.AR*0.5-(self.AR**2/(8*cos))+(6*self.static_margin*sin)/self.AR

        self.cn_beta_wing_factor = term1-term2*term3
        # -- Stability
        self.static_margin = self.h_ac-self.h_cg
        self.Cm_0 = self.h_ac*self.CL_0-self.eta_t*self.V_H_t*self.n_t*(self.incidence_t-self.self.epsilon_0)

    @classmethod
    def from_yml(cls,filepath: str) -> "AircraftParameters":
        """
        Extract parameters from yaml file, where contain aerodynamic and geometric parameters of aircraft
        """
        with open(filepath,"r",encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return cls( # Mapping parameters
            # Aircraft
            name = data["aircraft"]["name"],
            m=data['aircraft']['mass'],
            cd0 = data['aircraft']['cd0'],
            diameter_fus = data['aircraft']['diameter_fus'],
            width_fus = data['aircraft']['width_fus'],
            vol_fus = data['aircraft']['vol_fus'],
            h_cg = data['aircraft']['h_cg'],
            # Inertia
            ixx=data['inertia_mass']['ix'],
            iyy=data['inertia_mass']['iy'],
            izz=data['inertia_mass']['iz'],
            # Wing
            # -- Geometry
            s=data['wing']['s'],
            mac=data['wing']['mac'],
            taper_ratio_wing = data['wing']['taper_ratio'],
            AR = data['wing']['AR'],
            sweep_angle_wing = data['wing']["sweep"],
            incidence_wing = data['wing']['incidence'],
            twist_wing = data['wing']["twist"],
            dihedral_angle = data["wing"]["dihedral"],
            h_ac = data['wing']['h_ac'],
            # -- Aerodynamic
            e = data['wing']['e'],
            alpha_0 = data['wing']['alpha_0'],
            n = data['wing']['n'],
            CL_max = data['wing']["CL_max"],
            CL_0 = data['wing']["CL_0"],
            a1 = data['wing']['a1'],
            a2 = data['wing']['a2'],
            a3 = data['wing']['a3'],
            a4 = data['wing']['a4'],
            # Tail
            # -- Horizontal
            # ---- Geometry
            s_t=data['tail']['horizontal']['s'],
            l_t=data['tail']['horizontal']['l'],
            landa_t = data['tail']['horizontal']['taper_ratio'],
            twist_t =data['tail']['horizontal']['twist'],
            incidence_t = data['tail']['horizontal']['incidence'],
            # ---- Aerodynamic
            alpha_0t = data['tail']['horizontal']['alpha_0'],
            n_t = data['tail']['horizontal']['n'],
            eta_t = data['tail']['horizontal']['eta'],
            # ------- DOWNWASH
            epsilon_0 = data['tail']['horizontal']['epsilon_0'],
            deda = data['tail']['horizontal']['de_da'],

            # -- Vertical
            # ---- Geometry
            s_v=data['tail']['vertical']['s'],
            l_v=data['tail']['vertical']['l'],
            z_v=data['tail']['vertical']['z'],
            # ---- Aerodynamic
            n_v = data['tail']['vertical']['n'],

            # Engine
            eg1=np.asarray(data["engine"].get('eg1',[0,0,0])),
            eg2=np.asarray(data["engine"].get('eg2',[0,0,0])),

            # Surface Control
            Cl_n_a = data["surface_control"]["Cl_n_a"],
            Cn_n_a = data["surface_control"]["Cn_n_a"],
            CL_n_e = data["surface_control"]["CL_n_e"],
            Cm_n_e = data["surface_control"]["Cm_n_e"],
            Cn_n_r = data["surface_control"]["Cn_n_r"],

            # Aerodynamic Derivates.
            C_mq = data['aerodynamic_derivates']['C_mq'],
            C_lp = data['aerodynamic_derivates']['C_lp'],
            C_nr = data['aerodynamic_derivates']['C_nr']
        )
    