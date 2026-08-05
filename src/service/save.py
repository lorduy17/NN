import pandas as pd
from datetime import datetime
class Save:
    @staticmethod
    def s_sim(states):
        """
        States have to be array 9xN
        shorted u,v,w,p,q,r,phi,theta,psi,time
        """
        date = datetime.now().strftime("%Y%m%d")
        df = pd.DataFrame(states, columns=["u","v","w","p","q","r","phi","theta","psi","time"])
        df.to_csv(f"data/simulations_output/simulation_data_{date}.csv", index=False)
