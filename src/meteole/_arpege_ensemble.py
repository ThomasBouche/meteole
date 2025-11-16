from __future__ import annotations

import logging
from typing import Any, final

from meteole.clients import BaseClient, MeteoFranceClient
from meteole.forecast import WeatherForecast

logger = logging.getLogger(__name__)

AVAILABLE_ARPEGE_TERRITORY: list[str] = ["EUROPE", "GLOBE"]

ARPEGE_INSTANT_INDICATORS: list[str] = [
    "GEOMETRIC_HEIGHT__GROUND_OR_WATER_SURFACE",
    "ISOTHERMAL_LEVEL_TW27315__GROUND_OR_WATER_SURFACE",
    "ISOTHERMAL_LEVEL_TW27415__GROUND_OR_WATER_SURFACE",
    "ISOTHERMAL_LEVEL_TW27465__GROUND_OR_WATER_SURFACE",
    "ISOTHERMAL_LEVEL_T27315__GROUND_OR_WATER_SURFACE",
    "CLOUD_BASE_HEIGHT__GROUND_OR_WATER_SURFACE",
    "CONVECTIVE_AVAILABLE_POTENTIAL_ENERGY_MAX__GROUND_OR_WATER_SURFACE",
    "CONVECTIVE_AVAILABLE_POTENTIAL_ENERGY_MODEL__GROUND_OR_WATER_SURFACE",
    "INHIBITION_CONVECTIVE__GROUND_OR_WATER_SURFACE",
    "TOTAL_WATER_VAPOUR__GROUND_OR_WATER_SURFACE",
    "DIVERGENCE__ISOBARIC_SURFACE",
    "RELATIVE_HUMIDITY__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "RELATIVE_HUMIDITY__ISOBARIC_SURFACE",
    "PLANETARY_BOUNDARY_LAYER_HEIGHT__GROUND_OR_WATER_SURFACE",
    "LIGHTNING_DENSITY_MEAN_3H__GROUND_OR_WATER_SURFACE",
    "CONVECTIVE_AVAILABLE_POTENTIAL_ENERGY_MEAN_LAYER__GROUND_OR_WATER_SURFACE",
    "LOW_CLOUD_COVER__GROUND_OR_WATER_SURFACE",
    "CONVECTIVE_CLOUD_COVER__GROUND_OR_WATER_SURFACE",
    "HIGH_CLOUD_COVER__GROUND_OR_WATER_SURFACE",
    "MEDIUM_CLOUD_COVER__GROUND_OR_WATER_SURFACE",
    "TOTAL_CLOUD_COVER__GROUND_OR_WATER_SURFACE",
    "PRESSURE__GROUND_OR_WATER_SURFACE",
    "PRESSURE__MEAN_SEA_LEVEL",
    "POTENTIAL_TEMPERATURE__POTENTIAL_VORTICITY_SURFACE_1500",
    "POTENTIAL_TEMPERATURE__POTENTIAL_VORTICITY_SURFACE_2000",
    "MAXIMUM_TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "MINIMUM_TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "PSEUDO_ADIABATIC_POTENTIAL_TEMPERATURE__ISOBARIC_SURFACE",
    "TEMPERATURE__GROUND_OR_WATER_SURFACE",
    "TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "TEMPERATURE__ISOBARIC_SURFACE",
    "U_COMPONENT_OF_WIND_GUST__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "U_COMPONENT_OF_WIND__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "U_COMPONENT_OF_WIND__ISOBARIC_SURFACE",
    "U_COMPONENT_OF_WIND__POTENTIAL_VORTICITY_SURFACE_1500",
    "U_COMPONENT_OF_WIND__POTENTIAL_VORTICITY_SURFACE_2000",
    "MINIMUM_VISIBILITY_180_PRECIPITATING_HYDROMETEORS__GROUND_OR_WATER_SURFACE",
    "MINIMUM_VISIBILITY_PRECIPITATING_HYDROMETEORS__GROUND_OR_WATER_SURFACE",
    "MINIMUM_VISIBILITY_180_NON_PRECIPITATING_HYDROMETEORS__GROUND_OR_WATER_SURFACE",
    "MINIMUM_VISIBILITY_NON_PRECIPITATING_HYDROMETEORS__GROUND_OR_WATER_SURFACE",
    "VERTICAL_VELOCITY_PRESSURE__ISOBARIC_SURFACE",
    "V_COMPONENT_OF_WIND_GUST__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "V_COMPONENT_OF_WIND__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND",
    "V_COMPONENT_OF_WIND__ISOBARIC_SURFACE",
    "V_COMPONENT_OF_WIND__POTENTIAL_VORTICITY_SURFACE_1500",
    "V_COMPONENT_OF_WIND__POTENTIAL_VORTICITY_SURFACE_2000",
    "GEOPOTENTIAL__ISOBARIC_SURFACE",
    "GEOPOTENTIAL__POTENTIAL_VORTICITY_SURFACE_1500",
    "GEOPOTENTIAL__POTENTIAL_VORTICITY_SURFACE_2000",
]

ARPEGE_OTHER_INDICATORS: list[str] = [
    "TOTAL_WATER_PRECIPITATION__GROUND_OR_WATER_SURFACE",
    "LIGHTNING_DENSITY_CUMULATED__GROUND_OR_WATER_SURFACE",
    "TOTAL_SNOW_PRECIPITATION__GROUND_OR_WATER_SURFACE",
    "TOTAL_PRECIPITATION__GROUND_OR_WATER_SURFACE",
]


@final
class ArpegePEForecast(WeatherForecast):
    """Access the ARPEGE numerical weather forecast data from Meteo-France API.

    Doc:
        - https://portail-api.meteofrance.fr/web/fr/api/pe-arpege

    Attributes:
        territory: Covered area (e.g., FRANCE, EUROPE, ...).
        precision: Precision value of the forecast.
        capabilities: DataFrame containing details on all available coverage ids.
    """

    MODEL_NAME: str = "pearpege"
    BASE_ENTRY_POINT: str = "wcs/MF-NWP-GLOBAL-PEARP"
    MODEL_TYPE: str = "ENSEMBLE"
    ENSEMBLE_NUMBERS: int = 35
    DEFAULT_TERRITORY: str = "EUROPE"
    RELATION_TERRITORY_TO_PREC_ARPEGE: dict[str, float] = {"EUROPE": 0.1, "GLOBE": 0.25}
    CLIENT_CLASS: type[BaseClient] = MeteoFranceClient
    INDICATORS: list[str] = ARPEGE_INSTANT_INDICATORS + ARPEGE_OTHER_INDICATORS
    INSTANT_INDICATORS: list[str] = ARPEGE_INSTANT_INDICATORS

    def __init__(
        self,
        client: BaseClient | None = None,
        *,
        territory: str = "EUROPE",
        **kwargs: Any,
    ):
        """Initializes an ArpegeForecast object.

        The `precision` of the forecast is inferred from the specified `territory`.

        Args:
            territory: The ARPEGE territory to fetch. Defaults to "EUROPE".
            api_key: The API key for authentication. Defaults to None.
            token: The API token for authentication. Defaults to None.
            application_id: The Application ID for authentication. Defaults to None.

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

    def _validate_parameters(self) -> None:
        """Check the territory and the precision parameters.

        Raise:
            ValueError: At least, one parameter is not good.
        """
        if self.territory not in AVAILABLE_ARPEGE_TERRITORY:
            raise ValueError(f"The parameter precision must be in {AVAILABLE_ARPEGE_TERRITORY}")
