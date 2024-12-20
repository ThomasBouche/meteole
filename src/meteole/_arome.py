"""The interface for the observational data from the meteo-France API.

See :
- https://portail-api.meteofrance.fr/web/fr/api/arome
"""

from __future__ import annotations

import logging
from typing import final

from meteole.clients import BaseClient, MeteoFranceClient
from meteole.forecast import Forecast

logger = logging.getLogger(__name__)

AVAILABLE_AROME_TERRITORY: list[str] = [
    "FRANCE",
    "NCALED",
    "INDIEN",
    "POLYN",
    "GUYANE",
    "ANTIL",
]

AROME_INSTANT_INDICATORS: list[str] = [
    "GEOMETRIC_HEIGHT__GROUND_OR_WATER_SURFACE",
    "BRIGHTNESS_TEMPERATURE__GROUND_OR_WATER_SURFACE",
    "CONVECTIVE_AVAILABLE_POTENTIAL_ENERGY__GROUND_OR_WATER_SURFACE",
    "WIND_SPEED_GUST__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "WIND_SPEED__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "RELATIVE_HUMIDITY__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "LOW_CLOUD_COVER__GROUND_OR_WATER_SURFACE",
    "HIGH_CLOUD_COVER__GROUND_OR_WATER_SURFACE",
    "MEDIUM_CLOUD_COVER__GROUND_OR_WATER_SURFACE",
    "PRESSURE__GROUND_OR_WATER_SURFACE",
    "TOTAL_PRECIPITATION_RATE__GROUND_OR_WATER_SURFACE",
    "TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "U_COMPONENT_OF_WIND_GUST__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "U_COMPONENT_OF_WIND__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "V_COMPONENT_OF_WIND_GUST__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "V_COMPONENT_OF_WIND__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
]

AROME_OTHER_INDICATORS: list[str] = [
    "TOTAL_WATER_PRECIPITATION__GROUND_OR_WATER_SURFACE",
    "TOTAL_SNOW_PRECIPITATION__GROUND_OR_WATER_SURFACE",
    "TOTAL_PRECIPITATION__GROUND_OR_WATER_SURFACE",
]


@final
class AromeForecast(Forecast):
    """Access the AROME numerical forecast data."""

    # Model constants
    MODEL_NAME: str = "arome"
    RUN_FREQUENCY: int = 3
    INDICATORS: list[str] = AROME_INSTANT_INDICATORS + AROME_OTHER_INDICATORS
    INSTANT_INDICATORS: list[str] = AROME_INSTANT_INDICATORS
    BASE_ENTRY_POINT: str = "wcs/MF-NWP-HIGHRES-AROME"
    DEFAULT_TERRITORY: str = "FRANCE"
    DEFAULT_PRECISION: float = 0.01
    CLIENT_CLASS: type[BaseClient] = MeteoFranceClient

    def _validate_parameters(self):
        """Assert the parameters are valid."""
        if self.precision not in [0.01, 0.025]:
            raise ValueError("Parameter `precision` must be in (0.01, 0.025). It is inferred from argument `territory`")
        if self.territory not in AVAILABLE_AROME_TERRITORY:
            raise ValueError(f"Parameter `territory` must be in {AVAILABLE_AROME_TERRITORY}")
