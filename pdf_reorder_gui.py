import customtkinter as ctk
from tkinter import Canvas

def reorder_pdfs(pdfs):
    """Show a modern GUI to reorder PDFs with drag and drop. Returns reordered list or None if cancelled."""
    result = {'pdfs': None}
    drag_data = {'index': None, 'widget': None, 'y_offset': 0}
    items = []
    
    def create_pdf_card(parent, text, index):
        frame = ctk.CTkFrame(parent, fg_color=("#ffffff", "#2b2b2b"), corner_radius=10, 
                            border_width=2, border_color=("#e0e0e0", "#3f3f3f"))
        frame.pack(fill="x", padx=10, pady=5)
        
        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=12)
        
        label = ctk.CTkLabel(content, text=text, font=("Arial", 11), anchor="w")
        label.pack(side="left", fill="x", expand=True)
        
        drag_icon = ctk.CTkLabel(content, text="⋮⋮", font=("Arial", 16), text_color=("#999999", "#666666"))
        drag_icon.pack(side="right", padx=(10, 0))
        
        frame.bind('<Enter>', lambda e: on_hover(frame, True))
        frame.bind('<Leave>', lambda e: on_hover(frame, False))
        frame.bind('<Button-1>', lambda e: on_drag_start(e, frame, index))
        frame.bind('<B1-Motion>', lambda e: on_drag_motion(e))
        frame.bind('<ButtonRelease-1>', lambda e: on_drag_release(e))
        
        label.bind('<Button-1>', lambda e: on_drag_start(e, frame, index))
        label.bind('<B1-Motion>', lambda e: on_drag_motion(e))
        label.bind('<ButtonRelease-1>', lambda e: on_drag_release(e))
        
        drag_icon.bind('<Button-1>', lambda e: on_drag_start(e, frame, index))
        drag_icon.bind('<B1-Motion>', lambda e: on_drag_motion(e))
        drag_icon.bind('<ButtonRelease-1>', lambda e: on_drag_release(e))
        
        return frame
    
    def on_hover(frame, entering):
        if drag_data['widget'] != frame:
            if entering:
                frame.configure(border_color=("#4CAF50", "#66BB6A"))
            else:
                frame.configure(border_color=("#e0e0e0", "#3f3f3f"))
    
    def on_drag_start(event, widget, index):
        drag_data['index'] = index
        drag_data['widget'] = widget
        drag_data['y_offset'] = event.y
        widget.configure(border_color=("#4CAF50", "#66BB6A"), border_width=3)
        widget.lift()
    
    def on_drag_motion(event):
        if drag_data['widget']:
            widget = drag_data['widget']
            x = widget.winfo_x()
            y = scrollable_frame.winfo_rooty() + event.y - drag_data['y_offset'] - container.winfo_rooty()
            widget.place(x=x, y=y)
            
            # Find drop position
            for i, item in enumerate(items):
                if item != widget:
                    item_y = item.winfo_y()
                    item_height = item.winfo_height()
                    if item_y <= y <= item_y + item_height:
                        if i != drag_data['index']:
                            item.configure(fg_color=("#e8f5e9", "#1b5e20"))
                        break
                else:
                    if item != widget:
                        item.configure(fg_color=("#ffffff", "#2b2b2b"))
    
    def on_drag_release(event):
        if drag_data['widget'] and drag_data['index'] is not None:
            widget = drag_data['widget']
            widget.place_forget()
            
            # Find drop index
            drop_index = drag_data['index']
            widget_y = widget.winfo_rooty()
            
            for i, item in enumerate(items):
                if item != widget:
                    item_y = item.winfo_rooty()
                    item_height = item.winfo_height()
                    if widget_y < item_y + item_height / 2:
                        drop_index = i
                        break
                    else:
                        drop_index = i + 1 if i + 1 < len(items) else i
            
            # Reorder
            if drop_index != drag_data['index']:
                pdf = pdfs.pop(drag_data['index'])
                pdfs.insert(drop_index, pdf)
            
            drag_data['index'] = None
            drag_data['widget'] = None
            update_list()
    
    def update_list():
        for item in items:
            item.destroy()
        items.clear()
        
        for i, pdf in enumerate(pdfs):
            card = create_pdf_card(scrollable_frame, f"{i+1}. {pdf.name}", i)
            items.append(card)
    
    def confirm():
        result['pdfs'] = pdfs.copy()
        root.quit()
        root.destroy()
    
    def cancel():
        root.quit()
        root.destroy()
    
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("green")
    
    root = ctk.CTk()
    root.title("PDF Merger - Reorder Files")
    root.geometry("700x600")
    
    header = ctk.CTkLabel(root, text="📄 Reorder Your PDFs", font=("Arial", 20, "bold"))
    header.pack(pady=(20, 5))
    
    instruction = ctk.CTkLabel(root, text="Drag and drop items to reorder • Changes apply instantly", 
                              font=("Arial", 11), text_color=("#666666", "#999999"))
    instruction.pack(pady=(0, 20))
    
    container = ctk.CTkFrame(root, fg_color="transparent")
    container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    canvas = Canvas(container, highlightthickness=0)
    scrollbar = ctk.CTkScrollbar(container, command=canvas.yview)
    scrollable_frame = ctk.CTkFrame(canvas, fg_color="transparent")
    
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=650)
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    update_list()
    
    button_frame = ctk.CTkFrame(root, fg_color="transparent")
    button_frame.pack(pady=(0, 20))
    
    ctk.CTkButton(button_frame, text="✓ Merge PDFs", command=confirm, 
                 width=160, height=45, font=("Arial", 13, "bold"), 
                 fg_color="#4CAF50", hover_color="#45a049").pack(side="left", padx=10)
    ctk.CTkButton(button_frame, text="✗ Cancel", command=cancel,
                 width=160, height=45, font=("Arial", 13, "bold"),
                 fg_color="#f44336", hover_color="#da190b").pack(side="left", padx=10)
    
    root.mainloop()
    
    return result['pdfs']