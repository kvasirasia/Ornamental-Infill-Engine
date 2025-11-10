# Comprehensive Development Roadmap: Decorative Infill Pattern Generator

**Goal:** To develop an open-source, modular system for generating complex, decorative infill patterns within arbitrary, user-defined shapes for CNC, laser, and etching applications, with a clear integration path into the `Image2Crafts` project.

**Author:** Manus AI
**Date:** November 10, 2025

---

## 1. System Architecture

The proposed system, tentatively named **"Ornamental Infill Engine" (OIE)**, will follow a modular, pipeline-based architecture to ensure flexibility, extensibility, and clear separation of concerns. The core components will be implemented in Python, leveraging its strong ecosystem for computational geometry and vector graphics.

| Component | Function | Key Technology/Library |
| :--- | :--- | :--- |
| **Input Processor** | Handles the ingestion and normalization of the boundary shape (the "mask") and user parameters. | `Shapely`, `SVG` parsing library (e.g., `svgwrite` or `svgpathtools`) |
| **Pattern Generator** | The core module responsible for generating the raw, unbounded pattern based on the selected algorithm. | Custom Python modules for each pattern type (e.g., `LSystemGenerator`, `IGPGenerator`, `KnotGenerator`) |
| **Boundary Constrainer** | Clips, warps, and adapts the raw pattern to fit precisely within the boundary shape. This is the most critical component for a high-quality result. | `Shapely` (for clipping/boolean operations), Custom implementation for pattern-to-boundary alignment and warping. |
| **Vector Output** | Converts the final constrained pattern geometry into a standard vector format suitable for CNC/laser applications. | `svgwrite` (for SVG output), `ezdxf` (for DXF output) |
| **API/CLI Interface** | Provides a programmatic and command-line interface for the `Image2Crafts` integration and standalone use. | `FastAPI` (for API), `argparse` (for CLI) |

### Data Flow Pipeline

1.  **Input:** User provides a **Boundary Shape** (e.g., SVG path data for a knife handle) and **Pattern Parameters** (e.g., Pattern Type: Celtic Knot, Scale: 5mm, Rotation: 0°).
2.  **Normalization:** The Boundary Shape is converted into a canonical geometric object (e.g., a `Shapely` Polygon).
3.  **Generation:** The **Pattern Generator** creates a large, tiled, or procedurally generated **Raw Pattern** that covers the bounding box of the shape.
4.  **Constraint:** The **Boundary Constrainer** performs two main steps:
    *   **Clipping:** Boolean intersection of the Raw Pattern with the Boundary Shape (`Shapely.intersection`).
    *   **Adaptation/Warping (Optional):** Adjusts the pattern near the boundary to minimize truncated elements (e.g., scaling the outermost row of tiles).
5.  **Output:** The final constrained geometry is exported as a vector file (SVG/DXF).

---

## 2. Algorithm Selections and Variations

The system will support a variety of pattern types, each requiring a distinct generation algorithm.

