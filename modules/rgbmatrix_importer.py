from functools import cache

# largely a typing convenience, use emulator package when rgbmatrix fails to import (localdev)
# otherwise use rgbmatrix package (raspberrypi)
# there are certainly better ways to do this but I truly do not care for a project this simple
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics  # type: ignore # noqa: F401
except ImportError:
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics  # noqa: F401


@cache  # saves re-import when used across multiple files
def get_rgb_matrix_imports():
    return RGBMatrix, RGBMatrixOptions, graphics
