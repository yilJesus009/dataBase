import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

# Configuración de la conexión a la base de datos
config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',
    'database': 'ExamenBase2'
}

# Función para conectar a la base de datos
def conectar_db():
    try:
        conn = mysql.connector.connect(**config)
        print("Conexión establecida con éxito a la base de datos.")
        return conn
    except mysql.connector.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        return None

# Función para registrar un estudiante, materia y nota
def registrar_registro():
    nombre = nombre_var.get()
    fecha_nacimiento = fecha_nacimiento_var.get()
    carrera = carrera_var.get()
    codigo = codigo_var.get()
    nombre_materia = nombre_materia_var.get()
    creditos = creditos_var.get()
    valor = valor_var.get()

    conn = conectar_db()
    if conn:
        cursor = conn.cursor()

        try:
            # Registrar Estudiante
            query_estudiante = "INSERT INTO Estudiante (nombreCompleto, fechaNacimiento, carrera) VALUES (%s, %s, %s)"
            cursor.execute(query_estudiante, (nombre, fecha_nacimiento, carrera))

            # Obtener ID del estudiante
            id_estudiante = cursor.lastrowid

            # Verificar si el código de materia ya existe
            query_verificar_materia = "SELECT codigo_Materia FROM Materia WHERE codigo_Materia = %s"
            cursor.execute(query_verificar_materia, (codigo,))
            existing_materia = cursor.fetchone()

            if existing_materia:
                # Si la materia ya existe, solo obtenemos su código
                codigo = existing_materia[0]
            else:
                # Si la materia no existe, la registramos
                query_materia = "INSERT INTO Materia (codigo_Materia, nombre, creditos) VALUES (%s, %s, %s)"
                cursor.execute(query_materia, (codigo, nombre_materia, creditos))

            # Registrar Nota
            query_nota = "INSERT INTO Nota (ID_Estudiante, nombreEstudiante, codigo_Materia, valor) VALUES (%s, %s, %s, %s)"
            cursor.execute(query_nota, (id_estudiante, nombre, codigo, valor))

            conn.commit()
            messagebox.showinfo("Éxito", "Registro realizado con éxito.")

            # Limpiar campos de entrada
            limpiar_campos()

        except mysql.connector.Error as e:
            conn.rollback()
            print(f"Error al registrar el registro: {e}")
            messagebox.showerror("Error", f"Error al registrar el registro: {e}")

        cursor.close()
        conn.close()


# Función para limpiar los campos de entrada
def limpiar_campos():
    nombre_var.set("")
    fecha_nacimiento_var.set("")
    carrera_var.set("")
    codigo_var.set("")
    nombre_materia_var.set("")
    creditos_var.set(0)
    valor_var.set("")

# Función para mostrar los datos de las tablas
def mostrar_registros():
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()

        try:
            # Obtener registros de estudiantes, materias y notas relacionados
            query = """
                    SELECT Estudiante.ID_Estudiante, Estudiante.nombreCompleto, Estudiante.fechaNacimiento, 
                           Estudiante.carrera, Materia.codigo_Materia, Materia.nombre, Materia.creditos,
                           Nota.valor
                    FROM Estudiante
                    INNER JOIN Nota ON Estudiante.ID_Estudiante = Nota.ID_Estudiante
                    INNER JOIN Materia ON Nota.codigo_Materia = Materia.codigo_Materia
                    """
            cursor.execute(query)
            registros = cursor.fetchall()

            # Limpiar el Treeview antes de mostrar los datos actualizados
            for i in registros_treeview.get_children():
                registros_treeview.delete(i)

            # Insertar los registros en el Treeview
            for registro in registros:
                print(registro)  # Imprimir cada registro para depuración
                registros_treeview.insert("", "end", values=registro)

        except mysql.connector.Error as e:
            print(f"Error al obtener los registros: {e}")
            messagebox.showerror("Error", f"Error al obtener los registros: {e}")

        cursor.close()
        conn.close()



