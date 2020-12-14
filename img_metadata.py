import os
from importlib import reload
import win32clipboard
import win32ui
import image_meta
import image_meta.controller
reload(image_meta)
reload(image_meta.controller)
from image_meta.controller import Controller

# --- EXECUTE METADATA RUN FOR IMAGES ---
# * copy metadata.tpl and metadata_exif to target directory
# * set default gps / in case track is used, adjust the GPS data as needed (defaultname tracks.gpx)
# * in explorer simply copy path and start the script / alternatively paste the path into input

#control_params
showinfo = True # show info during execution
verbose = False # Show detailed information
ext_list = ["meta","geo"] # move / copy auxiliary files for given extensions after processing
del_list = [*ext_list,"jpg_original","tif","dop","arw"] # same but list of extension for file types to be deleted
persist = True # apply changes, eg copy files / delete files show upoming changes only otherwise
metadata_subdir = "metadata" #subdirectory to store any generated metadata of interest
metadata_file = "metadata.tpl" #default name of metadata file / is assumed to reside in working directory

print("--- IMAGE METADATA PROCESSING ----")

# get filepath either from clipboard, or from input, will be None if invalid filepath is given
fp = None

if isinstance(fp,str) and not(os.path.isdir(fp)):
    fp = None

if fp is None:
    # try to get path from clipboard
    win32clipboard.OpenClipboard()
    clipboard_data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    
    if isinstance(clipboard_data,str) and os.path.isdir(clipboard_data):
        fp = clipboard_data
    #get path 
    else:
        fp = input("Paste Filepath, hit any key to get path from config file\n --> ")
        if not os.path.isdir(fp):
            fp = None

print(f"---- Filepath of WORKING DIRECTORY set to {fp} ----\n")

if not(fp is None) and isinstance(metadata_subdir,str):
    copy_dir = os.path.join(fp,metadata_subdir)
    print(f"      METADATA SubDirectory {copy_dir}")

# metadata file
control_fp = None
if not(fp is None) and isinstance(metadata_file,str):
    control_fp = os.path.join(fp,metadata_file)
    print(f"      CONTROL FILE: {control_fp}")
    if os.path.isfile(control_fp):
        print(f"      USING METADATA CONFIGURATION FILE {control_fp}")
    else:
        print(f"      METADATA CONFIGURATION FILE {control_fp} can't be found, abort")
        
if os.path.isfile(control_fp):
    finished = Controller.process_images(template_fileref=control_fp,showinfo=showinfo,
                                         verbose=verbose,copy_dir=copy_dir,copy_ext_list=ext_list,
                                         del_ext_list=del_list,persist=persist,work_dir=fp)
    print(f"\nProcessing finished {finished}")
else:
    print(f"Control file {control_fp} does not exist")

input("--- Press Key To Finish ---")