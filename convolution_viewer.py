import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import sys
import os
import json
import matplotlib
matplotlib.use('TkAgg')

class ConvolutionViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("🔗 Real-Time Convolution Viewer")
        # Optimized for 100% display scaling
        self.root.geometry("1400x900")
        self.root.state('normal')  # Ensure normal window state
        
        # Configure styling
        self.setup_styles()
        
        # Initialize signals with dynamic n_points
        self.n_points = 7  # Initial value set to 7
        self.x_signal = np.array([1, 2, 1, 0, 0, 0, 0])
        self.h_signal = np.array([0.5, 0.3, 0.2, 0, 0, 0, 0])
        self.y_signal = np.convolve(self.x_signal, self.h_signal, mode='full')
        
        # Status tracking
        self.status_var = tk.StringVar(value="Ready - Select a signal to edit")
        self.current_signal = 'x'
        self.dragging = False
        
        self.setup_ui()
        self.setup_plots()
        self.update_plots()
        
    def setup_styles(self):
        """Configure clean, modern UI styles"""
        style = ttk.Style()
        
        try:
            style.theme_use('clam')
        except:
            style.theme_use('default')
        
        # Clean blue theme
        colors = {
            'primary': '#2563eb',
            'secondary': '#64748b',
            'background': '#f8fafc',
            'surface': '#ffffff',
            'text': '#1e293b'
        }
        
        # Button styles
        style.configure('Primary.TButton', 
                       font=('Segoe UI', 10, 'bold'),
                       foreground='white',
                       background=colors['primary'])
        
        style.configure('Secondary.TButton',
                       font=('Segoe UI', 9),
                       foreground=colors['text'],
                       background=colors['background'])
        
        # Label styles
        style.configure('Title.TLabel',
                       font=('Segoe UI', 16, 'bold'),
                       foreground=colors['primary'])
        
        style.configure('Section.TLabel',
                       font=('Segoe UI', 10, 'bold'),
                       foreground=colors['text'])
        
        style.configure('Info.TLabel',
                       font=('Segoe UI', 9),
                       foreground=colors['secondary'])
        
    def setup_ui(self):
        self.root.configure(bg='#f8fafc')
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header
        self.create_header(main_frame)
        
        # Content area
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Control panel (left side)
        self.create_control_panel(content_frame)
        
        # Plot area (right side)
        self.create_plot_area(content_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
        
    def create_header(self, parent):
        """Create clean header"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        ttk.Label(header_frame, text="🔗 Real-Time Convolution Viewer", 
                 style='Title.TLabel').pack(side=tk.LEFT)
        
        # Navigation
        nav_frame = ttk.Frame(header_frame)
        nav_frame.pack(side=tk.RIGHT)
        
        ttk.Button(nav_frame, text="🎬 Step-by-Step Animation", 
                  command=self.open_step_by_step,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        # Subtitle
        subtitle_frame = ttk.Frame(header_frame)
        subtitle_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(subtitle_frame, 
                 text="Interactive Platform for Discrete Convolution Learning • y[n] = x[n] ∗ h[n]",
                 style='Info.TLabel').pack(side=tk.LEFT)
        
        # Separator
        ttk.Separator(header_frame, orient='horizontal').pack(fill=tk.X, pady=(10, 0))
        
    def create_control_panel(self, parent):
        """Create streamlined control panel"""
        control_frame = ttk.Frame(parent)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        control_frame.configure(width=350)
        control_frame.pack_propagate(False)
        
        # Signal Selection
        signal_frame = ttk.LabelFrame(control_frame, text="Signal Selection", padding=10)
        signal_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.signal_var = tk.StringVar(value="x[n] - Input Signal")
        signal_combo = ttk.Combobox(signal_frame, textvariable=self.signal_var, 
                                   values=["x[n] - Input Signal", "h[n] - Impulse Response"], 
                                   state="readonly", font=('Segoe UI', 9))
        signal_combo.pack(fill=tk.X)
        signal_combo.bind('<<ComboboxSelected>>', self.on_signal_change)
        
        # Signal Properties
        self.create_signal_properties(signal_frame)
        
        # Preset Signals
        preset_frame = ttk.LabelFrame(control_frame, text="Signal Templates", padding=10)
        preset_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Preset buttons in grid
        presets = [
            ("Impulse δ[n]", "impulse"),
            ("Step u[n]", "step"),
            ("Exponential", "exponential"),
            ("Sinusoidal", "sine"),
            ("Triangular", "triangular"),
            ("Random", "random"),
            ("Gaussian", "gaussian"),
            ("Clear", "clear")
        ]
        
        preset_grid = ttk.Frame(preset_frame)
        preset_grid.pack(fill=tk.X)
        
        for i, (text, cmd) in enumerate(presets):
            row, col = i // 2, i % 2
            ttk.Button(preset_grid, text=text, 
                      command=lambda c=cmd: self.set_preset(c),
                      style='Secondary.TButton').grid(row=row, column=col, 
                                                     padx=2, pady=2, sticky='ew')
        
        preset_grid.grid_columnconfigure(0, weight=1)
        preset_grid.grid_columnconfigure(1, weight=1)
        
        # Manual Input
        input_frame = ttk.LabelFrame(control_frame, text="Manual Input", padding=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(input_frame, text="Values (comma-separated):", style='Info.TLabel').pack(anchor=tk.W)
        
        self.input_var = tk.StringVar()
        input_entry = ttk.Entry(input_frame, textvariable=self.input_var, font=('Consolas', 9))
        input_entry.pack(fill=tk.X, pady=(5, 10))
        input_entry.bind('<Return>', self.on_manual_input)
        
        ttk.Button(input_frame, text="Apply Changes", command=self.on_manual_input,
                  style='Primary.TButton').pack(fill=tk.X)
        
        # Signal Configuration
        config_frame = ttk.LabelFrame(control_frame, text="Configuration", padding=10)
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Length control - dynamic updates
        length_frame = ttk.Frame(config_frame)
        length_frame.pack(fill=tk.X)
        
        ttk.Label(length_frame, text="Signal Length:", style='Info.TLabel').pack(side=tk.LEFT)
        
        self.length_var = tk.IntVar(value=self.n_points)
        length_spinbox = tk.Spinbox(length_frame, from_=3, to=50, textvariable=self.length_var, 
                                   width=6, command=self.on_length_change, font=('Segoe UI', 9))
        length_spinbox.pack(side=tk.RIGHT)
        length_spinbox.bind('<KeyRelease>', lambda e: self.on_length_change())
        length_spinbox.bind('<ButtonRelease>', lambda e: self.on_length_change())
        length_spinbox.pack(side=tk.RIGHT)
        
        # Operations
        ops_frame = ttk.LabelFrame(control_frame, text="Operations", padding=10)
        ops_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(ops_frame, text="Swap x[n] ↔ h[n]", 
                  command=self.swap_signals,
                  style='Secondary.TButton').pack(fill=tk.X, pady=2)
        
        ttk.Button(ops_frame, text="Reverse h[n]", 
                  command=self.reverse_h_signal,
                  style='Secondary.TButton').pack(fill=tk.X, pady=2)
        
        ttk.Button(ops_frame, text="Normalize Signals", 
                  command=self.normalize_signals,
                  style='Secondary.TButton').pack(fill=tk.X, pady=2)
        
        # File Operations
        file_frame = ttk.LabelFrame(control_frame, text="File Operations", padding=10)
        file_frame.pack(fill=tk.X)
        
        ttk.Button(file_frame, text="Save Session", 
                  command=self.save_signals,
                  style='Secondary.TButton').pack(fill=tk.X, pady=2)
        
        ttk.Button(file_frame, text="Load Session", 
                  command=self.load_signals,
                  style='Secondary.TButton').pack(fill=tk.X, pady=2)
        
        ttk.Button(file_frame, text="Export Plot", 
                  command=self.export_plot,
                  style='Secondary.TButton').pack(fill=tk.X, pady=2)
        
    def create_signal_properties(self, parent):
        """Create signal properties display"""
        props_frame = ttk.Frame(parent)
        props_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(props_frame, text="Properties:", style='Section.TLabel').pack(anchor=tk.W)
        
        self.properties_frame = ttk.Frame(props_frame)
        self.properties_frame.pack(fill=tk.X, pady=(5, 0))
        
    def create_plot_area(self, parent):
        """Create plot area"""
        plot_container = ttk.LabelFrame(parent, text="Real-Time Visualization", padding=15)
        plot_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Plot controls
        controls_frame = ttk.Frame(plot_container)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(controls_frame, text="Display Options:", style='Section.TLabel').pack(side=tk.LEFT)
        
        self.grid_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(controls_frame, text="Grid", variable=self.grid_var,
                       command=self.update_plots).pack(side=tk.LEFT, padx=10)
        
        self.stem_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(controls_frame, text="Stem Plot", variable=self.stem_var,
                       command=self.update_plots).pack(side=tk.LEFT, padx=5)
        
        # Refresh button
        ttk.Button(controls_frame, text="🔄 Refresh", 
                  command=self.update_plots,
                  style='Secondary.TButton').pack(side=tk.RIGHT)
        
        # Configure matplotlib for clean appearance
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
        
        # Create figure with appropriate size for the layout
        self.fig = Figure(figsize=(11, 8), dpi=100, facecolor='white')
        
        self.canvas = FigureCanvasTkAgg(self.fig, plot_container)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Navigation toolbar
        toolbar_frame = ttk.Frame(plot_container)
        toolbar_frame.pack(fill=tk.X, pady=(10, 0))
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()
        
        # Connect mouse events for interactive editing
        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('motion_notify_event', self.on_drag)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        
    def create_status_bar(self, parent):
        """Create status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        status_bg = tk.Frame(status_frame, bg='#1e293b', height=25)
        status_bg.pack(fill=tk.X)
        
        status_content = tk.Frame(status_bg, bg='#1e293b')
        status_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=3)
        
        self.status_display = tk.Label(status_content, textvariable=self.status_var,
                                      font=('Segoe UI', 9), foreground='white', background='#1e293b')
        self.status_display.pack(side=tk.LEFT)
        
        # Add dynamic length indicator
        self.length_indicator = tk.Label(status_content, text=f"Length: {self.n_points}",
                                        font=('Segoe UI', 9, 'bold'), foreground='#60a5fa', background='#1e293b')
        self.length_indicator.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.info_label = tk.Label(status_content, text="Ready",
                                  font=('Segoe UI', 9), foreground='white', background='#1e293b')
        self.info_label.pack(side=tk.RIGHT)

    def setup_plots(self):
        """Setup plot layout"""
        self.fig.clear()
        
        # Create clean subplot layout
        gs = self.fig.add_gridspec(3, 1, height_ratios=[1, 1, 1.2], 
                                  hspace=0.4, left=0.1, right=0.95, 
                                  top=0.93, bottom=0.1)
        
        self.ax1 = self.fig.add_subplot(gs[0])
        self.ax2 = self.fig.add_subplot(gs[1])
        self.ax3 = self.fig.add_subplot(gs[2])
        
        # Style the axes
        for ax in [self.ax1, self.ax2, self.ax3]:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#2563eb')
            ax.spines['bottom'].set_color('#2563eb')
            ax.tick_params(colors='#64748b', labelsize=9)
        
    def update_plots(self):
        """Update all plots"""
        # Clear plots
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        
        # Color scheme
        colors = {
            'x_signal': '#3b82f6',
            'h_signal': '#1e40af',
            'y_signal': '#1e293b'
        }
        
        # Calculate convolution
        self.y_signal = np.convolve(self.x_signal, self.h_signal, mode='full')
        
        # Plot x[n]
        n_x = np.arange(len(self.x_signal))
        if self.stem_var.get():
            self.ax1.stem(n_x, self.x_signal, basefmt=' ', 
                         linefmt=colors['x_signal'], markerfmt='o' )
        else:
            self.ax1.plot(n_x, self.x_signal, color=colors['x_signal'], marker='o' )
        
        self.ax1.set_title('Input Signal x[n]', fontsize=12, fontweight='bold', color='#2563eb')
        self.ax1.set_ylabel('Amplitude', fontsize=10)
        
        if self.grid_var.get():
            self.ax1.grid(True, linestyle='--', color='#e2e8f0')
        
        self.ax1.set_ylim([-2, max(3, np.max(np.abs(self.x_signal)) + 1)])
        
        # Add editing hint for active signal
        if self.current_signal == 'x':
            self.ax1.text(0.02, 0.95, '✏️ Click and drag to edit', 
                         transform=self.ax1.transAxes, fontsize=9,
                         bbox=dict(boxstyle="round,pad=0.3", facecolor='#dbeafe'))
        
        # Plot h[n]
        n_h = np.arange(len(self.h_signal))
        if self.stem_var.get():
            self.ax2.stem(n_h, self.h_signal, basefmt=' ', 
                         linefmt=colors['h_signal'], markerfmt='s' )
        else:
            self.ax2.plot(n_h, self.h_signal, color=colors['h_signal'], marker='s' )
        
        self.ax2.set_title('Impulse Response h[n]', fontsize=12, fontweight='bold', color='#2563eb')
        self.ax2.set_ylabel('Amplitude', fontsize=10)
        
        if self.grid_var.get():
            self.ax2.grid(True, linestyle='--', color='#e2e8f0')
        
        self.ax2.set_ylim([-2, max(3, np.max(np.abs(self.h_signal)) + 1)])
        
        if self.current_signal == 'h':
            self.ax2.text(0.02, 0.95, '✏️ Click and drag to edit', 
                         transform=self.ax2.transAxes, fontsize=9,
                         bbox=dict(boxstyle="round,pad=0.3", facecolor='#dbeafe'))
        
        # Plot y[n]
        n_y = np.arange(len(self.y_signal))
        if self.stem_var.get():
            self.ax3.stem(n_y, self.y_signal, basefmt=' ', 
                         linefmt=colors['y_signal'], markerfmt='D' )
        else:
            self.ax3.plot(n_y, self.y_signal, color=colors['y_signal'], marker='D' )
        
        conv_length = len(self.y_signal)
        self.ax3.set_title(f'Convolution Output y[n] = x[n] ∗ h[n] (Length: {conv_length})', 
                          fontsize=12, fontweight='bold', color='#1e293b')
        self.ax3.set_xlabel('Sample Index (n)', fontsize=10)
        self.ax3.set_ylabel('Amplitude', fontsize=10)
        
        if self.grid_var.get():
            self.ax3.grid(True, linestyle='--', color='#e2e8f0')
        
        if len(self.y_signal) > 0:
            self.ax3.set_ylim([min(-1, np.min(self.y_signal) - 0.5), 
                              max(3, np.max(self.y_signal) + 0.5)])
        
        # Update properties and status
        self.update_signal_properties()
        self.status_var.set(f"Convolution computed: {len(self.x_signal)} + {len(self.h_signal)} - 1 = {conv_length} samples")
        self.info_label.config(text=f"Output Length: {conv_length}")
        
        self.canvas.draw()
        
    def update_signal_properties(self):
        """Update signal properties display"""
        # Clear existing properties
        for widget in self.properties_frame.winfo_children():
            widget.destroy()
        
        # Get current signal
        if self.signal_var.get().startswith("x[n]"):
            signal = self.x_signal
        else:
            signal = self.h_signal
        
        # Calculate properties with dynamic length info
        properties = {
            "Length": f"{len(signal)} / {self.n_points}",
            "Energy": f"{np.sum(signal**2):.3f}",
            "Max": f"{np.max(signal):.3f}",
            "Min": f"{np.min(signal):.3f}",
            "Mean": f"{np.mean(signal):.3f}",
            "Non-zero": f"{np.count_nonzero(signal)}"
        }
        
        # Display properties in grid
        row = 0
        for prop, value in properties.items():
            ttk.Label(self.properties_frame, text=f"{prop}:", 
                     style='Info.TLabel').grid(row=row, column=0, sticky='w', padx=(0, 10))
            ttk.Label(self.properties_frame, text=value, 
                     font=('Consolas', 9, 'bold')).grid(row=row, column=1, sticky='w')
            row += 1
    
    def set_preset(self, preset_type):
        """Set preset signal patterns"""
        n = np.arange(self.n_points)
        
        if preset_type == "impulse":
            signal = np.zeros(self.n_points)
            signal[0] = 1.0
        elif preset_type == "step":
            signal = np.ones(self.n_points)
        elif preset_type == "exponential":
            signal = 0.8 ** n
        elif preset_type == "sine":
            signal = np.sin(2 * np.pi * n / 8)
        elif preset_type == "triangular":
            signal = np.maximum(0, 1 - np.abs(n - self.n_points//4) / (self.n_points//8))
        elif preset_type == "gaussian":
            signal = np.exp(-0.5 * ((n - self.n_points//2) / (self.n_points//8))**2)
        elif preset_type == "random":
            signal = np.random.uniform(-1, 1, self.n_points)
        elif preset_type == "clear":
            signal = np.zeros(self.n_points)
        else:
            return
            
        if self.current_signal == 'x':
            self.x_signal = signal.copy()
            self.status_var.set(f"Applied {preset_type} preset to x[n]")
        else:
            self.h_signal = signal.copy()
            self.status_var.set(f"Applied {preset_type} preset to h[n]")
            
        self.input_var.set(','.join(f'{x:.3f}' for x in signal))
        self.update_plots()
    
    def swap_signals(self):
        """Swap x[n] and h[n] signals"""
        self.x_signal, self.h_signal = self.h_signal.copy(), self.x_signal.copy()
        self.on_signal_change()
        self.update_plots()
    
    def reverse_h_signal(self):
        """Reverse h[n] signal"""
        self.h_signal = np.flip(self.h_signal)
        if self.current_signal == 'h':
            self.input_var.set(','.join(f'{x:.3f}' for x in self.h_signal))
        self.update_plots()
    
    def normalize_signals(self):
        """Normalize both signals to [-1, 1]"""
        if np.max(np.abs(self.x_signal)) > 0:
            self.x_signal = self.x_signal / np.max(np.abs(self.x_signal))
        if np.max(np.abs(self.h_signal)) > 0:
            self.h_signal = self.h_signal / np.max(np.abs(self.h_signal))
        self.on_signal_change()
        self.update_plots()
    
    def export_plot(self):
        """Export current plot as PNG"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                title="Export Plot"
            )
            if filename:
                self.fig.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
                messagebox.showinfo("Success", f"Plot exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not export plot: {str(e)}")
    
    def save_signals(self):
        """Save current signals to JSON file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Save Signals"
            )
            if filename:
                data = {
                    'x_signal': self.x_signal.tolist(),
                    'h_signal': self.h_signal.tolist(),
                    'length': self.n_points
                }
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
                messagebox.showinfo("Success", f"Session saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {str(e)}")
            
    def load_signals(self):
        """Load signals from JSON file"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Load Signals"
            )
            if filename:
                with open(filename, 'r') as f:
                    data = json.load(f)
                
                self.x_signal = np.array(data['x_signal'])
                self.h_signal = np.array(data['h_signal'])
                self.n_points = data.get('length', len(self.x_signal))
                self.length_var.set(self.n_points)
                
                self.on_signal_change()
                self.update_plots()
                messagebox.showinfo("Success", f"Session loaded from {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load file: {str(e)}")
    
    def on_signal_change(self, event=None):
        """Handle signal selection change"""
        signal_type = self.signal_var.get()
        if signal_type.startswith("x[n]"):
            self.current_signal = 'x'
            self.input_var.set(','.join(f'{x:.3f}' for x in self.x_signal))
        else:
            self.current_signal = 'h'
            self.input_var.set(','.join(f'{x:.3f}' for x in self.h_signal))
        self.update_plots()
            
    def on_manual_input(self, event=None):
        """Handle manual signal input"""
        try:
            values = [float(x.strip()) for x in self.input_var.get().split(',') if x.strip()]
            if not values:
                return
                
            # Pad or truncate to current length
            while len(values) < self.n_points:
                values.append(0.0)
            values = values[:self.n_points]
            
            if self.current_signal == 'x':
                self.x_signal = np.array(values)
            else:
                self.h_signal = np.array(values)
                
            self.update_plots()
            
        except ValueError:
            messagebox.showerror("Input Error", "Invalid input. Please enter comma-separated numbers.")
            
    def on_length_change(self):
        """Handle signal length change with real-time updates"""
        try:
            new_length = self.length_var.get()
            
            if new_length < 3:  # Minimum length
                new_length = 3
                self.length_var.set(new_length)
            
            # Store current non-zero values
            x_nonzero = self.x_signal[self.x_signal != 0] if len(self.x_signal) > 0 else np.array([0])
            h_nonzero = self.h_signal[self.h_signal != 0] if len(self.h_signal) > 0 else np.array([0])
            
            # Resize signals intelligently
            if new_length > len(self.x_signal):
                # Pad with zeros
                self.x_signal = np.pad(self.x_signal, (0, new_length - len(self.x_signal)))
                self.h_signal = np.pad(self.h_signal, (0, new_length - len(self.h_signal)))
            else:
                # Truncate but preserve important values
                self.x_signal = np.zeros(new_length)
                self.h_signal = np.zeros(new_length)
                
                # Restore non-zero values up to new length
                self.x_signal[:min(len(x_nonzero), new_length)] = x_nonzero[:min(len(x_nonzero), new_length)]
                self.h_signal[:min(len(h_nonzero), new_length)] = h_nonzero[:min(len(h_nonzero), new_length)]
            
            self.n_points = new_length
            
            # Update status bar indicator
            self.length_indicator.config(text=f"Length: {self.n_points}")
            self.status_var.set(f"Signal length updated to {self.n_points}")
            
            self.on_signal_change()  # Update input field
            self.update_plots()      # Real-time graph update
            
        except (ValueError, tk.TclError):
            # Handle invalid input gracefully
            self.length_var.set(self.n_points)
        
    def on_click(self, event):
        """Handle mouse click for interactive editing"""
        if event.inaxes in [self.ax1, self.ax2] and event.button == 1:
            self.dragging = True
            if event.inaxes == self.ax1:
                self.current_signal = 'x'
                self.signal_var.set("x[n] - Input Signal")
            else:
                self.current_signal = 'h'
                self.signal_var.set("h[n] - Impulse Response")
            self.update_signal_value(event)
            
    def on_drag(self, event):
        """Handle mouse drag for interactive editing"""
        if self.dragging and event.inaxes in [self.ax1, self.ax2]:
            self.update_signal_value(event)
            
    def on_release(self, event):
        """Handle mouse release"""
        self.dragging = False
        if hasattr(self, 'current_signal'):
            self.on_signal_change()
            
    def update_signal_value(self, event):
        """Update signal value at mouse position"""
        if event.xdata is None or event.ydata is None:
            return
            
        n = int(round(event.xdata))
        if self.current_signal == 'x' and 0 <= n < len(self.x_signal):
            self.x_signal[n] = event.ydata
            self.update_plots()
        elif self.current_signal == 'h' and 0 <= n < len(self.h_signal):
            self.h_signal[n] = event.ydata
            self.update_plots()
            
    def open_step_by_step(self):
        """Open step-by-step convolution viewer"""
        try:
            # Import and launch the step-by-step viewer
            from convolution_step_by_step_viewer import StepByStepConvolutionViewer
            step_window = tk.Toplevel(self.root)
            StepByStepConvolutionViewer(step_window, self.x_signal, self.h_signal)
        except ImportError:
            # Fallback: try to run as separate process
            try:
                subprocess.Popen([sys.executable, "convolution_step_by_step_viewer.py"])
            except:
                messagebox.showwarning("Warning", "Step-by-step viewer not found. Please ensure convolution_step_by_step_viewer.py exists.")

def main():
    root = tk.Tk()
    app = ConvolutionViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
