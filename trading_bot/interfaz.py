import tkinter as tk
from tkinter import ttk, messagebox
from historial import leer_historial as cargar_historial, borrar_historial
from utils.config import obtener_saldo_actual
from trading_bot_core import ciclo_de_operaciones, detener_bot
import threading

class InterfazTrading:
    def __init__(self, root):
        self.root = root
        self.root.title("Bot de Trading Automático")
        self.root.configure(bg='#111111')
        self.root.geometry("920x600")
        self.root.resizable(False, False)

        self.bot_activo = False

        self.crear_panel_izquierdo()
        self.crear_panel_derecho()

    def crear_panel_izquierdo(self):
        panel = tk.Frame(self.root, bg='#111111')
        panel.pack(side=tk.LEFT, padx=30, pady=20, fill=tk.Y)

        self.inversion_var = tk.StringVar(value="10000")
        self.capital_var = tk.StringVar(value="50000")
        self.meta_var = tk.StringVar(value="200000")
        self.tiempo_var = tk.StringVar(value="30s")
        self.voz_var = tk.BooleanVar(value=True)
        self.ws_var = tk.BooleanVar(value=True)

        self._agregar_label_entry(panel, "Inversión inicial ($):", self.inversion_var)
        self._agregar_label_entry(panel, "Capital total disponible ($):", self.capital_var)
        self._agregar_label_entry(panel, "Meta de ciclo ($):", self.meta_var)

        tk.Label(panel, text="Tiempo de operación:", fg="white", bg='#111111').pack(anchor="w", pady=(20, 0))
        self.tiempo_combo = ttk.Combobox(panel, textvariable=self.tiempo_var, values=["30s", "1min", "2min"], width=10)
        self.tiempo_combo.pack(anchor="w", pady=(5, 10))

        tk.Checkbutton(panel, text="Voz activada", variable=self.voz_var, bg='#111111', fg='white', selectcolor='#111111').pack(anchor="w")
        tk.Checkbutton(panel, text="WhatsApp activado", variable=self.ws_var, bg='#111111', fg='white', selectcolor='#111111').pack(anchor="w")

        tk.Button(panel, text="Iniciar bot", command=self.iniciar_bot_thread, bg='#00c853', fg='white', font=('Arial', 12, 'bold')).pack(pady=(30, 10), fill="x")
        tk.Button(panel, text="Detener bot", command=self.detener_bot_accion, bg='#d32f2f', fg='white', font=('Arial', 12, 'bold')).pack(fill="x")
        tk.Button(panel, text="Borrar historial", command=self.borrar_historial_confirmar, bg='#607d8b', fg='white', font=('Arial', 10, 'bold')).pack(pady=(20, 0), fill="x")

    def _agregar_label_entry(self, parent, texto, variable):
        tk.Label(parent, text=texto, fg="white", bg='#111111').pack(anchor="w", pady=(10, 0))
        tk.Entry(parent, textvariable=variable, width=25).pack(anchor="w")

    def crear_panel_derecho(self):
        panel_derecho = tk.Frame(self.root, bg='#1e1e1e')
        panel_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=20)

        self.saldo_label = tk.Label(panel_derecho, text=f"Saldo actual: ${obtener_saldo_actual()}", fg='cyan', bg='#1e1e1e', font=('Arial', 14, 'bold'))
        self.saldo_label.pack(pady=(0, 10), anchor="center")

        self.historial_text = tk.Text(panel_derecho, bg='#111111', fg='white', font=('Consolas', 10), state='disabled', wrap="none")
        self.historial_text.pack(fill=tk.BOTH, expand=True)

        self.actualizar_historial_en_vivo()

    def actualizar_historial(self):
        operaciones = cargar_historial()
        self.historial_text.configure(state='normal')
        self.historial_text.delete(1.0, tk.END)

        fecha_actual = ""
        for op in operaciones:
            if op['fecha'] != fecha_actual:
                fecha_actual = op['fecha']
                self.historial_text.insert(tk.END, f"\n📅 {fecha_actual}\n", 'fecha')
            color = 'green' if op['resultado'] == 'ganancia' else 'red'
            self.historial_text.insert(tk.END, f"{op['activo']} - {op['resultado'].upper()} ${op['monto']}\n", color)

        self.historial_text.tag_configure('green', foreground='lime')
        self.historial_text.tag_configure('red', foreground='red')
        self.historial_text.tag_configure('fecha', foreground='cyan', font=('Consolas', 10, 'bold'))
        self.historial_text.configure(state='disabled')
        self.historial_text.see(tk.END)

        self.saldo_label.config(text=f"Saldo actual: ${obtener_saldo_actual()}")

    def actualizar_historial_en_vivo(self):
        self.actualizar_historial()
        self.root.after(2000, self.actualizar_historial_en_vivo)  # Cada 2 segundos

    def iniciar_bot_thread(self):
        t = threading.Thread(target=self.iniciar_bot)
        t.start()

    def iniciar_bot(self):
        self.bot_activo = True
        inversion = int(self.inversion_var.get())
        meta = int(self.meta_var.get())
        capital = int(self.capital_var.get())
        tiempo = self.tiempo_var.get()
        voz = self.voz_var.get()
        whatsapp = self.ws_var.get()

        ciclo_de_operaciones(
            inversion_inicial=inversion,
            meta_final=meta,
            tiempo_op=tiempo,
            capital_total=capital,
            voz_activa=voz,
            whatsapp_activo=whatsapp
        )

    def detener_bot_accion(self):
        detener_bot()
        self.bot_activo = False

    def borrar_historial_confirmar(self):
        if messagebox.askyesno("Confirmar", "¿Estás seguro que querés borrar todo el historial?"):
            borrar_historial()
            self.actualizar_historial()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazTrading(root)
    root.mainloop()
