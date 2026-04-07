import os
import threading
import json
import customtkinter as ctk
from tkinter import filedialog, messagebox
import fixer_logic

# Configure window appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FM 26 Auto Name Fixer")
        self.geometry("700x550")
        self.resizable(False, False)

        # Main Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(self, text="Real Name Fix Installer", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # 1. Source Selection Group
        self.source_frame = ctk.CTkFrame(self)
        self.source_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.source_frame.grid_columnconfigure(1, weight=1)

        self.source_label = ctk.CTkLabel(self.source_frame, text="Name Fix Source (Sortitoutsi ZIP or Folder):")
        self.source_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.source_entry = ctk.CTkEntry(self.source_frame)
        self.source_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        self.source_btn_zip = ctk.CTkButton(self.source_frame, text="Select ZIP", width=80, command=self.browse_zip)
        self.source_btn_zip.grid(row=0, column=2, padx=5, pady=10)
        
        self.source_btn_folder = ctk.CTkButton(self.source_frame, text="Select Folder", width=80, command=self.browse_folder)
        self.source_btn_folder.grid(row=0, column=3, padx=(5, 10), pady=10)

        # 2. Paths Group
        self.paths_frame = ctk.CTkFrame(self)
        self.paths_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.paths_frame.grid_columnconfigure(1, weight=1)

        # FM Path
        self.fm_path_label = ctk.CTkLabel(self.paths_frame, text="FM 26 Install Path:")
        self.fm_path_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.fm_path_entry = ctk.CTkEntry(self.paths_frame)
        self.fm_path_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        self.fm_path_btn = ctk.CTkButton(self.paths_frame, text="Browse", width=80, command=self.browse_fm_path)
        self.fm_path_btn.grid(row=0, column=2, padx=(5, 10), pady=10)

        # Docs Path
        self.docs_path_label = ctk.CTkLabel(self.paths_frame, text="Documents Path:")
        self.docs_path_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.docs_path_entry = ctk.CTkEntry(self.paths_frame)
        self.docs_path_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        self.docs_path_btn = ctk.CTkButton(self.paths_frame, text="Browse", width=80, command=self.browse_docs_path)
        self.docs_path_btn.grid(row=1, column=2, padx=(5, 10), pady=10)

        # 3. Action Button
        self.apply_btn = ctk.CTkButton(self, text="APPLY FIX", height=40, font=ctk.CTkFont(size=16, weight="bold"), command=self.apply_fix_thread)
        self.apply_btn.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # 4. Log Box
        self.log_box = ctk.CTkTextbox(self, state="disabled")
        self.log_box.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="nsew")

        # Initialize Auto Paths
        self.auto_detect_paths()
        self.load_config()

    def config_path(self):
        return os.path.expanduser("~/.fm26_fixer_config.json")

    def load_config(self):
        path = self.config_path()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("source"):
                    self.source_entry.delete(0, "end")
                    self.source_entry.insert(0, data["source"])
                if data.get("fm_path"):
                    self.fm_path_entry.delete(0, "end")
                    self.fm_path_entry.insert(0, data["fm_path"])
                if data.get("docs_path"):
                    self.docs_path_entry.delete(0, "end")
                    self.docs_path_entry.insert(0, data["docs_path"])
                self.log("Loaded previous path settings.")
            except Exception:
                pass

    def save_config(self, source, fm_path, docs_path):
        data = {"source": source, "fm_path": fm_path, "docs_path": docs_path}
        try:
            with open(self.config_path(), "w", encoding="utf-8") as f:
                json.dump(data, f)
        except Exception:
            pass

    def auto_detect_paths(self):
        fm_path, docs_path = fixer_logic.find_fm_paths()
        
        self.fm_path_entry.delete(0, "end")
        self.fm_path_entry.insert(0, fm_path)
        
        self.docs_path_entry.delete(0, "end")
        self.docs_path_entry.insert(0, docs_path)
        
        if fm_path:
            self.log("Auto-detected FM 26 installation path.")
        else:
            self.log("Could not auto-detect FM 26 installation path. Please select it manually.")
            
        self.log(f"Auto-detected Documents path: {docs_path}")
        self.log("Ready. Please select the Name Fix ZIP or Folder to begin.")

    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")
        # Ensure thread safety for UI updates
        self.update_idletasks()

    def browse_zip(self):
        path = filedialog.askopenfilename(title="Select Name Fix ZIP", filetypes=[("ZIP files", "*.zip")])
        if path:
            self.source_entry.delete(0, "end")
            self.source_entry.insert(0, path)

    def browse_folder(self):
        path = filedialog.askdirectory(title="Select Extracted Name Fix Folder")
        if path:
            self.source_entry.delete(0, "end")
            self.source_entry.insert(0, path)

    def browse_fm_path(self):
        path = filedialog.askdirectory(title="Select Football Manager 2026 Folder")
        if path:
            self.fm_path_entry.delete(0, "end")
            self.fm_path_entry.insert(0, path)

    def browse_docs_path(self):
        path = filedialog.askdirectory(title="Select FM 26 Documents Folder")
        if path:
            self.docs_path_entry.delete(0, "end")
            self.docs_path_entry.insert(0, path)

    def apply_fix_thread(self):
        source = self.source_entry.get()
        fm_path = self.fm_path_entry.get()
        docs_path = self.docs_path_entry.get()

        if not source or not os.path.exists(source):
            messagebox.showerror("Error", "Please select a valid Name Fix ZIP or Folder.")
            return
        if not fm_path or not os.path.exists(fm_path):
            messagebox.showerror("Error", "Please select a valid FM 26 Install path.")
            return
        if not docs_path:
            messagebox.showerror("Error", "Please select a valid Documents path.")
            return

        self.save_config(source, fm_path, docs_path)

        self.apply_btn.configure(state="disabled", text="PROCESSING...")
        self.log_box.configure(state="normal")
        self.log_box.delete("0.0", "end")
        self.log_box.configure(state="disabled")
        
        # Run logic in a background thread to keep UI responsive
        threading.Thread(target=self.run_logic, args=(fm_path, docs_path, source), daemon=True).start()

    def run_logic(self, fm_path, docs_path, source):
        self.log("Starting Real Name Fix process...")
        success = fixer_logic.apply_fix(fm_path, docs_path, source, self.log)
        
        def reset_btn():
            self.apply_btn.configure(state="normal", text="APPLY FIX")
            if success:
                messagebox.showinfo("Success", "Real Name Fix successfully applied!")
            else:
                messagebox.showerror("Error", "There was an error applying the fix. Check the log.")
                
        self.after(500, reset_btn)

if __name__ == "__main__":
    app = App()
    app.mainloop()
