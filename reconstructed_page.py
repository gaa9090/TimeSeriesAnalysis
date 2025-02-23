import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D  

# page to show reconstructed phase space
class reconstructed_page(tk.Frame):

    # Constructor
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  

        # widgets 
        self.plot_frame = tk.Frame(self)
        self.plot_frame.pack(fill="both", expand=True)

        self.gfnn_label = tk.Label(self, textvariable=self.controller.gfnn)
        self.gfnn_label.pack()

        self.back_button = tk.Button(self, text="Change 𝜏 or D_2", 
                                     command=lambda: self.controller.show_frame("process_page"))
        self.back_button.pack(pady=10, anchor="se")

    # Raise the page to the top of the stack
    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.create_plot()


    def create_plot(self):
        for child in self.plot_frame.winfo_children():
            child.destroy()

        Recons = getattr(self.controller, "reconstructed_data", None)
        if Recons is None:
            return  

        fig = Figure(figsize=(5, 4))
        ax = fig.add_subplot(111, projection="3d")

        ax.plot(
            Recons[:, 0],
            Recons[:, 1],
            Recons[:, 2],
            marker="o",
            linestyle="None",
            ms=2,
            color="blue"
        )
        ax.set_xlabel("R_X(t)")
        ax.set_ylabel("R_Y(t)")
        ax.set_zlabel("R_Z(t)")

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)