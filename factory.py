import numpy as np
from simulation import Simulate as sim
from flight_simulation import FlightSimulation as fs
from aircraft_model import AircraftModel as amodel
from save_load_files import SaveLoadFiles as slf
from cls import clean_screen as cs
import time
from tabulate import tabulate

class DatesForSim:
    def execute(self,context):
        print("Define simulation parameters")

        context["x0"] = np.array(
            list(map(float, input("Enter X0: ").split(',')))
        )
        context["u0"]  = np.array(
            list(map(float, input("Enter U0: ").split(',')))
        )
        context["time"],context["dt"] = map(float, input("Enter time, dt: ").split(','))
        
        ask = input("Set engine shutoff and/or aileron deflection? If not, press enter: ")

        if not ask:
            context["eg"] = None
            context["da"] = 0.0
            context["da_start"] = 0.0
            context["da_end"] = 0.0

        else:

            ask_eg = input("Set engine shutoff? If not, press enter: ")
            if not ask_eg:
                context["eg"] = None
            else:
                print(" Engine shutoff set:")
                context["eg"] = int(input("Which engine to shut off? (1 or 2): "))

            ask_da = input("Set aileron deflection? If not, press enter: ")
            if not ask_da:
                context["da"] = 0.0
                context["da_start"] = 0.0
                context["da_end"] = 0.0

            else:
                
                print(" Aileron deflection set:")
                context["da"] = float(input("Enter aileron deflection in degrees: "))
                context["da_start"],context["da_end"] = map(
                    float,
                    input("Enter deflection start time and end time (seg), separated by a comma: ").split(',')
                )
        cs()

        print("Show parameters for simulation:")
        pars = {
            "Initial states, X0": (np.array2string(context["x0"],separator=','),None),
            "Control vector, U0": (np.array2string(context["u0"],separator=','),None),
            "time": (f"{context["time"]}", "seg"),
            "time delta, dt ": (f"{context["dt"]}","seg"),
            "Aleron deflection": (f"{context["da"]}","degs"),
            "Deflection start": (f"{context["da_start"]}","seg"),
            "Deflection end": (f"{context["da_end"]}-{context["da_start"]}","seg"),
            "Engine fail": (f"{context["eg"]}",None)
        }
        
        table = [(key, value[0], value[1]) for key, value in pars.items()]
        print(
            tabulate(table, headers=["Parameter", "Value", "Units"], tablefmt="grid")
        )
        
        temp = input("Press Enter or any key to continue")

        if not temp or temp:
            simulator = sim(
                amodel,
                context["x0"],
                context["u0"],
                context["time"],
                context["dt"],
                context["da"],
                context["da_start"],
                context["da_end"],
                context["eg"]
            )

            cs()
            print(" Running simulation...")
            context["states"] = simulator.simulate()
            print(" Simulation completed.")
            time.sleep(5)
            cs()
            print(" Saving simulation states...")
            slf.save_simulation(context["states"])
            print(" Simulation states saved.")
            time.sleep(5)
            cs()
class FS:
    def execute(self,context):

        # Check: mesh,dt,states
        try:
            pars = {
                "mesh":context.get("mesh"),
                "states":context.get("states"),
                "dt":context.get("dt"),
            }

            missing = [par_ask for par_ask in pars.keys() if pars.get(par_ask) is None]

            bg = context.get("background_color")
            interval = context.get("interval")
            
            fsim = fs(
                context["states"],
                context["mesh"],
                context["dt"],
                interval=interval,
                background_color=bg
            )

            fsim.animation()

        except KeyError as e:
            if e:
                time.sleep(3)
                raise ValueError(f"Missing required parameter for flight simulation: {e}")
            
class OptionLoad:
    def execute(self, context):

        print("Select load option:")
        choice = input("Load (stl/states): ")

        loader = slf()

        if choice == "stl":
            context["mesh"] = loader.load_stl()

        elif choice == "states":
            context["states"], context["dt"], context["file_name"] = loader.load_states()

        else:
            raise ValueError("Invalid load option")
