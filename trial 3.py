import sys
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QWidget, QFileDialog, QMessageBox, 
                             QLabel, QGroupBox, QGridLayout, QTextEdit, QSplitter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.style as style

# Set matplotlib style
style.use('seaborn-v0_8')

class VoltageSOCAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dataset1 = None
        self.dataset2 = None
        self.merged_data = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Voltage vs SOC Charging/Discharging Analyzer")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                text-align: center;
                font-size: 14px;
                margin: 4px 2px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QLabel {
                font-size: 12px;
            }
        """)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel for controls
        left_panel = self.create_control_panel()
        splitter.addWidget(left_panel)
        
        # Right panel for plots
        right_panel = self.create_plot_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([400, 1000])
        
    def create_control_panel(self):
        """Create the control panel with buttons and information."""
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        
        # Title
        title_label = QLabel("Voltage vs SOC Analyzer")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        control_layout.addWidget(title_label)
        
        # Dataset loading section
        dataset_group = QGroupBox("Dataset Loading")
        dataset_layout = QVBoxLayout(dataset_group)
        
        self.load_dataset1_btn = QPushButton("Load Dataset 1")
        self.load_dataset1_btn.clicked.connect(lambda: self.load_dataset(1))
        dataset_layout.addWidget(self.load_dataset1_btn)
        
        self.dataset1_info = QLabel("No dataset loaded")
        self.dataset1_info.setWordWrap(True)
        dataset_layout.addWidget(self.dataset1_info)
        
        self.load_dataset2_btn = QPushButton("Load Dataset 2")
        self.load_dataset2_btn.clicked.connect(lambda: self.load_dataset(2))
        dataset_layout.addWidget(self.load_dataset2_btn)
        
        self.dataset2_info = QLabel("No dataset loaded")
        self.dataset2_info.setWordWrap(True)
        dataset_layout.addWidget(self.dataset2_info)
        
        control_layout.addWidget(dataset_group)
        
        # Individual plotting section
        plot_group = QGroupBox("Individual Dataset Plotting")
        plot_layout = QVBoxLayout(plot_group)
        
        self.plot_dataset1_btn = QPushButton("Plot Dataset 1")
        self.plot_dataset1_btn.clicked.connect(lambda: self.plot_individual_dataset(1))
        self.plot_dataset1_btn.setEnabled(False)
        plot_layout.addWidget(self.plot_dataset1_btn)
        
        self.plot_dataset2_btn = QPushButton("Plot Dataset 2")
        self.plot_dataset2_btn.clicked.connect(lambda: self.plot_individual_dataset(2))
        self.plot_dataset2_btn.setEnabled(False)
        plot_layout.addWidget(self.plot_dataset2_btn)
        
        self.plot_both_btn = QPushButton("Plot Both Datasets")
        self.plot_both_btn.clicked.connect(self.plot_both_datasets)
        self.plot_both_btn.setEnabled(False)
        plot_layout.addWidget(self.plot_both_btn)
        
        control_layout.addWidget(plot_group)
        
        # Merge and analysis section
        analysis_group = QGroupBox("Merge & Analysis")
        analysis_layout = QVBoxLayout(analysis_group)
        
        self.charging_btn = QPushButton("Charging Analysis")
        self.charging_btn.setStyleSheet("QPushButton { background-color: #2196F3; }")
        self.charging_btn.clicked.connect(self.charging_analysis)
        self.charging_btn.setEnabled(False)
        analysis_layout.addWidget(self.charging_btn)
        
        self.discharging_btn = QPushButton("Discharging Analysis")
        self.discharging_btn.setStyleSheet("QPushButton { background-color: #FF9800; }")
        self.discharging_btn.clicked.connect(self.discharging_analysis)
        self.discharging_btn.setEnabled(False)
        analysis_layout.addWidget(self.discharging_btn)
        
        control_layout.addWidget(analysis_group)
        
        # Export section
        export_group = QGroupBox("Export")
        export_layout = QVBoxLayout(export_group)
        
        self.save_plot_btn = QPushButton("Save Current Plot")
        self.save_plot_btn.clicked.connect(self.save_plot)
        export_layout.addWidget(self.save_plot_btn)
        
        self.export_data_btn = QPushButton("Export Merged Data")
        self.export_data_btn.clicked.connect(self.export_data)
        self.export_data_btn.setEnabled(False)
        export_layout.addWidget(self.export_data_btn)
        
        control_layout.addWidget(export_group)
        
        # Info section
        info_group = QGroupBox("Dataset Information")
        info_layout = QVBoxLayout(info_group)
        
        self.info_text = QTextEdit()
        self.info_text.setMaximumHeight(150)
        self.info_text.setReadOnly(True)
        self.info_text.setText("Load datasets to see information...")
        info_layout.addWidget(self.info_text)
        
        control_layout.addWidget(info_group)
        
        # Add stretch to push everything to top
        control_layout.addStretch()
        
        return control_widget
    
    def create_plot_panel(self):
        """Create the plotting panel."""
        plot_widget = QWidget()
        plot_layout = QVBoxLayout(plot_widget)
        
        # Create matplotlib figure and canvas
        self.figure = Figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)
        plot_layout.addWidget(self.canvas)
        
        # Initialize with welcome plot
        self.show_welcome_plot()
        
        return plot_widget
    
    def show_welcome_plot(self):
        """Show a welcome message on the plot area."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, 'Welcome to Voltage vs SOC Analyzer\n\nLoad your datasets to begin analysis',
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=16, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        self.canvas.draw()
    
    def load_dataset(self, dataset_num):
        """Load a CSV dataset."""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, f"Select Dataset {dataset_num}", "", 
                "CSV Files (*.csv);;All Files (*)"
            )
            
            if not file_path:
                return
            
            # Read the CSV file
            df = pd.read_csv(file_path)
            
            # Validate required columns
            required_columns = ['SOC', 'Voltage']
            if not all(col in df.columns for col in required_columns):
                # Check for alternative column names
                alternative_names = {
                    'SOC': ['soc', 'State_of_Charge', 'StateOfCharge', 'SoC'],
                    'Voltage': ['voltage', 'V', 'Volt', 'Volts']
                }
                
                column_mapping = {}
                for req_col in required_columns:
                    found = False
                    for col in df.columns:
                        if col in alternative_names[req_col] or req_col.lower() in col.lower():
                            column_mapping[col] = req_col
                            found = True
                            break
                    if not found:
                        QMessageBox.critical(
                            self, "Column Error",
                            f"Dataset must contain '{req_col}' column.\n"
                            f"Available columns: {list(df.columns)}"
                        )
                        return
                
                # Rename columns
                df = df.rename(columns=column_mapping)
            
            # Store dataset
            if dataset_num == 1:
                self.dataset1 = df
                self.dataset1_info.setText(f"Dataset 1: {len(df)} rows, {len(df.columns)} columns")
                self.plot_dataset1_btn.setEnabled(True)
            else:
                self.dataset2 = df
                self.dataset2_info.setText(f"Dataset 2: {len(df)} rows, {len(df.columns)} columns")
                self.plot_dataset2_btn.setEnabled(True)
            
            # Update info and enable buttons
            self.update_info_panel()
            self.update_button_states()
            
            QMessageBox.information(
                self, "Success", 
                f"Dataset {dataset_num} loaded successfully!\n"
                f"Rows: {len(df)}, Columns: {len(df.columns)}"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self, "Loading Error", 
                f"Error loading dataset {dataset_num}:\n{str(e)}"
            )
    
    def update_info_panel(self):
        """Update the information panel with dataset details."""
        info_text = "Dataset Information:\n\n"
        
        if self.dataset1 is not None:
            info_text += f"Dataset 1:\n"
            info_text += f"  Rows: {len(self.dataset1)}\n"
            info_text += f"  Columns: {list(self.dataset1.columns)}\n"
            info_text += f"  SOC range: {self.dataset1['SOC'].min():.2f} - {self.dataset1['SOC'].max():.2f}\n"
            info_text += f"  Voltage range: {self.dataset1['Voltage'].min():.3f} - {self.dataset1['Voltage'].max():.3f}\n\n"
        
        if self.dataset2 is not None:
            info_text += f"Dataset 2:\n"
            info_text += f"  Rows: {len(self.dataset2)}\n"
            info_text += f"  Columns: {list(self.dataset2.columns)}\n"
            info_text += f"  SOC range: {self.dataset2['SOC'].min():.2f} - {self.dataset2['SOC'].max():.2f}\n"
            info_text += f"  Voltage range: {self.dataset2['Voltage'].min():.3f} - {self.dataset2['Voltage'].max():.3f}\n\n"
        
        self.info_text.setText(info_text)
    
    def update_button_states(self):
        """Update button enabled states based on loaded datasets."""
        both_loaded = self.dataset1 is not None and self.dataset2 is not None
        
        self.plot_both_btn.setEnabled(both_loaded)
        self.charging_btn.setEnabled(both_loaded)
        self.discharging_btn.setEnabled(both_loaded)
    
    def plot_individual_dataset(self, dataset_num):
        """Plot an individual dataset."""
        try:
            dataset = self.dataset1 if dataset_num == 1 else self.dataset2
            
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            ax.plot(dataset['SOC'], dataset['Voltage'], 'o-', markersize=4, linewidth=2,
                   label=f'Dataset {dataset_num}')
            ax.set_xlabel('State of Charge (SOC) [%]', fontsize=12)
            ax.set_ylabel('Voltage [V]', fontsize=12)
            ax.set_title(f'Voltage vs SOC - Dataset {dataset_num}', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            self.figure.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            QMessageBox.critical(self, "Plotting Error", f"Error plotting dataset {dataset_num}:\n{str(e)}")
    
    def plot_both_datasets(self):
        """Plot both datasets on the same graph."""
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            ax.plot(self.dataset1['SOC'], self.dataset1['Voltage'], 'o-', 
                   markersize=4, linewidth=2, label='Dataset 1', alpha=0.8)
            ax.plot(self.dataset2['SOC'], self.dataset2['Voltage'], 's-', 
                   markersize=4, linewidth=2, label='Dataset 2', alpha=0.8)
            
            ax.set_xlabel('State of Charge (SOC) [%]', fontsize=12)
            ax.set_ylabel('Voltage [V]', fontsize=12)
            ax.set_title('Voltage vs SOC - Both Datasets Comparison', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            self.figure.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            QMessageBox.critical(self, "Plotting Error", f"Error plotting both datasets:\n{str(e)}")
    
    def merge_datasets_with_overlap_removal(self, df_a, df_b, sensor_column='SOC'):
        """
        Merge datasets using the specific logic:
        1. Get first and last values from Dataset A
        2. Remove overlapping range from Dataset B
        3. Concatenate remaining Dataset B with Dataset A
        """
        try:
            # Step 1: Get first and last values of sensor column from Dataset A
            first_value_a = df_a[sensor_column].iloc[0]
            last_value_a = df_a[sensor_column].iloc[-1]
            
            # Ensure we have min and max values (in case data is not sorted)
            min_val = min(first_value_a, last_value_a)
            max_val = max(first_value_a, last_value_a)
            
            # Step 2: Filter rows in Dataset B where sensor column is between first and last values from Dataset A
            filtered_b = df_b[(df_b[sensor_column] >= min_val) & 
                             (df_b[sensor_column] <= max_val)]
            
            # Step 3: Remove rows in Dataset B where sensor column falls within that range
            remaining_b = df_b[~((df_b[sensor_column] >= min_val) & 
                               (df_b[sensor_column] <= max_val))]
            
            # Step 4: Merge Dataset A into the space left by deleting rows in Dataset B
            merged_df = pd.concat([remaining_b, df_a], ignore_index=True)
            
            # Log merge information
            print(f"Dataset A range: {min_val:.3f} to {max_val:.3f}")
            print(f"Filtered out {len(filtered_b)} rows from Dataset B")
            print(f"Remaining Dataset B rows: {len(remaining_b)}")
            print(f"Final merged dataset: {len(merged_df)} rows")
            
            return merged_df
            
        except Exception as e:
            QMessageBox.critical(self, "Merge Error", f"Error merging datasets with overlap removal:\n{str(e)}")
            return None
    
    def charging_analysis(self):
        """Perform charging analysis (ascending SOC order) with overlap removal."""
        try:
            # Use the specific merge logic with overlap removal
            merged_data = self.merge_datasets_with_overlap_removal(
                self.dataset1, self.dataset2, 'SOC'
            )
            if merged_data is None:
                return
            
            # Sort in ascending order for charging
            merged_data = merged_data.sort_values('SOC', ascending=True).reset_index(drop=True)
            self.merged_data = merged_data
            
            # Plot the merged and sorted data
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            ax.plot(merged_data['SOC'], merged_data['Voltage'], 'o-', 
                   markersize=5, linewidth=2, color='blue', label='Charging Curve')
            
            ax.set_xlabel('State of Charge (SOC) [%]', fontsize=12)
            ax.set_ylabel('Voltage [V]', fontsize=12)
            ax.set_title('Charging Analysis - Voltage vs SOC (Ascending Order)', 
                        fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            # Add trend line
            z = np.polyfit(merged_data['SOC'], merged_data['Voltage'], 2)
            p = np.poly1d(z)
            ax.plot(merged_data['SOC'], p(merged_data['SOC']), '--', 
                   alpha=0.8, color='red', label='Trend')
            ax.legend()
            
            self.figure.tight_layout()
            self.canvas.draw()
            
            # Enable export button
            self.export_data_btn.setEnabled(True)
            
            # Show detailed merge information
            first_val = self.dataset1['SOC'].iloc[0]
            last_val = self.dataset1['SOC'].iloc[-1]
            min_val = min(first_val, last_val)
            max_val = max(first_val, last_val)
            
            QMessageBox.information(
                self, "Charging Analysis Complete",
                f"Merge Details:\n"
                f"• Dataset A SOC range: {min_val:.2f}% to {max_val:.2f}%\n"
                f"• Removed overlapping data from Dataset B\n"
                f"• Final merged dataset: {len(merged_data)} data points\n"
                f"• Sorted in ascending SOC order for charging analysis"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Analysis Error", f"Error in charging analysis:\n{str(e)}")
    
    def discharging_analysis(self):
        """Perform discharging analysis (descending SOC order) with overlap removal."""
        try:
            # Use the specific merge logic with overlap removal
            merged_data = self.merge_datasets_with_overlap_removal(
                self.dataset1, self.dataset2, 'SOC'
            )
            if merged_data is None:
                return
            
            # Sort in descending order for discharging
            merged_data = merged_data.sort_values('SOC', ascending=False).reset_index(drop=True)
            self.merged_data = merged_data
            
            # Plot the merged and sorted data
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            ax.plot(merged_data['SOC'], merged_data['Voltage'], 'o-', 
                   markersize=5, linewidth=2, color='orange', label='Discharging Curve')
            
            ax.set_xlabel('State of Charge (SOC) [%]', fontsize=12)
            ax.set_ylabel('Voltage [V]', fontsize=12)
            ax.set_title('Discharging Analysis - Voltage vs SOC (Descending Order)', 
                        fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            # Add trend line
            z = np.polyfit(merged_data['SOC'], merged_data['Voltage'], 2)
            p = np.poly1d(z)
            ax.plot(merged_data['SOC'], p(merged_data['SOC']), '--', 
                   alpha=0.8, color='red', label='Trend')
            ax.legend()
            
            self.figure.tight_layout()
            self.canvas.draw()
            
            # Enable export button
            self.export_data_btn.setEnabled(True)
            
            # Show detailed merge information
            first_val = self.dataset1['SOC'].iloc[0]
            last_val = self.dataset1['SOC'].iloc[-1]
            min_val = min(first_val, last_val)
            max_val = max(first_val, last_val)
            
            QMessageBox.information(
                self, "Discharging Analysis Complete",
                f"Merge Details:\n"
                f"• Dataset A SOC range: {min_val:.2f}% to {max_val:.2f}%\n"
                f"• Removed overlapping data from Dataset B\n"
                f"• Final merged dataset: {len(merged_data)} data points\n"
                f"• Sorted in descending SOC order for discharging analysis"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Analysis Error", f"Error in discharging analysis:\n{str(e)}")
    
    def save_plot(self):
        """Save the current plot to file."""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Plot", "", 
                "PNG Files (*.png);;PDF Files (*.pdf);;SVG Files (*.svg);;All Files (*)"
            )
            
            if file_path:
                self.figure.savefig(file_path, dpi=300, bbox_inches='tight')
                QMessageBox.information(self, "Success", f"Plot saved to:\n{file_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Error saving plot:\n{str(e)}")
    
    def export_data(self):
        """Export the merged data to CSV."""
        try:
            if self.merged_data is None:
                QMessageBox.warning(self, "No Data", "No merged data to export. Run analysis first.")
                return
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Export Merged Data", "", "CSV Files (*.csv);;All Files (*)"
            )
            
            if file_path:
                if not file_path.lower().endswith('.csv'):
                    file_path += '.csv'
                
                self.merged_data.to_csv(file_path, index=False)
                QMessageBox.information(self, "Success", f"Data exported to:\n{file_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Error exporting data:\n{str(e)}")


def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Voltage vs SOC Analyzer")
    
    # Set application icon and style
    app.setStyle('Fusion')  # Modern look
    
    window = VoltageSOCAnalyzer()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()