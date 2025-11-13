import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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
        nav_bar = tk.Frame(self.root, bg=self.colors['primary'], height=60)
        nav_bar.pack(fill=tk.X)
        nav_bar.pack_propagate(False)
        
        nav_content = tk.Frame(nav_bar, bg=self.colors['primary'])
        nav_content.pack(expand=True)
        
        tk.Label(
            nav_content,
            text="Quality Monitor Pro",
            font=('Segoe UI', 22, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            nav_content,
            text="Environmental Analysis Platform",
            font=('Segoe UI', 10),
            bg=self.colors['primary'],
            fg='#bfdbfe'
        ).pack(side=tk.LEFT, padx=10)
        
        # Main Content Area
        content = tk.Frame(self.root, bg=self.colors['bg_main'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Control Panel Card
        control_card = self.create_card(content)
        control_card.pack(fill=tk.X, pady=(0, 15))
        
        # Title
        tk.Label(
            control_card,
            text="Analysis Configuration",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(anchor=tk.W, padx=25, pady=(20, 15))
        
        # Monitor Type Selection
        type_frame = tk.Frame(control_card, bg=self.colors['bg_card'])
        type_frame.pack(padx=25, pady=(0, 15))
        
        tk.Label(
            type_frame,
            text="Select Analysis Type:",
            font=('Segoe UI', 11),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary']
        ).pack(anchor=tk.W, pady=(0, 10))
        
        self.monitor_type = tk.StringVar(value="air")
        
        btn_container = tk.Frame(type_frame, bg=self.colors['bg_card'])
        btn_container.pack(anchor=tk.W)
        
        self.air_btn = self.create_toggle_button(
            btn_container, "Air Quality", "air"
        )
        self.air_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.water_btn = self.create_toggle_button(
            btn_container, "Water Quality", "water", selected=False
        )
        self.water_btn.pack(side=tk.LEFT)
        
        # Divider
        tk.Frame(control_card, bg=self.colors['border'], height=1).pack(fill=tk.X, padx=25, pady=15)
        
        # Import Button
        import_frame = tk.Frame(control_card, bg=self.colors['bg_card'])
        import_frame.pack(padx=25, pady=(0, 20))
        
        import_btn = tk.Button(
            import_frame,
            text="📂  Import CSV Data",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.colors['primary_hover'],
            activeforeground='white',
            relief=tk.FLAT,
            padx=40,
            pady=14,
            cursor='hand2',
            borderwidth=0,
            command=self.load_csv
        )
        import_btn.pack()
        
        # Results Section with Tabs
        tk.Label(
            content,
            text="Analysis Results",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary']
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Tab Container
        tab_container = tk.Frame(content, bg=self.colors['bg_main'])
        tab_container.pack(fill=tk.BOTH, expand=True)
        
        # Tab Buttons
        tab_buttons = tk.Frame(tab_container, bg=self.colors['bg_main'])
        tab_buttons.pack(fill=tk.X, pady=(0, 8))
        
        self.report_tab_btn = tk.Button(
            tab_buttons,
            text="📄 Report",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.colors['primary_hover'],
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor='hand2',
            borderwidth=0,
            command=lambda: self.switch_tab('report')
        )
        self.report_tab_btn.pack(side=tk.LEFT, padx=(0, 6))
        
        self.graph_tab_btn = tk.Button(
            tab_buttons,
            text="📊 Graphs",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            activebackground=self.colors['primary_hover'],
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor='hand2',
            borderwidth=0,
            command=lambda: self.switch_tab('graph')
        )
        self.graph_tab_btn.pack(side=tk.LEFT)
        
        # Results Card
        results_card = self.create_card(tab_container)
        results_card.pack(fill=tk.BOTH, expand=True)
        
        # Report Tab Content
        self.report_frame = tk.Frame(results_card, bg=self.colors['bg_card'])
        self.report_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(self.report_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_text = tk.Text(
            self.report_frame,
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
        
        # Graph Tab Content
        self.graph_frame = tk.Frame(results_card, bg=self.colors['bg_card'])
        
        self.current_tab = 'report'
        self.current_data = None
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
            font=('Segoe UI', 11),
            bg=self.colors['primary'] if selected else self.colors['bg_main'],
            fg='white' if selected else self.colors['text_secondary'],
            activebackground=self.colors['primary_hover'],
            activeforeground='white',
            relief=tk.FLAT,
            padx=30,
            pady=12,
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
    
    def switch_tab(self, tab_name):
        """Switch between report and graph tabs"""
        self.current_tab = tab_name
        
        if tab_name == 'report':
            self.report_tab_btn.config(bg=self.colors['primary'], fg='white')
            self.graph_tab_btn.config(bg=self.colors['bg_card'], fg=self.colors['text_secondary'])
            self.graph_frame.pack_forget()
            self.report_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        else:
            self.graph_tab_btn.config(bg=self.colors['primary'], fg='white')
            self.report_tab_btn.config(bg=self.colors['bg_card'], fg=self.colors['text_secondary'])
            self.report_frame.pack_forget()
            self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            if self.current_data is not None:
                print("Showing graphs...")  # Debug
                self.show_graphs()
            else:
                print("No data loaded yet")  # Debug
                tk.Label(
                    self.graph_frame,
                    text="No data loaded. Please import a CSV file first.",
                    font=('Segoe UI', 13),
                    bg=self.colors['bg_card'],
                    fg=self.colors['text_secondary']
                ).pack(expand=True, pady=100)
    
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
                self.current_data = df
                self.results_text.config(state=tk.NORMAL)
                self.analyze_data(df)
                self.results_text.config(state=tk.DISABLED)
                
                # Switch to report tab
                self.switch_tab('report')
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV: {str(e)}")
    
    def analyze_data(self, df):
        """Analyze the loaded data"""
        self.results_text.delete(1.0, tk.END)
        
        # Configure text tags with high contrast colors
        self.results_text.tag_config("title", foreground='#1e40af', font=('Segoe UI', 22, 'bold'))
        self.results_text.tag_config("heading", foreground='#0f172a', font=('Segoe UI', 16, 'bold'))
        self.results_text.tag_config("param_label", foreground='#334155', font=('Segoe UI', 12))
        self.results_text.tag_config("param_value", foreground='#1e40af', font=('Segoe UI', 12, 'bold'))
        self.results_text.tag_config("good", foreground='#059669', font=('Segoe UI', 13, 'bold'))
        self.results_text.tag_config("moderate", foreground='#d97706', font=('Segoe UI', 13, 'bold'))
        self.results_text.tag_config("bad", foreground='#dc2626', font=('Segoe UI', 13, 'bold'))
        self.results_text.tag_config("divider", foreground='#cbd5e1')
        
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
    
    def show_graphs(self):
        """Display graphs for the current data"""
        print("show_graphs called")  # Debug
        
        # Clear previous graphs
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        if self.current_data is None:
            print("No data available")  # Debug
            tk.Label(
                self.graph_frame,
                text="No data to display. Please import a CSV file first.",
                font=('Segoe UI', 12),
                bg=self.colors['bg_card'],
                fg=self.colors['text_secondary']
            ).pack(expand=True)
            return
        
        print(f"Data shape: {self.current_data.shape}")  # Debug
        print(f"Columns: {self.current_data.columns.tolist()}")  # Debug
        
        # Create scrollable canvas for graphs
        canvas = tk.Canvas(self.graph_frame, bg=self.colors['bg_card'], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.graph_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_card'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Generate graphs based on monitor type
        if self.monitor_type.get() == "air":
            self.create_air_quality_graphs(scrollable_frame)
        else:
            self.create_water_quality_graphs(scrollable_frame)
        
        # Update scroll region after graphs are created
        scrollable_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_air_quality_graphs(self, parent):
        """Create graphs for air quality data"""
        print("Creating air quality graphs")  # Debug
        df = self.current_data
        params = {k.lower(): k for k in df.columns}
        print(f"Parameters found: {list(params.keys())}")  # Debug
        
        plot_count = 0
        plots_data = []
        
        # Collect available parameters
        if 'pm2.5' in params or 'pm25' in params:
            col = params.get('pm2.5', params.get('pm25'))
            plots_data.append(('PM2.5 (µg/m³)', df[col], [0, 12, 35.4]))
            plot_count += 1
        
        if 'pm10' in params:
            plots_data.append(('PM10 (µg/m³)', df[params['pm10']], [0, 54, 154]))
            plot_count += 1
        
        if 'temp' in params or 'temperature' in params:
            col = params.get('temp', params.get('temperature'))
            plots_data.append(('Temperature (°C)', df[col], [10, 15, 25, 30]))
            plot_count += 1
        
        if 'humidity' in params:
            plots_data.append(('Humidity (%)', df[params['humidity']], [20, 30, 60, 70]))
            plot_count += 1
        
        if 'co2' in params:
            plots_data.append(('CO2 (ppm)', df[params['co2']], [0, 1000, 2000]))
            plot_count += 1
        
        if plot_count == 0:
            tk.Label(
                parent,
                text="No compatible parameters found for graphing.",
                font=('Segoe UI', 12),
                bg=self.colors['bg_card'],
                fg=self.colors['text_secondary']
            ).pack(expand=True, pady=50)
            return
        
        # Create figure with proper sizing
        rows = (plot_count + 1) // 2
        fig = Figure(figsize=(10, 4.5 * rows), facecolor=self.colors['bg_card'], dpi=100)
        
        for idx, (title, data, thresholds) in enumerate(plots_data):
            ax = fig.add_subplot(rows, 2, idx + 1)
            
            # Line plot
            readings = list(range(1, len(data) + 1))
            ax.plot(readings, data, marker='o', linewidth=2.5, markersize=10, color=self.colors['primary'])
            
            # Add threshold lines
            if len(thresholds) >= 3:
                ax.axhline(y=thresholds[1], color=self.colors['success'], linestyle='--', alpha=0.6, linewidth=2, label='Good')
                ax.axhline(y=thresholds[2], color=self.colors['warning'], linestyle='--', alpha=0.6, linewidth=2, label='Moderate')
            
            ax.set_title(title, fontsize=13, fontweight='bold', color=self.colors['text_primary'], pad=10)
            ax.set_xlabel('Reading #', fontsize=11, color=self.colors['text_secondary'])
            ax.set_ylabel('Value', fontsize=11, color=self.colors['text_secondary'])
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.legend(fontsize=9, loc='best')
            
            # Style
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.tick_params(colors=self.colors['text_secondary'], labelsize=10)
        
        fig.tight_layout(pad=2.5)
        
        # Embed in tkinter
        canvas_widget = FigureCanvasTkAgg(fig, parent)
        canvas_widget.draw()
        canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    def create_water_quality_graphs(self, parent):
        """Create graphs for water quality data"""
        df = self.current_data
        params = {k.lower(): k for k in df.columns}
        
        plot_count = 0
        plots_data = []
        
        # Collect available parameters
        if 'ph' in params:
            plots_data.append(('pH Level', df[params['ph']], [6.0, 6.5, 8.5, 9.0]))
            plot_count += 1
        
        if 'temp' in params or 'temperature' in params:
            col = params.get('temp', params.get('temperature'))
            plots_data.append(('Temperature (°C)', df[col], [5, 10, 25, 30]))
            plot_count += 1
        
        if 'do' in params or 'dissolved_oxygen' in params:
            col = params.get('do', params.get('dissolved_oxygen'))
            plots_data.append(('Dissolved Oxygen (mg/L)', df[col], [0, 4, 6]))
            plot_count += 1
        
        if 'turbidity' in params:
            plots_data.append(('Turbidity (NTU)', df[params['turbidity']], [0, 5, 25]))
            plot_count += 1
        
        if 'tds' in params:
            plots_data.append(('TDS (mg/L)', df[params['tds']], [0, 300, 600]))
            plot_count += 1
        
        if plot_count == 0:
            tk.Label(
                parent,
                text="No compatible parameters found for graphing.",
                font=('Segoe UI', 12),
                bg=self.colors['bg_card'],
                fg=self.colors['text_secondary']
            ).pack(expand=True, pady=50)
            return
        
        # Create figure with proper sizing
        rows = (plot_count + 1) // 2
        fig = Figure(figsize=(10, 4.5 * rows), facecolor=self.colors['bg_card'], dpi=100)
        
        for idx, (title, data, thresholds) in enumerate(plots_data):
            ax = fig.add_subplot(rows, 2, idx + 1)
            
            # Line plot
            readings = list(range(1, len(data) + 1))
            ax.plot(readings, data, marker='o', linewidth=2.5, markersize=10, color=self.colors['primary'])
            
            # Add threshold lines
            if len(thresholds) >= 3:
                if 'pH' in title:
                    ax.axhline(y=thresholds[1], color=self.colors['success'], linestyle='--', alpha=0.6, linewidth=2, label='Good Min')
                    ax.axhline(y=thresholds[2], color=self.colors['success'], linestyle='--', alpha=0.6, linewidth=2, label='Good Max')
                else:
                    ax.axhline(y=thresholds[1], color=self.colors['success'], linestyle='--', alpha=0.6, linewidth=2, label='Good')
                    ax.axhline(y=thresholds[2], color=self.colors['warning'], linestyle='--', alpha=0.6, linewidth=2, label='Moderate')
            
            ax.set_title(title, fontsize=13, fontweight='bold', color=self.colors['text_primary'], pad=10)
            ax.set_xlabel('Reading #', fontsize=11, color=self.colors['text_secondary'])
            ax.set_ylabel('Value', fontsize=11, color=self.colors['text_secondary'])
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.legend(fontsize=9, loc='best')
            
            # Style
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.tick_params(colors=self.colors['text_secondary'], labelsize=10)
        
        fig.tight_layout(pad=2.5)
        
        # Embed in tkinter
        canvas_widget = FigureCanvasTkAgg(fig, parent)
        canvas_widget.draw()
        canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=15, pady=15)


if __name__ == "__main__":
    root = tk.Tk()
    app = QualityMonitorPro(root)
    root.mainloop()
