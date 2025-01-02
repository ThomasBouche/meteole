There is one reason for using **Meteole**:

> Easy access Météo-France forecast and vigilance data

## Before Meteole :cloud_with_rain:

Accessing weather data from Météo-France via Python could be quite challenging and time-consuming.

It involved:

* Diving into Météo-France documentation
* Handling expiring tokens manually
* Managing XML responses
* Dealing with the specificities of each weather indicator
* Parsing responses to get a clean dataframe

## After Meteole :sunny:

**Meteole** Meteole simplifies the process, allowing you to quickly fetch tidy pandas dataframes full of weather-rich data:

* By handling the API boilerplate
* By providing simple and well-documented function
* By using heuristics when necessary parameters are not provided
* By providing options to use individual parameters or a coverage_id for weather indicators
