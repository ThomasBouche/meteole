import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from meteole._arpege import ArpegeForecast
from meteole._arome import AromeForecast
from meteole.clients import MeteoFranceClient


class TestAromeForecast(unittest.TestCase):
    def setUp(self):
        self.precision = 0.01
        self.territory = "FRANCE"
        self._api_key = "fake_api_key"
        self.token = "fake_token"
        self.application_id = "fake_app_id"
        self.certs_path = "a/path/"
        self.client = MeteoFranceClient(
            api_key=self._api_key, token=self.token, application_id=self.application_id, certs_path=self.certs_path
        )

    @patch("meteole._arome.AromeForecast.get_capabilities")
    def test_initialization(self, mock_get_capabilities):
        mock_get_capabilities.return_value = None

        forecast = AromeForecast(
            self.client,
            precision=self.precision,
            territory=self.territory,
        )

        self.assertEqual(forecast.precision, self.precision)
        self.assertEqual(forecast.territory, self.territory)
        self.assertEqual(forecast._client._api_key, self._api_key)
        self.assertEqual(forecast._client._token, self.token)
        self.assertEqual(forecast._client._application_id, self.application_id)
        self.assertEqual(forecast._client._verify, self.certs_path)
        self.assertEqual(forecast.MODEL_NAME, "arome")
        self.assertEqual(forecast.RUN_FREQUENCY, 3)
        self.assertEqual(len(forecast.INDICATORS), 19)
        # mock_get_capabilities.assert_called_once()

    def test_invalid_precision(self):
        with self.assertRaises(ValueError):
            AromeForecast(self.client, precision=0.1)

    def test_invalid_territory(self):
        with self.assertRaises(ValueError):
            AromeForecast(self.client, territory="INVALID")

    @patch("meteole.clients.MeteoFranceClient.get")
    def test_get_capabilities(self, mock_get_request):
        mock_response = MagicMock()
        mock_response.text = """
            <wcs:Capabilities>
                <wcs:Contents>
                    <wcs:CoverageSummary>
                        <wcs:CoverageId>GEOMETRIC_HEIGHT__GROUND_OR_WATER_SURFACE___2024-10-31T00.00.00Z</wcs:CoverageId>
                        <ows:CoverageTitle>Geometric height</ows:CoverageTitle>
                        <wcs:CoverageSubtype>ReferenceableGridCoverage</wcs:CoverageSubtype>
                    </wcs:CoverageSummary>
                    <wcs:CoverageSummary>
                        <wcs:CoverageId>SHORT_WAVE_RADIATION_FLUX__GROUND_OR_WATER_SURFACE___2024-11-01T18.00.00Z_P2D</wcs:CoverageId>
                        <ows:CoverageTitle>short-wave radiation flux</ows:CoverageTitle>
                        <wcs:CoverageSubtype>ReferenceableGridCoverage</wcs:CoverageSubtype>
                    </wcs:CoverageSummary>
                </wcs:Contents>
            </wcs:Capabilities>
        """
        mock_get_request.return_value = mock_response

        arome = AromeForecast(
            self.client,
            precision=self.precision,
            territory=self.territory,
        )
        # arome.get_capabilities() is made during init
        # this means arome.capabilities exists now

        self.assertEqual(
            list(arome.capabilities["id"]),
            [
                "GEOMETRIC_HEIGHT__GROUND_OR_WATER_SURFACE___2024-10-31T00.00.00Z",
                "SHORT_WAVE_RADIATION_FLUX__GROUND_OR_WATER_SURFACE___2024-11-01T18.00.00Z_P2D",
            ],
        )

    @patch("meteole.clients.MeteoFranceClient.get")
    def test_get_coverage_id(self, mock_get_request):
        mock_response = MagicMock()
        mock_response.text = """
            <wcs:Capabilities>
                <wcs:Contents>
                    <wcs:CoverageSummary>
                        <wcs:CoverageId>GEOMETRIC_HEIGHT__GROUND_OR_WATER_SURFACE___2024-10-31T00.00.00Z</wcs:CoverageId>
                        <ows:CoverageTitle>Geometric height</ows:CoverageTitle>
                        <wcs:CoverageSubtype>ReferenceableGridCoverage</wcs:CoverageSubtype>
                    </wcs:CoverageSummary>
                    <wcs:CoverageSummary>
                        <wcs:CoverageId>TOTAL_WATER_PRECIPITATION__GROUND_OR_WATER_SURFACE___2024-11-01T18.00.00Z_P2D</wcs:CoverageId>
                        <ows:CoverageTitle>short-wave radiation flux</ows:CoverageTitle>
                        <wcs:CoverageSubtype>ReferenceableGridCoverage</wcs:CoverageSubtype>
                    </wcs:CoverageSummary>
                </wcs:Contents>
            </wcs:Capabilities>
        """
        mock_get_request.return_value = mock_response

        arome = AromeForecast(
            self.client,
            precision=self.precision,
            territory=self.territory,
        )  # arome.capabilities is set up

        run = "2024-11-01T18.00.00Z"
        interval = "P2D"

        # test wrong indicator raises
        indicator = "wrong_indicator"

        with pytest.raises(ValueError):
            coverage_id = arome._get_coverage_id(indicator, run, interval)

        indicator = "TOTAL_WATER_PRECIPITATION__GROUND_OR_WATER_SURFACE"
        coverage_id = arome._get_coverage_id(indicator, run, interval)
        assert coverage_id == "TOTAL_WATER_PRECIPITATION__GROUND_OR_WATER_SURFACE___2024-11-01T18.00.00Z_P2D"

    @patch("meteole._arome.AromeForecast.get_capabilities")
    @patch("meteole.clients.MeteoFranceClient.get")
    def test_get_coverage_description(self, mock_get_request, mock_get_capabilities):
        mock_response = MagicMock()
        mock_response.text = """
            <wcs:CoverageDescriptions xmlns:wcs="http://www.opengis.net/wcs/2.0" xmlns:swe="http://www.opengis.net/swe/2.0" xmlns:gmlrgrid="http://www.opengis.net/gml/3.3/rgrid" xmlns:gmlcov="http://www.opengis.net/gmlcov/1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gml="http://www.opengis.net/gml/3.2" xsi:schemaLocation="     http://www.opengis.net/wcs/2.0 http://schemas.opengis.net/wcs/2.0/wcsAll.xsd     http://www.opengis.net/gml/3.2 http://schemas.opengis.net/gml/3.2.1/gml.xsd     http://www.opengis.net/gmlcov/1.0 http://schemas.opengis.net/gmlcov/1.0/gmlcovAll.xsd     http://www.opengis.net/swe/2.0 http://schemas.opengis.net/sweCommon/2.0/swe.xsd     http://www.opengis.net/gml/3.3/rgrid http://schemas.opengis.net/gml/3.3/referenceableGrid.xsd">
            <wcs:CoverageDescription gml:id="U_COMPONENT_OF_WIND_GUST__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND___2024-06-20T09.00.00Z">
                <wcs:CoverageId>U_COMPONENT_OF_WIND_GUST__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND___2024-06-20T09.00.00Z</wcs:CoverageId>
                <wcs:ServiceParameters>
                <wcs:CoverageSubtype>ReferenceableGridCoverage</wcs:CoverageSubtype>
                <wcs:nativeFormat>application/wmo-grib</wcs:nativeFormat>
                </wcs:ServiceParameters>
            </wcs:CoverageDescription>
            </wcs:CoverageDescriptions>
        """
        mock_get_request.return_value = mock_response
        mock_get_capabilities.return_value = None

        forecast = AromeForecast(
            self.client,
            precision=self.precision,
            territory=self.territory,
        )

        description = forecast._get_coverage_description("coverage_1")
        self.assertIn("wcs:CoverageDescriptions", description)

    @patch("meteole._arome.AromeForecast.get_capabilities")
    @patch("meteole.clients.MeteoFranceClient.get")
    def test_get_coverage_file(self, mock_get_request, mock_get_capabilities):
        mock_response = MagicMock()
        mock_response.content = b"fake_data"
        mock_get_request.return_value = mock_response
        mock_get_capabilities.return_value = None

        forecast = AromeForecast(
            self.client,
            precision=self.precision,
            territory=self.territory,
        )

        coverage_id = "coverage_1"
        forecast._get_coverage_file(
            coverage_id=coverage_id,
            height=2,
            forecast_horizon_in_seconds=0,
            lat=(37.5, 55.4),
            long=(-12, 16),
        )

        import os

        expected_path = Path(os.getcwd()) / coverage_id / "2m_0Z_37.5-55.4_-12-16.grib"
        self.assertTrue(expected_path.exists())

        expected_path.unlink()

    @patch("meteole._arome.AromeForecast.get_capabilities")
    @patch("meteole._arome.AromeForecast._transform_grib_to_df")
    @patch("meteole._arome.AromeForecast._get_coverage_file")
    def test_get_data_single_forecast(self, mock_get_coverage_file, mock_transform_grib_to_df, mock_get_capabilities):
        mock_transform_grib_to_df.return_value = pd.DataFrame({"data": [1, 2, 3], "heightAboveGround": ["1", "2", "3"]})

        forecast = AromeForecast(
            self.client,
            precision=self.precision,
            territory=self.territory,
        )

        df = forecast._get_data_single_forecast(
            coverage_id="coverage_1",
            height=2,
            pressure=None,
            forecast_horizon=0,
            lat=(37.5, 55.4),
            long=(-12, 16),
        )

        self.assertTrue("data" in df.columns)

    @patch("meteole._arome.AromeForecast.get_coverage_description")
    @patch("meteole._arome.AromeForecast.get_capabilities")
    @patch("meteole._arome.AromeForecast._get_data_single_forecast")
    def test_get_coverage(self, mock_get_data_single_forecast, mock_get_capabilities, mock_get_coverage_description):
        mock_get_data_single_forecast.return_value = pd.DataFrame(
            {
                "latitude": [1, 2, 3],
                "longitude": [4, 5, 6],
                "time": [7, 8, 9],
                "step": [10, 11, 12],
                "valid_time": [16, 17, 18],
                "data": [19, 20, 21],  # this column name varies depending on the coverage_id
            }
        )
        mock_get_coverage_description.return_value = {"heights": [2], "forecast_horizons": [0], "pressures": []}

        forecast = AromeForecast(
            self.client,
            precision=self.precision,
            territory=self.territory,
        )

        forecast.get_coverage(
            coverage_id="toto",
            heights=[2],
            forecast_horizons=[0],
            lat=(37.5, 55.4),
            long=(-12, 16),
        )

        mock_get_data_single_forecast.assert_called_once_with(
            coverage_id="toto", height=2, pressure=None, forecast_horizon=0, lat=(37.5, 55.4), long=(-12, 16)
        )


