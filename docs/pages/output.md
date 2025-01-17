Meteole provides forecasts in pandas.DataFrame, a convenient standard format for integration into your modeling pipelines.

## Processing Indicator Names in Output DataFrame
Indicator names are reprocessed by Meteole for the following reasons:
- **Handling unknown column names**:

Sometimes the column name is "unknown", in which case meteole generates a name by taking the first letters of the indicator name.

- **Concatenation of height or pressure values**:

To simplify output (mainly for retrieving multiple indicators), if the data includes height or pressure values, these are concatenated into the indicator name and the column is deleted. In this case, height (in meters) or pressure (in hPa) values are added to the base name.

For further details, please refer to the function :
::: meteole.forecast._get_data_single_forecast