import customtkinter as ctk

def reorder_pdfs(pdfs):
    """Show a modern GUI to reorder PDFs with keyboard controls. Returns reordered list or None if cancelled."""
    result = {'pdfs': None}
    selected_index = [0]  # Use list to allow modification in nested functions
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
        
        number_label = ctk.CTkLabel(content, text=f"#{index+1}", font=("Arial", 10, "bold"), 
                                    text_color=("#999999", "#666666"), width=40)
        number_label.pack(side="right", padx=(10, 0))
        
        frame.pdf_index = index
        
        # Click to select
        for widget in [frame, content, label, number_label]:
            widget.bind('<Button-1>', lambda e, idx=index: select_item(idx))
        
        return frame
    
    def select_item(index):
        selected_index[0] = index
        update_selection()
    
    def update_selection():
        for i, item in enumerate(items):
            if i == selected_index[0]:
                item.configure(border_color=("#4CAF50", "#66BB6A"), border_width=3)
                item.configure(fg_color=("#e8f5e9", "#1b5e20"))
            else:
                item.configure(border_color=("#e0e0e0", "#3f3f3f"), border_width=2)
                item.configure(fg_color=("#ffffff", "#2b2b2b"))
    
    def move_up(event=None):
        idx = selected_index[0]
        if idx > 0:
            # Swap
            pdfs[idx], pdfs[idx-1] = pdfs[idx-1], pdfs[idx]
            selected_index[0] = idx - 1
            
            # Animate
            items[idx].configure(fg_color=("#f0f0f0", "#3a3a3a"))
            items[idx-1].configure(fg_color=("#f0f0f0", "#3a3a3a"))
            
            root.after(100, update_list)
    
    def move_down(event=None):
        idx = selected_index[0]
        if idx < len(pdfs) - 1:
            # Swap
            pdfs[idx], pdfs[idx+1] = pdfs[idx+1], pdfs[idx]
            selected_index[0] = idx + 1
            
            # Animate
            items[idx].configure(fg_color=("#f0f0f0", "#3a3a3a"))
            items[idx+1].configure(fg_color=("#f0f0f0", "#3a3a3a"))
            
            root.after(100, update_list)
    
    def navigate_up(event=None):
        if selected_index[0] > 0:
            selected_index[0] -= 1
            update_selection()
            scroll_to_selected()
    
    def navigate_down(event=None):
        if selected_index[0] < len(pdfs) - 1:
            selected_index[0] += 1
            update_selection()
            scroll_to_selected()
    
    def scroll_to_selected():
        """Scroll to keep selected item visible"""
        if items and selected_index[0] < len(items):
            item = items[selected_index[0]]
            scrollable_frame._parent_canvas.yview_moveto(selected_index[0] / len(items))
    
    def update_list():
        for item in items:
            item.destroy()
        items.clear()
        
        for i, pdf in enumerate(pdfs):
            card = create_pdf_card(scrollable_frame, f"{pdf.name}", i)
            items.append(card)
        
        update_selection()
        scrollable_frame.update_idletasks()
    
    def on_mousewheel(event):
        scrollable_frame._parent_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def confirm():
        result['pdfs'] = pdfs.copy()
        cleanup_and_close()
    
    def cancel():
        cleanup_and_close()
    
    def cleanup_and_close():
        try:
            scrollable_frame.unbind_all("<MouseWheel>")
            root.unbind_all("<Up>")
            root.unbind_all("<Down>")
            root.unbind_all("<Control-Up>")
            root.unbind_all("<Control-Down>")
            root.after(10, lambda: None)
            root.quit()
        except:
            pass
        finally:
            try:
                root.destroy()
            except:
                pass
    
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("green")
    
    root = ctk.CTk()
    root.title("PDF Merger - Reorder Files")
    root.geometry("700x600")
    
    header = ctk.CTkLabel(root, text="📄 Reorder Your PDFs", font=("Arial", 20, "bold"))
    header.pack(pady=(20, 5))
    
    instruction = ctk.CTkLabel(root, text="Click to select • ↑/↓ to navigate • Ctrl+↑/↓ to move", 
                              font=("Arial", 11), text_color=("#666666", "#999999"))
    instruction.pack(pady=(0, 15))
    
    # Keyboard shortcuts display
    shortcuts_frame = ctk.CTkFrame(root, fg_color="transparent")
    shortcuts_frame.pack(pady=(0, 10))
    
    ctk.CTkLabel(shortcuts_frame, text="⌨️", font=("Arial", 14)).pack(side="left", padx=(0, 5))
    ctk.CTkLabel(shortcuts_frame, text="Ctrl+↑", font=("Courier", 10, "bold"), 
                fg_color=("#e0e0e0", "#3f3f3f"), corner_radius=5, padx=8, pady=2).pack(side="left", padx=2)
    ctk.CTkLabel(shortcuts_frame, text="Move Up", font=("Arial", 9), 
                text_color=("#666666", "#999999")).pack(side="left", padx=(2, 10))
    
    ctk.CTkLabel(shortcuts_frame, text="Ctrl+↓", font=("Courier", 10, "bold"),
                fg_color=("#e0e0e0", "#3f3f3f"), corner_radius=5, padx=8, pady=2).pack(side="left", padx=2)
    ctk.CTkLabel(shortcuts_frame, text="Move Down", font=("Arial", 9),
                text_color=("#666666", "#999999")).pack(side="left", padx=2)
    
    scrollable_frame = ctk.CTkScrollableFrame(root, fg_color="transparent")
    scrollable_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    scrollable_frame.bind_all("<MouseWheel>", on_mousewheel)
    
    # Keyboard bindings
    root.bind("<Up>", navigate_up)
    root.bind("<Down>", navigate_down)
    root.bind("<Control-Up>", move_up)
    root.bind("<Control-Down>", move_down)
    
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