class TestArpegeForecast(unittest.TestCase):
    def setUp(self):
        self.territory = "EUROPE"
        self._api_key = "fake_api_key"
        self.token = "fake_token"
        self.application_id = "fake_app_id"
        self.client = MeteoFranceClient(token=self.token)

    @patch("meteole._arpege.ArpegeForecast.get_capabilities")
    def test_initialization(self, mock_get_capabilities):
        territory = "EUROPE"
        api_key = "test_api_key"
        token = "test_token"
        application_id = "test_app_id"

        client = MeteoFranceClient(api_key=api_key, token=token, application_id=application_id, certs_path="toto")

        arpege_forecast = ArpegeForecast(
            client,
            territory=territory,
        )

        self.assertEqual(arpege_forecast.territory, territory)
        self.assertEqual(arpege_forecast.precision, ArpegeForecast.RELATION_TERRITORY_TO_PREC_ARPEGE[territory])
        self.assertEqual(arpege_forecast._client._verify, "toto")
        self.assertEqual(arpege_forecast._client._api_key, api_key)
        self.assertEqual(arpege_forecast._client._token, token)
        self.assertEqual(arpege_forecast._client._application_id, application_id)
        self.assertEqual(arpege_forecast.MODEL_NAME, "arpege")
        self.assertEqual(arpege_forecast.RUN_FREQUENCY, 6)
        self.assertEqual(len(arpege_forecast.INDICATORS), 47)
        # mock_get_capabilities.assert_called_once()

    @patch("meteole._arpege.ArpegeForecast.get_capabilities")
    def test_validate_parameters(self, mock_get_capabilities):
        valid_territory = "EUROPE"
        invalid_territory = "INVALID_TERRITORY"

        # Test with a valid territory
        client = MeteoFranceClient(api_key="toto")
        arpege_forecast = ArpegeForecast(client, territory=valid_territory)

        try:
            arpege_forecast._validate_parameters()
        except ValueError:
            self.fail("_validate_parameters raised ValueError unexpectedly with valid territory!")

        # Test with an invalid territory
        arpege_forecast.territory = invalid_territory
        with self.assertRaises(ValueError):
            arpege_forecast._validate_parameters()

    @patch("meteole._arpege.ArpegeForecast.get_capabilities")
    @patch("meteole.clients.MeteoFranceClient._connect")
    def test_entry_point(self, mock_MeteoFranceClient_connect, mock_get_capabilities):
        territory = "EUROPE"
        arpege_forecast = ArpegeForecast(self.client, territory=territory)
        expected_entry_point = f"wcs/MF-NWP-GLOBAL-ARPEGE-{ArpegeForecast.PRECISION_FLOAT_TO_STR[ArpegeForecast.RELATION_TERRITORY_TO_PREC_ARPEGE[territory]]}-{territory}-WCS"
        self.assertEqual(arpege_forecast._entry_point, expected_entry_point)


