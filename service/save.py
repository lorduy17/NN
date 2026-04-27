import pandas as pd
from datetime import datetime
class Save:
    def __init__(self, states):
        self.states = states
    def s_sim(self):
        """
        States have to be array 9xN
        shorted u,v,w,p,q,r,phi,theta,psi,alpha,beta,gamma,time
        """
        date = datetime.now().strftime("%Y%m%d")
        df = pd.DataFrame(self.states, columns=["u","v","w","p","q","r","phi","theta","psi","alpha","beta","gamma","time"])
        df.to_csv(f"data/simulation_data_{date}.csv", index=False)
