# Ornamental Infill Engine (OIE)

This repository contains the source code for the **Ornamental Infill Engine**, a modular, open-source system designed to generate complex, decorative infill patterns within arbitrary, user-defined shapes.

The primary goal is to create high-quality vector graphics (SVG, DXF) suitable for CNC routing, laser cutting, etching, and engraving applications.

## Key Features

*   **Boundary Constraint:** Uses computational geometry (Shapely) to precisely clip and adapt patterns to any input shape.
*   **Modular Pattern Generation:** An abstract base class allows for easy addition of new pattern types (e.g., Celtic Knots, Islamic Geometric Patterns, Voronoi Diagrams).
*   **Vector Output:** Generates clean, scalable vector graphics (SVG) for direct use in fabrication software.

## Integration with Image2Crafts

The engine is designed to be integrated into the `Image2Crafts` project by calling the main function:

```python
from ornamental_infill_engine import generate_infill

output_path = generate_infill(
    boundary_svg_path="...",  # SVG path data for the shape
    pattern_type="parallel_lines",
    parameters={"spacing": 3.0, "angle_deg": 45.0}
)
```

## Implementation Roadmap

See the full `DEVELOPMENT_ROADMAP.md` for a detailed breakdown of the architecture, algorithm selections, and implementation phases.

## Phase 1: Core Geometry and Clipping

The initial phase focuses on establishing the core geometric pipeline:

1.  **Input Normalization:** Converting SVG path data to a `Shapely` Polygon.
2.  **Raw Pattern Generation:** Creating an unbounded pattern (currently simple parallel lines).
3.  **Clipping:** Using `Shapely.intersection` to constrain the pattern to the boundary.
4.  **Vector Output:** Converting the final geometry to an SVG file.

This foundational work is complete and ready for the next phase of adding complex pattern generators.
