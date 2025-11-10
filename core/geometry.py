# ornamental_infill_engine/core/geometry.py

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
