import tkinter as tk
from tkinter import filedialog, messagebox
from hlae_lockon_gui_math import executeHLAELockOn

def run():
    input_position = entry_position.get()
    input_filepath = entry_filepath.get()
    
    if not input_position and not input_filepath:
        messagebox.showerror("Error", "Missing both fields!")
        return
    elif not input_position:
        messagebox.showerror("Error", "Missing position field!")
        return
    elif not input_filepath:
        messagebox.showerror("Error", "Missing filepath field!")
        return
    
    # Save-as popup
    output_filepath = filedialog.asksaveasfilename(title="Save output file", defaultextension="")

    if not output_filepath:
        messagebox.showerror("Error", "Invalid/blank save filepath!")
        return

    # Run lock-on calculation + generate output campath file.
    try:
        executeHLAELockOn(input_position, input_filepath, output_filepath)
        messagebox.showinfo("Success", f"File saved to {output_filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to execute!\n(Possible Reasons: invalid position coordinates, invalid input filepath, input campath file's contents tampered with, cannot save to output location, math bug, etc.)\n\nError:\n{e}")
        return
    
    

    

def browse_file():
    file_path = filedialog.askopenfilename(title="Select input campath file")
    if file_path:
        entry_filepath.delete(0, tk.END)
        entry_filepath.insert(0, file_path)


# Tkinter GUI
root = tk.Tk()
root.title("HLAE - Lock On Tool")

# Position input field
tk.Label(root, text="Paste your chosen stationary cam position (use \"mirv_input position\"):").pack(pady=(10,0))
entry_position = tk.Entry(root, width=50)
entry_position.pack(pady=(0,10))
entry_position.insert(0, "0.000000 0.000000 0.000000")

# Campath file input field
tk.Label(root, text="Select your input campath file (points to rotate towards):").pack()
entry_filepath = tk.Entry(root, width=50)
entry_filepath.pack(side=tk.LEFT, padx=(15,0), pady=(0,10))
tk.Button(root, text="Browse", command=browse_file).pack(side=tk.LEFT, padx=(5,5), pady=(0,10))

# Run button
tk.Button(root, text="Run", command=run).pack(side=tk.LEFT, padx=(0,15), pady=(0,10))

root.mainloop()