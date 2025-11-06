import re
from pathlib import Path
from tkinter import filedialog, Tk, messagebox
from PyPDF2 import PdfMerger

root = Tk()
root.withdraw()
folder = filedialog.askdirectory(title="Select folder with PDFs")
if not folder:
    exit("No folder selected")
folder = Path(folder)

pdfs = sorted([f for f in folder.glob("*.pdf") if "_MERGED" not in f.name], 
              key=lambda x: int(re.search(r'\d+', x.name).group()) if re.search(r'\d+', x.name) else float('inf'))

merger = PdfMerger()
for pdf in pdfs:
    merger.append(str(pdf))

output = folder / f"{folder.name}_MERGED.pdf"
merger.write(str(output))
merger.close()
message = f"Merged {len(pdfs)} PDFs into:\n{output.name}\n\nOrder:\n" + "\n".join(p.name for p in pdfs)
print(message)
messagebox.showinfo("Merge Complete", message)