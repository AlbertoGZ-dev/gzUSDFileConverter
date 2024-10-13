'''
████████████████████████████████████████████████████████████████████████████
    
    gzUSDFileConverter
    
    Description: gzUSDFileConverter is a tool to convert format for.usd files,
    from binary to ascii or ascii to binary encoding.


    Author: AlbertoGZ
    albertogzonline@gmail.com
    https://github.com/AlbertoGZ-dev

████████████████████████████████████████████████████████████████████████████

'''


import os
import subprocess
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import messagebox
from PIL import Image, ImageTk


dir_path = os.path.dirname(os.path.realpath(__file__))
hou_bin = str("C:\\Program Files\\Side Effects Software\\Houdini 19.5.773\\bin\\")
os.chdir(hou_bin)

suffix = "ascii"
usdFormat = "usda"
print(suffix, usdFormat)

textLab = "Drop .usd file here..."


# Function to handle file drop
def on_file_drop(event):
    global dropped_filepath
    global textLab
    filepath = event.data

    # Check if the file extension is .usd or .usdc
    if filepath.endswith(('.usd', '.usdc', '.usda')) and ' ' not in filepath:
        dropped_filepath.set(filepath)
        dropAreaBG.itemconfig(2, text=str(event.data))
    else:
        messagebox.showerror("Invalid File", "Please drop a .usd file.")


# Function to swap between usd encodes binary and ascii
def swap():
    global usdFormat
    global suffix
    if usdFormat=='usda':
        binToAsciiBtn.place(x=1000, y=1000) #fake hides
        asciiToBinBtn.place(x=20, y=340)
        usdFormat = "usdc"
        suffix = "bin"
        print(suffix, usdFormat)
        return suffix, usdFormat
    
    elif usdFormat=='usdc':
        binToAsciiBtn.place(x=20, y=340)
        asciiToBinBtn.place(x=1000, y=1000) #fake hide
        usdFormat = "usda"
        suffix = "ascii"
        print(suffix, usdFormat)
        return suffix, usdFormat
        


# Function to convert file using usdcat
def convertFile():
    global filepath
    filepath = dropped_filepath.get()
    if filepath:
        output_file = os.path.splitext(filepath)[0] + "_" + suffix + ".usd"
        try:
            # Use usdcat command to convert
            os.system('hython.exe usdcat -o '+ output_file +' --usdFormat '+ usdFormat + " " + filepath)
            dropAreaBG.itemconfig(2, text=textLab)
            messagebox.showinfo("Success", f"File converted successfully to {output_file}")
            del filepath
            #print(filepath)
            
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to convert the file: {e}")
    else:
        messagebox.showwarning("No File", "Please drop a valid .usd or .usdc file first.")


def move_app(e):
    root.geometry(f'+{e.x_root}+{e.y_root}')

def exit():
    root.quit()




# Load images
img1 = Image.open(dir_path+"/"+"imgs/dropArea2.png")
img1res = img1.resize((360, 250))
img2 = Image.open(dir_path+"/"+"imgs/convertFile.png")
img2res = img2.resize((360, 54))
img3 = Image.open(dir_path+"/"+"imgs/binToAscii.png")
img3res = img3.resize((360, 54), resample=2)
img4 = Image.open(dir_path+"/"+"imgs/asciiToBin.png")
img4res = img4.resize((360, 54))
img5 = Image.open(dir_path+"/"+"imgs/exit.png")
img5res = img5.resize((30, 30), resample=5)
img6 = Image.open(dir_path+"/"+"imgs/swapFormat.png")
img6res = img6.resize((40, 40), resample=3)




######################################
###              GUI

# Initialize TkinterDnD window
root = TkinterDnD.Tk()
root.title("USD File Converter")
root.geometry('400x440')
root.overrideredirect(1)
root.wm_attributes("-transparentcolor", "grey")
root.resizable(False, False)

frameImg = tk.PhotoImage(file=dir_path+"/"+"imgs/uiFrame2.png")
frameLab = tk.Label(root, bg='grey', image=frameImg)
frameLab.pack(fill=tk.BOTH, expand=True)
frameLab.bind("<B1-Motion>", move_app)


dropped_filepath = tk.StringVar()

# Drop area
dropAreaImg = ImageTk.PhotoImage(img1res)
dropAreaBG = tk.Canvas(root, width=360, height=250, highlightthickness=0, bg="#4D4D4D")
dropAreaBG.place(x=20, y=70)
dropAreaBG.create_image(180, 125, image=dropAreaImg)
dropAreaBG.create_text(180, 125, text=textLab, font="Arial 16", fill="#CCC", width=300)

# Bind drag-and-drop event
dropAreaBG.drop_target_register(DND_FILES)
dropAreaBG.dnd_bind('<<Drop>>', on_file_drop)

# Create a binToAscii button
binToAsciiImg = ImageTk.PhotoImage(img3res)
binToAsciiBtn = tk.Button(root, image=binToAsciiImg, borderwidth=0, bg="#4D4D4D", activebackground="#4D4D4D", cursor="hand2", command=convertFile)
binToAsciiBtn.place(x=20, y=340)

# Create a asciiToBin button
asciiToBinImg = ImageTk.PhotoImage(img4res)
asciiToBinBtn = tk.Button(root, image=asciiToBinImg, borderwidth=0, bg="#4D4D4D", activebackground="#4D4D4D", cursor="hand2", command=convertFile)
asciiToBinBtn.place(x=1000, y=1000)

# Exit button
exitBtnImg = ImageTk.PhotoImage(img5res)
exitBtn = tk.Button(root, image=exitBtnImg, borderwidth=0, bg="#4D4D4D", activebackground="#4D4D4D", cursor="hand2", command=exit)
exitBtn.place(x=360, y=30)

# Swap button
swapBtnImg = ImageTk.PhotoImage(img6res)
swapBtn = tk.Button(root, image=swapBtnImg, borderwidth=0, bg="#4D4D4D", activebackground="#4D4D4D", cursor="hand2", command=swap)
swapBtn.place(x=5, y=347)


# Start the Tkinter event loop
root.eval('tk::PlaceWindow . center')
root.mainloop()