| Pattern Type | Algorithm Selection | Key Implementation Details |
| :--- | :--- | :--- |
| **Islamic Geometric Patterns (IGP)** | **Construction-based Tiling:** Use a grid of points and compass/straightedge rules to generate the underlying star/rosette geometry. | Focus on generating the "tiling" geometry (lines/arcs) rather than filled shapes. Requires a library for precise geometric construction (e.g., `sympy` for symbolic geometry, or a custom class for high-precision floating-point arithmetic). |
| **Celtic Knots / Gaelic Knots** | **Graph Theory / Tiling:** Represent the knot as a path on a grid, where each grid cell is a specific knot tile (e.g., a crossing or a turn). | Implement a **Knot Tile Set** and a **Grid Traversal Algorithm** to generate the path. The final output is a set of parallel curves (the "strands"). |
| **Escher-like Tessellations** | **Symmetry-based Tile Transformation:** Start with a simple polygon (square, triangle) and apply paired, complementary transformations (translation, rotation, glide reflection) to its edges to create a complex, interlocking tile. | Requires a **Tile Editor** class to manage edge transformations and a **Tiling Engine** to place the transformed tile across the plane. |
| **Voronoi Diagrams** | **Point-based Partitioning:** Generate a set of random or structured seed points, then compute the Voronoi diagram. | Use a library like `scipy.spatial.Voronoi` for the initial diagram, then use `Shapely` to clip the Voronoi cells to the boundary. The infill can be the cell boundaries or a sub-pattern within each cell. |
| **L-Systems / Fractals** | **Recursive String Rewriting:** Use a set of production rules to generate a string, which is then interpreted geometrically (e.g., "F" means draw forward, "+" means turn right). | Implement a **Rule Parser** and a **Turtle Graphics Engine** to convert the generated string into a vector path. This is ideal for tree-like or self-similar patterns. |
| **Damascus Knife Patterns** | **Procedural Simulation:** Model the pattern as a layered texture. For a "Twist" pattern, the texture coordinates are warped based on a spiral function. For "Ladder" or "Raindrop," use simple geometric repetition and perturbation. | Generate a high-resolution 2D texture (or vector field) and use it to define the infill lines/etching areas. This is a texture-based approach that needs vectorization for CNC. |

---

## 3. Shape Boundary Detection and Constraint Handling

The key challenge is ensuring the pattern interacts aesthetically and geometrically correctly with the boundary.

### 3.1. Boundary Detection

The input shape will be parsed into a `Shapely` Polygon object. This object inherently provides:
*   **Boundary:** The exterior ring of the polygon.
*   **Holes:** Any interior rings (e.g., a donut shape).
*   **Bounding Box:** The minimum and maximum coordinates for the pattern generation area.

### 3.2. Constraint Handling: Clipping

The primary constraint handling method is **Boolean Clipping**:

```python
from shapely.geometry import Polygon, MultiLineString

# 1. Normalize Boundary
boundary_shape = Polygon(...) # The user's shape

# 2. Generate Raw Pattern (as a Shapely MultiLineString or MultiPolygon)
raw_pattern = MultiLineString(...) 

# 3. Clip the Pattern
constrained_pattern = raw_pattern.intersection(boundary_shape)

# 4. Output
# constrained_pattern is the final geometry, ready for vector export.
```

### 3.3. Constraint Handling: Boundary Adaptation (Advanced)

For patterns like tessellations or knots, simply clipping can result in many small, truncated, and aesthetically poor elements along the edge. An advanced technique is **Boundary-Aware Warping**:

1.  **Distance Field:** Compute a distance field from the boundary inwards.
2.  **Warping:** Apply a non-linear transformation to the pattern's coordinates based on the distance field, causing the pattern to "stretch" or "compress" as it approaches the boundary.
3.  **Tiling Adjustment:** For grid-based patterns, adjust the scale of the outermost row of tiles so that the tile edge aligns perfectly with the boundary, as suggested in academic literature [1].

---

## 4. Code Structure and Implementation Phases

The project will be structured as a Python package, `ornamental_infill_engine`.

### Proposed Directory Structure

```
ornamental_infill_engine/
├── __init__.py
├── cli.py             # Command-line interface
├── core/
│   ├── geometry.py    # Shapely-based utilities, normalization, clipping
│   └── output.py      # SVG/DXF export functions
├── patterns/
│   ├── __init__.py
│   ├── base.py        # Abstract base class for all generators
│   ├── igp.py         # Islamic Geometric Pattern generator
│   ├── celtic.py      # Celtic Knot generator
│   ├── escher.py      # Escher Tessellation generator
│   └── voronoi.py     # Voronoi/Fractal generator
└── boundary/
    ├── constrainer.py # Clipping and advanced adaptation logic
    └── distance_field.py # Utility for distance field calculation
```

### Implementation Phases

