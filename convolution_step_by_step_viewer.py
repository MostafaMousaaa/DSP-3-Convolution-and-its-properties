import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib
matplotlib.use('TkAgg')

class StepByStepConvolutionViewer:
    def __init__(self, root, x_signal=None, h_signal=None):
        self.root = root
        self.root.title("🎬 Step-by-Step Convolution Animation")
        # Optimized for 100% display scaling
        self.root.geometry("1500x950")
        self.root.state('normal')
        
        # Configure styling
        self.setup_styles()
        
        # Initialize signals
        if x_signal is None:
            self.x_signal = np.array([1, 2, 1])
        else:
            self.x_signal = self._clean_signal(x_signal)
            
        if h_signal is None:
            self.h_signal = np.array([0.5, 0.3, 0.2])
        else:
            self.h_signal = self._clean_signal(h_signal)
        
        # Animation state
        self.output_length = len(self.x_signal) + len(self.h_signal) - 1
        self.current_n = 0
        self.is_playing = False
        self.animation = None
        
        # Status variables
        self.status_var = tk.StringVar(value="Ready to animate convolution")
        self.math_var = tk.StringVar(value="")
        
        self.setup_ui()
        self.setup_plots()
        self.update_plots()
        
    def _clean_signal(self, signal):
        """Remove trailing zeros from signal"""
        if np.any(signal != 0):
            last_nonzero = np.where(signal != 0)[0][-1]
            return signal[:last_nonzero + 1]
        return signal[:3]  # Minimum length
        
    def setup_styles(self):
        """Configure clean, modern UI styles"""
        style = ttk.Style()
        
        try:
            style.theme_use('clam')
        except:
            style.theme_use('default')
        
        # Clean theme colors
        colors = {
            'primary': '#2563eb',
            'success': '#059669',
            'warning': '#d97706',
            'secondary': '#64748b',
            'background': '#f8fafc',
            'surface': '#ffffff',
            'text': '#1e293b'
        }
        
        # Button styles
        style.configure('Play.TButton', 
                       font=('Segoe UI', 11, 'bold'),
                       foreground='white',
                       background=colors['success'])
        
        style.configure('Control.TButton',
                       font=('Segoe UI', 10),
                       foreground='white',
                       background=colors['primary'])
        
        style.configure('Nav.TButton',
                       font=('Segoe UI', 9),
                       foreground=colors['text'],
                       background=colors['background'])
        
        # Label styles
        style.configure('Title.TLabel',
                       font=('Segoe UI', 18, 'bold'),
                       foreground=colors['primary'])
        
        style.configure('Step.TLabel',
                       font=('Segoe UI', 14, 'bold'),
                       foreground=colors['success'])
        
        style.configure('Math.TLabel',
                       font=('Consolas', 12, 'bold'),
                       foreground=colors['warning'],
                       background=colors['background'])
        
    def setup_ui(self):
        self.root.configure(bg='#f8fafc')
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header
        self.create_header(main_frame)
        
        # Control panel
        self.create_control_panel(main_frame)
        
        # Plot area
        self.create_plot_area(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
        
    def create_header(self, parent):
        """Create header"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title and navigation
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(fill=tk.X)
        
        ttk.Label(title_frame, text="🎬 Step-by-Step Convolution", 
                 style='Title.TLabel').pack(side=tk.LEFT)
        
        # Navigation
        nav_frame = ttk.Frame(title_frame)
        nav_frame.pack(side=tk.RIGHT)
        
        ttk.Button(nav_frame, text="🔗 Main Viewer", command=self.open_main_viewer,
                  style='Nav.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="💾 Export", command=self.export_animation,
                  style='Nav.TButton').pack(side=tk.LEFT, padx=2)
        
        # Signal info
        info_frame = ttk.Frame(header_frame)
        info_frame.pack(fill=tk.X, pady=(5, 0))
        
        signal_info = f"x[n]: {len(self.x_signal)} samples • h[n]: {len(self.h_signal)} samples • Output: {self.output_length} samples"
        ttk.Label(info_frame, text=signal_info, font=('Segoe UI', 10)).pack(side=tk.LEFT)
        
        self.animation_indicator = ttk.Label(info_frame, text="⏸️", font=('Segoe UI', 14))
        self.animation_indicator.pack(side=tk.RIGHT)
        
        # Separator
        ttk.Separator(header_frame, orient='horizontal').pack(fill=tk.X, pady=(8, 0))
        
    def create_control_panel(self, parent):
        """Create control panel"""
        control_frame = ttk.LabelFrame(parent, text="Animation Controls", padding=12)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Step information
        step_frame = ttk.Frame(control_frame)
        step_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Step info and progress
        info_row = ttk.Frame(step_frame)
        info_row.pack(fill=tk.X)
        
        self.step_label = ttk.Label(info_row, text=f"Step {self.current_n + 1}/{self.output_length}", 
                                   style='Step.TLabel')
        self.step_label.pack(side=tk.LEFT)
        
        # Progress bar
        progress_frame = ttk.Frame(info_row)
        progress_frame.pack(side=tk.RIGHT)
        
        self.progress = ttk.Progressbar(progress_frame, length=200, mode='determinate')
        self.progress.pack(side=tk.LEFT, padx=(0, 10))
        self.progress['maximum'] = self.output_length - 1
        
        self.progress_label = ttk.Label(progress_frame, text="0%", font=('Segoe UI', 9))
        self.progress_label.pack(side=tk.LEFT)
        
        # Math equation
        self.equation_label = ttk.Label(step_frame, textvariable=self.math_var, 
                                       style='Math.TLabel')
        self.equation_label.pack(fill=tk.X, pady=(8, 0))
        
        # Control buttons
        controls_frame = ttk.Frame(control_frame)
        controls_frame.pack(fill=tk.X)
        
        # Navigation controls
        ttk.Button(controls_frame, text="⏮️", command=self.reset_animation,
                  style='Control.TButton', width=3).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls_frame, text="⏪", command=self.previous_step,
                  style='Control.TButton', width=3).pack(side=tk.LEFT, padx=2)
        
        # Play button
        self.play_button = ttk.Button(controls_frame, text="▶️ Play", 
                                     command=self.toggle_animation,
                                     style='Play.TButton')
        self.play_button.pack(side=tk.LEFT, padx=8)
        
        ttk.Button(controls_frame, text="⏩", command=self.next_step,
                  style='Control.TButton', width=3).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls_frame, text="⏭️", command=self.go_to_end,
                  style='Control.TButton', width=3).pack(side=tk.LEFT, padx=2)
        
        # Speed control
        speed_frame = ttk.Frame(controls_frame)
        speed_frame.pack(side=tk.RIGHT)
        
        ttk.Label(speed_frame, text="Speed:", font=('Segoe UI', 9)).pack(side=tk.LEFT)
        
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(speed_frame, from_=0.2, to=3.0, 
                               variable=self.speed_var, orient=tk.HORIZONTAL, length=100)
        speed_scale.pack(side=tk.LEFT, padx=(5, 5))
        
        self.speed_label = ttk.Label(speed_frame, text="1.0x", font=('Segoe UI', 9))
        self.speed_label.pack(side=tk.LEFT)
        speed_scale.bind("<Motion>", self.update_speed_label)
        
    def create_plot_area(self, parent):
        """Create plot area"""
        plot_container = ttk.LabelFrame(parent, text="Convolution Visualization", padding=15)
        plot_container.pack(fill=tk.BOTH, expand=True)
        
        # Configure matplotlib
        plt.style.use('default')
        plt.rcParams.update({
            'figure.facecolor': 'white',
            'axes.facecolor': 'white',
            'axes.edgecolor': '#2563eb',
            'axes.labelcolor': '#1e293b',
            'xtick.color': '#64748b',
            'ytick.color': '#64748b',
            'grid.color': '#e2e8f0',
            'text.color': '#1e293b',
            'font.size': 10
        })
        
        # Create figure
        self.fig = Figure(figsize=(16, 10), dpi=100, facecolor='white')
        
        self.canvas = FigureCanvasTkAgg(self.fig, plot_container)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Navigation toolbar
        toolbar_frame = ttk.Frame(plot_container)
        toolbar_frame.pack(fill=tk.X, pady=(10, 0))
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()
        
    def create_status_bar(self, parent):
        """Create status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        status_bg = tk.Frame(status_frame, bg='#1e293b', height=25)
        status_bg.pack(fill=tk.X)
        
        status_content = tk.Frame(status_bg, bg='#1e293b')
        status_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=3)
        
        self.status_display = tk.Label(status_content, 
                                      font=('Segoe UI', 9), foreground='white', background='#1e293b')
        self.status_display.pack(side=tk.LEFT)
        
        self.animation_info = tk.Label(status_content, text="Ready",
                                      font=('Segoe UI', 9), foreground='white', background='#1e293b')
        self.animation_info.pack(side=tk.RIGHT)

    def setup_plots(self):
        """Setup plot layout"""
        self.fig.clear()
        
        # Create subplot layout - 2x2 grid
        gs = self.fig.add_gridspec(2, 2, height_ratios=[1, 1], width_ratios=[1, 1],
                                  hspace=0.3, wspace=0.3, left=0.06, right=0.94, 
                                  top=0.92, bottom=0.08)
        
        self.ax_x = self.fig.add_subplot(gs[0, 0])      # Input signal x[n]
        self.ax_h = self.fig.add_subplot(gs[0, 1])      # Flipped h[n-k]
        self.ax_product = self.fig.add_subplot(gs[1, 0]) # Product x[k] * h[n-k]
        self.ax_output = self.fig.add_subplot(gs[1, 1])  # Output y[n]
        
        # Style all axes
        for ax in [self.ax_x, self.ax_h, self.ax_product, self.ax_output]:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#2563eb')
            ax.spines['bottom'].set_color('#2563eb')
            ax.tick_params(colors='#64748b', labelsize=9)
        
    def update_plots(self):
        """Update all plots for current step"""
        # Clear all axes
        self.ax_x.clear()
        self.ax_h.clear()
        self.ax_product.clear()
        self.ax_output.clear()
        
        # Color scheme
        colors = {
            'x_signal': '#3b82f6',
            'h_signal': '#1e40af',
            'product': '#059669',
            'output': '#1e293b',
            'highlight': '#dc2626'
        }
        
        # Current step
        n = self.current_n
        
        # 1. Plot x[n] - Input Signal
        k_x = np.arange(len(self.x_signal))
        self.ax_x.stem(k_x, self.x_signal, basefmt=' ', 
                      linefmt=colors['x_signal'], markerfmt='o' )
        self.ax_x.set_title('Input Signal x[k]', fontsize=11, fontweight='bold')
        self.ax_x.set_ylabel('Amplitude')
        self.ax_x.grid(True, linestyle='--' )
        self.ax_x.set_ylim([-0.5, max(2, np.max(self.x_signal) + 0.5)])
        
        # 2. Plot h[n-k] - Flipped and Shifted Impulse Response
        h_flipped = np.flip(self.h_signal)
        # Create extended range to show the shifted signal
        k_range = np.arange(-len(self.h_signal), len(self.x_signal) + len(self.h_signal))
        h_shifted = np.zeros(len(k_range))
        
        # Position the flipped h signal at position n
        start_idx = n + len(self.h_signal) - 1
        if start_idx >= 0 and start_idx < len(k_range):
            for i, val in enumerate(h_flipped):
                idx = start_idx - i
                if 0 <= idx < len(k_range):
                    h_shifted[idx] = val
        
        # Plot h[n-k]
        valid_indices = h_shifted != 0
        if np.any(valid_indices):
            self.ax_h.stem(k_range[valid_indices], h_shifted[valid_indices], 
                          basefmt=' ', linefmt=colors['h_signal'], markerfmt='s' )
        
        self.ax_h.set_title(f'h[{n}-k] (Flipped & Shifted)', fontsize=11, fontweight='bold')
        self.ax_h.set_ylabel('Amplitude')
        self.ax_h.grid(True, linestyle='--' )
        self.ax_h.set_xlim([-1, max(len(self.x_signal), len(self.h_signal)) + 1])
        self.ax_h.set_ylim([-0.5, max(2, np.max(self.h_signal) + 0.5)])
        
        # 3. Plot Product x[k] * h[n-k]
        product = np.zeros(len(self.x_signal))
        sum_value = 0
        
        for k in range(len(self.x_signal)):
            h_idx = n - k
            if 0 <= h_idx < len(self.h_signal):
                product[k] = self.x_signal[k] * self.h_signal[h_idx]
                sum_value += product[k]
        
        # Plot non-zero products
        non_zero_k = product != 0
        if np.any(non_zero_k):
            self.ax_product.stem(k_x[non_zero_k], product[non_zero_k], 
                               basefmt=' ', linefmt=colors['product'], markerfmt='D' )
        
        self.ax_product.axhline(y=0, color='gray', linestyle='-' )
        self.ax_product.set_title(f'x[k] × h[{n}-k] → Sum = {sum_value:.3f}', 
                                 fontsize=11, fontweight='bold')
        self.ax_product.set_ylabel('Product')
        self.ax_product.grid(True, linestyle='--' )
        self.ax_product.set_ylim([min(-0.5, np.min(product) - 0.2), 
                                 max(2, np.max(product) + 0.2)])
        
        # 4. Plot Output y[n] - Convolution Result
        y_computed = np.zeros(self.output_length)
        for i in range(min(n + 1, self.output_length)):
            for k in range(len(self.x_signal)):
                h_idx = i - k
                if 0 <= h_idx < len(self.h_signal):
                    y_computed[i] += self.x_signal[k] * self.h_signal[h_idx]
        
        # Plot computed output up to current step
        n_computed = np.arange(n + 1)
        if len(n_computed) > 0:
            self.ax_output.stem(n_computed, y_computed[:n + 1], 
                              basefmt=' ', linefmt=colors['output'], markerfmt='o' )
            
            # Highlight current output sample
            if n < len(y_computed):
                self.ax_output.stem([n], [y_computed[n]], 
                                  basefmt=' ', linefmt=colors['highlight'], 
                                  markerfmt='o')
        
        # Plot remaining samples as faded
        if n + 1 < self.output_length:
            remaining_n = np.arange(n + 1, self.output_length)
            remaining_y = np.zeros(len(remaining_n))
            self.ax_output.stem(remaining_n, remaining_y, 
                              basefmt=' ', linefmt='lightgray', markerfmt='o'
                              )
        
        self.ax_output.set_title(f'Convolution Output y[n] | Step {n + 1}/{self.output_length}', 
                               fontsize=11, fontweight='bold')
        self.ax_output.set_xlabel('Sample Index (n)')
        self.ax_output.set_ylabel('Amplitude')
        self.ax_output.grid(True, linestyle='--' )
        
        if self.output_length > 0:
            self.ax_output.set_xlim([-0.5, self.output_length - 0.5])
            y_max = max(2, np.max(np.abs(y_computed)) + 0.5) if np.any(y_computed) else 2
            self.ax_output.set_ylim([-y_max/2, y_max])
        
        # Update equation
        self.math_var.set(f"y[{n}] = Σ x[k] × h[{n}-k] = {sum_value:.3f}")
        
        # Update step info
        self.step_label.config(text=f"Step {n + 1}/{self.output_length}: Computing y[{n}]")
        
        # Update progress
        progress_percent = int((n / max(1, self.output_length - 1)) * 100)
        self.progress['value'] = n
        self.progress_label.config(text=f"{progress_percent}%")
        
        # Update status
        self.status_var.set(f"Computing y[{n}] = {sum_value:.3f}")
        
        self.canvas.draw()
        
    def next_step(self):
        """Go to next step"""
        if self.current_n < self.output_length - 1:
            self.current_n += 1
            self.update_plots()
            
    def previous_step(self):
        """Go to previous step"""
        if self.current_n > 0:
            self.current_n -= 1
            self.update_plots()
            
    def reset_animation(self):
        """Reset to first step"""
        self.stop_animation()
        self.current_n = 0
        self.update_plots()
        
    def go_to_end(self):
        """Go to last step"""
        self.stop_animation()
        self.current_n = self.output_length - 1
        self.update_plots()
        
    def toggle_animation(self):
        """Toggle animation play/pause"""
        if self.is_playing:
            self.stop_animation()
        else:
            self.start_animation()
            
    def start_animation(self):
        """Start animation"""
        self.is_playing = True
        self.play_button.config(text="⏸️ Pause")
        self.animation_indicator.config(text="▶️")
        self._animate_step()
        
    def _animate_step(self):
        """Animate one step"""
        if self.is_playing:
            self.next_step()
            
            if self.current_n >= self.output_length - 1:
                self.stop_animation()
            else:
                # Schedule next step based on speed
                delay = int(1000 / self.speed_var.get())  # Convert to milliseconds
                self.animation = self.root.after(delay, self._animate_step)
        
    def stop_animation(self):
        """Stop animation"""
        self.is_playing = False
        self.play_button.config(text="▶️ Play")
        self.animation_indicator.config(text="⏸️")
        if self.animation:
            self.root.after_cancel(self.animation)
            self.animation = None
        
    def update_speed_label(self, event=None):
        """Update speed label"""
        speed = self.speed_var.get()
        self.speed_label.config(text=f"{speed:.1f}x")
    
    def open_main_viewer(self):
        """Open main convolution viewer"""
        try:
            from convolution_viewer import ConvolutionViewer
            main_window = tk.Toplevel(self.root)
            ConvolutionViewer(main_window)
        except ImportError:
            try:
                import subprocess
                import sys
                subprocess.Popen([sys.executable, "convolution_viewer.py"])
            except:
                messagebox.showwarning("Warning", "Main viewer not found.")
    
    def export_animation(self):
        """Export animation frames"""
        try:
            from matplotlib.animation import FuncAnimation, PillowWriter
            
            def animate(frame):
                old_n = self.current_n
                self.current_n = frame
                self.update_plots()
                self.current_n = old_n
                return []
            
            anim = FuncAnimation(self.fig, animate, frames=self.output_length, 
                               interval=1000, blit=False, repeat=False)
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".gif",
                filetypes=[("GIF files", "*.gif"), ("All files", "*.*")],
                title="Export Animation"
            )
            
            if filename:
                anim.save(filename, writer=PillowWriter(fps=1))
                messagebox.showinfo("Success", f"Animation exported to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not export animation: {str(e)}")

def main():
    root = tk.Tk()
    app = StepByStepConvolutionViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
