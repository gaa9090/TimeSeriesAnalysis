import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")  # Make sure we use the Tk backend
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from phase_space import phase_space
from pyts.image import RecurrencePlot

# This page contains sliders for τ and Embedding Dimension
class process_page(tk.Frame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  

       # Page title
        self.label = tk.Label(self, text="Phase Space Reconstruction", font=("Arial", 14))
        self.label.pack(pady=20)

        # slider for lag time delay
        lag_frame = tk.Frame(self)
        lag_frame.pack(fill="both", pady=5)
        lag_label = tk.Label(lag_frame, text="Select Time Delay: ")  
        lag_label.pack(side="left",padx=(0,10))  
        self.lag_slider = tk.Scale(lag_frame, from_=1, to=10, orient="horizontal")
        self.lag_slider.set(10)  
        self.lag_slider.pack(side="left")

        # slider for dimension
        dim_frame = tk.Frame(self)
        dim_frame.pack(fill="both", pady=5)
        dim_label = tk.Label(dim_frame, text="Select Embedding Dimension: ")
        dim_label.pack(side="left",padx=(0,10))
        self.dim_slider = tk.Scale(dim_frame, from_=2, to=10, orient="horizontal")
        self.dim_slider.set(3)  
        self.dim_slider.pack(side="left")

        # phase space 
        self.next_button = tk.Button(self, text="Reconstruct Phase Space", command=self.reconstruct)
        self.next_button.pack(pady=10)

        # recurrence plot
        self.rp_button = tk.Button(self, text="Compute Recurrence Plot", command=self.compute_recurrence_plot)
        self.rp_button.pack(pady=10)

    # reconstructs the phase space 
    def reconstruct(self):
        print("Reconstruction initiated")
        lag = self.lag_slider.get()
        n_dims = self.dim_slider.get()
        analyze = phase_space(self.controller)

        try:
            _ = analyze.reconstruct(lag=lag, n_dims=n_dims) 
            dims, fnn_percentages = analyze.global_false_nearest_neighbors(
                lag=lag, min_dims=n_dims, max_dims=n_dims
            )
            print(f"Reconstruction complete.\nGFNN: {fnn_percentages}")
            self.controller.gfnn.set("GFNN Ratio: " + str(fnn_percentages))

            Recons = analyze.reconstruct(lag, n_dims)

            self.controller.reconstructed_data = Recons
            self.controller.show_frame("reconstructed_page")
                
        except Exception as e:
            result_text = f"Error during analysis: {str(e)}"


    # uses RecurrencePlot to compute and store a recurrence matrix
    def compute_recurrence_plot(self):
        lag = self.lag_slider.get()
        n_dims = self.dim_slider.get()

        x = self.controller.df
        X = x.reshape(1, -1)  # shape = (1, N)

        try:
            rp = RecurrencePlot(
                dimension=n_dims,
                time_delay=lag,
                threshold='point',
                percentage=10
            )

            # transform into a 2D recurrence matrix
            X_rp = rp.transform(X)  # shape = (1, size, size)
            rp_matrix = X_rp[0]     # shape = (size, size)

            self.controller.recurrence_data = rp_matrix

            self.controller.show_frame("recurrence_page")

        except Exception as exc:
            print(f"Error during Recurrence Plot analysis: {str(exc)}")