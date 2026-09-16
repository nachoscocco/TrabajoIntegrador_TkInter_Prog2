import tkinter as tk
from tkinter import ttk
from crud import GenericCRUDFrame
from repo import Repository

PACIENTE_FIELDS = [
    {"name": "dni", "label": "DNI"},
    {"name": "nombre", "label": "Nombre"},
    {"name": "apellido", "label": "Apellido"},
    {"name": "obra_social", "label": "Obra Social"},
    {"name": "telefono", "label": "Teléfono"},
]

MEDICO_FIELDS = [
    {"name": "matricula", "label": "Matrícula"},
    {"name": "nombre", "label": "Nombre"},
    {"name": "apellido", "label": "Apellido"},
    {"name": "especialidad", "label": "Especialidad"},
    {"name": "horario", "label": "Horario de Atención"},
]

def main():
    root = tk.Tk()
    root.title("Trabajo Práctico 2 - Programación II - Tkinter CRUD")
    root.geometry("900x550")
    
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    pacientes_repo = Repository()
    medicos_repo = Repository()

    pacientes_tab = GenericCRUDFrame(
        notebook, "Pacientes", PACIENTE_FIELDS, pacientes_repo
    )
    medicos_tab = GenericCRUDFrame(
        notebook, "Médicos", MEDICO_FIELDS, medicos_repo
    )

    notebook.add(pacientes_tab, text="Módulo de Pacientes")
    notebook.add(medicos_tab, text="Módulo de Médicos")

    root.mainloop()

if __name__ == "__main__":
    main()
