# Mesh Fairing Add-on for Blender 4.3+

![fairing](https://user-images.githubusercontent.com/8960984/59396054-36e85880-8d44-11e9-873b-d8aa2293b2d5.gif)

This Blender addon provides an alternative smoothing operation with **NEW Blender 4.3+ compatibility and N-Panel integration**. Conventional smoothing has a tendency to cause pinching, bumps, and other undesirable artifacts; however, mesh fairing results in a smooth-as-possible mesh patch.

## ✨ New Features in v1.1.0

- **Blender 4.3+ Compatibility**: Updated for the latest Blender versions
- **N-Panel Integration**: Easy access via the Tools panel (press N)
- **Quick Actions**: Fast access to common operations with saved settings
- **Enhanced UI**: Modern interface with contextual controls
- **Better Property Management**: Improved settings persistence

## Installation

![download](https://user-images.githubusercontent.com/8960984/59553680-ab461600-8f55-11e9-8332-8f617fb40965.png)

1. Download the addon files
2. Open Blender 4.3 or later
3. Go to Edit > Preferences > Add-ons
4. Click "Install..." and select the addon folder
5. Enable "Mesh: Mesh Fairing"
6. Install dependencies (NumPy/SciPy) via the N-panel

## Usage

### N-Panel Access (Recommended)

1. In the 3D Viewport, press `N` to open the side panel
2. Navigate to the "Tool" tab  
3. Find the "Mesh Fairing" panel
4. The panel adapts to your current mode (Edit or Sculpt)

### Traditional Menu Access

Mesh fairing is also available in both *Sculpt* and *Edit* modes via the traditional menus:

![fairing-menus](https://user-images.githubusercontent.com/8960984/59396675-18379100-8d47-11e9-8146-93c5b6ba5077.png)

## Tool Options

Mesh fairing displaces affected vertices to produce a smooth-as-possible mesh patch with respect to a specified continuity constraint.

* **Continuity:** Determines how inner vertices blend with surrounding faces to produce a smooth-as-possible mesh patch

	* **Smooth:** Simple Laplacian smoothing that averages neighboring vertices. Provides traditional mesh smoothing without bulging effects.

	* **Position:** Change in vertex position is minimized.

	* **Tangency:** Change in vertex tangency is minimized.

	* **Curvature:** Change in vertex curvature is minimized.

Mode-specific options also exist to affect the outcome of mesh fairing.

### **Sculpt Mode** ###

* **Invert Mask:** If this option is enabled, mesh fairing is applied to masked vertices; otherwise, only unmasked vertices are affected.

### **Edit Mode** ###

* **Triangulate:** Triangulates affected region to produce higher quality results

## Dependencies

The addon works best with NumPy and SciPy installed. Use the dependency installation buttons in the N-panel, or install manually via Blender's Python console:

```python
import subprocess
import sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy", "scipy"])
```

Blender ships with NumPy, but it is *highly* recommended that users install SciPy. Mesh fairing with the latter is much faster and less prone to crashing.

## Usage Examples

Here are a few examples that demonstrate the usefulness of mesh fairing:

1. Blend between sections of geometry.

	![blend](https://user-images.githubusercontent.com/8960984/59396662-09e97500-8d47-11e9-93a4-eb9d47ef007d.png)

2. Remove surface features.

	![feature-removal](https://user-images.githubusercontent.com/8960984/59397232-11aa1900-8d49-11e9-9fee-d54181dc2e0b.gif)

3. Create interesting shape keys.

	![shape-key](https://user-images.githubusercontent.com/8960984/59396649-00600d00-8d47-11e9-838d-77d3b1a06c81.gif)

## Tips for Best Results

- For best results in Edit mode, select a coherent region of vertices
- In Sculpt mode, use masks to define the area to be smoothed  
- Start with Position continuity and increase to Tangent or Curvature for smoother results
- Enable Triangulate for higher quality results on complex geometry
- Use the Quick Fair button in the N-panel for rapid iteration

## Credits

* **Addon Author:** Brett Fedack

* **David Model:** 3D scan of Michelangelo's David provided by [Scan the World](https://www.myminifactory.com/object/3d-print-head-of-michelangelo-s-david-52645) initiative

* **Monkey Model:** Suzanne is Blender's mascot who we've all come to know and love.

* **Other:** Special thanks to Jane Tournois whose mesh fairing implementation for [CGAL](https://github.com/CGAL/cgal/blob/master/Polygon_mesh_processing/include/CGAL/Polygon_mesh_processing/internal/fair_impl.h) proved highly instructive in designing this addon