class FlightSimulationMenu:

    def __init__(self):
        self.commands = {
            "bg_color":self._bg_color,
            "interval":self._interval,
            "show":self._show
        }

    def _bg_color(self,context,args):
        if not args:
            raise ValueError("Background color invalid")
        context["background_color"] = args[0]
        print(f"Background color set to: {args[0]}")
        temp = input("Press Enter or any key to exit")
        cs()

    def _interval(self,context,args):
       if not args:
              raise ValueError("Interval value is required")
       try:
           interval = float(args[0])
       except ValueError:
           raise ValueError("Interval must be a numeric value")
       
       if interval <= 0:
           raise ValueError("Interval must be a positive value")
       
       context["interval"] = interval
       print(f"Interval set to {interval} ms")
       temp = input("Press Enter or any key to exit")
       cs()
    
    def _show(self,context):
        actual_config = f"""
        . Fligth simulations settings
            Background color:    {context.get("background_color")}.
            Interval:            {context.get("interval")} ms.
        """
        print(actual_config)
        temp = input("Press Enter or any key to exit")
        cs()
        
    def execute_subcom(self,context,sub_com,args):
        if sub_com not in self.commands:
            raise ValueError(f"Invalid subcommand: {sub_com}")
        try:
            self.commands[sub_com](context,args)
        except (ValueError,IndexError) as e:
            raise ValueError(f"Invalid arguments for: {sub_com}")
        
        if sub_com != "show":
            actual_config = f"""
            . Fligth simulations settings
            Background color:    {context.get("background_color")}.
            Interval:            {context.get("interval")} ms.
        """
            print(actual_config)
            temp = input("Press Enter or any key to exit")
            cs()
    def execute(self,context):

        actual_config = f"""
        . Fligth simulations settings
            Background color:    {context.get("background_color")}.
            Interval:            {context.get("interval")} ms.
        """
        print(actual_config)
        temp = input("Press Enter or any key to exit")
        cs()

        
class notes:
    def __init__(self,):
        self.commands_notes = {
            "dates_sim":self._dates_sim,
            "flight_sim":self._flight_sim,
            "load_files":self._load_files,
            "show":self._show
        }
    def _dates_sim(self,):
        dates_sim = """
- Input initial states X0 as u,v,w,p,q,r,phi,theta,psi in a 
comma-separated format.
Units:
u,v,w: m/s
p,q,r: rad/s 
phi,theta,psi: rad.

e.g:
    X0 = 85,0,0,0,0,0,0,0.1,0

- Input control vector U0 as aileron, elevator, rudder, throttle1,
throttle2 in a comma-separated format.
Units:
aileron, elevator, rudder: rads.
throttle1, throttle2:  adm with range: [0,1].

e.g: U0 = 0,0,0,0.8,0.8

- Input time and dt in seconds, separated by a comma.

e.g: time, dt = 180, 0.01

~ Values recommend for dt < 0.1 for get better results. 

- Engines shut off and aileron deflection: 
Set engine shut off (1 or 2)
Set aileron deflection (degrees) 
Set start and end times deflection in seconds.

*** Once an engine is shut down, it cannot be
    turn on during the simulation. ***

~~ The states are save in simlate_dates like .txt ~~
"""
        print(dates_sim)
        temp = input("Press Enter or any key to exit")
        cs()

    def _flight_sim(self,):
        note = """
- Ensure that STL files are loaded before running the flight simulation.

- Ensure that simulation states are loaded before running the flight simulation.

- Backgroud color: colors valids can be found in matplotlib documentation.
    Change with: fs_options.bc_color "color".

- interval: time between frames in milliseconds.
    Recommended values:
     ~ 10-20 for fast animation.
     ~ 30-50 for smoother animation.
     ~ Default is dt for see real-time animation.

    Change with: fs_options.interval "time" (time in ms).

~~ See flight simulation settings with fs_options ~~
"""
        print(note)
        temp = input("Press Enter or any key to exit")
        cs()

    def _load_files(self,):
        note = """           
- Load stl:
    Recommend for better visualization:
    ~ C.G at origin CAD
    ~ Noise in x axis direcction
    ~ Mesh with good quality (not too many faces).
    ~ The CAD model must be oriented with the belly facing downwards.

- Load states format:
    The states file must be a .txt file with the following format:
    
        # u,v,w,phi,theta,psi,alpha,beta,gamma,time
        value1,value2,value3,... (separated by commas)

    Units:
    u,v,w: m/s
    phi,theta,psi: rads.
    alpha,beta,gamma: rads.
    time: seconds.
""" 
        print(note)
        temp = input("Press Enter or any key to exit")
        cs()     

    def execute_subcom(self,sub_com):
        if sub_com not in self.commands_notes:
            raise ValueError(f"Invalid subcommand: {sub_com}")
        try:
            self.commands_notes[sub_com]()
        except (ValueError,IndexError) as e:
            raise ValueError(f"Invalid arguments for: {sub_com}")
    
    def execute(self,context):
        notes = """
        Use: notes.commad
        ~~ Valid commands ~~
          . dates_sim
          . flight_sim
          . load_files
                """
        print(notes)
        time.sleep(5)
        cs()
        
   
class Factory:

    _commands = {
        "dates_sim":DatesForSim,
        "flight_sim": FS,
        "load_files": OptionLoad, 
        "fs_options": FlightSimulationMenu,
        "notes":notes
    }
    @staticmethod
    def create(option):
        
        if "." in option:
            main_com,sub_com = option.split(".",1)
            if main_com in Factory._commands:
                main_com = Factory._commands[main_com]()
                if sub_com and hasattr(main_com,"execute_subcom"):
                    return main_com,sub_com
                return main_com
            else:
                raise ValueError(f"Invalid option: {main_com}")
        else:
            try:
                return Factory._commands[option]()
            except KeyError:
                raise ValueError(f"Invalid option: {option}\nPossible options:\n\t{list(Factory._commands.keys())}")
