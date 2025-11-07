import tkinter as tk
from tkinter import ttk

def reorder_pdfs(pdfs):
    """Show a GUI to reorder PDFs. Returns reordered list or None if cancelled."""
    result = {'pdfs': None}
    
    def move_up():
        selected = listbox.curselection()
        if selected and selected[0] > 0:
            idx = selected[0]
            pdfs[idx], pdfs[idx-1] = pdfs[idx-1], pdfs[idx]
            update_listbox()
            listbox.selection_set(idx-1)
    
    def move_down():
        selected = listbox.curselection()
        if selected and selected[0] < len(pdfs) - 1:
            idx = selected[0]
            pdfs[idx], pdfs[idx+1] = pdfs[idx+1], pdfs[idx]
            update_listbox()
            listbox.selection_set(idx+1)
    
    def update_listbox():
        listbox.delete(0, tk.END)
        for i, pdf in enumerate(pdfs, 1):
            listbox.insert(tk.END, f"{i}. {pdf.name}")
    
    def confirm():
        result['pdfs'] = pdfs.copy()
        root.quit()
        root.destroy()
    
    def cancel():
        root.quit()
        root.destroy()
    
    root = tk.Tk()
    root.title("Reorder PDFs")
    root.geometry("600x500")
    
    tk.Label(root, text="Reorder PDFs before merging:", font=("Arial", 12, "bold")).pack(pady=10)
    
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("Arial", 10))
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)
    
    update_listbox()
    listbox.selection_set(0)
    
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    
    tk.Button(btn_frame, text="Move Up ↑", command=move_up, width=12).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Move Down ↓", command=move_down, width=12).pack(side=tk.LEFT, padx=5)
    
    confirm_frame = tk.Frame(root)
    confirm_frame.pack(pady=10)
    
    tk.Button(confirm_frame, text="Merge PDFs", command=confirm, bg="#4CAF50", fg="white", width=15, height=2).pack(side=tk.LEFT, padx=10)
    tk.Button(confirm_frame, text="Cancel", command=cancel, width=15, height=2).pack(side=tk.LEFT, padx=10)
    
    root.mainloop()
    
    return result['pdfs']