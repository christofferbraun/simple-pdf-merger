import customtkinter as ctk

def reorder_pdfs(pdfs):
    """Show a modern GUI to reorder PDFs with drag and drop. Returns reordered list or None if cancelled."""
    result = {'pdfs': None}
    drag_data = {'index': None, 'start_y': 0}
    items = []
    
    def create_pdf_card(parent, text, index):
        frame = ctk.CTkFrame(parent, fg_color=("#ffffff", "#2b2b2b"), corner_radius=10, 
                            border_width=2, border_color=("#e0e0e0", "#3f3f3f"), height=50)
        frame.pack(fill="x", padx=10, pady=5)
        frame.pack_propagate(False)
        
        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=10)
        
        label = ctk.CTkLabel(content, text=text, font=("Arial", 11), anchor="w")
        label.pack(side="left", fill="x", expand=True)
        
        drag_icon = ctk.CTkLabel(content, text="⋮⋮", font=("Arial", 16), text_color=("#999999", "#666666"))
        drag_icon.pack(side="right", padx=(10, 0))
        
        # Store index in frame
        frame.pdf_index = index
        
        # Bind events to all widgets
        for widget in [frame, content, label, drag_icon]:
            widget.bind('<Enter>', lambda e, f=frame: on_hover(f, True))
            widget.bind('<Leave>', lambda e, f=frame: on_hover(f, False))
            widget.bind('<Button-1>', lambda e, f=frame: on_drag_start(e, f))
            widget.bind('<B1-Motion>', lambda e: on_drag_motion(e))
            widget.bind('<ButtonRelease-1>', lambda e: on_drag_release(e))
        
        return frame
    
    def on_hover(frame, entering):
        if drag_data['index'] is None:
            if entering:
                frame.configure(border_color=("#4CAF50", "#66BB6A"))
            else:
                frame.configure(border_color=("#e0e0e0", "#3f3f3f"))
    
    def on_drag_start(event, frame):
        drag_data['index'] = frame.pdf_index
        drag_data['start_y'] = event.y_root
        frame.configure(border_color=("#4CAF50", "#66BB6A"), border_width=3)
        for item in items:
            item.configure(fg_color=("#ffffff", "#2b2b2b"))
    
    def on_drag_motion(event):
        if drag_data['index'] is not None:
            delta = event.y_root - drag_data['start_y']
            
            if abs(delta) > 30:  # Threshold for swapping
                current_idx = drag_data['index']
                
                if delta > 0 and current_idx < len(pdfs) - 1:  # Moving down
                    pdfs[current_idx], pdfs[current_idx + 1] = pdfs[current_idx + 1], pdfs[current_idx]
                    drag_data['index'] = current_idx + 1
                    drag_data['start_y'] = event.y_root
                    update_list()
                    items[drag_data['index']].configure(border_width=3, border_color=("#4CAF50", "#66BB6A"))
                    
                elif delta < 0 and current_idx > 0:  # Moving up
                    pdfs[current_idx], pdfs[current_idx - 1] = pdfs[current_idx - 1], pdfs[current_idx]
                    drag_data['index'] = current_idx - 1
                    drag_data['start_y'] = event.y_root
                    update_list()
                    items[drag_data['index']].configure(border_width=3, border_color=("#4CAF50", "#66BB6A"))
    
    def on_drag_release(event):
        if drag_data['index'] is not None:
            items[drag_data['index']].configure(border_width=2, border_color=("#e0e0e0", "#3f3f3f"))
            drag_data['index'] = None
    
    def update_list():
        for item in items:
            item.destroy()
        items.clear()
        
        for i, pdf in enumerate(pdfs):
            card = create_pdf_card(scrollable_frame, f"{i+1}. {pdf.name}", i)
            items.append(card)
        
        scrollable_frame.update_idletasks()
    
    def on_mousewheel(event):
        scrollable_frame._parent_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
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
    
    instruction = ctk.CTkLabel(root, text="Drag items up or down to reorder", 
                              font=("Arial", 11), text_color=("#666666", "#999999"))
    instruction.pack(pady=(0, 20))
    
    scrollable_frame = ctk.CTkScrollableFrame(root, fg_color="transparent")
    scrollable_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    # Enable mousewheel scrolling
    scrollable_frame.bind_all("<MouseWheel>", on_mousewheel)
    
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