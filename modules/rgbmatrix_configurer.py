# hiding all the ugly configuration and type suppression in here to keep main driver program clean
from modules.rgbmatrix_importer import getRgbMatrixImports

RGBMatrix, RGBMatrixOptions, _ = getRgbMatrixImports()


# WARNING: The RGBMatrix class returned by this function MUST be kept in memory while using canvas
# Failure to do so results in SEGMENTATION FAULT and BUS ERROR problems
def getRGBMatrix(
    *,
    rows: int,
    cols: int,
    chain_length: int,
    parallel: int,
    gpio_slowdown: int,
    hardware_mapping: str,
    matrix_brightness: int,
):
    """
    WARNING: The returned RGBMatrix object must be kept in memory while using its canvas.
    Failure to do so may result in segmentation faults or bus errors.

    Initializes and returns an RGBMatrix object with the specified configuration.

    This function sets up the RGBMatrix with the provided options, such as the number of rows, columns,
    chain length, parallel chains, GPIO slowdown, hardware mapping, and brightness. It is compatible with
    both the actual 'rgbmatrix' package (for Raspberry Pi) and the 'RGBMatrixEmulator' package (for local development).

    Args:
        rows (int): Number of rows in the LED matrix.
        cols (int): Number of columns in the LED matrix.
        chain_length (int): Number of daisy-chained LED panels.
        parallel (int): Number of parallel chains.
        gpio_slowdown (int): GPIO slowdown value for timing adjustments.
        hardware_mapping (str): Hardware mapping string for the matrix.
        matrix_brightness (int): Brightness level of the matrix (0-100).

    Returns:
        RGBMatrix: Configured RGBMatrix object ready for use.
    """

    options = RGBMatrixOptions()
    options.rows = rows
    options.cols = cols
    options.chain_length = chain_length
    options.parallel = parallel
    options.gpio_slowdown = gpio_slowdown  # type: ignore
    options.hardware_mapping = hardware_mapping
    options.drop_privileges = False  # type: ignore # prevents python from removing root privileges at execution time

    matrix = RGBMatrix(options=options)
    matrix.brightness = matrix_brightness
    return matrix
