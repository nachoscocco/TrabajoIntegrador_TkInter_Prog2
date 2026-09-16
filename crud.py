import tkinter as tk
from tkinter import ttk, messagebox

class GenericCRUDFrame(tk.Frame):
    def __init__(self, master, title, fields, repository):
        super().__init__(master)
        self.title = title
        self.fields = fields
        self.repository = repository
        
        self.entries: dict[str, tk.Entry] = {}
        self._selected_id = None

        self._build_ui()
        self._refresh_table()

    def _build_ui(self):
        header = tk.Label(
            self, text=f"Gestión de {self.title}",
            font=("Arial", 14, "bold")
        )
        header.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        form_frame = tk.Frame(self)
        form_frame.grid(row=1, column=0, sticky="n", padx=20)

        for row_index, field in enumerate(self.fields):
            label = tk.Label(form_frame, text=f'{field["label"]}:', font=("Arial", 10))
            label.grid(row=row_index, column=0, sticky="e", padx=5, pady=5)

            entry = tk.Entry(form_frame, width=35)
            entry.grid(row=row_index, column=1, padx=5, pady=5)
            
            self.entries[field["name"]] = entry

        button_row = len(self.fields)
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=button_row, column=0, columnspan=2, pady=15)

        acciones = [
            ("Crear", self._on_add),
            ("Actualizar", self._on_update),
            ("Eliminar", self._on_delete),
            ("Limpiar", self._clear_fields),
        ]
        
        for col_index, (texto, comando) in enumerate(acciones):
            btn = tk.Button(btn_frame, text=texto, width=12, command=comando, bg="#e0e0e0")
            btn.grid(row=0, column=col_index, padx=5)

        columnas = ["id"] + [f["name"] for f in self.fields]
        self.tree = ttk.Treeview(self, columns=columnas, show="headings", height=15)
        
        for col in columnas:
            if col == "id":
                encabezado = "ID"
            else:
                encabezado = next(f["label"] for f in self.fields if f["name"] == col)
            self.tree.heading(col, text=encabezado)
            self.tree.column(col, width=120, anchor="center")

        self.tree.grid(row=1, column=1, padx=20, sticky="n")
        self.tree.bind("<<TreeviewSelect>>", self._on_row_select)

    def _read_fields(self) -> dict:
        return {name: entry.get().strip() for name, entry in self.entries.items()}

    def _clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self._selected_id = None
        
        seleccion = self.tree.selection()
        if seleccion:
            self.tree.selection_remove(seleccion)

    def _fill_fields(self, record: dict):
        for name, entry in self.entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, record.get(name, ""))

    def _on_add(self):
        record = self._read_fields()
        if not all(record.values()):
            messagebox.showerror("Error de Validación", "Todos los campos deben ser completados para crear un registro.")
            return
            
        self.repository.add(record)
        messagebox.showinfo("Éxito", "Registro creado correctamente.")
        self._clear_fields()
        self._refresh_table()

    def _on_update(self):
        if self._selected_id is None:
            messagebox.showwarning("Atención", "Debe seleccionar un registro de la tabla antes de Actualizar.")
            return
            
        record = self._read_fields()
        if not all(record.values()):
            messagebox.showerror("Error de Validación", "No se pueden dejar campos vacíos al actualizar.")
            return
            
        self.repository.update(self._selected_id, record)
        messagebox.showinfo("Éxito", "Registro actualizado correctamente.")
        self._clear_fields()
        self._refresh_table()

    def _on_delete(self):
        if self._selected_id is None:
            messagebox.showwarning("Atención", "Debe seleccionar un registro de la tabla antes de Eliminar.")
            return
            
        confirm = messagebox.askyesno("Confirmar", "¿Está seguro que desea eliminar este registro?")
        if confirm:
            self.repository.delete(self._selected_id)
            messagebox.showinfo("Éxito", "Registro eliminado correctamente.")
            self._clear_fields()
            self._refresh_table()

    def _on_row_select(self, event):
        seleccion = self.tree.selection()
        if not seleccion:
            return
            
        item = self.tree.item(seleccion[0])
        valores = item["values"]
        
        self._selected_id = int(valores[0])
        nombres_campos = [f["name"] for f in self.fields]
        record = dict(zip(nombres_campos, valores[1:]))
        self._fill_fields(record)

    def _refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        for record_id, record in self.repository.get_all():
            fila = [record_id] + [record.get(f["name"], "") for f in self.fields]
            self.tree.insert("", tk.END, values=fila)
