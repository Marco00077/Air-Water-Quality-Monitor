# Air/Water Quality Monitor

A Python application with Tkinter GUI to analyze air and water quality from CSV data.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python quality_monitor.py
```

2. Select monitor type (Air or Water Quality)
3. Click "Load CSV File" and select your CSV file
4. View the analysis results

## CSV Format

### Air Quality CSV
Columns: PM2.5, PM10, Temp, Humidity, CO2
- PM2.5: Particulate Matter 2.5 (µg/m³)
- PM10: Particulate Matter 10 (µg/m³)
- Temp: Temperature (°C)
- Humidity: Relative Humidity (%)
- CO2: Carbon Dioxide (ppm)

### Water Quality CSV
Columns: pH, Temp, DO, Turbidity, TDS
- pH: pH level (0-14)
- Temp: Temperature (°C)
- DO: Dissolved Oxygen (mg/L)
- Turbidity: Turbidity (NTU)
- TDS: Total Dissolved Solids (mg/L)

## Sample Files

- `sample_air_quality.csv` - Example air quality data
- `sample_water_quality.csv` - Example water quality data
