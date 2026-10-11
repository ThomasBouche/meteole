from importlib.metadata import version

from meteole._arome import AromeForecast
from meteole._arome_ensemble import AromePEForecast
from meteole._arome_ifs import AromeIFSForecast
from meteole._arome_instantane import AromePIForecast
from meteole._arpege import ArpegeForecast
from meteole._arpege_ensemble import ArpegePEForecast
from meteole._dpclim import DPClim
from meteole._piaf import PiafForecast
from meteole._vigilance import Vigilance

__all__ = [
    "AromeForecast",
    "AromeIFSForecast",
    "AromePIForecast",
    "ArpegeForecast",
    "PiafForecast",
    "Vigilance",
    "AromePEForecast",
    "ArpegePEForecast",
    "DPClim",
]

__version__ = version("meteole")
