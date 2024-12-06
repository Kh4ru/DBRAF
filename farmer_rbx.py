import keyboard
from pynput.keyboard import Controller,Key
import threading,os
import time,json
import tkinter,sys,winsound
from tkinter import messagebox
# Variables globales
beep = True
beep_param = tkinter.IntVar()
modules_number = 0
modules = ["pynput","keyboard"]
actif = False  # État du mode auto-farm
path = os.path.dirname(os.path.abspath(__file__))+"/"
thread = None  # Référence au thread de l'auto-farm
energy_loose = 17  # Temps pour vider l'énergie
energy_get = 8  # Temps pour regagner de l'énergie
f = open(path+"config.json","r")
data = json.load(f)
beep = data["beep"]
hotkey = data["hotkey"]
f.close()
def installation():
    os.system("py -m pip install -r requirements.txt")
def sauvegarder():
    global hotkey
    new_hotkey = raccourci.get()
    hotkey = new_hotkey
    with open(path+"config.json","r+") as x:
        data = json.load(x)
        data["hotkey"] = new_hotkey
        x.seek(0)
        json.dump(data,x)
        x.truncate()
    x.close()
    messagebox.showinfo("Touche Sauvegardée",f'"{hotkey.upper()}" a été configuré comme raccourci !')
    keyboard.clear_hotkey(switch)
    switch = keyboard.add_hotkey(hotkey,toggle_auto_farm)

# Contrôleur clavier avec pynput
pynput_keyboard = Controller()
window = tkinter.Tk()
window.iconphoto(False,tkinter.PhotoImage(file=path+"icon.png"))
window.title("Auto Farmer: Dragon Ball Rage")
window.config(bg="#2b2828")
button = tkinter.Button(window,text="Oui",bg="#e64337",fg="#ffffff",justify="center")
save_btn = tkinter.Button(window,text="Sauvegarder Touche",command=sauvegarder,bg="#eb2617",fg="#ffffff",justify="center")
default = tkinter.StringVar()
default.set(hotkey)
raccourci = tkinter.Entry(window,textvariable=default,bg="#bcbfb8",fg="#eb2617",justify="center")
info = tkinter.Label(window,text="Option Choisi",bg="#2b2828",fg="#ffffff",justify="center")
titre = tkinter.Label(window,text="Auto Farmer Dragon Ball Rage",bg="#2b2828",fg="#ffffff",justify="center")
statut =tkinter.Label(window,text="Auto Farmer: Inactif",bg="#2b2828",fg="#ffffff",justify="center")
credits = tkinter.Label(window,text="Développé par Kh4ru",bg="#2b2828",fg="#ffffff",justify="center")
titre.grid(pady=(0,2))
info.grid(pady=(0,2))
statut.grid(pady=(0,2))
for module in modules:
    if(module in sys.modules):
        modules_number += 1

if not(modules_number == len(modules)):
    info.config(text="Modules manquants pour faire fonctionner l'auto farmer")
    button.config(text="Installer Modules Requis")
    button.config(command=installation)
    button.grid(pady=(0,2))
else:
    info.config(text="Touche pour activer/desactiver")
    raccourci.grid(pady=(0,2))
    save_btn.grid(pady=(0,2))
credits.grid(pady=(0,2))

def full_farm():
    while actif:  # Boucle tant que l'auto-farm est activé
        print("Perte d'énergie...")
        for _ in range(energy_loose):
            if not actif:  # Si désactivé, sortir
                return
            pynput_keyboard.press('a')
            time.sleep(0.1)
            pynput_keyboard.release('a')
            time.sleep(0.4)
        print("Récupération d'énergie...")
        if not(actif):
            return
        else:
            pynput_keyboard.press('c')
            time.sleep(5)
            pynput_keyboard.release('c')
            time.sleep(0.4)
        for _ in range(energy_loose):
            if not actif:
                return
            else:
                pynput_keyboard.press('r')
                time.sleep(0.1)
                pynput_keyboard.release('r')
                time.sleep(0.4)
        if not(actif):
            return
        else:
            pynput_keyboard.press('c')
            time.sleep(5)
            pynput_keyboard.release('c')
            time.sleep(0.4)
        for _ in range(energy_loose):
            if not(actif):
                return
            else:
                pynput_keyboard.press('e')
                time.sleep(0.1)
                pynput_keyboard.release('e')
                time.sleep(0.4)
def semi_farm():
    while actif:  # Boucle tant que l'auto-farm est activé
        for _ in range(20+1):
            if not(actif):
                return
            else:
                pynput_keyboard.press('e')
                time.sleep(0.1)
                pynput_keyboard.release('e')
                time.sleep(0.4)
     
def toggle_auto_farm():
    global actif
    if not(actif):
        winsound.Beep(440,500)
        actif = True
        statut.config(text="Auto Farmer: Actif")
        # Lancer un thread pour auto_farm
        thread = threading.Thread(target=full_farm)
        thread.start()
    else:
        winsound.Beep(440,500)
        actif = False
        statut.config(text="Auto Farmer: Inactif")
        # Le thread s'arrêtera automatiquement grâce à la condition dans auto_farm
switch = keyboard.add_hotkey(hotkey,toggle_auto_farm)
window.mainloop()