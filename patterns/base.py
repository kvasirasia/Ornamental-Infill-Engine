# ornamental_infill_engine/patterns/base.py

from abc import ABC, abstractmethod
from typing import Dict, Any, Union
from shapely.geometry import GeometryCollection, MultiLineString, LineString
from shapely import affinity

class PatternGenerator(ABC):
    """
    Abstract base class for all decorative infill pattern generators.
    Defines the required interface for the Ornamental Infill Engine (OIE).
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """A human-readable name for the pattern."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """A brief description of the pattern and its parameters."""
        pass

    @property
    @abstractmethod
    def default_parameters(self) -> Dict[str, Any]:
        """A dictionary of default parameters for the generator."""
        pass

    @abstractmethod
    def generate(self, bbox: tuple, parameters: Dict[str, Any]) -> GeometryCollection:
        """
        Generates the raw, unbounded pattern geometry that covers the given bounding box.
        
        :param bbox: The bounding box (minx, miny, maxx, maxy) of the area to cover.
        :param parameters: A dictionary of user-defined parameters for the pattern.
        :return: A Shapely GeometryCollection (e.g., MultiLineString) representing the raw pattern.
        """
        pass

    def get_parameters(self, user_params: Dict[str, Any]) -> Dict[str, Any]:
        """Merges user parameters with default parameters."""
        params = self.default_parameters.copy()
        params.update(user_params)
        return params

# A concrete implementation of a simple pattern for Phase 1 testing
class ParallelLineGenerator(PatternGenerator):
    @property
    def name(self) -> str:
        return "Parallel Lines"

    @property
    def description(self) -> str:
        return "Simple parallel lines pattern, useful for testing and basic infill."

    @property
    def default_parameters(self) -> Dict[str, Any]:
        return {"spacing": 5.0, "angle_deg": 0.0}

    def generate(self, bbox: tuple, parameters: Dict[str, Any]) -> GeometryCollection:
        minx, miny, maxx, maxy = bbox
        spacing = parameters.get("spacing", 5.0)
        angle_deg = parameters.get("angle_deg", 0.0)
        
        lines = []
        # Determine the range for line generation based on the bounding box
        # We generate lines along the y-axis and then rotate them
        y = miny - max(maxx - minx, maxy - miny) # Start well outside the box
        end_y = maxy + max(maxx - minx, maxy - miny) # End well outside the box
        
        # Line length must be long enough to cover the rotated bounding box
        line_length = 2 * max(maxx - minx, maxy - miny)
        center_x = (minx + maxx) / 2
        
        while y < end_y:
            # Create a horizontal line segment centered at center_x
            line = LineString([(center_x - line_length / 2, y), (center_x + line_length / 2, y)])
            lines.append(line)
            y += spacing
            
        raw_pattern = MultiLineString(lines)
        
        # Apply rotation around the center of the bounding box
        if angle_deg != 0.0:
            center = ((minx + maxx) / 2, (miny + maxy) / 2)
            raw_pattern = affinity.rotate(raw_pattern, angle_deg, origin=center)
            
        return raw_pattern
