import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

'''
   @Authors Eli Hofmann, Austin Jansky, Leo Dunor
   @Version 12-20-2024
   DESCRIPTION: A BASIC INTRUSION RESPONSE PROGRAM FOR ROBOTIC COMMANDS
   [DEFENSIVE NETWORK SECURITY]
'''

class Client:
   
   def __init__(self, root):
      self.ascii_title = '''                                                                                                  


  ______   ______   .___  ___. .___  ___.      ___      .__   __.  _______     .______       _______     _______..______     ______   .__   __.      _______. _______      
 /      | /  __  \  |   \/   | |   \/   |     /   \     |  \ |  | |       \    |   _  \     |   ____|   /       ||   _  \   /  __  \  |  \ |  |     /       ||   ____|     
|  ,----'|  |  |  | |  \  /  | |  \  /  |    /  ^  \    |   \|  | |  .--.  |   |  |_)  |    |  |__     |   (----`|  |_)  | |  |  |  | |   \|  |    |   (----`|  |__        
|  |     |  |  |  | |  |\/|  | |  |\/|  |   /  /_\  \   |  . `  | |  |  |  |   |      /     |   __|     \   \    |   ___/  |  |  |  | |  . `  |     \   \    |   __|       
|  `----.|  `--'  | |  |  |  | |  |  |  |  /  _____  \  |  |\   | |  '--'  |   |  |\  \----.|  |____.----)   |   |  |      |  `--'  | |  |\   | .----)   |   |  |____      
 \______| \______/  |__|  |__| |__|  |__| /__/     \__\ |__| \__| |_______/    | _| `._____||_______|_______/    | _|       \______/  |__| \__| |_______/    |_______|     
                                                                                                                                                                           
                                               _______.____    ____  _______.___________. _______ .___  ___.                                                               
                                              /       |\   \  /   / /       |           ||   ____||   \/   |                                                               
                                             |   (----` \   \/   / |   (----`---|  |----`|  |__   |  \  /  |                                                               
                                              \   \      \_    _/   \   \       |  |     |   __|  |  |\/|  |                                                               
                                          .----)   |       |  | .----)   |      |  |     |  |____ |  |  |  |                                                               
                                          |_______/        |__| |_______/       |__|     |_______||__|  |__|                                                               
      '''
      
      self.root = root
      self.root.title('Command Intrusion Response System')
      self.root.geometry('900x900')
      self.root.configure(bg='#C0C0C0')
      
      self.title_font = ('Comic Sans MS', 10, 'bold')
      self.normal_font = ('MS Sans Serif', 10)
      self.root.configure(relief=tk.RAISED, borderwidth=4)
      self.defcon_var = tk.StringVar(value='[DEFCON 5] ALL SYSTEMS ARE ONLINE AND IN STANDBY')
      self.defcon_label = None

      #EXECUTE DATABASE
      self.init_database()
      
      #EXECUTE UI
      self.create_ui()
   
   '''
      DATABASE METHOD THAT CONNECTS THE THE INTEGRATED PYTHON DATABASE AND IS USED TO STORE TECHNIQUES AND LOGS
   '''
   def init_database(self):
      
      #CONNECT TO DATABASE
      self.conn = sqlite3.connect('command_response.db')
      self.cursor = self.conn.cursor()

      #LOGIC OF TECHNIQUE TABLE
      self.cursor.execute('''
         CREATE TABLE IF NOT EXISTS intrusion_command_techniques (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            description TEXT,
            severity TEXT,
            response TEXT             
            )
      ''')

      #LOGIC OF LOG TABLE
      self.cursor.execute('''
         CREATE TABLE IF NOT EXISTS intrusion_command_events (
            id INTEGER PRIMARY KEY,
            timestamp DATETIME,
            source_ip TEXT,
            attack_type TEXT,
            severity TEXT,
            response TEXT,
            is_active BOOLEAN                
            )
      ''')

      self.prepopulate_techniques()

   '''
      PREPOPULATION METHOD THAT POPULATES A FEW INSTANCES OF TECHNIQUES FOR THE DATABASE
   '''
   def prepopulate_techniques(self):
      predefined = [
         {
            'name': 'MALWARE INJECTION',
            'description': 'INSERTING MALICIOUS CODE INTO A SYSTEM',
            'severity': 'HIGH',
            'response': 'ISOLATE SYSTEM, RUN FULL VIRUS SCAN, BLOCK SOURCE IP'
         },
         {
            'name': 'PASSWORD BRUTE FORCE',
            'description': 'ATTEMPTING MULTIPLE PASSWORDS TO GAIN ACCESS TO THE SYSTEM',
            'severity': 'CRITICAL',
            'response': 'TEMPORARILY LOCK ACCOUNT, IMPLEMENT IP BLOCK, RESET CREDENTIALS'
         },
         {
            'name': 'NETWORK SCANNING',
            'description': 'PROBING A NETWORK TO FIND POTENTIAL VULNERABILITIES',
            'severity': 'LOW',
            'response': 'LOG AND MONITOR SOURCE IP, UPDATE FIREWALL RULES'
         }
      ]

      #LOOP THAT POPULATES THE DATABASE WITH SAMPLE DATA
      for x in predefined:
         try:
            self.cursor.execute('''
               INSERT OR IGNORE INTO intrusion_command_techniques
               (name, description, severity, response)
               VALUES (?, ?, ?, ?)
            ''', (x['name'], x['description'], x['severity'], x['response']))
         except sqlite3.IntegrityError:
            pass

      self.conn.commit()
   
   '''
      CREATES HOME UI AND CONNECTS TO THE SIMULATION AND MANAGEMENT UI
   '''
   def create_ui(self):
      #DISPLAY PROGRAM TITLE
      title_label = tk.Label(self.root, text=self.ascii_title, font=('Courier', 6, 'bold'), fg='green', bg='#C0C0C0')
      title_label.pack(pady=10)
      self.root.grid_rowconfigure(0, weight=1)
      self.root.grid_columnconfigure(0, weight=1)
      
      #FRAMES
      notebook = ttk.Notebook(self.root, style='TNotebook')
      notebook.pack(expand=True, fill='both', padx=10, pady=10)
      
      #CUSTOM STYLE for NOTEBOOK
      style = ttk.Style()
      style.theme_use('default')
      style.configure('TNotebook', background='#C0C0C0', borderwidth=2, relief='raised')
      style.configure('TNotebook.Tab', background='#C0C0C0', foreground='black', font=self.normal_font, padding=[10, 5])
      style.map('TNotebook.Tab', background=[('selected', 'white')], expand=[('selected', [1, 1, 1, 1])])

      simulation_frame = tk.Frame(notebook, bg='#C0C0C0', relief=tk.RIDGE, borderwidth=2)
      notebook.add(simulation_frame, text='SIMULATION')
      simulation_frame.grid_rowconfigure(0, weight=1)
      simulation_frame.grid_columnconfigure(0, weight=1)

      technique_management_frame = tk.Frame(notebook, bg='#C0C0C0', relief=tk.RIDGE, borderwidth=2)
      notebook.add(technique_management_frame, text='TECHNIQUE MANAGEMENT')
      technique_management_frame.grid_rowconfigure(0, weight=1)
      technique_management_frame.grid_columnconfigure(0, weight=1)

      network_frame = tk.Frame(notebook, bg='#C0C0C0', relief=tk.RIDGE, borderwidth=2)
      notebook.add(network_frame, text='NETWORK VISUAL')
      network_frame.grid_rowconfigure(0, weight=1)
      network_frame.grid_columnconfigure(0, weight=1)
      
      self.create_simulation_ui(simulation_frame)
      self.create_technique_management_ui(technique_management_frame)
      self.create_network_visual_ui(network_frame)

   '''
      METHOD THAT GENERATES UI CONTROLS AND EVENTS FOR THE SIMULATION
   '''   
   def create_simulation_ui(self, parent):
      parent.configure(bg='#C0C0C0')
      
      #PARENT GRID
      parent.grid_rowconfigure(0, weight=0)
      parent.grid_rowconfigure(1, weight=0)
      parent.grid_rowconfigure(2, weight=0)
      parent.grid_rowconfigure(3, weight=0)
      parent.grid_columnconfigure(0, weight=1)
      
      
      #TITLE LABEL
      title_label = tk.Label(parent, text='NETWORK INTRUSION SIMULATOR', font=self.title_font, bg='#C0C0C0', fg='navy', anchor='center')
      title_label.grid(row=0, column=0,pady=10, sticky='ew')
      
      #DEFCON LABEL
      self.defcon_label = tk.Label(parent, textvariable=self.defcon_var, font=('Courier', 12, 'bold'), bg='#C0C0C0', fg='green', anchor='center')
      self.defcon_label.grid(row=1, column=0, pady=10, sticky='ew')

      control_frame = tk.Frame(parent, bg='#C0C0C0')
      control_frame.grid(row=2, column=0, pady=10, sticky='ew')
      control_frame.grid_columnconfigure(0, weight=1)
      control_frame.grid_columnconfigure(1, weight=1)

      #SELECT TECHNIQUE
      technique_label = tk.Label(control_frame, text='SELECT TECHNIQUE:', font=self.normal_font, bg='#C0C0C0')
      technique_label.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
    
      self.technique_var = tk.StringVar()
      techniques = self.get_technique_names()
      technique_dropdown = ttk.Combobox(control_frame, textvariable=self.technique_var, values=techniques, width=30, state='readonly', font=self.normal_font)
      technique_dropdown.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

      #START SIM
      self.start_button = tk.Button(control_frame, text='START SIMULATION', command=self.start_simulation, font=self.normal_font, relief=tk.RAISED, borderwidth=2)
      self.start_button.grid(row=2, column=0, padx=5, pady=5, sticky='ew')
      
      #STOP SIM
      self.stop_button = tk.Button(control_frame, text='STOP SIMULATION', command=self.stop_simulation, state=tk.DISABLED, font=self.normal_font, relief=tk.RAISED, borderwidth=2)
      self.stop_button.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

      #UPDATE LOG DISPLAY
      self.simulation_log = tk.Text(parent, height=40, width=80, wrap=tk.WORD, font=('Courier', 10), bg='white', fg='black')
      self.simulation_log.grid(row=3, column=0, pady=10, sticky='nsew')
      self.simulation_log.config(state=tk.DISABLED)

   '''
      METHOD THAT GENERATES THE MANAGEMENT UI CONTROLS AND EVENTS
   '''
   def create_technique_management_ui(self, parent):
      parent.configure(bg='#C0C0C0')
      
      #PARENT GRID
      parent.grid_rowconfigure(0, weight=0)
      parent.grid_rowconfigure(1, weight=0)
      parent.grid_rowconfigure(2, weight=0)
      parent.grid_rowconfigure(3, weight=1)
      parent.grid_columnconfigure(0, weight=1)
      
      
      title_label = tk.Label(parent, text='INTRUSION TECHNIQUE MANAGEMENT', font=self.title_font, bg='#C0C0C0', fg='navy')
      title_label.grid(row=1, column=0, pady=10, sticky='ew')

      input_frame = tk.Frame(parent, bg='#C0C0C0')
      input_frame.grid(row=1, column=0, pady=10, sticky='ew')
      
      input_frame.grid_columnconfigure(0, weight=1)
      input_frame.grid_columnconfigure(1, weight=3)
      
      #DEFAULT
      self.name_var = tk.StringVar(value='')
      self.description_var = tk.StringVar(value='')
      self.severity_var = tk.StringVar(value='LOW')
      self.response_var = tk.StringVar(value='')

      labels = ['TECHNIQUE NAME:', 'DESCRIPTION:', 'SEVERITY:', 'RESPONSE:']
      variables = [self.name_var, self.description_var, self.severity_var, self.response_var]
    
      #LABELS AND ENTRIES
      for i, (label_text, var) in enumerate(zip(labels, variables)):
         label = tk.Label(input_frame, text=label_text, font=self.normal_font, bg='#C0C0C0')
         label.grid(row=i, column=0, padx=5, pady=5, sticky='e')
        
         if label_text == 'SEVERITY:':
            severity_options = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
            entry = ttk.Combobox(input_frame, textvariable=var, values=severity_options, 
                                 width=27, state='readonly', font=self.normal_font)
         else:
            entry = tk.Entry(input_frame, width=30, textvariable=var, font=self.normal_font)
        
         entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')

      #ADD BUTTON
      add_button = tk.Button(parent, text='ADD TECHNIQUE', command=self.add_technique, font=self.normal_font, relief=tk.RAISED, borderwidth=2)
      add_button.grid(row=2, column=0, pady=10)

      #LIST
      self.techniques_list = tk.Text(parent, width=100, height=15, wrap=tk.WORD, font=('Courier', 10), bg='white', fg='black')
      self.techniques_list.grid(row=3, column=0, pady=10, sticky='nsew')
      

      #CLOSE
      close_button = tk.Button(parent, text='CLOSE', command=self.root.quit, font=self.normal_font, relief=tk.RAISED, borderwidth=2, bg='red', fg='white')
      close_button.grid(row=4, column=0, pady=10)
      
      #REFRESH
      self.refresh()
   
   '''
      GENERATE NETWORK VISUALS UI
   '''
   def create_network_visual_ui(self, parent):
      parent.configure(bg='#C0C0C0')
      
      #PARENT GRID
      parent.grid_rowconfigure(0, weight=0)
      parent.grid_rowconfigure(1, weight=0)
      parent.grid_rowconfigure(2, weight=1)
      parent.grid_rowconfigure(3, weight=0)
      parent.grid_columnconfigure(0, weight=1)
      
      #TITLE
      title_label = tk.Label(parent, text='NETWORK TOPOLOGY ANALYZER', font=self.title_font, bg='#C0C0C0', fg='navy')
      title_label.grid(row=0, column=0, pady=10, sticky='ew')
      
      #CONTROL FRAME
      control_frame = tk.Frame(parent, bg='#C0C0C0')
      control_frame.grid(row=1, column=0, pady=10, sticky='ew')
      control_frame.grid_columnconfigure(0, weight=1)
      
      
      #VISUAL FRAME
      visual_frame = tk.Frame(parent, bg='#C0C0C0')
      visual_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
      visual_frame.grid_rowconfigure(0, weight=1)
      visual_frame.grid_columnconfigure(0, weight=1)
      
      #LOG DISPLAY
      log_display = tk.Text(parent, height=8, width=30, wrap=tk.WORD, font=('Courier', 10), bg='white', fg='black')
      log_display.grid(row=3, column=0, pady=10, sticky='ew')
      
      #GENERATE NETWORK
      generate_btn = tk.Button(control_frame, text='GENERATE NETWORK', command=lambda: self.generate_network_topology(visual_frame, log_display), font=self.normal_font, relief=tk.RAISED, borderwidth=2)
      generate_btn.grid(row=0, column=0, padx=10)
      
      #CLOSE
      close_button = tk.Button(parent, text='CLOSE', command=self.root.quit, font=self.normal_font, relief=tk.RAISED, borderwidth=2, bg='red', fg='white')
      close_button.grid(row=4, column=0, pady=10)
      
   '''
      GENERATES GRAPH
   '''
   def generate_network_topology(self, visual_frame, log_display):
      #CLEAR PREVIOUS VISUAL
      for widget in visual_frame.winfo_children():
         widget.destroy()
      
      #CLEAR LOGS
      log_display.config(state=tk.NORMAL)
      log_display.delete(1.0, tk.END)
      
      #CREATE GRAPH
      graph = nx.barabasi_albert_graph(n=15, m=2)
      
      #CREATE FIGURE
      fig, ax = plt.subplots(figsize=(4, 2), facecolor='#C0C0C0')
      ax.set_facecolor('#C0C0C0')
      
      #DRAW NETWORK
      pos = nx.spring_layout(graph, seed=42)
      
      #NODES
      node_colors = ['blue', 'green', 'red', 'yellow']
      colors = [random.choice(node_colors) for _ in graph.nodes()]
      
      nx.draw_networkx_nodes(graph, pos, node_color=colors, node_size=200, ax=ax)
      
      #EDGES
      nx.draw_networkx_edges(graph, pos, alpha=0.5, ax=ax)
      
      #NODE LABELS
      nx.draw_networkx_labels(graph, pos, ax=ax)
      
      ax.set_title('NETWORK TOPOLOGY', fontsize=10)
      ax.axis('off')
      
      #EMBED
      canvas = FigureCanvasTkAgg(fig, master=visual_frame)
      canvas_widget = canvas.get_tk_widget()
      canvas_widget.grid(row=0, column=0, sticky='nsew')
      visual_frame.grid_rowconfigure(0, weight=1)
      visual_frame.grid_columnconfigure(0, weight=1)
      
      #NETWORK DETAIL LOG
      log_display.insert(tk.END, f'[NETWORK ANALYSIS]\n')
      log_display.insert(tk.END, f'TOTAL NODES: {len(graph.nodes())}\n')
      log_display.insert(tk.END, f'TOTAL CONNECTIONS: {len(graph.edges())}\n')
      log_display.config(state=tk.DISABLED)
   
   '''
      ADD METHOD THAT ADDS INPUT FROM MANAGEMENT UI INTO THE DATABASE FOR STORAGE
   '''
   def add_technique(self):
      #TAKES INPUT AND FORMATS IT IN DATABASE
      name = self.name_var.get().strip().upper()
      description = self.description_var.get().strip().upper()
      severity = self.severity_var.get().strip().upper()
      response = self.response_var.get().strip().upper()

      #SIMPLE VALIDATION
      if not all([name, description, severity, response]):
         messagebox.showerror('[ERROR]', 'PLEASE FILL IN ALL FIELDS')
         return
      
      try:
         self.cursor.execute('''
            INSERT OR REPLACE INTO intrusion_command_techniques
            (name, description, severity, response)
            VALUES (?, ?, ?, ?)
         ''', (name, description, severity, response))
         self.conn.commit()

         #CLEAR FIELDS TO DEFAULT
         self.name_var.set('')
         self.description_var.set('')
         self.severity_var.set('LOW')
         self.response_var.set('')

         #UPDATE DROPDOWN BOX IN SIM
         techniques = self.get_technique_names()
         notebook = self.root.winfo_children()[1]
         simulation_frame = notebook.winfo_children()[0]
         
         for widget in simulation_frame.winfo_children():
            if isinstance(widget, tk.Frame):
               for subwidget in widget.winfo_children():
                  if isinstance(subwidget, ttk.Combobox):
                     subwidget['values'] = techniques
                     break
         
         self.refresh()
         
         messagebox.showinfo('[SUCCESS]', 'SUCCESSFULLY ADDED TECHNIQUE')

      except sqlite3.IntegrityError:
         messagebox.showerror('[ERROR]', 'ERROR ADDING TECHNIQUE')
   
   '''
      METHOD THAT REFRESHES THE LIST SO IT UPDATES WHEN ADDIDNG NEW TECHNIQUES
   '''
   def refresh(self):
      self.techniques_list.config(state=tk.NORMAL)
      self.techniques_list.delete(1.0, tk.END)
      self.cursor.execute('SELECT name, description, severity, response FROM intrusion_command_techniques')
      intrusion_command_techniques = self.cursor.fetchall()

      #LOOP THAT FILLS DISPLAY WITH DATABASE INFO
      for name, description, severity, response in intrusion_command_techniques:
         self.techniques_list.insert(tk.END, f'{name} [{severity}]: {description} | Response: {response}\n\n')
      
      self.techniques_list.config(state=tk.DISABLED)
   
   '''
      HELPER METHOD THAT RANDOMLY GENERATES IP FOR SIM PURPOSES
   '''
   def generate_ip(self):
      return '.'.join(str(random.randint(0, 255)) for _ in range(4))
   
   '''
      HELPER METHOD THAT RETRIEVES ALL TECHNIQUES FROM DATABASE
   '''
   def get_technique_names(self):
      self.cursor.execute('SELECT name FROM intrusion_command_techniques')
      return [technique[0] for technique in self.cursor.fetchall()]
      
   '''
      METHOD THAT STARTS SIMULATION FOR SELECTED TECHNIQUE
   '''
   def start_simulation(self):
      technique = self.technique_var.get()
      
      #SIMPLE VALIDATION
      if not technique:
         messagebox.showerror('[ERROR]', 'SELECT A TECHNIQUE TO SIMULATE')
         return

      
      #UPDATE DEFCON
      self.cursor.execute('''
         SELECT severity, response
         FROM intrusion_command_techniques
         WHERE name = ?
      ''', (technique,))
      result = self.cursor.fetchone()
      severity, response = result if result else ('UNKOWN', 'NO RESPONSE DEFINED')
      
      if severity == 'LOW':
         defcon_level = '[DEFCON 4] ELEVATED THREAT'
         defcon_color = 'green'
      elif severity == 'MEDIUM':
         defcon_level = '[DEFCON 3] INCREASED READINESS'
         defcon_color = 'yellow'
      elif severity == 'HIGH':
         defcon_level = '[DEFCON 2] FURTHER ESCALATION'
         defcon_color = 'red'
      elif severity == 'CRITICAL':
         defcon_level = '[DEFCON 1] MAXIMUM ALERT'
         defcon_color = 'white'
      else:
         defcon_level = '[DEFCON 5] ALL SYSTEMS ARE ONLINE AND IN STANDBY'
         defcon_color = 'blue'
         
      '''
      CUSTOM MESSAGE BOX THAT SCALES
      '''
      def custom_messagebox(title, message, message_type='info'):
         root = tk.Tk()
         root.title(title)
         root.resizable(False, False)
      
         #MATCH SYSTEM
         root.configure(bg='SystemButtonFace')
      
         #FRAME
         frame = tk.Frame(root, padx=20, pady=20)
         frame.pack(fill='both', expand=True)
      
         #WORD WRAP
         msg_label = tk.Label(frame, text=message, wraplength=400, justify=tk.CENTER, font=('Arial', 10))
         msg_label.pack(pady=10)
      
      
         if message_type == 'question':
            #YES
            def on_yes():
               root.result = True
               root.destroy()
            #NO
            def on_no():
               root.result = False
               root.destroy()
         
            btn_frame = tk.Frame(frame)
            btn_frame.pack(pady=10)
         
            yes_btn = tk.Button(btn_frame, text='YES', command=on_yes, width=10)
            no_btn = tk.Button(btn_frame, text='NO', command=on_no, width=10)
         
            yes_btn.pack(padx=5)
            no_btn.pack(padx=5)
         
            #WAIT FOR RESPONSE
            root.wait_window(root)
            return root.result
         
      #PROMPT USER WITH THREATE DETAILS AND RESPONSES
      alert_message = (
         f"THREAT DETECTED!\n\n"
         f"TYPE: {technique}\n"
         f"SEVERITY: {severity}\n"
         f"RECOMMENDED RESPONSE: {response}\n\n"
         "ELIMINATE THREAT?"
      )

      
      
      #SET UP LOG
      self.simulation_log.config(state=tk.NORMAL)
      self.simulation_log.delete(1.0, tk.END)
      
      #INSERT START TIME
      self.simulation_log.insert(tk.END, f'STARTING SIMULATION: {technique}\n')
      self.simulation_log.insert(tk.END, f'TIMESTAMP: {datetime.now()}\n')
      
      #GENERATE RANDOM IP
      source_ip = self.generate_ip()
      self.simulation_log.insert(tk.END, f'SOURCE IP: {source_ip}\n')
      
      #DISPLAY RESPONSE
      self.simulation_log.insert(tk.END, f'SEVERITY: [{severity}]\n')
      self.simulation_log.insert(tk.END, f'RESPONSE: {response}\n')
      
      threat_response = custom_messagebox(defcon_level, alert_message, 'question')
      
      #FETCH RESPONSE AND SEVERITY
      self.cursor.execute('''
         SELECT severity, response 
         FROM intrusion_command_techniques 
         WHERE name = ?
      ''', (technique,))
      result = self.cursor.fetchone()
      severity, response = result if result else ('UNKNOWN', 'NO RESPONSE DEFINED')
      
      
      
      #INSERT EVENT INTO LOG TABLE
      try:
         if threat_response:
            self.simulation_log.insert(tk.END, 'THREAT STATUS: NEUTRALIZED\n')
            messagebox.showinfo(
               '[DEFCON 5] THREAT ELIMINATED',
               'THREAT HAS BEEN ELIMINATED\n'
               'ALL ISSUES RESOLVED')
            
            #LOGGED AS RESOLVED
            self.cursor.execute('''
               INSERT INTO intrusion_command_events
               (timestamp, source_ip, attack_type, severity, response, is_active)
               VALUES (?, ?, ?, ?, ?, ?)
            ''', (datetime.now(), source_ip, technique, severity, 'HANDLED', False))
            self.conn.commit()
            
            self.defcon_var.set('[DEFCON 5] ALL SYSTEMS ARE ONLINE AND IN STANDBY')
            self.defcon_label.config(fg='blue')
         else:
            #USER CHOSE NO
            are_you_positive = ('ARE YOU SURE YOU DONT WANT TO ACT?\n\n'
                                '[YES: THREAT STAYS ACTIVE] | [NO: THREAT IS NEUTRALIZED]\n')
            
            confirm_nonreact = custom_messagebox(defcon_level, are_you_positive, 'question'
               
            )
            
            #USER DECIDES TO ACT
            if not confirm_nonreact:
               self.simulation_log.insert(tk.END, 'THREAT STATUS: NEUTRALIZED\n')
               
               messagebox.showinfo(
               '[DEFCON 5] THREAT ELIMINATED',
               'THREAT HAS BEEN ELIMINATED\n'
               'ALL ISSUES RESOLVED')
               
               #LOGGED AS RESOLVED
               self.cursor.execute('''
                  INSERT INTO intrusion_command_events
                  (timestamp, source_ip, attack_type, severity, response, is_active)
                  VALUES (?, ?, ?, ?, ?, ?)
               ''', (datetime.now(), source_ip, technique, severity, 'HANDLED', True))
               self.conn.commit()
               
               self.defcon_var.set('[DEFCON 5] ALL SYSTEMS ARE ONLINE AND IN STANDBY')
               self.defcon_label.config(fg='blue')
            else:
               #USER CONFIRMS NONREACTION
               self.simulation_log.insert(tk.END, 'THREAT STATUS: ACTIVE\n')
               
               #LOGGED AS ACTIVE
               self.cursor.execute('''
                  INSERT INTO intrusion_command_events
                  (timestamp, source_ip, attack_type, severity, response, is_active)
                  VALUES (?, ?, ?, ?, ?, ?)
               ''', (datetime.now(), source_ip, technique, severity, 'IGNORED', True))
               self.conn.commit()
               
               self.defcon_var.set(defcon_level)
               self.defcon_label.config(fg=defcon_color)
      except sqlite3.Error as e:
         self.simulation_log.insert(tk.END, f'DATABASE ERROR: {str(e)}\n')
      
      self.simulation_log.config(state=tk.DISABLED)
      
      self.start_button.config(state=tk.DISABLED)
      self.stop_button.config(state=tk.NORMAL)

   '''
      METHOD THAT STOPS SIMULATION AND UPDATES LOG TABLE
   '''
   def stop_simulation(self):
      self.defcon_var.set('[DEFCON 5] ALL SYSTEMS ARE ONLINE AND IN STANDBY')
      self.defcon_label.config(fg='blue')
      
      
      
      self.simulation_log.config(state=tk.NORMAL)
      self.simulation_log.insert(tk.END, f'SIMULATION STOPPED: {datetime.now()}\n\n')
      self.simulation_log.config(state=tk.DISABLED)
      
      self.start_button.config(state=tk.NORMAL)
      self.stop_button.config(state=tk.DISABLED)

   '''
      CLOSE CONNECTION TO DATABASE
   '''
   def __del__(self):
      if hasattr(self, 'conn'):
         self.conn.close()

def main():
   root = tk.Tk()
   app = Client(root)
   root.mainloop()

if __name__ == '__main__':
   main()