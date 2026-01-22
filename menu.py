#%%
from factory import Factory as fact
from aircraft_model import AircraftModel as amodel
from save_load_files import SaveLoadFiles as slf
from simulation import Simulate as sim
from flight_simulation import FlightSimulation as fsm
import numpy as np
from cls import clean_screen as cs
import os

class Menu:
    def __init__(self):
        self.context = {}
        self.factory = fact()

    def display_options(self):
        cs()
        
        menu = """
        Menu                                  Commands
        . Simulate dates        ............. dates_sim
        . Flight Simulation     ............. flight_sim
        . Load files ........................ load_files
        
        . Exit .............................. exit
        
        Note: Use the "notes.command" command before using any other commands.
        """

        return print(menu)

    def loop(self,context):
        while True:
            self.display_options()
            tokens = input().strip().split(" ",maxsplit=1)
            command = tokens[0]
            args = tokens[1].split() if len(tokens) > 1 else []
            try:
                result = fact.create(command)
                if isinstance(result,tuple):
                    if args == []:
                        command,sub_com = result
                        command.execute_subcom(sub_com)
                    else:
                        command,sub_com = result
                        command.execute_subcom(context, sub_com, args)

                else:
                    result.execute(context)
            except ValueError as e:
                print(e)


if __name__ == "__main__":
    context = {}
    menu = Menu()
    menu.loop(context)