# Función para modificar un registro seleccionado
def modificar_registro():
    # Obtener el registro seleccionado en el Treeview
    seleccionado = registros_treeview.selection()
    if not seleccionado:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un registro.")
        return

    # Obtener los valores del registro seleccionado
    valores = registros_treeview.item(seleccionado)['values']

    # Mostrar los valores en los campos de entrada
    nombre_var.set(valores[1])
    fecha_nacimiento_var.set(valores[2])
    carrera_var.set(valores[3])
    codigo_var.set(valores[4])
    nombre_materia_var.set(valores[5])
    creditos_var.set(valores[6])
    valor_var.set(valores[7])

    # Deshabilitar el botón de registrar
    registrar_button.config(state=tk.DISABLED)

# Función para eliminar un registro seleccionado
def eliminar_registro():
    # Obtener el registro seleccionado en el Treeview
    seleccionado = registros_treeview.selection()
    if not seleccionado:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un registro.")
        return

    # Obtener el ID del registro seleccionado
    id_estudiante = registros_treeview.item(seleccionado)['values'][0]

    # Imprimir el ID del estudiante para verificar
    print(f"ID del estudiante a eliminar: {id_estudiante}")

    conn = conectar_db()
    if conn:
        cursor = conn.cursor()

        try:
            # Eliminar el registro de la tabla Nota relacionado con el ID_Estudiante
            query_nota = "DELETE FROM Nota WHERE ID_Estudiante = %s"
            cursor.execute(query_nota, (id_estudiante,))

            # Eliminar el registro de la tabla Estudiante
            query_estudiante = "DELETE FROM Estudiante WHERE ID_Estudiante = %s"
            cursor.execute(query_estudiante, (id_estudiante,))

            conn.commit()
            messagebox.showinfo("Éxito", "Registro eliminado con éxito.")

            # Actualizar el Treeview
            mostrar_registros()

        except mysql.connector.Error as e:
            conn.rollback()
            print(f"Error al eliminar el registro: {e}")
            messagebox.showerror("Error", f"Error al eliminar el registro: {e}")

        cursor.close()
        conn.close()
# Función para mostrar la lista de materias y cantidad de inscritos
def mostrar_materias_inscritos():
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()

        try:
            # Consulta para obtener la lista de materias y cantidad de inscritos
            query = """
                    SELECT Materia.codigo_Materia, Materia.nombre, COUNT(Nota.ID_Estudiante) as cantidad_inscritos
                    FROM Materia
                    LEFT JOIN Nota ON Materia.codigo_Materia = Nota.codigo_Materia
                    GROUP BY Materia.codigo_Materia, Materia.nombre
                    """
            cursor.execute(query)
            materias = cursor.fetchall()

            # Mostrar los resultados en una nueva ventana
            mostrar_materias_window = tk.Toplevel()
            mostrar_materias_window.title("Materias e Inscritos")

            ttk.Label(mostrar_materias_window, text="Código de Materia").grid(row=0, column=0, padx=10, pady=5)
            ttk.Label(mostrar_materias_window, text="Nombre de Materia").grid(row=0, column=1, padx=10, pady=5)
            ttk.Label(mostrar_materias_window, text="Cantidad de Inscritos").grid(row=0, column=2, padx=10, pady=5)

            for index, (codigo, nombre, cantidad) in enumerate(materias, start=1):
                ttk.Label(mostrar_materias_window, text=codigo).grid(row=index, column=0, padx=10, pady=5)
                ttk.Label(mostrar_materias_window, text=nombre).grid(row=index, column=1, padx=10, pady=5)
                ttk.Label(mostrar_materias_window, text=cantidad).grid(row=index, column=2, padx=10, pady=5)

        except mysql.connector.Error as e:
            print(f"Error al obtener la lista de materias e inscritos: {e}")
            messagebox.showerror("Error", f"Error al obtener la lista de materias e inscritos: {e}")

        cursor.close()
        conn.close()


