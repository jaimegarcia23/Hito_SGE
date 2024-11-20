import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from sqlalchemy import create_engine, text
import pymysql
import matplotlib.pyplot as plt
import pandas as pd
import os

class EncuestaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Encuestas")
        self.root.geometry("9000x1000")
        self.root.configure(bg="#EAEAEA")

        # Conectar a la base de datos
        self.engine = self.conectar_base_datos()
        if not self.engine:
            return

        # Configurar la interfaz
        self.configurar_interfaz()

    def conectar_base_datos(self):
        try:
            engine = create_engine("mysql+pymysql://root:curso@localhost/ENCUESTAS")
            return engine
        except Exception as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")
            return None

    def configurar_interfaz(self):
        # Estilo global
        style = ttk.Style()
        
        # Botones con color de fondo verde y texto negro
        style.configure("TButton",
                        font=("Arial", 12, "bold"),
                        background="#4CAF50",
                        foreground="black",  # Aquí se pone el color negro para el texto
                        padding=6)
        style.configure("TButtonHover", background="#45a049")  # Color hover

        # Estilo de la tabla Treeview
        style.configure("Treeview",
                        font=("Arial", 10),
                        background="#FFFFFF",
                        foreground="#000000",
                        rowheight=25,
                        fieldbackground="#FFFFFF")
        style.map("Treeview", background=[('selected', '#a3c2c2')])

        # Estilo de la ventana y etiquetas
        style.configure("TFrame", background="#EAEAEA")
        style.configure("TLabel", background="#EAEAEA", font=("Arial", 12, "bold"))

        # Crear el marco principal
        frame = ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Configurar Treeview
        self.tree = ttk.Treeview(frame, columns=("id", "edad", "sexo", "bebidas_semana", "cervezas_semana",
                                                 "bebidas_fin_semana", "destiladas_semana", "vinos_semana",
                                                 "perdidas_control", "diversion_dependencia", "problemas_digestivos",
                                                 "tension_alta", "dolor_cabeza"), show='headings')

        columnas = ["ID", "Edad", "Sexo", "Bebidas/Semana", "Cervezas/Semana", "Bebidas Fin de Semana",
                    "Destiladas/Semana", "Vinos/Semana", "Pérdidas Control", "Diversión Dependencia",
                    "Problemas Digestivos", "Tensión Alta", "Dolor de Cabeza"]

        for col, name in zip(self.tree["columns"], columnas):
            self.tree.heading(col, text=name, anchor="center")
            self.tree.column(col, width=120, anchor="center")

        self.tree.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Botones de acción
        button_frame = ttk.Frame(self.root, padding="20", style="TFrame")
        button_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        # Botones de acción
        self.crear_boton(button_frame, "Agregar Registro", self.agregar_registro_gui, 0, 0)
        self.crear_boton(button_frame, "Eliminar Registro", self.eliminar_registro_gui, 0, 1)
        self.crear_boton(button_frame, "Actualizar Tabla", self.actualizar_registro_gui, 1, 0)
        self.crear_boton(button_frame, "Filtrar Registros", self.filtrar_registros_gui, 1, 1)
        self.crear_boton(button_frame, "Ver Gráfico Consumo por Sexo", self.ver_grafico_sexo, 2, 0, colspan=2)
        self.crear_boton(button_frame, "Ver Gráfico Consumo por Edad", self.ver_grafico_edad, 3, 0, colspan=2)
        self.crear_boton(button_frame, "Ver Gráfico de Problemas de Salud", self.ver_grafico_problemas_salud, 5, 0, colspan=2)
        self.crear_boton(button_frame, "Exportar a Excel", self.exportar_a_excel, 6, 0, colspan=2)

        # Leer los registros inicialmente
        self.leer_registros()

    def crear_boton(self, frame, texto, comando, fila, columna, colspan=1):
        boton = ttk.Button(frame, text=texto, command=comando, width=25, style="TButton")
        boton.grid(row=fila, column=columna, padx=10, pady=10, columnspan=colspan, sticky="ew")
        boton.bind("<Enter>", self.on_enter)
        boton.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        event.widget.config(style="TButtonHover")

    def on_leave(self, event):
        event.widget.config(style="TButton")

    def leer_registros(self, filtro=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = "SELECT * FROM ENCUESTA"

        if filtro:
            filtro = self.formatear_filtro(filtro)
            query += f" WHERE {filtro}"

        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query)).fetchall()
            for row in result:
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error de consulta", f"Error al ejecutar la consulta: {e}")

    def formatear_filtro(self, filtro):
        parts = filtro.split('=')
        if len(parts) == 2:
            campo, valor = parts
            campo = campo.strip()
            valor = valor.strip()
            if valor.isalpha():
                valor = f"'{valor}'"
            return f"{campo} = {valor}"
        return filtro

    def agregar_registro_gui(self):
        agregar_window = Toplevel(self.root)
        agregar_window.title("Agregar Registro")
        agregar_window.geometry("500x700")  # Ajustar altura por los combobox
        agregar_window.configure(bg="#f4f4f4")

        # Campos y sus tipos (texto o desplegable con opciones)
        campos = [
            ("Edad", "entry"),
            ("Sexo", "combobox", ["Hombre", "Mujer"]),
            ("BebidasSemana", "entry"),
            ("CervezasSemana", "entry"),
            ("BebidasFinSemana", "entry"),
            ("BebidasDestiladasSemana", "entry"),
            ("VinosSemana", "entry"),
            ("PerdidasControl", "entry"),
            ("DiversionDependenciaAlcohol", "combobox", ["Sí", "No"]),
            ("ProblemasDigestivos", "combobox", ["Sí", "No"]),
            ("TensionAlta", "combobox", ["Sí", "No"]),
            ("DolorCabeza", "combobox", ["Sí", "No", "Alguna vez", "A veces", "Regularmente"]),
        ]

        inputs = {}
        for i, (campo, tipo, *opciones) in enumerate(campos):
            ttk.Label(agregar_window, text=campo, background="#f4f4f4", font=("Arial", 11)).grid(row=i, column=0, padx=10, pady=5)

            if tipo == "entry":
                # Campo de texto
                input_widget = tk.Entry(agregar_window, font=("Arial", 11))
            elif tipo == "combobox":
                # Menú desplegable con opciones
                input_widget = ttk.Combobox(agregar_window, font=("Arial", 11), state="readonly")
                input_widget['values'] = opciones[0]

            input_widget.grid(row=i, column=1, padx=10, pady=5)
            inputs[campo] = input_widget

        def agregar():
            try:
                values = {}
                for campo, widget in inputs.items():
                    values[campo] = widget.get().strip()
                    if not values[campo]:  # Validar que no haya campos vacíos
                        raise ValueError(f"El campo '{campo}' está vacío.")

                # Mapeo a columnas SQL
                columnas = ["edad", "sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana", 
                            "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl", 
                            "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"]
                valores_sql = {col: values[c] for col, c in zip(columnas, inputs)}

                query = f"""
                    INSERT INTO ENCUESTA ({", ".join(columnas)})
                    VALUES ({", ".join([f":{col}" for col in columnas])})
                """
                with self.engine.connect() as connection:
                    connection.execute(text(query), valores_sql)

                self.leer_registros()
                agregar_window.destroy()
                messagebox.showinfo("Éxito", "Registro agregado correctamente")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar el registro: {e}")

        ttk.Button(agregar_window, text="Agregar", command=agregar, style="TButton").grid(row=len(campos), column=0, columnspan=2, pady=20)



    def eliminar_registro_gui(self):
        eliminar_window = Toplevel(self.root)
        eliminar_window.title("Eliminar Registro")
        eliminar_window.geometry("600x150")
        eliminar_window.configure(bg="#f4f4f4")

        ttk.Label(eliminar_window, text="Ingrese el ID del registro a eliminar:", background="#f4f4f4", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10)
        id_entry = tk.Entry(eliminar_window, font=("Arial", 11))
        id_entry.grid(row=0, column=1, padx=10, pady=10)

        def eliminar():
            try:
                id_registro = id_entry.get()
                if not id_registro.isdigit():
                    messagebox.showerror("Error", "El ID debe ser un número entero.")
                    return
                
                query = f"DELETE FROM ENCUESTA WHERE idEncuesta = {id_registro}"  # Cambiado a idEncuesta
                with self.engine.connect() as connection:
                    result = connection.execute(text(query))
                    if result.rowcount == 0:
                        messagebox.showerror("Error", "No se encontró un registro con ese ID.")
                    else:
                        self.leer_registros()
                        eliminar_window.destroy()
                        messagebox.showinfo("Éxito", "Registro eliminado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el registro: {e}")

        ttk.Button(eliminar_window, text="Eliminar", command=eliminar, style="TButton").grid(row=1, column=0, columnspan=2, pady=10)


    def actualizar_registro_gui(self):
        try:
            self.leer_registros()  # Refresca la tabla leyendo nuevamente los registros
            messagebox.showinfo("Éxito", "¡Tabla actualizada correctamente!")  # Muestra el mensaje
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la tabla: {e}")


    def filtrar_registros_gui(self):
            filtro_window = Toplevel(self.root)
            filtro_window.title("Filtrar Registros")
            filtro_window.geometry("800x200")
            filtro_window.configure(bg="#f4f4f4")

            ttk.Label(filtro_window, text="Ingrese el filtro por sexo o edad (ej: edad=20):", background="#f4f4f4", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10)
            filtro_entry = tk.Entry(filtro_window, font=("Arial", 11))
            filtro_entry.grid(row=0, column=1, padx=10, pady=10)

            def aplicar_filtro():
                filtro = filtro_entry.get()
                self.leer_registros(filtro)
                filtro_window.destroy()

            ttk.Button(filtro_window, text="Aplicar Filtro", command=aplicar_filtro, style="TButton").grid(row=1, column=0, columnspan=2, pady=10)


    def ver_grafico_sexo(self):
        query = "SELECT sexo, COUNT(*) FROM ENCUESTA GROUP BY sexo"
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query)).fetchall()

            data = pd.DataFrame(result, columns=["Sexo", "Cantidad"])
            data.plot(kind="bar", x="Sexo", y="Cantidad", color=["blue", "orange"])
            plt.title("Distribución por Sexo")
            plt.ylabel("Cantidad de Registros")
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el gráfico: {e}")

    def ver_grafico_edad(self):
        query = "SELECT edad, COUNT(*) FROM ENCUESTA GROUP BY edad"
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query)).fetchall()

            data = pd.DataFrame(result, columns=["Edad", "Cantidad"])
            data.plot(kind="bar", x="Edad", y="Cantidad", color="green")
            plt.title("Distribución por Edad")
            plt.ylabel("Cantidad de Registros")
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el gráfico: {e}")

    def ver_grafico_problemas_salud(self):
        query = """
            SELECT PerdidasControl, COUNT(*) FROM ENCUESTA GROUP BY PerdidasControl
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query)).fetchall()

            data = pd.DataFrame(result, columns=["Pérdidas de Control", "Cantidad"])
            data.plot(kind="bar", x="Pérdidas de Control", y="Cantidad", color="red")
            plt.title("Problemas de Salud Relacionados con el Consumo")
            plt.ylabel("Cantidad de Registros")
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el gráfico: {e}")

    def exportar_a_excel(self):
        try:
            query = "SELECT * FROM ENCUESTA"
            with self.engine.connect() as connection:
                result = connection.execute(text(query)).fetchall()

            data = pd.DataFrame(result)
            filename = "encuesta_registros.xlsx"
            data.to_excel(filename, index=False)
            messagebox.showinfo("Éxito", f"Datos exportados a {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar a Excel: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EncuestaApp(root)
    root.mainloop()
