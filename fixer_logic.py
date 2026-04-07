import os
import shutil
import tempfile
import zipfile
import winreg

def get_documents_folder():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
        path = winreg.QueryValueEx(key, "Personal")[0]
        return path
    except Exception:
        return os.path.expanduser("~/Documents")

def find_fm_paths():
    docs_base = get_documents_folder()
    docs_path = os.path.join(docs_base, "Sports Interactive", "Football Manager 2026")
    
    # Common install paths
    possible_paths = [
        r"C:\Program Files (x86)\Steam\steamapps\common\Football Manager 2026",
        r"D:\SteamLibrary\steamapps\common\Football Manager 2026",
        r"C:\Program Files\Epic Games\FootballManager2026",
        r"D:\Epic Games\FootballManager2026",
        r"E:\SteamLibrary\steamapps\common\Football Manager 2026"
    ]
    
    fm_install = ""
    for path in possible_paths:
        if os.path.exists(path):
            fm_install = path
            break
            
    return fm_install, docs_path

def find_folders(root_dir, target_names):
    """Recursively find folders that exactly match any of target_names."""
    found = {name: [] for name in target_names}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            if dirname.lower() in target_names:
                found[dirname.lower()].append(os.path.join(dirpath, dirname))
    return found

def apply_fix(fm_install_path, docs_path, source_path, log_callback):
    try:
        temp_dir = None
        work_dir = source_path
        
        # 1. Extract zip if provided
        if source_path.lower().endswith(".zip"):
            log_callback(f"Extracting '{os.path.basename(source_path)}'...")
            temp_dir = tempfile.mkdtemp(prefix="fm26_name_fix_")
            try:
                with zipfile.ZipFile(source_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                work_dir = temp_dir
                log_callback("Extraction complete.")
            except Exception as e:
                log_callback(f"Failed to extract zip: {e}")
                return False

        log_callback("Searching for lnc, edt, and dbc folders in source...")
        targets = ["lnc", "edt", "dbc", "editor data"]
        found_source_folders = find_folders(work_dir, targets)
        
        # Also let's find all .fmf files just in case they are not in an "editor data" folder
        fmf_files = []
        for root, dirs, files in os.walk(work_dir):
            for file in files:
                if file.lower().endswith('.fmf'):
                    fmf_files.append(os.path.join(root, file))

        # Check DB folders in FM Install path
        possible_db_paths = [
            os.path.join(fm_install_path, "data", "database", "db"),
            os.path.join(fm_install_path, "Content", "data", "database", "db") # Game Pass version
        ]
        
        db_path = None
        for p in possible_db_paths:
            if os.path.exists(p):
                db_path = p
                break
                
        # If not found directly, perform a quick recursive search to locate it
        if not db_path:
            log_callback("Standard database path not found. Scanning deeper into subfolders...")
            for root, dirs, files in os.walk(fm_install_path):
                if os.path.basename(root).lower() == "db":
                    parent = os.path.dirname(root)
                    grandparent = os.path.dirname(parent)
                    if os.path.basename(parent).lower() == "database" and os.path.basename(grandparent).lower() == "data":
                        db_path = root
                        break

        if not db_path:
            log_callback(f"Could not find the 'data/database/db' folder anywhere inside {fm_install_path}. Please check your FM 2026 path.")
            return False
            
        log_callback(f"Found database folder at: {db_path}")
            
        log_callback("Searching for database versions (23xx, 24xx, 25xx, 26xx)...")
        db_versions = []
        for folder in os.listdir(db_path):
            if folder.startswith(("23", "24", "25", "26")) and os.path.isdir(os.path.join(db_path, folder)):
                db_versions.append(folder)
                
        if not db_versions:
            log_callback("No database versions found starting with 23, 24, 25, or 26.")
        
        folders_to_replace = ["lnc", "edt", "dbc"]
        
        for version in db_versions:
            log_callback(f"\n--- Processing DB Version: {version} ---")
            version_path = os.path.join(db_path, version)
            
            for f_name in folders_to_replace:
                target_folder = os.path.join(version_path, f_name)
                
                # Delete existing
                if os.path.exists(target_folder):
                    try:
                        shutil.rmtree(target_folder)
                        log_callback(f"Deleted original '{f_name}' folder in {version}...")
                    except Exception as e:
                        log_callback(f"Error deleting {target_folder}: {e}")
                        
                # Copy from source
                if found_source_folders[f_name]:
                    source_f = found_source_folders[f_name][0] # take the first matching one
                    try:
                        shutil.copytree(source_f, target_folder)
                        log_callback(f"Copied '{f_name}' folder to {version}...")
                    except Exception as e:
                        log_callback(f"Error copying {f_name} to {version}: {e}")
                else:
                    log_callback(f"Warning: No '{f_name}' folder found in the source to copy!")

        # Process Editor Data
        log_callback("\n--- Processing Editor Data (.fmf files) ---")
        editor_data_target = os.path.join(docs_path, "editor data")
        os.makedirs(editor_data_target, exist_ok=True)
        
        if found_source_folders["editor data"]:
            source_ed = found_source_folders["editor data"][0]
            count = 0
            for item in os.listdir(source_ed):
                s = os.path.join(source_ed, item)
                d = os.path.join(editor_data_target, item)
                if os.path.isfile(s) and s.lower().endswith(".fmf"):
                    shutil.copy2(s, d)
                    count += 1
            log_callback(f"Copied {count} .fmf files from 'editor data' folder to your Documents.")
        elif fmf_files:
            log_callback(f"Found {len(fmf_files)} .fmf files scattered in source. Copying...")
            for fmf in fmf_files:
                shutil.copy2(fmf, os.path.join(editor_data_target, os.path.basename(fmf)))
            log_callback("Copied all .fmf files to your Documents.")
        else:
            log_callback("No Editor Data / .fmf files found in source.")

        log_callback("\n=== Name Fix Application Complete! ===")
        log_callback("You can now enjoy Football Manager 2026 with real names.")
        
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
                
        return True
    except Exception as e:
        log_callback(f"A critical error occurred: {e}")
        return False
