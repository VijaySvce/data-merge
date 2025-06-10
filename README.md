# data-merge
# Voltage vs SOC Analyzer

A comprehensive PyQt5-based desktop application for analyzing battery voltage vs State of Charge (SOC) data with advanced dataset merging capabilities for charging and discharging analysis.

## Features

- **Dual Dataset Loading**: Load and analyze two separate CSV datasets
- **Individual Dataset Visualization**: Plot datasets separately or together for comparison
- **Advanced Dataset Merging**: Intelligent overlap removal algorithm for combining datasets
- **Charging/Discharging Analysis**: Specialized analysis modes with proper data sorting
- **Interactive GUI**: Modern, user-friendly interface with real-time feedback
- **Data Export**: Save merged datasets and high-quality plots
- **Flexible Column Detection**: Automatic detection of various column naming conventions

## Requirements

### Python Dependencies
```
PyQt5>=5.15.0
pandas>=1.3.0
numpy>=1.20.0
matplotlib>=3.3.0
```

### System Requirements
- Python 3.7 or higher
- Windows, macOS, or Linux
- At least 4GB RAM recommended
- 100MB free disk space

## Installation

1. **Clone or download the application file**
2. **Install required dependencies:**
   ```bash
   pip install PyQt5 pandas numpy matplotlib
   ```
3. **Run the application:**
   ```bash
   python voltage_soc_analyzer.py
   ```

## Data Format Requirements

### CSV File Structure
Your CSV files must contain the following columns (case-insensitive):
- **SOC** (State of Charge): Percentage values (0-100)
- **Voltage**: Voltage measurements in Volts

### Supported Column Names
The application automatically detects various naming conventions:
- **SOC**: `SOC`, `soc`, `State_of_Charge`, `StateOfCharge`, `SoC`
- **Voltage**: `Voltage`, `voltage`, `V`, `Volt`, `Volts`

### Example Data Format
```csv
SOC,Voltage
0.0,3.200
10.5,3.450
25.0,3.600
50.0,3.750
75.0,3.900
100.0,4.200
```

## Usage Guide

### Basic Workflow

1. **Load Datasets**
   - Click "Load Dataset 1" and select your first CSV file
   - Click "Load Dataset 2" and select your second CSV file
   - Verify dataset information in the info panel

2. **Individual Analysis**
   - Use "Plot Dataset 1" or "Plot Dataset 2" for individual visualization
   - Use "Plot Both Datasets" for side-by-side comparison

3. **Advanced Analysis**
   - **Charging Analysis**: Merges datasets and sorts in ascending SOC order
   - **Discharging Analysis**: Merges datasets and sorts in descending SOC order

4. **Export Results**
   - "Save Current Plot": Export visualization as PNG, PDF, or SVG
   - "Export Merged Data": Save merged dataset as CSV

### Dataset Merging Algorithm

The application uses a sophisticated merging algorithm:

1. **Overlap Detection**: Identifies SOC range covered by Dataset 1
2. **Overlap Removal**: Removes overlapping data points from Dataset 2
3. **Intelligent Merging**: Combines remaining Dataset 2 data with complete Dataset 1
4. **Proper Sorting**: Orders data appropriately for charging/discharging analysis

### Analysis Modes

#### Charging Analysis
- Sorts merged data in **ascending SOC order** (0% → 100%)
- Ideal for analyzing battery charging behavior
- Includes polynomial trend line fitting

#### Discharging Analysis
- Sorts merged data in **descending SOC order** (100% → 0%)
- Perfect for analyzing battery discharge characteristics
- Includes polynomial trend line fitting

## Interface Overview

### Control Panel (Left)
- **Dataset Loading**: Import and manage CSV files
- **Individual Plotting**: Visualize datasets separately or together
- **Merge & Analysis**: Advanced charging/discharging analysis
- **Export**: Save plots and data
- **Dataset Information**: Real-time dataset statistics

### Plot Panel (Right)
- **Interactive Plots**: High-quality matplotlib visualizations
- **Zoom & Pan**: Built-in matplotlib navigation tools
- **Professional Styling**: Clean, publication-ready plots
- **Trend Analysis**: Automatic polynomial trend line fitting

## Troubleshooting

### Common Issues

**"Column Error" Message**
- Ensure your CSV contains 'SOC' and 'Voltage' columns
- Check for typos in column headers
- Verify data is not corrupted

**Empty or Incorrect Plots**
- Verify data ranges are reasonable (SOC: 0-100%, Voltage: positive values)
- Check for missing or NaN values in datasets
- Ensure datasets contain sufficient data points

**Memory Issues with Large Datasets**
- Consider data sampling for datasets >100,000 rows
- Close other applications to free memory
- Split very large datasets into smaller chunks

### Error Handling
The application includes comprehensive error handling:
- **File Loading**: Validates CSV format and required columns
- **Data Processing**: Handles missing values and data type issues
- **Plotting**: Manages matplotlib rendering errors
- **Export**: Validates file paths and permissions

## Technical Details

### Architecture
- **Framework**: PyQt5 for cross-platform GUI
- **Data Processing**: pandas for efficient data manipulation
- **Visualization**: matplotlib with seaborn styling
- **File I/O**: Built-in CSV readers with error handling

### Performance
- **Memory Efficient**: Optimized for datasets up to 1M rows
- **Fast Rendering**: Hardware-accelerated matplotlib backend
- **Responsive UI**: Non-blocking file operations

## Example Use Cases

### Battery Research
- Analyze charging curves from different test conditions
- Compare discharge characteristics across battery types
- Merge partial test data for complete SOC range analysis

### Quality Control
- Validate battery performance against specifications
- Identify anomalies in charging/discharging behavior
- Generate reports with professional visualizations

### Academic Research
- Combine experimental data from multiple test sessions
- Create publication-ready plots with trend analysis
- Export processed data for further statistical analysis

## Support and Contributions

### Getting Help
- Check the troubleshooting section above
- Verify your data format matches requirements
- Ensure all dependencies are properly installed

### Feature Requests
The application is designed to be extensible. Common requested features:
- Support for additional file formats (Excel, JSON)
- Advanced statistical analysis tools
- Batch processing capabilities
- Custom styling options

## License

This application is provided as-is for educational and research purposes. 

## Version History

- **v1.0**: Initial release with basic plotting functionality
- **v2.0**: Added advanced merging algorithm and analysis modes
- **Current**: Enhanced UI, error handling, and export capabilities

---

