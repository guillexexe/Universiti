import tkinter as tk
from tkinter import ttk
import random

# --- Clase Proceso ---
class Proceso:
    def __init__(self, id, tamano, prioridad, tiempo_ejecucion):
        self.id = id
        self.tamano = tamano
        self.prioridad = prioridad
        self.tiempo_ejecucion = tiempo_ejecucion
        self.estado = "activo"

    def __str__(self):
        return f"ID: {self.id} | Tamaño: {self.tamano}MB | Prioridad: {self.prioridad} | Estado: {self.estado}"

# --- Clase GestorMemoria ---
class GestorMemoria:
    def __init__(self, tamano_total):
        self.tamano_total = tamano_total
        self.memoria_usada = 0
        self.procesos_activos = []
        self.bloques_libres = [tamano_total]
        self.swap = []

    def agregar_proceso(self, proceso):
        for i, bloque in enumerate(self.bloques_libres):
            if bloque >= proceso.tamano:
                self.bloques_libres[i] -= proceso.tamano
                self.procesos_activos.append(proceso)
                self.memoria_usada += proceso.tamano
                self._actualizar_bloques()
                return f"Proceso {proceso.id} agregado a la memoria principal."
        return self._realizar_swapping(proceso)

    def _realizar_swapping(self, proceso):
        if self.procesos_activos:
            proceso_removido = self.procesos_activos.pop(0)
            self.swap.append(proceso_removido)
            self.memoria_usada -= proceso_removido.tamano
            self.bloques_libres.append(proceso_removido.tamano)
            self._actualizar_bloques()
            return f"Proceso {proceso_removido.id} movido a swap. Intentando agregar el proceso {proceso.id}."
        return "No se puede realizar swapping; no hay procesos activos."

    def liberar_memoria(self, id_proceso):
        for proceso in self.procesos_activos:
            if proceso.id == id_proceso:
                self.procesos_activos.remove(proceso)
                self.memoria_usada -= proceso.tamano
                self.bloques_libres.append(proceso.tamano)
                self._actualizar_bloques()
                return f"Proceso {proceso.id} liberado."
        return "Proceso no encontrado en la memoria principal."

    def compactar(self):
        memoria_compactada = sum(self.bloques_libres)
        self.bloques_libres = [memoria_compactada]
        return f"Memoria compactada: {memoria_compactada}MB disponible."

    def reubicar(self):
        memoria_libre = sum(self.bloques_libres)
        self.bloques_libres = []
        posicion_actual = 0
        for proceso in self.procesos_activos:
            posicion_actual += proceso.tamano
        self.bloques_libres.append(memoria_libre)
        return "Todos los procesos activos han sido reubicados. La fragmentación externa ha sido eliminada."

    def revisar_swap(self):
        while self.swap:
            proceso_en_swap = self.swap[0]
            if proceso_en_swap.tamano <= self.bloques_libres[0]:
                self.swap.pop(0)
                self.agregar_proceso(proceso_en_swap)
            else:
                break

    def _actualizar_bloques(self):
        self.bloques_libres = [bloque for bloque in self.bloques_libres if bloque > 0]

