
from Neurons import NonSpikingNeuron
from Synapses import NonSpikingSynapse
import tkinter as tk
from tkinter import simpledialog, messagebox


""""
dic = {
    "NonSpikingSynapse":{
        "Ia_Alpha":{"Veq":0,"g_max":1,"Vthr_pre":-65,"Vsat_pre":-20},
        "Ia_Pn":{"Veq":0,"g_max":1,"Vthr_pre":-65,"Vsat_pre":-20},
        "Pn_Alpha":{"Veq":0,"g_max":1,"Vthr_pre":-65,"Vsat_pre":-20},

    },"NonSpikingNeuron":{
        "Ia":{"V_rest":-65,"tau":5,"Rm":1},
        "Alpha":{"V_rest":-65,"tau":5,"Rm":1},
        "Pn":{"V_rest":-65,"tau":5,"Rm":1},
    }
}
"""
from Neurons import NonSpikingNeuron
from Synapses import NonSpikingSynapse
import tkinter as tk
from tkinter import messagebox

# Dictionnaires globaux
dic = {
    "NonSpikingNeuron": {},
    "NonSpikingSynapse": {}
}
neurons = {}
synapses = {}

# === Fonctions d'ajout ===

def ajouter_neurone():
    fenetre = tk.Toplevel(root)
    fenetre.title("Ajouter un neurone")

    tk.Label(fenetre, text="Nom du neurone:").grid(row=0, column=0)
    tk.Label(fenetre, text="V_rest:").grid(row=1, column=0)
    tk.Label(fenetre, text="tau:").grid(row=2, column=0)
    tk.Label(fenetre, text="Rm:").grid(row=3, column=0)

    e_nom = tk.Entry(fenetre)
    e_vrest = tk.Entry(fenetre)
    e_tau = tk.Entry(fenetre)
    e_rm = tk.Entry(fenetre)

    e_nom.grid(row=0, column=1)
    e_vrest.grid(row=1, column=1)
    e_tau.grid(row=2, column=1)
    e_rm.grid(row=3, column=1)

    def valider():
        try:
            nom = e_nom.get()
            V_rest = float(e_vrest.get())
            tau = float(e_tau.get())
            Rm = float(e_rm.get())
            dic["NonSpikingNeuron"][nom] = {"V_rest": V_rest, "tau": tau, "Rm": Rm}
            neurons[nom] = NonSpikingNeuron(V_rest, tau, Rm)
            messagebox.showinfo("Succès", f"Neurone '{nom}' ajouté.")
            fenetre.destroy()
        except ValueError:
            messagebox.showerror("Erreur", "Paramètres invalides.")

    tk.Button(fenetre, text="Valider", command=valider).grid(row=4, column=0, columnspan=2)

def ajouter_synapse():
    fenetre = tk.Toplevel(root)
    fenetre.title("Ajouter une synapse")

    tk.Label(fenetre, text="Nom de la synapse (pre_post):").grid(row=0, column=0)
    tk.Label(fenetre, text="Veq:").grid(row=1, column=0)
    tk.Label(fenetre, text="g_max:").grid(row=2, column=0)
    tk.Label(fenetre, text="V_thr:").grid(row=3, column=0)
    tk.Label(fenetre, text="V_sat:").grid(row=4, column=0)

    e_nom = tk.Entry(fenetre)
    e_veq = tk.Entry(fenetre)
    e_gmax = tk.Entry(fenetre)
    e_vthr = tk.Entry(fenetre)
    e_vsat = tk.Entry(fenetre)

    e_nom.grid(row=0, column=1)
    e_veq.grid(row=1, column=1)
    e_gmax.grid(row=2, column=1)
    e_vthr.grid(row=3, column=1)
    e_vsat.grid(row=4, column=1)

    def valider():
        try:
            nom = e_nom.get()
            Veq = float(e_veq.get())
            g_max = float(e_gmax.get())
            V_thr = float(e_vthr.get())
            V_sat = float(e_vsat.get())
            dic["NonSpikingSynapse"][nom] = {
                "Veq": Veq, "g_max": g_max,
                "V_thr": V_thr, "V_sat": V_sat
            }
            synapses[nom] = NonSpikingSynapse(Veq, g_max, V_thr, V_sat)
            messagebox.showinfo("Succès", f"Synapse '{nom}' ajoutée.")
            fenetre.destroy()
        except ValueError:
            messagebox.showerror("Erreur", "Paramètres invalides.")

    tk.Button(fenetre, text="Valider", command=valider).grid(row=5, column=0, columnspan=2)

# === Interface principale ===
root = tk.Tk()
root.title("Création de neurones et synapses")

frame = tk.Frame(root)
frame.pack(pady=10)

btn_neurone = tk.Button(frame, text="Ajouter un neurone", command=ajouter_neurone)
btn_synapse = tk.Button(frame, text="Ajouter une synapse", command=ajouter_synapse)

btn_neurone.grid(row=0, column=0, padx=10)
btn_synapse.grid(row=0, column=1, padx=10)

root.mainloop()

# === Générer l’architecture des connexions ===
Neuron_architecture = {n: {"presynaptiques": [], "postsynaptiques": []} for n in neurons}

for nom_synapse in synapses:
    try:
        pre, post = nom_synapse.split("_")
        if post in Neuron_architecture:
            Neuron_architecture[post]["presynaptiques"].append(pre)
        if pre in Neuron_architecture:
            Neuron_architecture[pre]["postsynaptiques"].append(post)
    except ValueError:
        print(f"⚠️ Format de synapse invalide : '{nom_synapse}' (attendu: 'pre_post')")

