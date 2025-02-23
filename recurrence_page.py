import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class recurrence_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.plot_frame = tk.Frame(self)
        self.plot_frame.pack(fill="both", expand=True)

        self.back_button = tk.Button(
            self, text="Back to Process Page",
            command=lambda: controller.show_frame("process_page")
        )
        self.back_button.pack(pady=10, anchor="se")

    def tkraise(self, aboveThis=None):
        """Called automatically when this frame is shown."""
        super().tkraise(aboveThis)
        self.create_plot()

    def create_plot(self):
        for child in self.plot_frame.winfo_children():
            child.destroy()

        X_rp = getattr(self.controller, "recurrence_data", None)
        if X_rp is None:
            return  # No data to plot

        fig = Figure(figsize=(5, 4))
        ax = fig.add_subplot(111)

        ax.imshow(X_rp, cmap='binary', origin='lower')
        ax.set_title("Recurrence Plot")
        ax.set_xlabel("Time")
        ax.set_ylabel("Time")

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
