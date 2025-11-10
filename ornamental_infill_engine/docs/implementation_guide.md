# Implementation Guide: Core Geometry and Clipping (Phase 1)

This guide details the foundational code structure and implementation for the core geometry processing and boundary clipping, which is essential for the **Ornamental Infill Engine (OIE)**.

## 1. Required Dependencies

The following Python packages are necessary for handling geometric operations and vector output.

```bash
# Install required packages
pip3 install shapely svgwrite
```

## 2. Core Geometry Utility (`core/geometry.py`)

This module will handle the conversion of input data (like SVG path strings) into `Shapely` objects and provide utility functions for geometric operations.

```python
# core/geometry.py

from shapely.geometry import Polygon, MultiLineString, LineString, GeometryCollection
from typing import Union, List

# Type alias for clarity
ShapelyGeometry = Union[Polygon, MultiLineString, LineString, GeometryCollection]

def normalize_boundary(svg_path_data: str) -> Polygon:
    """
    Converts an SVG path string into a Shapely Polygon object.
    
    NOTE: A full implementation would require an SVG path parser (e.g., svgpathtools)
    to convert the path data into coordinates. For this guide, we assume a simple
    rectangular boundary for demonstration.
    """
    # Placeholder for a real SVG path parser
    # In a real implementation, this would parse the 'd' attribute of an SVG path.
    
    # Example: A simple square boundary
    coords = [(0, 0), (100, 0), (100, 100), (0, 100), (0, 0)]
    return Polygon(coords)

def generate_raw_parallel_lines(bbox: tuple, spacing: float, angle_deg: float) -> MultiLineString:
    """
    Generates a simple, unbounded pattern of parallel lines covering a bounding box.
    This serves as a simple test case for the clipping function.
    
    :param bbox: (minx, miny, maxx, maxy) of the area to cover.
    :param spacing: Distance between lines.
    :param angle_deg: Rotation angle in degrees.
    :return: A Shapely MultiLineString of the raw pattern.
    """
    minx, miny, maxx, maxy = bbox
    lines = []
    
    # Simplified generation: just horizontal lines for now
    y = miny - spacing
    while y < maxy + spacing:
        lines.append(LineString([(minx - 10, y), (maxx + 10, y)]))
        y += spacing
        
    # TODO: Implement rotation logic using shapely.affinity.rotate
    
    return MultiLineString(lines)

def clip_pattern_to_boundary(pattern: ShapelyGeometry, boundary: Polygon) -> ShapelyGeometry:
    """
    Performs the core boundary constraint using Shapely's intersection.
    
    :param pattern: The raw pattern geometry (MultiLineString, MultiPolygon, etc.).
    :param boundary: The Polygon defining the shape to fill.
    :return: The clipped geometry.
    """
    # The intersection operation is the heart of the boundary constraint
    clipped_geometry = pattern.intersection(boundary)
    
    # The result can be a GeometryCollection, MultiLineString, or MultiPolygon
    return clipped_geometry
```

## 3. Vector Output Utility (`core/output.py`)

This module handles the conversion of `Shapely` geometry objects into a standard vector format, specifically SVG for web and CNC preview.

```python
# core/output.py

import svgwrite
from shapely.geometry import Polygon, MultiLineString, LineString, GeometryCollection
from typing import Union

def geometry_to_svg(geometry: Union[Polygon, MultiLineString, LineString, GeometryCollection], 
                    output_path: str, 
                    line_color: str = 'black', 
                    line_width: float = 0.5):
    """
    Converts Shapely geometry into an SVG file.
    """
    # Determine the bounding box for the SVG viewbox
    minx, miny, maxx, maxy = geometry.bounds
    width = maxx - minx
    height = maxy - miny
    
    dwg = svgwrite.Drawing(output_path, size=(f'{width}mm', f'{height}mm'), profile='tiny')
    # Set the viewbox to ensure the geometry fits
    dwg.viewbox(minx, miny, width, height)

    def add_geometry(geom):
        if geom.geom_type == 'LineString':
            points = [(x, y) for x, y in geom.coords]
            dwg.add(dwg.polyline(points, 
                                 stroke=line_color, 
                                 stroke_width=line_width, 
                                 fill='none', 
                                 stroke_linecap='round'))
        elif geom.geom_type == 'MultiLineString':
            for line in geom.geoms:
                add_geometry(line)
        elif geom.geom_type == 'Polygon':
            # For infill, we typically only care about the lines, but we can draw the boundary
            # For a filled pattern, we would use dwg.polygon
            pass # For this phase, we focus on line patterns
        elif geom.geom_type == 'GeometryCollection':
            for g in geom.geoms:
                add_geometry(g)

    add_geometry(geometry)
    dwg.save()
    print(f"SVG saved to {output_path}")

# Example usage (to be run in a test script)
# if __name__ == '__main__':
#     # 1. Define a boundary (e.g., a simple triangle)
#     boundary = Polygon([(10, 10), (90, 10), (50, 90), (10, 10)])
#     
#     # 2. Generate a raw pattern
#     bbox = boundary.bounds
#     raw_pattern = generate_raw_parallel_lines(bbox, spacing=5.0, angle_deg=0)
#     
#     # 3. Clip
#     clipped = clip_pattern_to_boundary(raw_pattern, boundary)
#     
#     # 4. Output
#     geometry_to_svg(clipped, 'clipped_infill_example.svg')
```

## 4. Test Script (`test_phase1.py`)

A simple script to demonstrate the core functionality.

```python
# test_phase1.py

import sys
import os

# Add the current directory to the path to import core modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from shapely.geometry import Polygon
from core.geometry import generate_raw_parallel_lines, clip_pattern_to_boundary
from core.output import geometry_to_svg

def run_test():
    print("--- Running Phase 1 Core Geometry and Clipping Test ---")
    
    # 1. Define a boundary (a simple square)
    # In a real scenario, this would come from the Input Processor
    boundary_coords = [(20, 20), (80, 20), (80, 80), (20, 80), (20, 20)]
    boundary_shape = Polygon(boundary_coords)
    print(f"Boundary defined: {boundary_shape.geom_type}")
    
    # 2. Generate a raw pattern (horizontal lines)
    bbox = boundary_shape.bounds
    raw_pattern = generate_raw_parallel_lines(bbox, spacing=4.0, angle_deg=0)
    print(f"Raw pattern generated: {raw_pattern.geom_type} with {len(raw_pattern.geoms)} lines")
    
    # 3. Clip the pattern to the boundary
    clipped_geometry = clip_pattern_to_boundary(raw_pattern, boundary_shape)
    print(f"Clipped geometry type: {clipped_geometry.geom_type}")
    
    # 4. Output the result to an SVG file
    output_file = 'clipped_infill_example.svg'
    geometry_to_svg(clipped_geometry, output_file, line_width=0.3)
    print(f"Successfully generated infill pattern: {output_file}")

if __name__ == '__main__':
    # Ensure the core directory exists before running
    os.makedirs('core', exist_ok=True)
    
    # NOTE: In a real environment, the core files would be written first.
    # For this guide, we assume they are present.
    
    # To run this test, you would need to execute:
    # python3 test_phase1.py
    
    # For the purpose of this roadmap, this file serves as the guide.
    pass
```