# Función principal
def main():
    global nombre_var, fecha_nacimiento_var, carrera_var
    global codigo_var, nombre_materia_var, creditos_var, valor_var
    global registros_treeview, registrar_button

    root = tk.Tk()
    root.title("Registro de Estudiantes, Materias y Notas")

    # Variables para Estudiante
    nombre_var = tk.StringVar()
    fecha_nacimiento_var = tk.StringVar()
    carrera_var = tk.StringVar()

    # Variables para Materia
    codigo_var = tk.StringVar()
    nombre_materia_var = tk.StringVar()
    creditos_var = tk.IntVar()

    # Variables para Nota
    valor_var = tk.DoubleVar()

    ttk.Button(root, text="Registrar Actualizado", command=registrar_registro).grid(row=7, column=0, pady=10)
    ttk.Button(root, text="Modificar Registro", command=modificar_registro).grid(row=7, column=1, pady=10)
    ttk.Button(root, text="Eliminar Registro", command=eliminar_registro).grid(row=8, column=1, pady=10)
    ttk.Button(root, text="Ver Registros", command=mostrar_registros).grid(row=8, column=0, columnspan=3, pady=10)
    ttk.Button(root, text="Ver Materias e Inscritos", command=mostrar_materias_inscritos).grid(row=9, column=0,
                                                                                               columnspan=3, pady=10)

    # Etiquetas y campos de entrada
    ttk.Label(root, text="Nombre:").grid(row=0, column=0, padx=10, pady=5)
    ttk.Entry(root, textvariable=nombre_var).grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(root, text="Fecha de Nacimiento (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5)
    ttk.Entry(root, textvariable=fecha_nacimiento_var).grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(root, text="Carrera:").grid(row=2, column=0, padx=10, pady=5)
    ttk.Entry(root, textvariable=carrera_var).grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(root, text="Código de Materia:").grid(row=3, column=0, padx=10, pady=5)
    ttk.Entry(root, textvariable=codigo_var).grid(row=3, column=1, padx=10, pady=5)

    ttk.Label(root, text="Nombre de Materia:").grid(row=4, column=0, padx=10, pady=5)
    ttk.Entry(root, textvariable=nombre_materia_var).grid(row=4, column=1, padx=10, pady=5)

    ttk.Label(root, text="Créditos:").grid(row=5, column=0, padx=10, pady=5)
    ttk.Entry(root, textvariable=creditos_var).grid(row=5, column=1, padx=10, pady=5)

    ttk.Label(root, text="Valor:").grid(row=6, column=0, padx=10, pady=5)
    ttk.Entry(root, textvariable=valor_var).grid(row=6, column=1, padx=10, pady=5)

    ttk.Button(root, text="Registrar Actualizado", command=registrar_registro).grid(row=7, column=0, pady=10)
    ttk.Button(root, text="Modificar Registro", command=modificar_registro).grid(row=7, column=1, pady=10)
    ttk.Button(root, text="Eliminar Registro", command=eliminar_registro).grid(row=8, column=1, pady=10)
    ttk.Button(root, text="Ver Registros", command=mostrar_registros).grid(row=8, column=0, columnspan=3, pady=10)

    registrar_button = ttk.Button(root, text="Registrar Registro", command=registrar_registro)
    registrar_button.grid(row=7, column=0, columnspan=3, pady=10)

    # Árbol para mostrar registros
    registros_treeview = ttk.Treeview(root, columns=("ID Estudiante", "Nombre", "Fecha Nacimiento", "Carrera",
                                                     "Código Materia", "Nombre Materia", "Créditos", "Valor"),
                                      show="headings")
    registros_treeview.heading("ID Estudiante", text="ID Estudiante")
    registros_treeview.heading("Nombre", text="Nombre")
    registros_treeview.heading("Fecha Nacimiento", text="Fecha Nacimiento")
    registros_treeview.heading("Carrera", text="Carrera")
    registros_treeview.heading("Código Materia", text="Código Materia")
    registros_treeview.heading("Nombre Materia", text="Nombre Materia")
    registros_treeview.heading("Créditos", text="Créditos")
    registros_treeview.heading("Valor", text="Valor")
    registros_treeview.grid(row=10, column=0, columnspan=3, padx=1, pady=1)

    root.mainloop()

if __name__ == "__main__":
    main()

