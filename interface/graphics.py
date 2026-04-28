import matplotlib.pyplot  as plt

class Interface:
    """
    
    """
    def plotter(states):
        """
        Plot simulation

        Input
        -----
        states


        """
        body_speed = states[:,0:3]
        angle_rates = states[:,3:6]
        euler_angles = states[:,6:9]
        vector = [body_speed,angle_rates,euler_angles]
        time = states[:,9]
        labels_bs = ["u, m/s", "v, m/s", "w, m/s"]
        labels_ar = ["p, rad/s", "q, rad/s", "r, rad/s"]
        labels_ea = ["phi, rad", "theta, rad", "psi, rad"]
        vector_labels = [labels_bs,labels_ar,labels_ea]
        fig, axs = plt.subplots(3,1)
        for i in range(3):
            for j in range(3):
                axs[i].plot(time,vector[i][:,j],label=vector_labels[i][j])
            axs[i].legend()
            axs[i].grid()
            
        axs[-1].set_xlabel("Time, s")
        plt.tight_layout()
        plt.show(block=False)
