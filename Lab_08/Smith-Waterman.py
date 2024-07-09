import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk, messagebox

# Función para inicializar la matriz de puntuación
def initialize_score_matrix_sw(seq1, seq2):
    n, m = len(seq1), len(seq2)
    score_matrix = np.zeros((n + 1, m + 1))
    direction_matrix = np.zeros((n + 1, m + 1), dtype=str)
    return score_matrix, direction_matrix

# Función para llenar la matriz de puntuación
def fill_score_matrix_sw(score_matrix, direction_matrix, seq1, seq2, match_score, mismatch_penalty, gap_penalty):
    n, m = len(seq1), len(seq2)
    
    max_i, max_j, max_score = 0, 0, 0  # Para rastrear la posición del puntaje máximo

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match = score_matrix[i-1][j-1] + (match_score if seq1[i-1] == seq2[j-1] else mismatch_penalty)
            delete = score_matrix[i-1][j] + gap_penalty
            insert = score_matrix[i][j-1] + gap_penalty
            score_matrix[i][j] = max(0, match, delete, insert)
            
            if score_matrix[i][j] == match:
                direction_matrix[i][j] = 'D'  # Diagonal
            elif score_matrix[i][j] == delete:
                direction_matrix[i][j] = 'U'  # Up
            elif score_matrix[i][j] == insert:
                direction_matrix[i][j] = 'L'  # Left
            else:
                direction_matrix[i][j] = '0'  # Zero

            # Rastrear la posición del puntaje máximo
            if score_matrix[i][j] > max_score:
                max_i, max_j, max_score = i, j, score_matrix[i][j]
                
    return score_matrix, direction_matrix, max_i, max_j

# Función para trazar la matriz de puntuación con flechas de dirección
def plot_score_matrix_with_directions_sw(score_matrix, direction_matrix, seq1, seq2):
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(score_matrix, annot=True, fmt=".1f", cmap="viridis", cbar=True, ax=ax)
    
    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):
            if direction_matrix[i][j] == 'D':
                ax.arrow(j - 0.5, i - 0.5, -0.5, -0.5, head_width=0.2, head_length=0.2, fc='red', ec='red')
            elif direction_matrix[i][j] == 'U':
                ax.arrow(j - 0.5, i - 0.5, 0, -0.5, head_width=0.2, head_length=0.2, fc='red', ec='red')
            elif direction_matrix[i][j] == 'L':
                ax.arrow(j - 0.5, i - 0.5, -0.5, 0, head_width=0.2, head_length=0.2, fc='red', ec='red')
    
    ax.set_xticks(np.arange(len(seq2) + 1) + 0.5)
    ax.set_yticks(np.arange(len(seq1) + 1) + 0.5)
    ax.set_xticklabels(['-'] + list(seq2))
    ax.set_yticklabels(['-'] + list(seq1))
    ax.set_xlabel('Secuencia 2')
    ax.set_ylabel('Secuencia 1')
    ax.set_title('Smith-Waterman Score Matrix with Directions')
    plt.show()

# Función para obtener el alineamiento óptimo
def traceback_sw(score_matrix, direction_matrix, seq1, seq2, start_i, start_j):
    aligned_seq1 = []
    aligned_seq2 = []
    i, j = start_i, start_j

    while i > 0 and j > 0 and score_matrix[i][j] != 0:
        if direction_matrix[i][j] == 'D':
            aligned_seq1.append(seq1[i-1])
            aligned_seq2.append(seq2[j-1])
            i -= 1
            j -= 1
        elif direction_matrix[i][j] == 'U':
            aligned_seq1.append(seq1[i-1])
            aligned_seq2.append('-')
            i -= 1
        elif direction_matrix[i][j] == 'L':
            aligned_seq1.append('-')
            aligned_seq2.append(seq2[j-1])
            j -= 1

    return ''.join(reversed(aligned_seq1)), ''.join(reversed(aligned_seq2))

# Función para ejecutar el algoritmo con los parámetros ingresados
def run_smith_waterman():
    seq1 = entry_seq1.get()
    seq2 = entry_seq2.get()
    match_score = int(entry_match_score.get())
    mismatch_penalty = int(entry_mismatch_penalty.get())
    gap_penalty = int(entry_gap_penalty.get())

    score_matrix, direction_matrix = initialize_score_matrix_sw(seq1, seq2)
    score_matrix, direction_matrix, max_i, max_j = fill_score_matrix_sw(score_matrix, direction_matrix, seq1, seq2, match_score, mismatch_penalty, gap_penalty)

    plot_score_matrix_with_directions_sw(score_matrix, direction_matrix, seq1, seq2)

    aligned_seq1, aligned_seq2 = traceback_sw(score_matrix, direction_matrix, seq1, seq2, max_i, max_j)
    messagebox.showinfo("Alineamiento Óptimo", f"Secuencia 1 alineada: {aligned_seq1}\nSecuencia 2 alineada: {aligned_seq2}")

# Crear la ventana principal
root = tk.Tk()
root.title("Smith-Waterman Algorithm")

# Crear y colocar los widgets
tk.Label(root, text="Secuencia 1:").grid(row=0, column=0, padx=10, pady=5)
entry_seq1 = tk.Entry(root)
entry_seq1.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Secuencia 2:").grid(row=1, column=0, padx=10, pady=5)
entry_seq2 = tk.Entry(root)
entry_seq2.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Puntaje de coincidencia:").grid(row=2, column=0, padx=10, pady=5)
entry_match_score = tk.Entry(root)
entry_match_score.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Penalización por desajuste:").grid(row=3, column=0, padx=10, pady=5)
entry_mismatch_penalty = tk.Entry(root)
entry_mismatch_penalty.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Penalización por gap:").grid(row=4, column=0, padx=10, pady=5)
entry_gap_penalty = tk.Entry(root)
entry_gap_penalty.grid(row=4, column=1, padx=10, pady=5)

btn_run = tk.Button(root, text="Ejecutar", command=run_smith_waterman)
btn_run.grid(row=5, columnspan=2, pady=10)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
