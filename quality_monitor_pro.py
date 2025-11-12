import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

class QualityMonitorPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Quality Monitor Pro")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f8fafc')
        
        # Professional color palette
        self.colors = {
            'primary': '#2563eb',
            'primary_hover': '#1d4ed8',
            'secondary': '#64748b',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'bg_main': '#f8fafc',
            'bg_card': '#ffffff',
            'text_primary': '#0f172a',
            'text_secondary': '#475569',
            'text_muted': '#94a3b8',
            'border': '#e2e8f0'
        }
        
        self.create_ui()
    
    def create_ui(self):
        # Top Navigation Bar
        nav_bar = tk.Frame(self.root, bg=self.colors['primary'], height=70)
        nav_bar.pack(fill=tk.X)
        nav_bar.pack_propagate(False)
        
        nav_content = tk.Frame(nav_bar, bg=self.colors['primary'])
        nav_content.pack(expand=True)
        
        tk.Label(
            nav_content,
            text="Quality Monitor Pro",
            font=('Segoe UI', 24, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            nav_content,
            text="Environmental Analysis Platform",
            font=('Segoe UI', 11),
            bg=self.colors['primary'],
            fg='#bfdbfe'
        ).pack(side=tk.LEFT, padx=10)
        
        # Main Content Area
        content = tk.Frame(self.root, bg=self.colors['bg_main'])
        content.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Control Panel Card
        control_card = self.create_card(content)
        control_card.pack(fill=tk.X, pady=(0, 25))
        
        # Title
        tk.Label(
            control_card,
            text="Analysis Configuration",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(anchor=tk.W, padx=30, pady=(25, 20))
        
        # Monitor Type Selection
        type_frame = tk.Frame(control_card, bg=self.colors['bg_card'])
        type_frame.pack(padx=30, pady=(0, 20))
        
        tk.Label(
            type_frame,
            text="Select Analysis Type:",
            font=('Segoe UI', 12),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary']
        ).pack(anchor=tk.W, pady=(0, 12))
        
        self.monitor_type = tk.StringVar(value="air")
        
        btn_container = tk.Frame(type_frame, bg=self.colors['bg_card'])
        btn_container.pack(anchor=tk.W)
        
        self.air_btn = self.create_toggle_button(
            btn_container, "Air Quality", "air"
        )
        self.air_btn.pack(side=tk.LEFT, padx=(0, 12))
        
        self.water_btn = self.create_toggle_button(
            btn_container, "Water Quality", "water", selected=False
        )
        self.water_btn.pack(side=tk.LEFT)
        
        # Divider
        tk.Frame(control_card, bg=self.colors['border'], height=1).pack(fill=tk.X, padx=30, pady=20)
        
        # Import Button
        import_frame = tk.Frame(control_card, bg=self.colors['bg_card'])
        import_frame.pack(padx=30, pady=(0, 25))
        
        import_btn = tk.Button(
            import_frame,
            text="📂  Import CSV Data",
            font=('Segoe UI', 13, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.colors['primary_hover'],
            activeforeground='white',
            relief=tk.FLAT,
            padx=45,
            pady=16,
            cursor='hand2',
            borderwidth=0,
            command=self.load_csv
        )
        import_btn.pack()
        
        # Results Section
        tk.Label(
            content,
            text="Analysis Results",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary']
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # Results Card
        results_card = self.create_card(content)
        results_card.pack(fill=tk.BOTH, expand=True)
        
        # Text widget with scrollbar
        text_container = tk.Frame(results_card, bg=self.colors['bg_card'])
        text_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(text_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_text = tk.Text(
            text_container,
            font=('Segoe UI', 11),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            relief=tk.FLAT,
            padx=25,
            pady=20,
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD,
            borderwidth=0
        )
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.results_text.yview)
        
        self.show_welcome()
    
    def create_card(self, parent):
        """Create a card-style frame"""
        card = tk.Frame(
            parent,
            bg=self.colors['bg_card'],
            relief=tk.FLAT,
            highlightbackground=self.colors['border'],
            highlightthickness=1
        )
        return card
    
    def create_toggle_button(self, parent, text, value, selected=True):
        """Create a toggle button"""
        btn = tk.Button(
            parent,
            text=text,
            font=('Segoe UI', 12),
            bg=self.colors['primary'] if selected else self.colors['bg_main'],
            fg='white' if selected else self.colors['text_secondary'],
            activebackground=self.colors['primary_hover'],
            activeforeground='white',
            relief=tk.FLAT,
            padx=35,
            pady=14,
            cursor='hand2',
            borderwidth=0,
            command=lambda: self.select_type(value)
        )
        return btn
    
    def select_type(self, type_val):
        """Handle monitor type selection"""
        self.monitor_type.set(type_val)
        if type_val == "air":
            self.air_btn.config(bg=self.colors['primary'], fg='white')
            self.water_btn.config(bg=self.colors['bg_main'], fg=self.colors['text_secondary'])
        else:
            self.water_btn.config(bg=self.colors['primary'], fg='white')
            self.air_btn.config(bg=self.colors['bg_main'], fg=self.colors['text_secondary'])
    
    def show_welcome(self):
        """Display welcome message"""
        welcome = """Welcome to Quality Monitor Pro

Get started in three simple steps:

1. Select Analysis Type
   Choose between Air Quality or Water Quality monitoring based on your data

2. Import Your Data
   Click 'Import CSV Data' to load your measurement file
   
3. Review Results
   View comprehensive analysis with quality ratings and detailed metrics


Sample CSV files are included for testing. The system supports various parameters
including temperature, humidity, pH, dissolved oxygen, turbidity, and more.
        """
        self.results_text.insert(tk.END, welcome)
        self.results_text.config(state=tk.DISABLED)
    
    def load_csv(self):
        """Load and analyze CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                df = pd.read_csv(file_path)
                self.results_text.config(state=tk.NORMAL)
                self.analyze_data(df)
                self.results_text.config(state=tk.DISABLED)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV: {str(e)}")
    
    def analyze_data(self, df):
        """Analyze the loaded data"""
        self.results_text.delete(1.0, tk.END)
        
        # Configure text tags
        self.results_text.tag_config("title", foreground=self.colors['primary'], font=('Segoe UI', 20, 'bold'))
        self.results_text.tag_config("heading", foreground=self.colors['text_primary'], font=('Segoe UI', 15, 'bold'))
        self.results_text.tag_config("param_label", foreground=self.colors['text_secondary'], font=('Segoe UI', 11))
        self.results_text.tag_config("param_value", foreground=self.colors['primary'], font=('Segoe UI', 11, 'bold'))
        self.results_text.tag_config("good", foreground=self.colors['success'], font=('Segoe UI', 12, 'bold'))
        self.results_text.tag_config("moderate", foreground=self.colors['warning'], font=('Segoe UI', 12, 'bold'))
        self.results_text.tag_config("bad", foreground=self.colors['danger'], font=('Segoe UI', 12, 'bold'))
        self.results_text.tag_config("divider", foreground=self.colors['border'])
        
        if self.monitor_type.get() == "air":
            self.analyze_air_quality(df)
        else:
            self.analyze_water_quality(df)
    
    def analyze_air_quality(self, df):
        """Analyze air quality data"""
        self.results_text.insert(tk.END, "Air Quality Analysis Report\n\n", "title")
        
        for index, row in df.iterrows():
            self.results_text.insert(tk.END, f"Reading #{index + 1}\n", "heading")
            self.results_text.insert(tk.END, "─" * 90 + "\n\n", "divider")
            
            params = {k.lower(): v for k, v in row.items()}
            scores = []
            
            # PM2.5
            if 'pm2.5' in params or 'pm25' in params:
                pm25 = params.get('pm2.5', params.get('pm25', 0))
                self.results_text.insert(tk.END, "PM2.5: ", "param_label")
                self.results_text.insert(tk.END, f"{pm25} µg/m³", "param_value")
                self.results_text.insert(tk.END, "  →  ", "param_label")
                if pm25 <= 12:
                    self.results_text.insert(tk.END, "✓ Good\n", "good")
                    scores.append(1)
                elif pm25 <= 35.4:
                    self.results_text.insert(tk.END, "⚠ Moderate\n", "moderate")
                    scores.append(2)
                else:
                    self.results_text.insert(tk.END, "✗ Poor\n", "bad")
                    scores.append(3)
            
            # PM10
            if 'pm10' in params:
                pm10 = params['pm10']
                self.results_text.insert(tk.END, "PM10: ", "param_label")
                self.results_text.insert(tk.END, f"{pm10} µg/m³", "param_value")
                self.results_text.insert(tk.END, "  →  ", "param_label")
                if pm10 <= 54:
                    self.results_text.insert(tk.END, "✓ Good\n", "good")
                    scores.append(1)
                elif pm10 <= 154:
                    self.results_text.insert(tk.END, "⚠ Moderate\n", "moderate")
                    scores.append(2)
                else:
                    self.results_text.insert(tk.END, "✗ Poor\n", "bad")
                    scores.append(3)
            
            # Temperature
            if 'temp' in params or 'temperature' in params:
                temp = params.get('temp', params.get('temperature', 0))
                self.results_text.insert(tk.END, "Temperature: ", "param_label")
                self.results_text.insert(tk.END, f"{temp}°C", "param_value")
                self.results_text.insert(tk.END, "  →  ", "param_label")
                if 15 <= temp <= 25:
                    self.results_text.insert(tk.END, "✓ Good\n", "good")
                    scores.append(1)
                elif (10 <= temp < 15) or (25 < temp <= 30):
                    self.results_text.insert(tk.END, "⚠ Moderate\n", "moderate")
                    scores.append(2)
                else:
                    self.results_text.insert(tk.END, "✗ Poor\n", "bad")
                    scores.append(3)
            
            # Humidity
            if 'humidity' in params:
                humidity = params['humidity']
                self.results_text.insert(tk.END, "Humidity: ", "param_label")
                self.results_text.insert(tk.END, f"{humidity}%", "param_value")
                self.results_text.insert(tk.END, "  →  ", "param_label")
                if 30 <= humidity <= 60:
                    self.results_text.insert(tk.END, "✓ Good\n", "good")
                    scores.append(1)
                elif (20 <= humidity < 30) or (60 < humidity <= 70):
                    self.results_text.insert(tk.END, "⚠ Moderate\n", "moderate")
                    scores.append(2)
                else:
                    self.results_text.insert(tk.END, "✗ Poor\n", "bad")
                    scores.append(3)
            
            # CO2
            if 'co2' in params:
                co2 = params['co2']
                self.results_text.insert(tk.END, "CO2: ", "param_label")
                self.results_text.insert(tk.END, f"{co2} ppm", "param_value")
                self.results_text.insert(tk.END, "  →  ", "param_label")
                if co2 <= 1000:
                    self.results_text.insert(tk.END, "✓ Good\n", "good")
                    scores.append(1)
                elif co2 <= 2000:
                    self.results_text.insert(tk.END, "⚠ Moderate\n", "moderate")
                    scores.append(2)
                else:
                    self.results_text.insert(tk.END, "✗ Poor\n", "bad")
                    scores.append(3)
            
            # Overall Assessment
            if scores:
                avg_score = sum(scores) / len(scores)
                self.results_text.insert(tk.END, "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n", "divider")
                self.results_text.insert(tk.END, "Overall Air Quality: ", "heading")
                if avg_score <= 1.5:
                    self.results_text.insert(tk.END, "✓ GOOD\n", "good")
                elif avg_score <= 2.5:
                    self.results_text.insert(tk.END, "⚠ MODERATE\n", "moderate")
                else:
                    self.results_text.insert(tk.END, "✗ POOR\n", "bad")
                self.results_text.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n", "divider")
    
    def analyze_water_quality(self, df):
        """Analyze water quality data"""
        self.results_text.insert(tk.END, "Water Quality Analysis Report\n\n", "title")
        
        for index, row in df.iterrows():
            self.results_text.insert(tk.END, f"Reading #{index + 1}\n", "heading")
            self.results_text.insert(tk.END, "─" * 90 + "\n\n", "divider")
            
            params = {k.lower(): v for k, v in row.items()}
            scores = []
            
            # pH
            if 'ph' in params:
                ph = params['ph']
                self.results_text.insert(tk.END, "pH Level: ", "param_label")
                self.results_text.insert(tk.END, f"{ph}", "param_value")
                self.results_text.insert(tk.END, "  →  ", "param_label")
                if 6.5 <= ph <= 8.5:
                    self.results_text.insert(tk.END, "✓ Good\n", "good")
                    scores.append(1)
                elif (6.0 <= ph < 6.5) or (8.5 < ph <= 9.0):
                    self.results_text.insert(tk.END, "⚠ Moderate\n", "moderate")
                    scores.append(2)
                else:
                    self.results_text.insert(tk.END, "✗ Poor\n", "bad")
                    scores.append(3)
            
            # Temperature
            if 'temp' in params or 'temperature' in params:
                temp = params.get('temp', params.get('temperature', 0))
                self.results_text.insert(tk.END, "Temperature: ", "param_label")
                self.results_text.insert(tk.END, f"{temp}°C", "param_value")
                self.results_text.insert(tk.END, "  →  ", "param_label")
                if 10 <= temp <= 25:
                    self.results_text.insert(tk.END, "✓ Good\n", "good")
                    scores.append(1)
                elif (5 <= temp < 10) or (25 < temp <= 30):
                    self.results_text.insert(tk.END, "⚠ Moderate\n", "moderate")
                    scores.append(2)
                else:
                    self.results_text.insert(tk.END, "✗ Poor\n", "bad")
                    scores.append(3)
            
            # Dissolved Oxygen
            if 'do' in params or 'dissolved_oxygen' in params:
                do = params.get('do', params.get('dissolved_oxygen', 0))
                self.results_text.insert(tk.END, "Dissolved Oxygen: ", "param_label")
                self.results_text.insert(tk.END, f"{do} mg/L", "param_value")
                self.results_text.insert(tk.END, "  →  ", "param_label")
                if do >= 6:
                    self.results_text.insert(tk.END, "✓ Good\n", "good")
                    scores.append(1)
                elif 4 <= do < 6:
                    self.results_text.insert(tk.END, "⚠ Moderate\n", "moderate")
                    scores.append(2)
                else:
                    self.results_text.insert(tk.END, "✗ Poor\n", "bad")
                    scores.append(3)
            
            # Turbidity
            if 'turbidity' in params:
                turbidity = params['turbidity']
                self.results_text.insert(tk.END, "Turbidity: ", "param_label")
                self.results_text.insert(tk.END, f"{turbidity} NTU", "param_value")
                self.results_text.insert(tk.END, "  →  ", "param_label")
                if turbidity <= 5:
                    self.results_text.insert(tk.END, "✓ Good\n", "good")
                    scores.append(1)
                elif turbidity <= 25:
                    self.results_text.insert(tk.END, "⚠ Moderate\n", "moderate")
                    scores.append(2)
                else:
                    self.results_text.insert(tk.END, "✗ Poor\n", "bad")
                    scores.append(3)
            
            # TDS
            if 'tds' in params:
                tds = params['tds']
                self.results_text.insert(tk.END, "TDS: ", "param_label")
                self.results_text.insert(tk.END, f"{tds} mg/L", "param_value")
                self.results_text.insert(tk.END, "  →  ", "param_label")
                if tds <= 300:
                    self.results_text.insert(tk.END, "✓ Good\n", "good")
                    scores.append(1)
                elif tds <= 600:
                    self.results_text.insert(tk.END, "⚠ Moderate\n", "moderate")
                    scores.append(2)
                else:
                    self.results_text.insert(tk.END, "✗ Poor\n", "bad")
                    scores.append(3)
            
            # Overall Assessment
            if scores:
                avg_score = sum(scores) / len(scores)
                self.results_text.insert(tk.END, "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n", "divider")
                self.results_text.insert(tk.END, "Overall Water Quality: ", "heading")
                if avg_score <= 1.5:
                    self.results_text.insert(tk.END, "✓ GOOD\n", "good")
                elif avg_score <= 2.5:
                    self.results_text.insert(tk.END, "⚠ MODERATE\n", "moderate")
                else:
                    self.results_text.insert(tk.END, "✗ POOR\n", "bad")
                self.results_text.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n", "divider")

if __name__ == "__main__":
    root = tk.Tk()
    app = QualityMonitorPro(root)
    root.mainloop()
