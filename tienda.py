import tkinter as tk
from tkinter import messagebox
import sqlite3


class TiendaApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Tienda de Abarrotes")
        self.geometry("720x560")
        self.configure(bg="#D9F2D9")

        self.conn = sqlite3.connect("TiendaAbarrotes.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                precio REAL NOT NULL,
                cantidad INTEGER NOT NULL
            )""")
        self.conn.commit()

        self._crear_widgets()
        self.id_actual = None
        self._cargar_lista()

    def _crear_widgets(self):
        self.nombre = tk.Label(
            self,
            text="Nombre del producto:",
            bg="#D9F2D9",
            font=("Segoe UI", 11, "bold")
        )
        self.nombre.grid(row=0, column=0, pady=6)

        self.entry_nombre = tk.Entry(self, width=32)
        self.entry_nombre.grid(row=1, column=0, pady=6)

        self.categoria = tk.Label(
            self,
            text="Categoría:",
            bg="#D9F2D9",
            font=("Segoe UI", 11, "bold")
        )
        self.categoria.grid(row=2, column=0, pady=6)

        self.entry_categoria = tk.Entry(self, width=32)
        self.entry_categoria.grid(row=3, column=0, pady=6)

        self.precio = tk.Label(
            self,
            text="Precio:",
            bg="#D9F2D9",
            font=("Segoe UI", 11, "bold")
        )
        self.precio.grid(row=4, column=0, pady=6)

        self.entry_precio = tk.Entry(self, width=32)
        self.entry_precio.grid(row=5, column=0, pady=6)

        self.cantidad = tk.Label(
            self,
            text="Cantidad:",
            bg="#D9F2D9",
            font=("Segoe UI", 11, "bold")
        )
        self.cantidad.grid(row=6, column=0, pady=6)

        self.entry_cantidad = tk.Entry(self, width=32)
        self.entry_cantidad.grid(row=7, column=0, pady=6)

        self.boton_guardar = tk.Button(
            self,
            text="Agregar",
            command=self._guardar,
            bg="#2E8B57",
            fg="white",
            width=15
        )
        self.boton_guardar.grid(row=1, column=1, pady=6)

        self.boton_eliminar = tk.Button(
            self,
            text="Eliminar",
            command=self._eliminar,
            bg="#B22222",
            fg="white",
            width=15
        )
        self.boton_eliminar.grid(row=2, column=1, pady=6)

        self.boton_actualizar = tk.Button(
            self,
            text="Actualizar",
            command=self._actualizar,
            bg="#DAA520",
            fg="white",
            width=15
        )
        self.boton_actualizar.grid(row=3, column=1, pady=6)

        self.boton_consultar = tk.Button(
            self,
            text="Consultar",
            command=self._cargar_lista,
            bg="#4682B4",
            fg="white",
            width=15
        )
        self.boton_consultar.grid(row=4, column=1, pady=6)

        self.boton_limpiar = tk.Button(
            self,
            text="Limpiar",
            command=self._limpiar,
            bg="#555555",
            fg="white",
            width=15
        )
        self.boton_limpiar.grid(row=5, column=1, pady=6)

        self.listbox = tk.Listbox(self, width=88, height=15)
        self.listbox.grid(row=9, column=0, columnspan=2, pady=10)

    def _guardar(self):
        nombre = self.entry_nombre.get().strip()
        categoria = self.entry_categoria.get().strip()
        precio = self.entry_precio.get().strip()
        cantidad = self.entry_cantidad.get().strip()

        if nombre == "":
            messagebox.showerror(
                "Error",
                "Debes escribir el nombre del producto."
            )
            return

        if categoria == "":
            messagebox.showerror(
                "Error",
                "Debes escribir la categoría del producto."
            )
            return

        if precio == "":
            messagebox.showerror(
                "Error",
                "Debes escribir el precio del producto."
            )
            return

        if cantidad == "":
            messagebox.showerror(
                "Error",
                "Debes escribir la cantidad del producto."
            )
            return

        try:
            precio = float(precio)
        except ValueError:
            messagebox.showerror(
                "Error",
                "El precio debe ser un número. Ejemplo: 25.50"
            )
            return

        try:
            cantidad = int(cantidad)
        except ValueError:
            messagebox.showerror(
                "Error",
                "La cantidad debe ser un número entero. Ejemplo: 10"
            )
            return

        if precio < 0:
            messagebox.showerror(
                "Error",
                "El precio no puede ser negativo."
            )
            return

        if cantidad < 0:
            messagebox.showerror(
                "Error",
                "La cantidad no puede ser negativa."
            )
            return

        opciones = (
            nombre,
            categoria,
            precio,
            cantidad
        )

        if self.id_actual is None:

            self.cursor.execute(
                """
                INSERT INTO productos
                (nombre, categoria, precio, cantidad)
                VALUES (?, ?, ?, ?)
                """,
                opciones
            )

        else:

            self.cursor.execute(
                """
                UPDATE productos
                SET nombre = ?, categoria = ?, precio = ?, cantidad = ?
                WHERE id = ?
                """,
                (
                    nombre,
                    categoria,
                    precio,
                    cantidad,
                    self.id_actual
                )
            )

            self.id_actual = None

        self.conn.commit()

        self._limpiar()
        self._cargar_lista()

    def _eliminar(self):
        seleccion = self.listbox.curselection()

        if not seleccion:
            messagebox.showerror(
                "Error",
                "Selecciona un producto de la lista para eliminarlo."
            )
            return

        indice = seleccion[0]
        dato = self.listbox.get(indice)

        try:
            id_producto = int(
                dato.split("|")[0]
                .replace("[", "")
                .replace("]", "")
                .strip()
            )
        except ValueError:
            messagebox.showerror(
                "Error",
                "No se pudo identificar el producto seleccionado."
            )
            return

        self.cursor.execute(
            "DELETE FROM productos WHERE id = ?",
            (id_producto,)
        )

        self.conn.commit()

        self.listbox.delete(indice)
        self._cargar_lista()

    def _actualizar(self):
        seleccion = self.listbox.curselection()

        if not seleccion:
            messagebox.showerror(
                "Error",
                "Selecciona un producto de la lista para actualizarlo."
            )
            return

        indice = seleccion[0]
        dato = self.listbox.get(indice)

        partes = dato.split("|")

        if len(partes) != 5:
            messagebox.showerror(
                "Error",
                "No se pudieron obtener correctamente los datos del producto."
            )
            return

        try:
            self.id_actual = int(
                partes[0]
                .replace("[", "")
                .replace("]", "")
                .strip()
            )
        except ValueError:
            messagebox.showerror(
                "Error",
                "No se pudo identificar el producto seleccionado."
            )
            return

        nombre = partes[1].strip()
        categoria = partes[2].strip()
        precio = partes[3].strip()
        cantidad = partes[4].strip()

        self.entry_nombre.delete(0, tk.END)
        self.entry_categoria.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)

        self.entry_nombre.insert(0, nombre)
        self.entry_categoria.insert(0, categoria)
        self.entry_precio.insert(0, precio)
        self.entry_cantidad.insert(0, cantidad)

    def _cargar_lista(self):
        self.listbox.delete(0, "end")

        self.cursor.execute(
            "SELECT id, nombre, categoria, precio, cantidad FROM productos"
        )

        for fila in self.cursor.fetchall():
            self.listbox.insert(
                "end",
                f"[{fila[0]}] | {fila[1]} | {fila[2]} | "
                f"{fila[3]:.2f} | {fila[4]}"
            )

    def _limpiar(self):
        self.entry_nombre.delete(0, "end")
        self.entry_categoria.delete(0, "end")
        self.entry_precio.delete(0, "end")
        self.entry_cantidad.delete(0, "end")

        self.id_actual = None


if __name__ == "__main__":
    app = TiendaApp()
    app.mainloop()