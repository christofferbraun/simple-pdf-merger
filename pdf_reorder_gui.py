import tkinter as tk

def reorder_pdfs(pdfs):
    """Show a GUI to reorder PDFs with drag and drop. Returns reordered list or None if cancelled."""
    result = {'pdfs': None}
    drag_data = {'index': None, 'last_index': None}
    
    def on_drag_start(event):
        index = listbox.nearest(event.y)
        drag_data['index'] = index
        drag_data['last_index'] = index
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(index)
        listbox.itemconfig(index, bg='#4CAF50', fg='white')
    
    def on_drag_motion(event):
        current_index = listbox.nearest(event.y)
        if drag_data['index'] is not None and current_index != drag_data['last_index']:
            # Remove highlight from last position
            if drag_data['last_index'] is not None and drag_data['last_index'] != drag_data['index']:
                listbox.itemconfig(drag_data['last_index'], bg='white', fg='black')
            
            # Highlight drop target
            if current_index != drag_data['index']:
                listbox.itemconfig(current_index, bg='#E8F5E9', fg='black')
            
            drag_data['last_index'] = current_index
    
    def on_drag_release(event):
        if drag_data['index'] is not None:
            drop_index = listbox.nearest(event.y)
            
            # Perform the reorder
            if drop_index != drag_data['index']:
                item = pdfs.pop(drag_data['index'])
                pdfs.insert(drop_index, item)
            
            # Reset and refresh
            drag_data['index'] = None
            drag_data['last_index'] = None
            update_listbox()
            listbox.selection_set(drop_index)
    
    def update_listbox():
        listbox.delete(0, tk.END)
        for i, pdf in enumerate(pdfs, 1):
            listbox.insert(tk.END, f"{i}. {pdf.name}")
            listbox.itemconfig(i-1, bg='white', fg='black')
    
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
    root.configure(bg='#f0f0f0')
    
    header = tk.Label(root, text="Drag and drop to reorder PDFs:", font=("Arial", 12, "bold"), bg='#f0f0f0')
    header.pack(pady=10)
    
    instruction = tk.Label(root, text="Click and hold to drag • Release to drop", font=("Arial", 9), fg='#666', bg='#f0f0f0')
    instruction.pack(pady=(0, 10))
    
    frame = tk.Frame(root, bg='#f0f0f0')
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("Arial", 10), 
                         selectmode=tk.SINGLE, activestyle='none', 
                         highlightthickness=1, highlightcolor='#4CAF50',
                         bd=0, relief=tk.FLAT)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)
    
    # Bind drag and drop events
    listbox.bind('<Button-1>', on_drag_start)
    listbox.bind('<B1-Motion>', on_drag_motion)
    listbox.bind('<ButtonRelease-1>', on_drag_release)
    
    update_listbox()
    listbox.selection_set(0)
    
    confirm_frame = tk.Frame(root, bg='#f0f0f0')
    confirm_frame.pack(pady=20)
    
    tk.Button(confirm_frame, text="✓ Merge PDFs", command=confirm, bg="#4CAF50", fg="white", 
              width=15, height=2, font=("Arial", 10, "bold"), relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=10)
    tk.Button(confirm_frame, text="✗ Cancel", command=cancel, bg="#f44336", fg="white",
              width=15, height=2, font=("Arial", 10, "bold"), relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=10)
    
    root.mainloop()
    
    return result['pdfs']