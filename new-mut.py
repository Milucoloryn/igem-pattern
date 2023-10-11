import re
import tkinter as tk
from tkinter import messagebox, scrolledtext


class MutP(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.winfo_toplevel().title("Welcome to Mut-P")

        self.num_seq_label = tk.Label(self, text="Number of sequences：")
        self.num_seq_label.pack()
        self.num_seq_entry = tk.Entry(self)
        self.num_seq_entry.pack()

        self.generate = tk.Button(self)
        self.generate["text"] = "Generate Input Fields"
        self.generate["command"] = self.generate_inputs
        self.generate.pack()

        self.execute = tk.Button(self)
        self.execute["text"] = "Execute Mutation"
        self.execute["command"] = self.mutate_protein_str
        self.execute.pack()

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack()

        self.result_text = scrolledtext.ScrolledText(self)
        self.result_text.pack()

    def generate_inputs(self):
        try:
            num_sequences = int(self.num_seq_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid number of sequences")
            return

        self.entries = []
        self.input_frame = tk.Frame(self)
        self.input_frame.pack()

        self.canvas = tk.Canvas(self.input_frame)
        self.canvas.pack(side="left")

        scrollbar = tk.Scrollbar(self.input_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="left", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.inputs = tk.Frame(self.canvas)

        for i in range(num_sequences):
            label = tk.Label(self.inputs, text=f"Sequence {i+1}：")
            label.pack()
            seq_entry = tk.Entry(self.inputs)
            seq_entry.pack()
            pos_label = tk.Label(self.inputs, text=f"Mutation site for Sequence {i+1}（comma-separated）：")
            pos_label.pack()
            pos_entry = tk.Entry(self.inputs)
            pos_entry.pack()
            aa_label = tk.Label(self.inputs, text=f"Amino acid for Sequence {i+1}（comma-separated）：")
            aa_label.pack()
            aa_entry = tk.Entry(self.inputs)
            aa_entry.pack()
            self.entries.append((seq_entry, pos_entry, aa_entry))

        self.canvas.create_window((0,0), window=self.inputs, anchor="nw")
        self.inputs.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def mutate_protein_str(self):
        for i, (seq_entry, pos_entry, aa_entry) in enumerate(self.entries):
            seq = seq_entry.get()
            positions = list(map(int, pos_entry.get().split(',')))
            targets = aa_entry.get().split(',')

            if not self.valid_sequence(seq):
                messagebox.showerror("Error", f"Wrong sequence in Sequence {i+1}")
                return

            if self.is_dna(seq):
                messagebox.showinfo("Info", f"DNA sequence detected in Sequence {i+1}")

            for position, target in zip(positions, targets):
                seq = self.mutate_protein(seq, position, target)
                if not isinstance(seq, str):
                    result = f"Invalid option in Sequence {i+1}, Please check the sequence and mutation site."
                    break
            else:
                result = f"Mutated sequence for Sequence {i+1} is: {seq}\n"

            self.result_text.insert(tk.END, result)

    def mutate_protein(self, seq, position, target):
        if not re.fullmatch("^[ACDEFGHIKLMNPQRSTVWY]*$", seq):
            return "Incorrect Sequence"

        if position > len(seq) or position < 1:
            return "Incorrect Sequence"

        if target not in 'ACDEFGHIKLMNPQRSTVWY':
            return "Incorrect amino acids"

        return seq[:position - 1] + target + seq[position:]

    def valid_sequence(self, seq):
        return not any(c in seq for c in "BJOUXZ")

    def is_dna(self, seq):
        return set(seq) <= set("ACTG") and len(set(seq)) == 4


root = tk.Tk()
app = MutP(master=root)
app.mainloop()