import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random
from datetime import datetime

'''
   @Author Eli Hofmann
   @Version 12-20-2024
   DESCRIPTION: A BASIC INTRUSION RESPONSE PROGRAM FOR ROBOTIC COMMANDS
   [DEFENSIVE NETWORK SECURITY]
'''

class Client:
   
   def __init__(self, root):
      self.ascii_title = '''

  ______   ______   .___  ___. .___  ___.      ___      .__   __.  _______      __  .__   __. .___________..______       __    __       _______. __    ______   .__   __.
 /      | /  __  \  |   \/   | |   \/   |     /   \     |  \ |  | |       \    |  | |  \ |  | |           ||   _  \     |  |  |  |     /       ||  |  /  __  \  |  \ |  |
|  ,----'|  |  |  | |  \  /  | |  \  /  |    /  ^  \    |   \|  | |  .--.  |   |  | |   \|  | `---|  |----`|  |_)  |    |  |  |  |    |   (----`|  | |  |  |  | |   \|  |
|  |     |  |  |  | |  |\/|  | |  |\/|  |   /  /_\  \   |  . `  | |  |  |  |   |  | |  . `  |     |  |     |      /     |  |  |  |     \   \    |  | |  |  |  | |  . `  |
|  `----.|  `--'  | |  |  |  | |  |  |  |  /  _____  \  |  |\   | |  '--'  |   |  | |  |\   |     |  |     |  |\  \----.|  `--'  | .----)   |   |  | |  `--'  | |  |\   |
 \______| \______/  |__|  |__| |__|  |__| /__/     \__\ |__| \__| |_______/    |__| |__| \__|     |__|     | _| `._____| \______/  |_______/    |__|  \______/  |__| \__|
                                                                                                                                                                         
.______       _______      _______..______     ______   .__   __.      _______. _______         _______.____    ____  _______..___________. _______ .___  ___.           
|   _  \     |   ____|    /       ||   _  \   /  __  \  |  \ |  |     /       ||   ____|       /       |\   \  /   / /       ||           ||   ____||   \/   |           
|  |_)  |    |  |__      |   (----`|  |_)  | |  |  |  | |   \|  |    |   (----`|  |__         |   (----` \   \/   / |   (----``---|  |----`|  |__   |  \  /  |           
|      /     |   __|      \   \    |   ___/  |  |  |  | |  . `  |     \   \    |   __|         \   \      \_    _/   \   \        |  |     |   __|  |  |\/|  |           
|  |\  \----.|  |____ .----)   |   |  |      |  `--'  | |  |\   | .----)   |   |  |____    .----)   |       |  | .----)   |       |  |     |  |____ |  |  |  |           
| _| `._____||_______||_______/    | _|       \______/  |__| \__| |_______/    |_______|   |_______/        |__| |_______/        |__|     |_______||__|  |__|           

      '''

      
      self.ascii_art = ''' 
        	
         ______________
        /             /|
       /             / |
      /____________ /  |
     | ___________ |   |
     ||           ||   |
     ||           ||   |
     ||           ||   |
     ||___________||   |
     |   _______   |  /
    /|  (_______)  | /
   ( |_____________|/
    \\
.=======================.
| ::::::::::::::::  ::: |
| ::::::::::::::[]  ::: |
|   -----------     ::: |
`-----------------------'

      '''
      
      self.root = root
      self.root.title('Command Intrusion Response System')
      self.root.geometry('900x850')
      self.root.configure(bg='#C0C0C0')
      
      self.title_font = ('Comic Sans MS', 12, 'bold')
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
            response TEXT                
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

      technique_management_frame = tk.Frame(notebook, bg='#C0C0C0', relief=tk.RIDGE, borderwidth=2)
      notebook.add(technique_management_frame, text='TECHNIQUE MANAGEMENT')

      
      self.create_simulation_ui(simulation_frame)
      self.create_technique_management_ui(technique_management_frame)

   '''
      METHOD THAT GENERATES UI CONTROLS AND EVENTS FOR THE SIMULATION
   '''   
   def create_simulation_ui(self, parent):
      parent.configure(bg='#C0C0C0')
      
      #SPLIT FRAME FOR ART
      left_frame = tk.Frame(parent, bg='#C0C0C0', width=300)
      left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
      left_frame.pack_propagate(False)
      
      right_frame = tk.Frame(parent, bg='#C0C0C0')
      right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)
      
      #DISPLAY ART
      ascii_art_label = tk.Label(left_frame, text=self.ascii_art, font=('Courier', 14), fg='black', bg='#C0C0C0', justify=tk.LEFT)
      ascii_art_label.pack(pady=20)
      
      #TITLE LABEL
      title_label = tk.Label(parent, text='NETWORK INTRUSION SIMULATOR', font=self.title_font, bg='#C0C0C0', fg='navy')
      title_label.pack(pady=10)
      
      #DEFCON LABEL
      self.defcon_label = tk.Label(parent, textvariable=self.defcon_var, font=('Courier', 12, 'bold'), bg='#C0C0C0', fg='green')
      self.defcon_label.pack(pady=5)

      control_frame = tk.Frame(parent, bg='#C0C0C0')
      control_frame.pack(pady=10)

      #SELECT TECHNIQUE
      tk.Label(control_frame, text='SELECT TECHNIQUE:', font=self.normal_font, bg='#C0C0C0').grid(row=0, column=0, padx=5, pady=5)
      self.technique_var = tk.StringVar()
      techniques = self.get_technique_names()
      technique_dropdown = ttk.Combobox(control_frame, textvariable=self.technique_var, values=techniques, width=30, state='readonly', font=self.normal_font)
      technique_dropdown.grid(row=0, column=1, padx=5, pady=5)

      #START SIM
      self.start_button = tk.Button(control_frame, text='START SIMULATION', command=self.start_simulation, font=self.normal_font, relief=tk.RAISED, borderwidth=2)
      self.start_button.grid(row=1, column=0, padx=5, pady=5)

      #STOP SIM
      self.stop_button = tk.Button(control_frame, text='STOP SIMULATION', command=self.stop_simulation, state=tk.DISABLED, font=self.normal_font, relief=tk.RAISED, borderwidth=2)
      self.stop_button.grid(row=1, column=1, padx=5, pady=5)

      #UPDATE LOG DISPLAY
      self.simulation_log = tk.Text(parent, height=50, width=90, wrap=tk.WORD, font=('Courier', 10), bg='white', fg='black')
      self.simulation_log.pack(pady=10)
      self.simulation_log.config(state=tk.DISABLED)
      
      #CLOSE
      close_button = tk.Button(left_frame, text='CLOSE', command=self.root.quit, font=self.normal_font, relief=tk.RAISED, borderwidth=2, bg='red', fg='white')
      close_button.pack(side=tk.BOTTOM, pady=5)

   '''
      METHOD THAT GENERATES THE MANAGEMENT UI CONTROLS AND EVENTS
   '''
   def create_technique_management_ui(self, parent):
      parent.configure(bg='#C0C0C0')
      
      title_label = tk.Label(parent, text='INTRUSION TECHNIQUE MANAGEMENT', font=self.title_font, bg='#C0C0C0', fg='navy')
      title_label.pack(pady=10)

      input_frame = tk.Frame(parent, bg='#C0C0C0')
      input_frame.pack(pady=10)

      #TECHNIQUE NAME
      tk.Label(input_frame, text='TECHNIQUE NAME:', font=self.normal_font, bg='#C0C0C0').grid(row=0, column=0, padx=5, pady=5)
      self.name_var = tk.StringVar()
      name_entry = tk.Entry(input_frame, width=30, textvariable=self.name_var, font=self.normal_font)
      name_entry.grid(row=0, column=1, padx=5, pady=5)

      #DESCRIPTION
      tk.Label(input_frame, text='DESCRIPTION:', font=self.normal_font, bg='#C0C0C0').grid(row=1, column=0, padx=5, pady=5)
      self.description_var = tk.StringVar()
      description_entry = tk.Entry(input_frame, width=30, textvariable=self.description_var, font=self.normal_font)
      description_entry.grid(row=1, column=1, padx=5, pady=5)

      #SEVERITY
      tk.Label(input_frame, text='SEVERITY:', font=self.normal_font, bg='#C0C0C0').grid(row=2, column=0, padx=5, pady=5)
      self.severity_var = tk.StringVar(value='LOW')
      severity_options = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
      severity_dropdown = ttk.Combobox(input_frame, textvariable=self.severity_var, values=severity_options, width=27, state='readonly', font=self.normal_font)
      severity_dropdown.grid(row=2, column=1, padx=5, pady=5)

      #RESPONSE
      tk.Label(input_frame, text='RESPONSE:', font=self.normal_font, bg='#C0C0C0').grid(row=3, column=0, padx=5, pady=5)
      self.response_var = tk.StringVar()
      response_entry = tk.Entry(input_frame, width=30, textvariable=self.response_var, font=self.normal_font)
      response_entry.grid(row=3, column=1, padx=5, pady=5)

      #ADD BUTTON
      add_button = tk.Button(parent, text='ADD TECHNIQUE', command=self.add_technique, font=self.normal_font, relief=tk.RAISED, borderwidth=2)
      add_button.pack(pady=10)

      #LIST
      self.techniques_list = tk.Text(parent, width=100, height=15, wrap=tk.WORD, font=('Courier', 10), bg='white', fg='black')
      self.techniques_list.pack(pady=10)

      #CLOSE
      close_button = tk.Button(parent, text='CLOSE', command=self.root.quit, font=self.normal_font, relief=tk.RAISED, borderwidth=2, bg='red', fg='white')
      close_button.pack(side=tk.BOTTOM, pady=10)
      
      #REFRESH
      self.refresh()
   

   '''
      ADD METHOD THAT ADDS INPUT FROM MANAGEMENT UI INTO THE DATABSE FOR STORAGE
   '''
   def add_technique(self):
      #TAKES INPUT AND FORMATS IT IN DATABASE
      name = self.name_var.get().strip().upper()
      description = self.description_var.get().strip().upper()
      severity = self.severity_var.get().strip().upper()
      response = self.response_var.get().strip().upper()

      #SIMPLE VALIDATION
      if not name or not description or not response:
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
         self.defcon_var.set('[DEFCON 4] ELEVATED THREAT')
         self.defcon_label.config(fg='green')
      elif severity == 'MEDIUM':
         self.defcon_var.set('[DEFCON 3] INCREASED READINESS')
         self.defcon_label.config(fg='yellow')
      elif severity == 'HIGH':
         self.defcon_var.set('[DEFCON 2] FURTHER ESCALATION')
         self.defcon_label.config(fg='red')
      elif severity == 'CRITICAL':
         self.defcon_var.set('[DEFCON 1] MAXIMUM ALERT')
         self.defcon_label.config(fg='white')
      else:
         self.defcon_var.set('[DEFCON 5] ALL SYSTEMS ARE ONLINE AND IN STANDBY')
         self.defcon_label.config(fg='blue')
         
      
      self.simulation_log.config(state=tk.NORMAL)
      self.simulation_log.delete(1.0, tk.END)
      
      self.simulation_log.insert(tk.END, f'STARTING SIMULATION: {technique}\n')
      self.simulation_log.insert(tk.END, f'TIMESTAMP: {datetime.now()}\n')
      
      #GENERATE RANDOM IP
      source_ip = self.generate_ip()
      self.simulation_log.insert(tk.END, f'SOURCE IP: {source_ip}\n')
      
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
         self.cursor.execute('''
            INSERT INTO intrusion_command_events
            (timestamp, source_ip, attack_type, severity, response)
            VALUES (?, ?, ?, ?, ?)
         ''', (datetime.now(), source_ip, technique, severity, response))
         self.conn.commit()
      except sqlite3.Error as e:
         self.simulation_log.insert(tk.END, f'DATABASE ERROR: {str(e)}\n')
      
      #DISPLAY RESPONSE
      self.simulation_log.insert(tk.END, f'SEVERITY: [{severity}]\n')
      self.simulation_log.insert(tk.END, f'RESPONSE: {response}\n')
      
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