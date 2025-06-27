# DSP Convolution Visualization Suite

A comprehensive, modular toolkit for interactive convolution visualization and education. This project demonstrates clean software architecture with separated concerns for maintainability and reusability.

## 🏗️ Modular Architecture

This project has been refactored into a clean, modular architecture that separates concerns:

### Core Modules

- **`convolution_logic.py`** - Pure mathematical operations and signal generation
- **`visualization.py`** - All plotting and visualization functionality  
- **`animation_controller.py`** - Animation state management and timing
- **`ui_components.py`** - Reusable UI components and styling

### Applications

- **`main_launcher.py`** - Unified launcher with architecture overview
- **`convolution_viewer_refactored.py`** - Interactive real-time convolution viewer
- **`convolution_step_by_step_viewer_refactored.py`** - Animated step-by-step visualization
- **`example_modular_usage.py`** - Demonstrations of using components independently

### Legacy Applications (Original)

- **`convolution_viewer_enhanced.py`** - Original monolithic viewer
- **`convolution_step_by_step_viewer_enhanced.py`** - Original step-by-step viewer

## 🚀 Quick Start

### Option 1: Use the Main Launcher (Recommended)
```bash
python main_launcher.py
```

### Option 2: Run Applications Directly
```bash
# Real-time interactive viewer
python convolution_viewer_refactored.py

# Step-by-step animation viewer  
python convolution_step_by_step_viewer_refactored.py

# See modular usage examples
python example_modular_usage.py
```

## ✨ Features

### Real-Time Convolution Viewer
- **Interactive Editing**: Click and drag to modify signal values
- **Signal Generation**: Built-in generators for common signal types
- **Live Updates**: Real-time convolution computation and visualization
- **File Operations**: Save/load signal configurations
- **Export**: High-quality plot export

### Step-by-Step Animation Viewer  
- **Educational Animation**: Visual step-by-step convolution computation
- **Animation Controls**: Play, pause, step forward/backward, speed control
- **Mathematical Display**: Shows equations and intermediate calculations
- **Export**: Save animations as GIF files
- **Progress Tracking**: Progress bar and step information

### Modular Components
- **Pure Logic**: Mathematical operations independent of UI
- **Reusable Visualization**: Consistent plotting across applications
- **Flexible Animation**: State management for any animation needs
- **UI Components**: Styled, reusable interface elements

## 🎯 Educational Value

This suite is designed for learning:

1. **Convolution Concepts**: Visual understanding of convolution mathematics
2. **Signal Processing**: Hands-on experience with signals and systems
3. **Software Architecture**: Demonstrates modular design principles
4. **Interactive Learning**: Engage with concepts through visualization

## 📚 Architecture Benefits

### Before (Monolithic)
- All code mixed in large classes
- Logic coupled with UI code  
- Hard to test individual components
- Difficult to reuse functionality

### After (Modular)
- Clear separation of concerns
- Pure functions easily testable
- Components reusable across applications
- Maintainable and extensible codebase

## 🛠️ Installation

```bash
# Clone repository
git clone <repository-url>
cd DSP-3-Convolution-and-its-properties

# Install dependencies
pip install -r requirements.txt

# Run main launcher
python main_launcher.py
```

## 📊 Usage Examples

### Using Components Independently

```python
from convolution_logic import ConvolutionCalculator, SignalGenerator

# Create signals
x = SignalGenerator.rectangular(10, 5, 1.0)
h = SignalGenerator.exponential(8, 0.8)

# Calculate convolution
calc = ConvolutionCalculator()
calc.set_signals(x, h)
step_data = calc.compute_step(3)

print(f"Step 3: {step_data['equation']}")
```

### Custom Visualization

```python
from visualization import ConvolutionPlotter
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
plotter = ConvolutionPlotter(fig)
plotter.plot_input_signal(ax, signal, "My Signal")
plt.show()
```

## 🎨 Customization

The modular architecture makes customization easy:

