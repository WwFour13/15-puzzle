# Prompt to Gemini 3.8 Flash:
"""
in [coloring.py](file;file:///c%3A/dev/15-puzzle/coloring.py) , 
make a func to interpolate between two colors with finite steps, 
(in this format "#f0f0f0"), cache result with lru cache
def interpolate(start_color, end_color, total_steps, desired_step)
"""




from functools import lru_cache


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.strip().lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: {hex_color}")
    return (
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16),
    )


@lru_cache(maxsize=None)
def interpolate(start_color: str, end_color: str, total_steps: int, desired_step: int) -> str:
    """
    Interpolate between two hex colors across finite steps.

    Args:
        start_color: Starting color as a hex string (e.g., "#f0f0f0").
        end_color: Ending color as a hex string (e.g., "#df9809").
        total_steps: Total number of steps between start and end.
        desired_step: The target step to interpolate to (from 0 to total_steps).

    Returns:
        The interpolated hex color string in format "#rrggbb".
    """
    if total_steps <= 0:
        t = 0.0
    else:
        t = max(0.0, min(1.0, desired_step / total_steps))

    r1, g1, b1 = _hex_to_rgb(start_color)
    r2, g2, b2 = _hex_to_rgb(end_color)

    r = round(r1 + (r2 - r1) * t)
    g = round(g1 + (g2 - g1) * t)
    b = round(b1 + (b2 - b1) * t)

    return f"#{r:02x}{g:02x}{b:02x}"
