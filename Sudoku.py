import tkinter as tk
from tkinter import messagebox
import random

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        # Adaptation à une taille d'écran de mobile
        self.root.geometry('360x640') 
        self.grille = [[0] * 9 for _ in range(9)]
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.selected_row = -1
        self.selected_col = -1
        self.fill_grid()
        self.create_grid()
        self.root.bind("<Key>", self.handle_keypress)
        self.create_number_bar()

    def fill_grid(self):
        # Génère une grille partiellement remplie
        self.generate_sudoku(3)  # Exemple avec 3 nombres par ligne
        for i in range(9):
            for j in range(9):
                if self.grille[i][j] != 0:
                    self.cells[i][j] = self.grille[i][j]

    def generate_sudoku(self, num_per_row):
        for i in range(9):
            nums = random.sample(range(1, 10), num_per_row)
            for num in nums:
                col = random.randint(0, 8)
                if self.est_valide(i, col, num):
                    self.grille[i][col] = num

    def est_valide(self, row, col, num, check_completion=False):
        # Vérifie la validité de num dans la position (row, col)
        for x in range(9):
            if self.grille[row][x] == num or self.grille[x][col] == num:
                return False
        startRow = row - row % 3
        startCol = col - col % 3
        for i in range(3):
            for j in range(3):
                if self.grille[i + startRow][j + startCol] == num:
                    return False
        if check_completion:
            return self.verifier_completion()
        return True

    def verifier_completion(self):
        for row in range(9):
            for col in range(9):
                num = self.grille[row][col]
                if num == 0 or not self.est_valide(row, col, num):
                    return False
        return True

    def create_grid(self):
        for i in range(9):
            for j in range(9):
                if (i // 3 * 3 + j // 3) % 2 == 0:
                    color = 'grey'  # Couleur plus foncée pour les carrés 3x3
                else:
                    color = 'white'  # Couleur plus claire pour les autres carrés
                
                cell_frame = tk.Frame(self.root, bg=color, highlightthickness=0, width=40, height=40)
                cell_frame.grid(row=i, column=j, padx=1, pady=1, sticky='nsew')
                cell = tk.Entry(cell_frame, font=('Arial', 18), borderwidth=0, justify='center')
                cell.pack(expand=True, fill='both')
                
                if (i % 3 == 0 and i != 0) and (j % 3 == 0 and j != 0):
                    cell_frame.grid_configure(padx=(4,1), pady=(4,1))
                elif i % 3 == 0 and i != 0:
                    cell_frame.grid_configure(pady=(4,1))
                elif j % 3 == 0 and j != 0:
                    cell_frame.grid_configure(padx=(4,1))
                
                cell.bind("<Button-1>", lambda event, row=i, col=j: self.select_cell(row, col))
                if self.grille[i][j] != 0:
                    cell.insert(tk.END, str(self.grille[i][j]))
                    cell.config(state='readonly', readonlybackground='lightgrey', fg='black')
                self.cells[i][j] = cell
        
        # Configurer l'expansion des lignes et des colonnes
        for i in range(9):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

    def select_cell(self, row, col):
        self.selected_row, self.selected_col = row, col
        for i in range(9):
            for j in range(9):
                self.cells[i][j].configure(bg='white')
        self.cells[row][col].configure(bg='lightgrey')

    def handle_keypress(self, event):
        if self.selected_row >= 0 and self.selected_col >= 0 and event.char.isdigit():
            num = int(event.char)
            if 1 <= num <= 9 and self.est_valide(self.selected_row, self.selected_col, num):
                self.grille[self.selected_row][self.selected_col] = num
                self.cells[self.selected_row][self.selected_col].delete(0, tk.END)
                self.cells[self.selected_row][self.selected_col].insert(tk.END, str(num))
                if self.verifier_completion():
                    messagebox.showinfo("Succès", "Félicitations ! Vous avez complété le Sudoku avec succès.")
            else:
                messagebox.showerror("Erreur", "Coup invalide selon les règles du Sudoku.")

    def create_number_bar(self):
        self.number_bar = tk.Frame(self.root)
        self.number_bar.grid(row=9, column=0, columnspan=9, sticky='nsew')

        for num in range(1, 10):
            btn = tk.Button(self.number_bar, text=str(num), command=lambda n=num: self.place_number(n), width=2, height=1)
            btn.grid(row=0, column=num-1, sticky='nsew', padx=1, pady=1)
            self.root.grid_columnconfigure(num-1, weight=1)

    def place_number(self, num):
        if self.selected_row >= 0 and self.selected_col >= 0:  # Vérifiez qu'une cellule est sélectionnée
            current_cell = self.cells[self.selected_row][self.selected_col]
            current_cell_value = current_cell.get()
            
            # Tentez de placer le numéro et vérifiez la validité du coup
            current_cell.delete(0, tk.END)
            current_cell.insert(tk.END, str(num))
            if not self.est_valide(self.selected_row, self.selected_col, num):
                current_cell.delete(0, tk.END)
                current_cell.insert(tk.END, current_cell_value)  # Remettez l'ancienne valeur si le coup est invalide
                messagebox.showwarning("Impossible", "Ce numéro ne peut pas aller ici selon les règles du Sudoku.")
                return
            
            # Si le numéro est valide, mettez à jour la grille
            self.grille[self.selected_row][self.selected_col] = num
            if self.verifier_completion():
                messagebox.showinfo("Succès", "Félicitations ! Vous avez complété le Sudoku avec succès.")


if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()