- **New Signal Types**: Add to `SignalGenerator` class
- **Different Visualizations**: Extend `ConvolutionPlotter`
- **Custom UI**: Use components from `ui_components`
- **Animation Styles**: Modify `AnimationController` behavior

## 🔬 Testing

Components can be tested independently:

```python
# Test signal generation
signal = SignalGenerator.impulse(10, 3)
assert signal[3] == 1.0 and sum(signal) == 1.0

# Test convolution properties
from convolution_logic import ConvolutionProperties
result = ConvolutionProperties.verify_linearity(x1, x2, h)
assert result['is_linear'] == True
```

## 📁 Project Structure

```
DSP-3-Convolution-and-its-properties/
├── convolution_logic.py              # Core mathematical operations
├── visualization.py                  # Plotting and visualization
├── animation_controller.py           # Animation state management  
├── ui_components.py                  # Reusable UI components
├── main_launcher.py                  # Main application launcher
├── convolution_viewer_refactored.py          # Interactive viewer
├── convolution_step_by_step_viewer_refactored.py  # Step-by-step viewer
├── example_modular_usage.py          # Usage examples
├── requirements.txt                  # Dependencies
└── README.md                        # This file
```

## 🤝 Contributing

The modular architecture makes contributions easier:

1. **Bug Fixes**: Issues are isolated to specific modules
2. **New Features**: Add to appropriate module or create new ones
3. **Testing**: Each module can be tested independently
4. **Documentation**: Clear module boundaries make documentation easier

## 📝 Legacy Applications

The original enhanced applications are still available:
- **Four-panel layout**:
  - Input signal x[k]
  - Flipped and shifted h[n-k] 
  - Point-wise product x[k] × h[n-k]
  - Progressive convolution output y[n]
- **Interactive controls**: Play/Pause, step navigation, variable speed control
- **Mathematical equations** showing current computation
- **Progress tracking** with visual progress bar
- **Export animation** as GIF
- **Clean, optimized layout** for better understanding

### Original Versions (Legacy)
- `convolution_viewer.py` - Original basic version
- `convolution_step_by_step_viewer.py` - Original animation version

## Quick Start

### Option 1: Run Enhanced Viewer (Recommended)
```bash
python run_enhanced_viewer.py
```

### Option 2: Direct Launch
```bash
# Enhanced main viewer
python convolution_viewer_enhanced.py

# Enhanced step-by-step animation
python convolution_step_by_step_viewer_enhanced.py
```

## Installation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the application** using any of the methods above.

## What's New in Enhanced Version

### ✅ Optimizations
- **Streamlined UI** with better space utilization
- **Optimized for 100% display scaling** (1400x900 main, 1500x950 animation)
- **Removed non-functional code** and placeholder features
- **Clean, professional styling** with consistent blue theme
- **Better performance** with simplified plot updates

### ✅ Core Features Only
- **Focused functionality** - only working features included
- **Simplified navigation** between main viewer and animation
- **Essential signal operations** that actually work
- **Reliable file I/O** with proper error handling
- **Interactive editing** that responds immediately

### ✅ Improved User Experience
- **Clearer visual hierarchy** with proper font sizing
- **Better feedback** with status updates and progress indicators
- **Intuitive controls** with recognizable icons and labels
- **Responsive interface** that updates in real-time
- **Educational focus** with clear mathematical displays

## Usage Tips

1. **Start with the main viewer** to set up your signals
2. **Use preset templates** for common signal types
3. **Click and drag** on plots to edit signal values interactively
4. **Launch animation** to see step-by-step convolution process
5. **Adjust animation speed** to match your learning pace
6. **Save sessions** to preserve your work
7. **Export plots** for reports or presentations

## Usage

### Interactive Editing
- **Click and drag** on the x[n] or h[n] plots to modify signal values
- The convolution y[n] = x[n] * h[n] updates automatically in real-time

