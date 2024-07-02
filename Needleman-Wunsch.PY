import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk, messagebox

# Función para inicializar la matriz de puntuación
def initialize_score_matrix_nw(seq1, seq2, gap_penalty):
    n, m = len(seq1), len(seq2)
    score_matrix = np.zeros((n + 1, m + 1))
    direction_matrix = np.zeros((n + 1, m + 1), dtype=str)

    for i in range(1, n + 1):
        score_matrix[i][0] = gap_penalty * i
        direction_matrix[i][0] = 'U'  # Up

    for j in range(1, m + 1):
        score_matrix[0][j] = gap_penalty * j
        direction_matrix[0][j] = 'L'  # Left

    return score_matrix, direction_matrix

# Función para llenar la matriz de puntuación
def fill_score_matrix_nw(score_matrix, direction_matrix, seq1, seq2, match_score, mismatch_penalty, gap_penalty):
    n, m = len(seq1), len(seq2)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match = score_matrix[i-1][j-1] + (match_score if seq1[i-1] == seq2[j-1] else mismatch_penalty)
            delete = score_matrix[i-1][j] + gap_penalty
            insert = score_matrix[i][j-1] + gap_penalty
            score_matrix[i][j] = max(match, delete, insert)

            if score_matrix[i][j] == match:
                direction_matrix[i][j] = 'D'  # Diagonal
            elif score_matrix[i][j] == delete:
                direction_matrix[i][j] = 'U'  # Up
            elif score_matrix[i][j] == insert:
                direction_matrix[i][j] = 'L'  # Left

    return score_matrix, direction_matrix

# Función para trazar la matriz de puntuación con flechas de dirección
def plot_score_matrix_with_directions_nw(score_matrix, direction_matrix, seq1, seq2):
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
    ax.set_xlabel('Sequence 2')
    ax.set_ylabel('Sequence 1')
    ax.set_title('Needleman-Wunsch Score Matrix with Directions')
    plt.show()

# Función para obtener el alineamiento óptimo
def traceback_nw(direction_matrix, seq1, seq2):
    aligned_seq1 = []
    aligned_seq2 = []
    i, j = len(seq1), len(seq2)

    while i > 0 or j > 0:
        if i > 0 and j > 0 and direction_matrix[i][j] == 'D':
            aligned_seq1.append(seq1[i-1])
            aligned_seq2.append(seq2[j-1])
            i -= 1
            j -= 1
        elif i > 0 and direction_matrix[i][j] == 'U':
            aligned_seq1.append(seq1[i-1])
            aligned_seq2.append('-')
            i -= 1
        else:
            aligned_seq1.append('-')
            aligned_seq2.append(seq2[j-1])
            j -= 1

    return ''.join(reversed(aligned_seq1)), ''.join(reversed(aligned_seq2))

# Función para ejecutar el algoritmo con los parámetros ingresados
def run_needleman_wunsch():
    seq1 = entry_seq1.get()
    seq2 = entry_seq2.get()
    match_score = int(entry_match_score.get())
    mismatch_penalty = int(entry_mismatch_penalty.get())
    gap_penalty = int(entry_gap_penalty.get())

    score_matrix, direction_matrix = initialize_score_matrix_nw(seq1, seq2, gap_penalty)
    score_matrix, direction_matrix = fill_score_matrix_nw(score_matrix, direction_matrix, seq1, seq2, match_score, mismatch_penalty, gap_penalty)
    
    plot_score_matrix_with_directions_nw(score_matrix, direction_matrix, seq1, seq2)

    aligned_seq1, aligned_seq2 = traceback_nw(direction_matrix, seq1, seq2)
    messagebox.showinfo("Alineamiento Óptimo", f"Secuencia 1 alineada: {aligned_seq1}\nSecuencia 2 alineada: {aligned_seq2}")

# Crear la ventana principal
root = tk.Tk()
root.title("Needleman-Wunsch Algorithm")

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

btn_run = tk.Button(root, text="Ejecutar", command=run_needleman_wunsch)
btn_run.grid(row=5, columnspan=2, pady=10)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
