import tkinter as tk
from tkinter import messagebox, simpledialog
from collections import defaultdict
import re
from datetime import datetime

citas_por_especialista = defaultdict(list)
LIMITE_CITAS_POR_ESPECIALISTA = 10
NUMERO_MAXIMO_CAMILLAS = 150 
camillas_asignadas = 0

class VentanaBienvenida(tk.Tk):
   
    def __init__(self):
        super().__init__()
        self.title("Bienvenido al Hospital General")
        self.geometry("600x800")
        self.config(bg="#e0f7fa") 
        self.resizable(False, False)

        self.label_saludo = tk.Label(self, text="¡Bienvenido al sistema de citas del Hospital General!",
                                     font=("Helvetica", 16, "bold"), fg="#00796b", bg="#e0f7fa")
        self.label_saludo.pack(pady=40)

        self.btn_ir_registro = tk.Button(self, text="Agendar Cita",
                                         font=("Helvetica", 14), bg="#009688", fg="white", 
                                         activebackground="#00796b", activeforeground="white",
                                         cursor="hand2",
                                         command=self.abrir_ventana_registro)
        self.btn_ir_registro.pack(pady=20)

    def abrir_ventana_registro(self):
     
        self.destroy() 
        VentanaRegistroCitas()


class VentanaRegistroCitas(tk.Tk):
  
    def __init__(self):
        super().__init__()
        self.title("Registro de Citas - Hospital General")
        self.geometry("800x800")
        self.config(bg="#e3f2fd")
        self.resizable(False, False)

        tk.Label(self, text="Registro de Citas Médicas",
                 font=("Helvetica", 18, "bold"), fg="#1a237e", bg="#e3f2fd").pack(pady=20) 

        self.frame_campos = tk.LabelFrame(self, text="Datos del Paciente y Cita",
                                          font=("Helvetica", 12, "bold"), fg="#283593", bg="#e3f2fd", bd=2,
                                          relief="groove")
        self.frame_campos.pack(padx=30, pady=10, fill="x")

        self.entry_nombre = self.crear_campo(self.frame_campos, "Nombre Completo:", 0)
        self.entry_fecha = self.crear_campo(self.frame_campos, "Fecha de Cita (DD/MM/AAAA):", 1)
        self.entry_hora = self.crear_campo(self.frame_campos, "Hora de Cita (HH:MM):", 2)

        tk.Label(self.frame_campos, text="Especialista:", font=("Helvetica", 10), bg="#e3f2fd").grid(row=3, column=0,
                                                                                                     padx=10, pady=5,
                                                                                                     sticky="w")
        self.especialistas = ["Cardiología", "Pediatría", "Dermatología", "Odontología", "Medicina General"]
        self.especialista_elegido = tk.StringVar(self)
        self.especialista_elegido.set(self.especialistas[0])  # Default initial value
        self.menu_especialistas = tk.OptionMenu(self.frame_campos, self.especialista_elegido, *self.especialistas)
        self.menu_especialistas.config(font=("Helvetica", 10), bg="white", width=30)
        self.menu_especialistas.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        self.btn_registrar = tk.Button(self, text="Registrar Cita",
                                       font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", 
                                       activebackground="#388E3C", activeforeground="white",
                                       cursor="hand2",
                                       command=self.registrar_cita)
        self.btn_registrar.pack(pady=20)

        self.btn_ver_citas = tk.Button(self, text="Ver Citas por Especialista",
                                       font=("Helvetica", 12), bg="#2196F3", fg="white",
                                       activebackground="#1976D2", activeforeground="white",
                                       cursor="hand2",
                                       command=self.abrir_ventana_ver_citas)
        self.btn_ver_citas.pack(pady=10)

        self.btn_volver = tk.Button(self, text="Volver al Inicio",
                                    font=("Helvetica", 10), bg="#78909c", fg="white", 
                                    activebackground="#546E7A", activeforeground="white",
                                    cursor="hand2",
                                    command=self.volver_bienvenida)
        self.btn_volver.pack(pady=10)

    def crear_campo(self, parent_frame, label_text, row):
     
        tk.Label(parent_frame, text=label_text, font=("Helvetica", 10), bg="#e3f2fd").grid(row=row, column=0, padx=10,
                                                                                           pady=5, sticky="w")
        entry = tk.Entry(parent_frame, width=40, font=("Helvetica", 10), bd=1, relief="solid")
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        return entry

    def validar_nombre(self, nombre):
     
        # Regular expression that only allows letters and spaces
        if not re.fullmatch(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑÑüÜ\s]+$', nombre):
            return False, "El nombre del paciente solo debe contener letras y espacios."

        if len(nombre.strip().split()) < 2:
            return False, "Por favor, ingrese el nombre completo (nombre y apellido)."

        return True, ""

    def validar_fecha(self, fecha_str):
    
        try:
          datetime.strptime(fecha_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def validar_hora(self, hora_str):
    
        try:
           
            datetime.strptime(hora_str, "%H:%M")
            return True
        except ValueError:
            return False

    def verificar_disponibilidad_especialista(self, especialista, fecha, hora):
      
        for cita in citas_por_especialista[especialista]:
            if cita["Fecha"] == fecha and cita["Hora"] == hora:
                return False 
        return True  

    def registrar_cita(self):
     
        global camillas_asignadas

        nombre = self.entry_nombre.get().strip()
        fecha = self.entry_fecha.get().strip()
        hora = self.entry_hora.get().strip()
        especialista = self.especialista_elegido.get()

        if not all([nombre, fecha, hora, especialista]):
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos para registrar la cita.")
            return

        is_name_valid, name_error_msg = self.validar_nombre(nombre)
        if not is_name_valid:
            messagebox.showerror("Error en el Nombre", name_error_msg)
            return

        if not self.validar_fecha(fecha):
            messagebox.showerror("Formato de Fecha Inválido", "Por favor, ingrese la fecha en formato DD/MM/AAAA (ej. 31/12/2023).")
            return

        if not self.validar_hora(hora):
            messagebox.showerror("Formato de Hora Inválido", "Por favor, ingrese la hora en formato HH:MM (ej. 14:30).")
            return
        if not self.verificar_disponibilidad_especialista(especialista, fecha, hora):
            messagebox.showerror("Especialista No Disponible",
                                 f"El especialista de {especialista} ya tiene una cita agendada para el {fecha} a las {hora}. Por favor, elija otra hora o especialista.")
            return

        if len(citas_por_especialista[especialista]) >= LIMITE_CITAS_POR_ESPECIALISTA:
            messagebox.showerror("Límite de Citas Excedido",
                                 f"El especialista de {especialista} ya tiene {LIMITE_CITAS_POR_ESPECIALISTA} citas agendadas. Por favor, intente agendar para otro día o con otro especialista.")
            return

        if camillas_asignadas >= NUMERO_MAXIMO_CAMILLAS:
            messagebox.showerror("Camillas No Disponibles",
                                 f"No hay camillas disponibles en este momento ({camillas_asignadas}/{NUMERO_MAXIMO_CAMILLAS} ocupadas). Por favor, intente más tarde.")
            return

        camillas_asignadas += 1 
        numero_camilla = camillas_asignadas # Assign the current bed number

        cita_info = {
            "Paciente": nombre,
            "Fecha": fecha,
            "Hora": hora,
            "Especialista": especialista,
            "Número de Camilla": numero_camilla
        }

        citas_por_especialista[especialista].append(cita_info) 

        messagebox.showinfo("Cita Registrada",
                            f"La cita para {nombre} con {especialista} ha sido registrada exitosamente.\nSu número de camilla asignado es: {numero_camilla}.")

      
        self.entry_nombre.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)
        self.entry_hora.delete(0, tk.END)
        self.especialista_elegido.set(self.especialistas[0]) 

    def abrir_ventana_ver_citas(self):
      
        VentanaVerCitas() 
    def volver_bienvenida(self):
    
        self.destroy() 
        VentanaBienvenida() 

