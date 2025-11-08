import re
from pathlib import Path
from tkinter import filedialog, Tk, messagebox
from PyPDF2 import PdfMerger
from pdf_reorder_gui import reorder_pdfs

root = Tk()
root.withdraw()
folder = filedialog.askdirectory(title="Select folder with PDFs")
if not folder:
    exit("No folder selected")
folder = Path(folder)

pdfs = sorted([f for f in folder.glob("*.pdf") if "_MERGED" not in f.name], 
              key=lambda x: int(re.search(r'\d+', x.name).group()) if re.search(r'\d+', x.name) else float('inf'))

if not pdfs:
    messagebox.showerror("Error", "No PDF files found in the selected folder.")
    exit()

pdfs = reorder_pdfs(pdfs)
if not pdfs:
    exit("Merge cancelled")

merger = PdfMerger()
for pdf in pdfs:
    merger.append(str(pdf))

output = folder / f"{folder.name}_MERGED.pdf"
merger.write(str(output))
merger.close()
message = f"Merged {len(pdfs)} PDFs into:\n{output.name}\n\nOrder:\n" + "\n".join(p.name for p in pdfs)
print(message)
messagebox.showinfo("Merge Complete", message)