| Phase ID | Focus Area | Deliverable | Required Libraries |
| :--- | :--- | :--- | :--- |
| **Phase 1** | **Core Geometry & Clipping** | A functional script that takes a simple square and a set of parallel lines, clips the lines to the square, and outputs an SVG. Establishes the `core/geometry.py` and `core/output.py` foundation. | `Shapely`, `svgwrite` |
| **Phase 2** | **First Pattern Generator (Voronoi)** | Implement the `patterns/voronoi.py` generator. This is the simplest to constrain as it's point-based. Integrate it with the Phase 1 clipping core. | `scipy.spatial` |
| **Phase 3** | **Complex Pattern Generator (IGP/Celtic)** | Implement the `patterns/igp.py` or `patterns/celtic.py` module. Focus on generating the raw, unbounded pattern correctly. | Custom geometric classes |
| **Phase 4** | **Advanced Constraint Handling** | Implement the **Boundary Adaptation** logic in `boundary/constrainer.py`. Test with a complex, non-convex shape (e.g., a knife handle). | Custom distance field calculation |
| **Phase 5** | **Image2Crafts Integration** | Create the `cli.py` and a simple `FastAPI` wrapper to expose the core functionality for seamless integration. | `FastAPI`, `uvicorn` |

---

## 5. Integration Strategy for Image2Crafts

The integration with `Image2Crafts` will be achieved by exposing the **Ornamental Infill Engine (OIE)** as a microservice or a callable library function.

### Strategy A: Microservice (Recommended for Scalability)

1.  **OIE Deployment:** Deploy the OIE as a standalone service (e.g., using Docker) with a simple REST API endpoint: `/api/generate_infill`.
2.  **Request:** `Image2Crafts` sends a JSON payload to the OIE service:
    ```json
    {
      "boundary_svg_path": "M 10 10 L 100 10 L 100 100 L 10 100 Z",
      "pattern_type": "celtic_knot",
      "parameters": {
        "scale": 5,
        "line_width": 0.5,
        "rotation": 45
      }
    }
    ```
3.  **Response:** The OIE service returns the final infill pattern as an SVG string.
    ```json
    {
      "status": "success",
      "infill_svg": "<svg>...</svg>"
    }
    ```

### Strategy B: Direct Library Integration (Recommended for Initial Development)

1.  Install the `ornamental_infill_engine` package directly into the `Image2Crafts` environment.
2.  Call the main generation function from within the `Image2Crafts` codebase:

```python
from ornamental_infill_engine import generate_infill

# Get the boundary shape from Image2Crafts's existing geometry processing
boundary_data = image2crafts_geometry_processor.get_shape_data()

# Call the new engine
infill_svg = generate_infill(
    boundary_svg_path=boundary_data,
    pattern_type="islamic_geometric",
    parameters={"scale": 10, "rosette_type": "8-fold"}
)

# Use the resulting SVG in the Image2Crafts output
```

---

## References

[1] Chen, M., et al. (2019). *Manufacturable pattern collage along a boundary*. The Visual Computer. [link.springer.com/content/pdf/10.1007/s41095-019-0143-2.pdf](https://link.springer.com/content/pdf/10.1007/s41095-019-0143-2.pdf)
[2] Lu, J., et al. (2014). *Decobrush: Drawing structured decorative patterns by example*. ACM Transactions on Graphics. [dl.acm.org/doi/abs/10.1145/2601097.2601190](https://dl.acm.org/doi/abs/10.1145/2601097.2601190)
[3] yahya-ben. *Islamic_geometric_patterns_app*. GitHub. [github.com/yahya-ben/Islamic_geometric_patterns_app](https://github.com/yahya-ben/Islamic_geometric_patterns_app)
[4] codeplea. *celtic_knots*. GitHub. [github.com/codeplea/celtic_knots](https://github.com/codeplea/celtic_knots)
[5] Maker.js. *Create parametric CNC drawings using JavaScript*. [maker.js.org/](https://maker.js.org/)
[6] Shapely. *Geometric objects for Python*. [pypi.org/project/Shapely/](https://pypi.org/project/Shapely/)
[7] SciPy. *scipy.spatial.Voronoi*. [docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Voronoi.html](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Voronoi.html)
[8] ezdxf. *DXF R12-R2025 library for Python*. [pypi.org/project/ezdxf/](https://pypi.org/project/ezdxf/)
