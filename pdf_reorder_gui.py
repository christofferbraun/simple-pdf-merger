import tkinter as tk

def reorder_pdfs(pdfs):
    """Show a GUI to reorder PDFs with drag and drop. Returns reordered list or None if cancelled."""
    result = {'pdfs': None}
    drag_data = {'index': None}
    
    def on_drag_start(event):
        index = listbox.nearest(event.y)
        drag_data['index'] = index
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(index)
    
    def on_drag_motion(event):
        current_index = listbox.nearest(event.y)
        if drag_data['index'] is not None and current_index != drag_data['index']:
            # Swap items
            pdfs[drag_data['index']], pdfs[current_index] = pdfs[current_index], pdfs[drag_data['index']]
            drag_data['index'] = current_index
            update_listbox()
            listbox.selection_set(current_index)
    
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
    
    tk.Label(root, text="Drag and drop to reorder PDFs:", font=("Arial", 12, "bold")).pack(pady=10)
    
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("Arial", 10))
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)
    
    # Bind drag and drop events
    listbox.bind('<Button-1>', on_drag_start)
    listbox.bind('<B1-Motion>', on_drag_motion)
    
    update_listbox()
    listbox.selection_set(0)
    
    confirm_frame = tk.Frame(root)
    confirm_frame.pack(pady=20)
    
    tk.Button(confirm_frame, text="Merge PDFs", command=confirm, bg="#4CAF50", fg="white", width=15, height=2).pack(side=tk.LEFT, padx=10)
    tk.Button(confirm_frame, text="Cancel", command=cancel, width=15, height=2).pack(side=tk.LEFT, padx=10)
    
    root.mainloop()
    
    return result['pdfs']