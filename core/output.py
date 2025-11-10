# ornamental_infill_engine/core/output.py

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
    
    # Add a small buffer for better visualization
    buffer = 5
    minx -= buffer
    miny -= buffer
    width += 2 * buffer
    height += 2 * buffer
    
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
        elif geom.geom_type == 'GeometryCollection':
            for g in geom.geoms:
                add_geometry(g)

    add_geometry(geometry)
    dwg.save()
    print(f"SVG saved to {output_path}")
