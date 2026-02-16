# -- coding: utf-8 --
"""
KenKen Puzzle Generator & Solver
--------------------------------
Autor: Angel De la Rosa
Descripción: Juego de lógica matemática implementado en Python con Tkinter.
Tecnologías: Backtracking (para generación), Recursividad, GUI (Tkinter).
"""

import tkinter as tk
from tkinter import messagebox
import random

class KenKen:
    def __init__(self, root):
        # Configuración inicial de la ventana principal
        self.root = root
        self.root.title("KenKen Puzzle - Angel De la Rosa")
        self.root.configure(bg='white') 
        
        # Variables de estado del juego
        self.size = 0          # Tamaño del tablero (NxN)
        self.grid = []         # Grid actual del jugador
        self.solucion = []     # Grid con la solución correcta
        self.grupos = []       # Lista de "jaulas" (cages) con sus operaciones
        self.celdas = []       # Referencias a los widgets Entry de la UI
        
        # UI Elements
        self.check_btn = None
        self.canvas = None
        self.tutorial_mostrado = False

        # Iniciar menú principal
        self.setup_menu()

    def setup_menu(self):
        """Muestra la pantalla de selección de dificultad."""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        if not self.tutorial_mostrado:
            self.mostrar_tutorial()
            self.tutorial_mostrado = True
        
        menu_frame = tk.Frame(self.root, bg='white')
        menu_frame.pack(expand=True, pady=50)
        
        tk.Label(menu_frame, text="Seleccione el tamaño del tablero", 
                font=('Arial', 20, 'bold'), bg='white').pack(pady=20)
        
        # Botones para elegir dificultad (Tamaño de matriz)
        tk.Button(menu_frame, text="5x5", font=('Arial', 16), width=12, height=2,
                 command=lambda: self.start_game(5)).pack(pady=10)

        tk.Button(menu_frame, text="7x7", font=('Arial', 16), width=12, height=2,
                 command=lambda: self.start_game(7)).pack(pady=10)

    def mostrar_tutorial(self):
        """Despliega las reglas básicas del juego al iniciar."""
        texto_tutorial = (
            "Bienvenido al KenKen:\n\n"
            "1) Seleccione un tamaño de tablero.\n" 
            "2) Cada grupo (jaula) tiene un número objetivo y una operación (ej. '6+' suma 6).\n"
            "3) REGLA DE ORO: No se pueden repetir números en filas ni columnas.\n"
            "4) Use 'Comprobar' para validar su lógica."
        )
        messagebox.showinfo("Tutorial", texto_tutorial)

    def validar_entrada(self, P):
        """Validador para asegurar que solo se ingresen números válidos en la UI."""
        if P == "": return True
        # Solo permite dígitos y evita el 0
        if len(P) == 1 and P.isdigit() and P != '0':
            return True
        return False

    def start_game(self, size):
        """Inicializa una nueva partida con el tamaño seleccionado."""
        self.size = size
        self.crear_kenken()   # Generación lógica
        self.setup_game_ui()  # Renderizado gráfico

    def crear_kenken(self):
        """Orquesta la generación del puzzle: Solución -> Grupos -> Tablero vacío."""
        # 1. Generar un Cuadrado Latino válido usando Backtracking
        self.solucion = self.generar_solucion(self.size)
        # 2. Dividir el tablero en grupos irregulares (jaulas)
        self.grupos = self.generar_grupos()
        # 3. Iniciar grid del jugador vacío
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]

    def generar_solucion(self, n):
        """
        Algoritmo de Backtracking para generar un tablero válido.
        Asegura que no haya números repetidos en filas ni columnas.
        """
        grid = [[0 for _ in range(n)] for _ in range(n)]
        
        def solve(row, col):
            # Caso base: Si llegamos al final del tablero, éxito
            if row == n: return True
            
            # Calcular siguiente posición
            next_row, next_col = (row, col + 1) if col + 1 < n else (row + 1, 0)
            
            # Probar números aleatorios del 1 al N
            nums = list(range(1, n + 1))
            random.shuffle(nums)
            
            for num in nums:
                # Verificar restricciones (Fila y Columna)
                if num not in grid[row] and num not in [grid[r][col] for r in range(n)]:
                    grid[row][col] = num
                    # Llamada recursiva
                    if solve(next_row, next_col): return True
                    # Backtracking: Si falla, reseteamos la celda
                    grid[row][col] = 0
            return False
            
        solve(0, 0)
        return grid

    def generar_grupos(self):
        """
        Divide el tablero en 'jaulas' aleatorias utilizando un algoritmo de expansión (Flood Fill modificado).
        Asigna operaciones matemáticas a cada grupo basándose en los números que contiene.
        """
        usada = [[False for _ in range(self.size)] for _ in range(self.size)]
        grupos = []
        grupo_min, grupo_max = 2, self.size - 1
         
        for i in range(self.size):
            for j in range(self.size):
                if usada[i][j]: continue
                
                # Intentar crear un grupo de tamaño aleatorio
                target_size = random.randint(grupo_min, grupo_max)
                celdas = self.crear_grupo(i, j, target_size, usada)
                
                # Si el grupo es muy pequeño (1 celda), lo fusionamos con otro
                if len(celdas) < 2:
                    self.fusionar_celda(celdas[0], grupos)
                    continue
                
                # Calcular operación y objetivo basado en la solución generada
                valores = [self.solucion[r][c] for r, c in celdas]
                operacion, objetivo = self.elegir_operacion(valores)
                grupos.append({'celdas': celdas, 'operacion': operacion, 'objetivo': objetivo})
        return grupos

    def crear_grupo(self, start_row, start_col, size, usada):
        """Expande un grupo desde una celda inicial buscando vecinos disponibles."""
        celdas = [(start_row, start_col)]
        usada[start_row][start_col] = True
        
        for _ in range(size - 1):
            posible = []
            # Buscar vecinos ortogonales (arriba, abajo, izq, der)
            for r, c in celdas:
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size and not usada[nr][nc]:
                        posible.append((nr, nc))
            
            if not posible: break
            
            # Elegir un vecino aleatorio para expandir el grupo
            next_c = random.choice(posible)
            celdas.append(next_c)
            usada[next_c[0]][next_c[1]] = True
        return celdas

    def fusionar_celda(self, celda, grupos):
        """Manejo de casos borde: Fusiona celdas huérfanas con grupos vecinos existentes."""
        r, c = celda
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            nr, nc = r + dr, c + dc
            for grupo in grupos:
                if (nr, nc) in grupo['celdas']:
                    grupo['celdas'].append((r, c))
                    # Recalcular la operación del grupo con el nuevo miembro
                    valores = [self.solucion[x][y] for x, y in grupo['celdas']]
                    grupo['operacion'], grupo['objetivo'] = self.elegir_operacion(valores)
                    return

    def elegir_operacion(self, valores):
        """Determina la operación matemática (+, -, *, /) más adecuada para un conjunto de valores."""
        operaciones = ['/', '-', '*', '+']
        random.shuffle(operaciones)
        
        for operacion in operaciones:
            if operacion == '/':
                # La división solo aplica a pares de números divisibles entre sí
                if len(valores) == 2:
                    v1, v2 = sorted(valores)
                    if v1 != 0 and v2 % v1 == 0: return '/', v2 // v1
            elif operacion == '-':
                # La resta solo aplica a pares
                if len(valores) == 2:
                    v1, v2 = sorted(valores)
                    return '-', v2 - v1
            elif operacion == '*':
                res = 1
                for v in valores: res *= v
                # Evitar números astronómicos para la dificultad actual
                if res <= 504: return '*', res
            elif operacion == '+':
                res = sum(valores)
                if res <= 504: return '+', res
        
        # Fallback: Si nada cuadra, usar suma por defecto
        return '+', sum(valores)

    def setup_game_ui(self):
        """Renderiza la interfaz gráfica del tablero usando Tkinter Canvas."""
        for widget in self.root.winfo_children(): widget.destroy()
        
        # Validacion de input en tiempo real
        vcmd = (self.root.register(self.validar_entrada), '%P')
        
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(padx=20, pady=20)  

        size_celda = 70
        canvas_width = size_celda * self.size

        # Canvas para dibujar líneas y bordes personalizados
        self.canvas = tk.Canvas(main_frame, width=canvas_width, height=canvas_width, 
                               bg='white', highlightthickness=0)
        self.canvas.pack(pady=10)
        self.celdas = []

        # Dibujar celdas y entradas
        for i in range(self.size):
            row_celdas = []
            for j in range(self.size):
                self.canvas.create_rectangle(j*size_celda, i*size_celda, 
                                           (j+1)*size_celda, (i+1)*size_celda, outline='#D3D3D3')
                entry = tk.Entry(self.canvas, font=('Arial', 20, 'bold'), fg='goldenrod', 
                               bg='white', justify='center', bd=0, 
                               validate='key', validatecommand=vcmd)
                self.canvas.create_window(j*size_celda + 35, i*size_celda + 40, 
                                        window=entry, width=40, height=40)
                row_celdas.append(entry)
            self.celdas.append(row_celdas)
          
        # Dibujar bordes gruesos para definir las "jaulas" visualmente
        self.resaltar_grupos(size_celda)
        self.canvas.create_rectangle(2, 2, canvas_width-2, canvas_width-2, outline='black', width=4)
        
        # Panel de Botones
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(pady=10)
        
        self.check_btn = tk.Button(btn_frame, text="Comprobar", font=('Arial', 10, 'bold'), width=12,
                                  bg='#4CAF50', fg='white', command=self.verificar_solucion)
        self.check_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Borrar tablero", font=('Arial', 10), width=12,
                 bg='#f44336', fg='white', command=self.borrar_tablero).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Solución", font=('Arial', 10), width=10,
                 command=self.mostrar_solucion).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Nueva ronda", font=('Arial', 10, 'bold'), width=12,
                 bg='#2196F3', fg='white', command=self.setup_menu).pack(side=tk.LEFT, padx=5)
        
        self.root.focus_force()

    def borrar_tablero(self):
        """Reinicia el input del usuario sin cambiar el puzzle."""
        if self.check_btn:
            self.check_btn.config(state=tk.NORMAL, bg='#4CAF50')
        for i in range(self.size):
            for j in range(self.size):
                self.celdas[i][j].config(state=tk.NORMAL, fg='goldenrod')
                self.celdas[i][j].delete(0, tk.END)

    def resaltar_grupos(self, size_celda):
        """Algoritmo de dibujo: Traza líneas gruesas solo en los bordes externos de cada grupo."""
        for grupo in self.grupos:
            celdas = grupo['celdas']
            # Poner la etiqueta de la operación en la celda superior izquierda del grupo
            top = min(celdas, key=lambda c: (c[0], c[1]))
            self.canvas.create_text(top[1]*size_celda+5, top[0]*size_celda+5, 
                                    text=f"{grupo['objetivo']}{grupo['operacion']}", 
                                    font=('Arial', 8, 'bold'), anchor='nw', fill='black')
            
            # Dibujar bordes solo si el vecino no pertenece al mismo grupo
            for r, c in celdas:
                x1, y1, x2, y2 = c*size_celda, r*size_celda, (c+1)*size_celda, (r+1)*size_celda
                if (r-1, c) not in celdas: self.canvas.create_line(x1, y1, x2, y1, width=3, fill='black') # Arriba
                if (r+1, c) not in celdas: self.canvas.create_line(x1, y2, x2, y2, width=3, fill='black') # Abajo
                if (r, c-1) not in celdas: self.canvas.create_line(x1, y1, x1, y2, width=3, fill='black') # Izquierda
                if (r, c+1) not in celdas: self.canvas.create_line(x2, y1, x2, y2, width=3, fill='black') # Derecha

    def verificar_solucion(self):
        """
        Valida el estado actual del tablero contra las reglas matemáticas y de unicidad.
        """
        try:
            current_grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
            lleno = True
            
            # 1. Extraer datos de la UI
            for i in range(self.size):
                for j in range(self.size):
                    valor = self.celdas[i][j].get()
                    if not valor: lleno = False
                    else: current_grid[i][j] = int(valor)
            
            if not lleno:
                messagebox.showwarning("Incompleto", "Por favor, llena todas las celdas antes de comprobar.")
                return
            
            # 2. Validar matemáticas de cada grupo (jaula)
            for grupo in self.grupos:
                valores = [current_grid[r][c] for r, c in grupo['celdas']]
                op, obj = grupo['operacion'], grupo['objetivo']
                valido = False
                
                if op == '+': valido = (sum(valores) == obj)
                elif op == '*':
                    res = 1
                    for v in valores: res *= v
                    valido = (res == obj)
                elif op == '-':
                    v1, v2 = sorted(valores)
                    valido = (v2 - v1 == obj)
                elif op == '/':
                    v1, v2 = sorted(valores)
                    valido = (v1 != 0 and v2 / v1 == obj)
                
                if not valido:
                    messagebox.showerror("Incorrecto", f"Error en el grupo {obj}{op}. Revisa tus cálculos.")
                    return
            
            messagebox.showinfo("¡Felicidades!", "¡Has resuelto el KenKen correctamente!")
            
        except Exception as e:
            print(f"Error de validación: {e}")
            messagebox.showerror("Error", "Ocurrió un error al validar.")

    def mostrar_solucion(self):
        """Cheat mode: Rellena el tablero con la solución generada."""
        if self.check_btn:
            self.check_btn.config(state=tk.DISABLED, bg='#cccccc')
        for i in range(self.size):
            for j in range(self.size):
                self.celdas[i][j].config(state=tk.NORMAL)
                self.celdas[i][j].delete(0, tk.END)
                self.celdas[i][j].insert(0, str(self.solucion[i][j]))
                self.celdas[i][j].config(fg='blue', state='readonly')

if __name__ == "__main__":
    root = tk.Tk()
    app = KenKen(root)
    root.mainloop()