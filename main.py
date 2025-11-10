# ornamental_infill_engine/main.py

import os
from typing import Dict, Any
from shapely.geometry import Polygon
from ornamental_infill_engine.core.geometry import normalize_boundary, clip_pattern_to_boundary
from ornamental_infill_engine.core.output import geometry_to_svg
from ornamental_infill_engine.patterns.base import ParallelLineGenerator, PatternGenerator

# A simple registry to hold all available pattern generators
PATTERN_REGISTRY: Dict[str, PatternGenerator] = {
    "parallel_lines": ParallelLineGenerator(),
    # Future generators will be added here:
    # "voronoi": VoronoiGenerator(),
    # "celtic_knot": CelticKnotGenerator(),
    # "igp": IGPGenerator(),
}

def generate_infill(
    boundary_svg_path: str, 
    pattern_type: str, 
    parameters: Dict[str, Any],
    output_file: str = "infill_pattern.svg"
) -> str:
    """
    The main function to generate a decorative infill pattern.
    
    :param boundary_svg_path: The SVG path data string defining the boundary shape.
    :param pattern_type: The key for the desired pattern generator (e.g., "parallel_lines").
    :param parameters: A dictionary of pattern-specific parameters.
    :param output_file: The path to save the resulting SVG file.
    :return: The absolute path to the generated SVG file.
    """
    
    # 1. Input Processing and Normalization
    try:
        boundary_shape: Polygon = normalize_boundary(boundary_svg_path)
    except Exception as e:
        raise ValueError(f"Error normalizing boundary shape: {e}")

    # 2. Pattern Selection and Parameter Merging
    if pattern_type not in PATTERN_REGISTRY:
        raise ValueError(f"Unknown pattern type: {pattern_type}. Available types: {list(PATTERN_REGISTRY.keys())}")
        
    generator = PATTERN_REGISTRY[pattern_type]
    final_params = generator.get_parameters(parameters)
    
    # 3. Raw Pattern Generation
    bbox = boundary_shape.bounds
    raw_pattern = generator.generate(bbox, final_params)
    
    # 4. Boundary Constraint (Clipping)
    clipped_geometry = clip_pattern_to_boundary(raw_pattern, boundary_shape)
    
    # 5. Vector Output
    geometry_to_svg(clipped_geometry, output_file, line_width=final_params.get("line_width", 0.5))
    
    return os.path.abspath(output_file)

if __name__ == '__main__':
    # Example usage for testing Phase 1 functionality
    
    # 1. Define a complex boundary (e.g., a simple square for now)
    # In a real scenario, this would be a complex SVG path from Image2Crafts
    knife_handle_svg_path = "M 10 10 L 100 10 L 100 100 L 10 100 Z" 
    
    # 2. Define pattern parameters
    params = {
        "spacing": 3.0,
        "angle_deg": 45.0,
        "line_width": 0.2
    }
    
    try:
        output_path = generate_infill(
            boundary_svg_path=knife_handle_svg_path,
            pattern_type="parallel_lines",
            parameters=params,
            output_file="phase1_infill_test.svg"
        )
        print(f"\n--- SUCCESS ---")
        print(f"Test pattern generated and saved to: {output_path}")
        print(f"Open the SVG file to view the result.")
        
    except Exception as e:
        print(f"\n--- FAILURE ---")
        print(f"An error occurred during generation: {e}")
