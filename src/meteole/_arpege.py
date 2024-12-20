"""The interface for the observational data from the meteo-France API.

See :
- https://portail-api.meteofrance.fr/web/fr/api/arpege
"""

from typing import Any

from meteole.clients import BaseClient, MeteoFranceClient
from meteole.forecast import Forecast

AVAILABLE_ARPEGE_TERRITORY = ["EUROPE", "GLOBE", "ATOURX", "EURAT"]

ARPEGE_INSTANT_INDICATORS = [
    "GEOMETRIC_HEIGHT__GROUND_OR_WATER_SURFACE",
    "BRIGHTNESS_TEMPERATURE__GROUND_OR_WATER_SURFACE",
    "CONVECTIVE_AVAILABLE_POTENTIAL_ENERGY__GROUND_OR_WATER_SURFACE",
    "SPECIFIC_CLOUD_ICE_WATER_CONTENT__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "SPECIFIC_CLOUD_ICE_WATER_CONTENT__ISOBARIC_SURFACE",
    "WIND_SPEED_GUST__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "WIND_SPEED__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "WIND_SPEED__ISOBARIC_SURFACE",
    "DOWNWARD_SHORT_WAVE_RADIATION_FLUX__GROUND_OR_WATER_SURFACE",
    "SHORT_WAVE_RADIATION_FLUX__GROUND_OR_WATER_SURFACE",
    "RELATIVE_HUMIDITY__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "RELATIVE_HUMIDITY__ISOBARIC_SURFACE",
    "PLANETARY_BOUNDARY_LAYER_HEIGHT__GROUND_OR_WATER_SURFACE",
    "LOW_CLOUD_COVER__GROUND_OR_WATER_SURFACE",
    "HIGH_CLOUD_COVER__GROUND_OR_WATER_SURFACE",
    "MEDIUM_CLOUD_COVER__GROUND_OR_WATER_SURFACE",
    "PRESSURE__GROUND_OR_WATER_SURFACE",
    "PRESSURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "PRESSURE__MEAN_SEA_LEVEL",
    "ABSOLUTE_VORTICITY__ISOBARIC_SURFACE",
    "DEW_POINT_TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "DEW_POINT_TEMPERATURE__ISOBARIC_SURFACE",
    "TURBULENT_KINETIC_ENERGY__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "TURBULENT_KINETIC_ENERGY__ISOBARIC_SURFACE",
    "MAXIMUM_TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "MINIMUM_TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "PSEUDO_ADIABATIC_POTENTIAL_TEMPERATURE__ISOBARIC_SURFACE",
    "POTENTIAL_VORTICITY__ISOBARIC_SURFACE",
    "TEMPERATURE__GROUND_OR_WATER_SURFACE",
    "TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "TEMPERATURE__ISOBARIC_SURFACE",
    "U_COMPONENT_OF_WIND_GUST__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "U_COMPONENT_OF_WIND__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "U_COMPONENT_OF_WIND__ISOBARIC_SURFACE",
    "U_COMPONENT_OF_WIND__POTENTIAL_VORTICITY_SURFACE_1500",
    "U_COMPONENT_OF_WIND__POTENTIAL_VORTICITY_SURFACE_2000",
    "VERTICAL_VELOCITY_PRESSURE__ISOBARIC_SURFACE",
    "V_COMPONENT_OF_WIND_GUST__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "V_COMPONENT_OF_WIND__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "V_COMPONENT_OF_WIND__ISOBARIC_SURFACE",
    "V_COMPONENT_OF_WIND__POTENTIAL_VORTICITY_SURFACE_1500",
    "V_COMPONENT_OF_WIND__POTENTIAL_VORTICITY_SURFACE_2000",
    "GEOPOTENTIAL__ISOBARIC_SURFACE",
]

ARPEGE_OTHER_INDICATORS = [
    "TOTAL_WATER_PRECIPITATION__GROUND_OR_WATER_SURFACE",
    "TOTAL_CLOUD_COVER__GROUND_OR_WATER_SURFACE",
    "TOTAL_SNOW_PRECIPITATION__GROUND_OR_WATER_SURFACE",
    "TOTAL_PRECIPITATION__GROUND_OR_WATER_SURFACE",
]


class ArpegeForecast(Forecast):
    """Access the ARPEGE numerical forecast data."""

    # Model constants
    MODEL_NAME: str = "arpege"
    RUN_FREQUENCY: int = 6
    INDICATORS: list[str] = ARPEGE_INSTANT_INDICATORS + ARPEGE_OTHER_INDICATORS
    INSTANT_INDICATORS: list[str] = ARPEGE_INSTANT_INDICATORS
    BASE_ENTRY_POINT: str = "wcs/MF-NWP-GLOBAL-ARPEGE"
    DEFAULT_TERRITORY: str = "EUROPE"
    RELATION_TERRITORY_TO_PREC_ARPEGE: dict[str, float] = {"EUROPE": 0.1, "GLOBE": 0.25, "ATOURX": 0.1, "EURAT": 0.05}
    CLIENT_CLASS: type[BaseClient] = MeteoFranceClient

    def __init__(
        self,
        client: BaseClient | None = None,
        *,
        territory: str = "EUROPE",
        **kwargs: Any,
    ):
        """
        Initializes an ArpegeForecast object for accessing ARPEGE forecast data.

        The `precision` of the forecast is inferred from the specified `territory`.

        Args:
            territory (str, optional): The ARPEGE territory to fetch. Defaults to "EUROPE".
            api_key (str | None, optional): The API key for authentication. Defaults to None.
            token (str | None, optional): The API token for authentication. Defaults to None.
            application_id (str | None, optional): The Application ID for authentication. Defaults to None.
            cache_dir (str | None, optional): Path to the cache directory. Defaults to None.
                If not provided, the cache directory is set to "/tmp/cache".

        Notes:
            - See `MeteoFranceClient` for additional details on the parameters `api_key`, `token`,
                and `application_id`.
            - Available territories are listed in the `AVAILABLE_TERRITORY` constant.

        """
        super().__init__(
            client=client,
            territory=territory,
            precision=self.RELATION_TERRITORY_TO_PREC_ARPEGE[territory],
            **kwargs,
        )

    def _validate_parameters(self):
        """Assert the parameters are valid."""
        if self.territory not in AVAILABLE_ARPEGE_TERRITORY:
            raise ValueError(f"The parameter precision must be in {AVAILABLE_ARPEGE_TERRITORY}")