class VentanaVerCitas(tk.Toplevel):
   
    def __init__(self):
        super().__init__()
        self.title("Citas Registradas por Especialista")
        self.geometry("600x500")
        self.config(bg="#e8f5e9") 
        self.resizable(False, False)

        tk.Label(self, text="Citas Agendadas",
                 font=("Helvetica", 16, "bold"), fg="#1b5e20", bg="#e8f5e9").pack(pady=20) 

        frame_text = tk.Frame(self, padx=20, pady=10, bg="#e8f5e9")
        frame_text.pack(fill="both", expand=True)

        self.text_citas = tk.Text(frame_text, width=70, height=20, font=("Courier New", 10),
                                  bg="white", relief="sunken", borderwidth=2, wrap="word")
        self.text_citas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_text, command=self.text_citas.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_citas.config(yscrollcommand=scrollbar.set) 

        self.text_citas.config(state="disabled") 
        self.mostrar_citas() 
        self.btn_cerrar = tk.Button(self, text="Cerrar",
                                    font=("Helvetica", 12), bg="#ef5350", fg="white",
                                    activebackground="#d32f2f", activeforeground="white",
                                    cursor="hand2",
                                    command=self.destroy)
        self.btn_cerrar.pack(pady=15)

    def mostrar_citas(self):
     
        self.text_citas.config(state="normal") 
        self.text_citas.delete("1.0", tk.END) 
        self.text_citas.insert(tk.END, f"--- Camillas Ocupadas: {camillas_asignadas}/{NUMERO_MAXIMO_CAMILLAS} ---\n\n",
                               "header")

        if not citas_por_especialista:
            self.text_citas.insert(tk.END, "No hay citas registradas aún.")
        else:
            # Iterate over each specialist and their appointments
            for especialista, citas in citas_por_especialista.items():
                self.text_citas.insert(tk.END,
                                       f"--- {especialista} ({len(citas)}/{LIMITE_CITAS_POR_ESPECIALISTA}) ---\n",
                                       "header_especialista")
                if not citas: 
                    self.text_citas.insert(tk.END, "  No hay citas para este especialista.\n\n")
                else:
                  
                    for i, cita in enumerate(citas):
                        self.text_citas.insert(tk.END, f"  Cita {i + 1} (Camilla: {cita['Número de Camilla']}):\n")
                        for key, value in cita.items():
                           
                            if key != "Número de Camilla":
                                self.text_citas.insert(tk.END, f"    {key}: {value}\n")
                        self.text_citas.insert(tk.END, "\n")
                self.text_citas.insert(tk.END, "\n")

        self.text_citas.config(state="disabled") # Make the text widget read-only again

       
        self.text_citas.tag_config("header", font=("Helvetica", 12, "bold"), foreground="#d32f2f") 
        self.text_citas.tag_config("header_especialista", font=("Helvetica", 12, "bold"), foreground="#0d47a1") 


if __name__ == "__main__":
    app = VentanaBienvenida()
    app.mainloop()