# --- Clase SimuladorInterfaz ---
class SimuladorInterfaz:
    def __init__(self, root, gestor):
        self.root = root
        self.gestor = gestor

        self.root.title("Simulador de Gestión de Memoria")
        self.root.geometry("800x600")

        # Crear Notebook para pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        # Pestaña de Simulación
        self.tab_simulacion = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_simulacion, text="Simulación")

        # Pestaña de Historial
        self.tab_historial = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_historial, text="Historial")

        # Elementos de la pestaña Simulación
        self.estado_label = tk.Label(self.tab_simulacion, text="Estado de la Memoria", font=("Arial", 14))
        self.estado_label.pack(pady=10)

        self.canvas = tk.Canvas(self.tab_simulacion, width=600, height=200, bg="white")
        self.canvas.pack()

        self.swap_label = tk.Label(self.tab_simulacion, text="Procesos en Swap", font=("Arial", 12))
        self.swap_label.pack(pady=5)

        self.swap_list = tk.Listbox(self.tab_simulacion, width=80, height=5)
        self.swap_list.pack()

        self.leyenda_label = tk.Label(self.tab_simulacion, text="Tareas Activas", font=("Arial", 12), fg="blue")
        self.leyenda_label.pack(pady=5)

        self.tareas_text = tk.Text(self.tab_simulacion, width=80, height=8, bg="lightgrey", state="disabled")
        self.tareas_text.pack()

        self.botones_frame = tk.Frame(self.tab_simulacion)
        self.botones_frame.pack(pady=10)

        self.generar_btn = tk.Button(self.botones_frame, text="Generar Tarea", command=self.generar_tarea)
        self.generar_btn.grid(row=0, column=0, padx=5)

        self.liberar_btn = tk.Button(self.botones_frame, text="Liberar Memoria", command=self.liberar_memoria)
        self.liberar_btn.grid(row=0, column=1, padx=5)

        self.compactar_btn = tk.Button(self.botones_frame, text="Compactar Memoria", command=self.compactar_memoria)
        self.compactar_btn.grid(row=0, column=2, padx=5)

        self.reubicar_btn = tk.Button(self.botones_frame, text="Reubicar Memoria", command=self.reubicar_memoria)
        self.reubicar_btn.grid(row=0, column=3, padx=5)

        # Elementos de la pestaña Historial
        self.historial_text = tk.Text(self.tab_historial, width=80, height=30, bg="white", state="disabled")
        self.historial_text.pack()

        self.actualizar_vista()

    def agregar_a_historial(self, mensaje):
        self.historial_text.configure(state="normal")
        self.historial_text.insert(tk.END, f"{mensaje}\n")
        self.historial_text.configure(state="disabled")
        self.historial_text.see(tk.END)

    def actualizar_vista(self):
        self.canvas.delete("all")
        x = 10
        for proceso in self.gestor.procesos_activos:
            ancho = (proceso.tamano / self.gestor.tamano_total) * 580
            self.canvas.create_rectangle(x, 50, x + ancho, 150, fill="blue")
            self.canvas.create_text(x + ancho / 2, 100, text=f"P{proceso.id}", fill="white")
            x += ancho

        for bloque in self.gestor.bloques_libres:
            ancho = (bloque / self.gestor.tamano_total) * 580
            self.canvas.create_rectangle(x, 50, x + ancho, 150, fill="gray")
            self.canvas.create_text(x + ancho / 2, 100, text=f"{bloque}MB", fill="black")
            x += ancho

        self.swap_list.delete(0, tk.END)
        for proceso in self.gestor.swap:
            self.swap_list.insert(tk.END, f"Proceso {proceso.id} - Tamaño: {proceso.tamano}MB")

        self.tareas_text.configure(state="normal")
        self.tareas_text.delete(1.0, tk.END)
        for proceso in self.gestor.procesos_activos:
            self.tareas_text.insert(tk.END, f"ID: {proceso.id} | Tamaño: {proceso.tamano}MB | Prioridad: {proceso.prioridad} | Estado: {proceso.estado}\n")
        self.tareas_text.configure(state="disabled")

    def generar_tarea(self):
        id_proceso = len(self.gestor.procesos_activos) + len(self.gestor.swap) + 1
        tamano = random.randint(10, 50)  # Tamaño entre 10 y 50MB
        prioridad = random.randint(1, 10)  # Prioridad entre 1 y 10
        tiempo_ejecucion = random.randint(1, 20)  # Tiempo de ejecución en segundos
        nueva_tarea = Proceso(id_proceso, tamano, prioridad, tiempo_ejecucion)

        mensaje = self.gestor.agregar_proceso(nueva_tarea)
        self.agregar_a_historial(f"[Generar] {mensaje}")
        self.actualizar_vista()

    def liberar_memoria(self):
        if self.gestor.procesos_activos:
            id_proceso = self.gestor.procesos_activos[0].id
            mensaje = self.gestor.liberar_memoria(id_proceso)
            self.agregar_a_historial(f"[Liberar] {mensaje}")
            self.actualizar_vista()
        else:
            self.agregar_a_historial("[Liberar] No hay procesos activos para liberar.")

    def compactar_memoria(self):
        mensaje = self.gestor.compactar()
        self.agregar_a_historial(f"[Compactar] {mensaje}")
        self.actualizar_vista()

    def reubicar_memoria(self):
        mensaje = self.gestor.reubicar()
        self.gestor.revisar_swap()  # Intentar mover procesos desde swap si es posible
        self.agregar_a_historial(f"[Reubicar] {mensaje}")
        self.actualizar_vista()

# --- Ejecutar el Simulador ---
if __name__ == "__main__":
    gestor = GestorMemoria(200)  # Configurar 200MB de memoria total
    root = tk.Tk()  # Crear la ventana principal
    app = SimuladorInterfaz(root, gestor)  # Inicializar la interfaz gráfica
    root.mainloop()  # Iniciar el bucle principal de la interfaz