### Signal Controls
1. **Select Active Signal**: Choose between x[n] and h[n] for editing
2. **Signal Length**: Adjust the length of both signals (5-30 samples)
3. **Preset Signals**: Apply common signal types:
   - **Impulse δ[n]**: Unit impulse at n=0
   - **Step u[n]**: Unit step function
   - **Exponential**: Decaying exponential sequence
   - **Sinusoidal**: Sine wave sequence
   - **Triangular**: Triangular pulse
   - **Random**: Random values
   - **Clear**: Zero signal

### Manual Input
- Enter comma-separated values in the input field
- Press Enter or click "Apply" to update the signal
- Values are automatically padded or truncated to match signal length

### File Operations (Advanced Version)
- **Save Signals**: Export current x[n] and h[n] to JSON file
- **Load Signals**: Import previously saved signals

### Step-by-Step Convolution Animation
1. **Launch from main viewer**: Click the "🎬 Step-by-Step Convolution Animation" button
2. **Navigation Controls**:
   - **Play/Pause**: Start or stop automatic animation
   - **Next/Previous**: Manual step-by-step navigation
   - **Reset**: Return to the beginning
   - **Speed Control**: Adjust animation speed (0.2x to 3.0x)

3. **Understanding the Animation**:
   - **Top plot**: Original input signal x[n]
   - **Middle left**: Original impulse response h[n]
   - **Middle right**: Flipped and shifted h[n-k] (red stems)
   - **Third plot**: Point-wise multiplication x[k] × h[n-k] (green stems)
   - **Bottom plot**: Progressive convolution output y[n] (purple completed, red current)

4. **Mathematical Insight**:
   - Watch how h[n] is flipped to become h[-k]
   - See h[-k] sliding to position h[n-k] for each output sample
   - Observe point-wise multiplication at each position
   - See the sum of products forming each output sample y[n]

## Mathematical Background

The discrete convolution operation is defined as:

```
y[n] = x[n] * h[n] = Σ x[k] · h[n-k]
                     k
```

Where:
- `x[n]` is the input signal
- `h[n]` is the impulse response
- `y[n]` is the convolution output
- The output length is `len(x) + len(h) - 1`

## Key Features for DSP Learning

1. **Real-time Visualization**: See how changes in input signals immediately affect the convolution output
2. **Interactive Learning**: Experiment with different signal types and observe their convolution properties
3. **Signal Properties**: Monitor energy, amplitude, and other characteristics
4. **Length Relationships**: Understand how convolution affects signal length

## Examples

### Basic Convolution Example
1. Set x[n] to a step function: `[1, 1, 1, 0, 0, ...]`
2. Set h[n] to an exponential: `[1, 0.5, 0.25, 0.125, ...]`
3. Observe the smoothed output in y[n]

### System Response Analysis
1. Set x[n] to an impulse: `[1, 0, 0, 0, ...]`
2. Set h[n] to your system's impulse response
3. The output y[n] shows the system's impulse response

### Filter Design
1. Design h[n] as a simple moving average filter: `[0.33, 0.33, 0.33, 0, ...]`
2. Apply to noisy input signal x[n]
3. Observe the smoothing effect in y[n]

### Convolution Animation Example
1. Set x[n] to `[1, 2, 1]` and h[n] to `[0.5, 0.3, 0.2]`
2. Click "Step-by-Step Convolution Animation"
3. Watch how:
   - h[n] flips to h[-k]
   - h[-k] slides from position to position
   - Each y[n] is computed as the sum of point-wise products
   - The output length becomes len(x) + len(h) - 1 = 5

## Troubleshooting

- **Import Errors**: Ensure numpy and matplotlib are installed
- **Display Issues**: Try running with different backends if plots don't appear
- **Performance**: For large signals, consider reducing the update frequency

## Requirements

- Python 3.7+
- NumPy 1.21+
- Matplotlib 3.5+
- Tkinter (usually included with Python)

## License

This project is for educational purposes in Digital Signal Processing.