class TestGetAvailableFeature(unittest.TestCase):
    def setUp(self):
        self.grid_axis = [
            {
                "gmlrgrid:GeneralGridAxis": {
                    "gmlrgrid:gridAxesSpanned": "time",
                    "gmlrgrid:coefficients": "3600 7200 10800",
                }
            },
            {
                "gmlrgrid:GeneralGridAxis": {
                    "gmlrgrid:gridAxesSpanned": "height",
                    "gmlrgrid:coefficients": "100 200 300",
                }
            },
            {
                "gmlrgrid:GeneralGridAxis": {
                    "gmlrgrid:gridAxesSpanned": "pressure",
                    "gmlrgrid:coefficients": "1000 2000 3000",
                }
            },
        ]

    def test_get_available_feature_time(self):
        result = AromeForecast._get_available_feature(self.grid_axis, "time")
        self.assertEqual(result, [3600, 7200, 10800])

    def test_get_available_feature_height(self):
        result = AromeForecast._get_available_feature(self.grid_axis, "height")
        self.assertEqual(result, [100, 200, 300])

    def test_get_available_feature_pressure(self):
        result = AromeForecast._get_available_feature(self.grid_axis, "pressure")
        self.assertEqual(result, [1000, 2000, 3000])

    def test_get_available_feature_not_found(self):
        result = AromeForecast._get_available_feature(self.grid_axis, "nonexistent")
        self.assertEqual(result, [])
