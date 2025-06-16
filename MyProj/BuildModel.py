from Neurons import NonSpikingNeuron
from Synapses import NonSpikingSynapse
from MileusnicSpindle import MileusnicIntrafusal, MileusnicSpindle
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
dic = {"NonSpikingNeuron": {}, "NonSpikingSynapse": {}, "Spindle": {}}
neurons = {}
synapses = {}

# === Fonctions d'ajout ===


def neuron():
    fenetre = tk.Toplevel(root)
    fenetre.title("Ajouter ou modifier un neurone")

    # Choix du neurone
    tk.Label(fenetre, text="Neurone:").grid(row=0, column=0)
    options = ["<Nouveau>"] + list(dic["NonSpikingNeuron"].keys())
    var_choix = tk.StringVar(fenetre)
    var_choix.set("<Nouveau>")
    menu = tk.OptionMenu(fenetre, var_choix, *options)
    menu.grid(row=0, column=1)

    # Champs de saisie
    tk.Label(fenetre, text="Nom du neurone:").grid(row=1, column=0)
    tk.Label(fenetre, text="V_rest:").grid(row=2, column=0)
    tk.Label(fenetre, text="tau:").grid(row=3, column=0)
    tk.Label(fenetre, text="Rm:").grid(row=4, column=0)

    e_nom = tk.Entry(fenetre)
    e_vrest = tk.Entry(fenetre)
    e_tau = tk.Entry(fenetre)
    e_rm = tk.Entry(fenetre)

    e_nom.grid(row=1, column=1)
    e_vrest.grid(row=2, column=1)
    e_tau.grid(row=3, column=1)
    e_rm.grid(row=4, column=1)

    def remplir_champs(*args):
        choix = var_choix.get()
        if choix != "<Nouveau>" and choix in dic["NonSpikingNeuron"]:
            props = dic["NonSpikingNeuron"][choix]
            e_nom.delete(0, tk.END)
            e_nom.insert(0, choix)
            e_vrest.delete(0, tk.END)
            e_vrest.insert(0, str(props["V_rest"]))
            e_tau.delete(0, tk.END)
            e_tau.insert(0, str(props["tau"]))
            e_rm.delete(0, tk.END)
            e_rm.insert(0, str(props["Rm"]))
        else:
            e_nom.delete(0, tk.END)
            e_vrest.delete(0, tk.END)
            e_tau.delete(0, tk.END)
            e_rm.delete(0, tk.END)

    var_choix.trace("w", remplir_champs)

    def valider():
        try:
            nom = e_nom.get()
            V_rest = float(e_vrest.get())
            tau = float(e_tau.get())
            Rm = float(e_rm.get())

            dic["NonSpikingNeuron"][nom] = {"V_rest": V_rest, "tau": tau, "Rm": Rm}
            neurons[nom] = NonSpikingNeuron(V_rest, tau, Rm)

            messagebox.showinfo("Succès", f"Neurone '{nom}' ajouté ou modifié.")
            fenetre.destroy()
        except ValueError:
            messagebox.showerror("Erreur", "Paramètres invalides.")

    tk.Button(fenetre, text="Valider", command=valider).grid(
        row=5, column=0, columnspan=2, pady=10
    )


def synapse():
    fenetre = tk.Toplevel(root)
    fenetre.title("Ajouter ou modifier une synapse")

    # Sélecteur de synapse existante
    tk.Label(fenetre, text="Sélectionner une synapse:").grid(row=0, column=0)
    options = ["<Nouveau>"] + list(dic["NonSpikingSynapse"].keys())
    var_choix = tk.StringVar(fenetre)
    var_choix.set("<Nouveau>")
    menu = tk.OptionMenu(fenetre, var_choix, *options)
    menu.grid(row=0, column=1)

    # Champs d'édition
    tk.Label(fenetre, text="Nom (pre_post):").grid(row=1, column=0)
    tk.Label(fenetre, text="Veq:").grid(row=2, column=0)
    tk.Label(fenetre, text="g_max:").grid(row=3, column=0)
    tk.Label(fenetre, text="V_thr:").grid(row=4, column=0)
    tk.Label(fenetre, text="V_sat:").grid(row=5, column=0)

    e_nom = tk.Entry(fenetre)
    e_veq = tk.Entry(fenetre)
    e_gmax = tk.Entry(fenetre)
    e_vthr = tk.Entry(fenetre)
    e_vsat = tk.Entry(fenetre)

    e_nom.grid(row=1, column=1)
    e_veq.grid(row=2, column=1)
    e_gmax.grid(row=3, column=1)
    e_vthr.grid(row=4, column=1)
    e_vsat.grid(row=5, column=1)

    # Remplir les champs si une synapse existante est sélectionnée
    def remplir_champs(*args):
        choix = var_choix.get()
        if choix != "<Nouveau>" and choix in dic["NonSpikingSynapse"]:
            props = dic["NonSpikingSynapse"][choix]
            e_nom.delete(0, tk.END)
            e_nom.insert(0, choix)
            e_veq.delete(0, tk.END)
            e_veq.insert(0, str(props["Veq"]))
            e_gmax.delete(0, tk.END)
            e_gmax.insert(0, str(props["g_max"]))
            e_vthr.delete(0, tk.END)
            e_vthr.insert(0, str(props["V_thr"]))
            e_vsat.delete(0, tk.END)
            e_vsat.insert(0, str(props["V_sat"]))
        else:
            e_nom.delete(0, tk.END)
            e_veq.delete(0, tk.END)
            e_gmax.delete(0, tk.END)
            e_vthr.delete(0, tk.END)
            e_vsat.delete(0, tk.END)

    var_choix.trace_add("write", remplir_champs)
    remplir_champs()  # appel initial

    # Validation
    def valider():
        try:
            nom = e_nom.get().strip()
            Veq = float(e_veq.get())
            g_max = float(e_gmax.get())
            V_thr = float(e_vthr.get())
            V_sat = float(e_vsat.get())

            dic["NonSpikingSynapse"][nom] = {
                "Veq": Veq,
                "g_max": g_max,
                "V_thr": V_thr,
                "V_sat": V_sat,
            }
            synapses[nom] = NonSpikingSynapse(Veq, g_max, V_thr, V_sat)
            messagebox.showinfo("Succès", f"Synapse '{nom}' ajoutée ou modifiée.")
            fenetre.destroy()
        except ValueError:
            messagebox.showerror(
                "Erreur", "Veuillez entrer des valeurs numériques valides."
            )

    tk.Button(fenetre, text="Valider", command=valider).grid(
        row=6, column=0, columnspan=2, pady=10
    )


def spindle():
    fenetre = tk.Toplevel(root)
    fenetre.title("Ajouter ou modifier un spindle")

    tk.Label(fenetre, text="Nom du spindle:").grid(row=0, column=0)
    entry_nom = tk.Entry(fenetre)
    entry_nom.grid(row=0, column=1)

    parametres = [
        "Ksr",
        "Kpr",
        "tau",
        "beta",
        "beta_dyn",
        "beta_stat",
        "L0pr",
        "L0sr",
        "Lnsr",
        "G",
        "M",
        "R",
        "F_gamma",
        "C_shortening",
        "C_lengthening",
        "a",
        "gamma_freq",
        "freq_to_activation",
        "dt",
        "p",
        "L0",
    ]

    fibres = ["Bag1", "Bag2", "Chain"]
    entries = {fibre: {} for fibre in fibres}

    for col, fibre in enumerate(fibres):
        tk.Label(fenetre, text=fibre, font=("Arial", 10, "bold")).grid(
            row=1, column=col * 2, columnspan=2
        )
        for i, param in enumerate(parametres):
            tk.Label(fenetre, text=param + ":").grid(row=i + 2, column=col * 2)
            entry = tk.Entry(fenetre)
            entry.grid(row=i + 2, column=col * 2 + 1)
            entries[fibre][param] = entry

    def charger_valeurs():
        nom = entry_nom.get().strip()
        if nom in dic.get("Spindle", {}):
            for fibre in fibres:
                for param in parametres:
                    try:
                        val = dic["Spindle"][nom][fibre][param]
                        entries[fibre][param].delete(0, tk.END)
                        entries[fibre][param].insert(0, str(val))
                    except KeyError:
                        continue
        else:
            messagebox.showinfo("Info", f"Aucun spindle nommé '{nom}' trouvé.")

    def valider():
        nom = entry_nom.get().strip()
        if not nom:
            messagebox.showerror("Erreur", "Nom du spindle requis.")
            return
        try:
            dic.setdefault("Spindle", {})[nom] = {}
            for fibre in fibres:
                dic["Spindle"][nom][fibre] = {
                    param: float(entries[fibre][param].get()) for param in parametres
                }
            messagebox.showinfo("Succès", f"Spindle '{nom}' ajouté ou modifié.")
            fenetre.destroy()
        except ValueError:
            messagebox.showerror("Erreur", "Tous les champs doivent être des nombres.")

    # Boutons
    tk.Button(fenetre, text="Charger", command=charger_valeurs).grid(
        row=0, column=2, padx=10
    )
    tk.Button(fenetre, text="Valider", command=valider).grid(
        row=len(parametres) + 3, column=0, columnspan=6, pady=10
    )


def DisplayArchitecture():
    fenetre = tk.Toplevel(root)
    fenetre.title("Architecture des neurones")

    text = tk.Text(fenetre, width=60, height=25)
    text.pack(padx=10, pady=10)

    Neuron_architecture = {
        n: {"presynaptiques": [], "postsynaptiques": []} for n in neurons
    }

    for nom_synapse in synapses:
        try:
            pre, post = nom_synapse.split("_")
            if post in Neuron_architecture:
                Neuron_architecture[post]["presynaptiques"].append(pre)
            if pre in Neuron_architecture:
                Neuron_architecture[pre]["postsynaptiques"].append(post)
        except ValueError:
            text.insert(tk.END, f"⚠️ Synapse mal nommée : '{nom_synapse}'\n")

    for nom_neurone, connexions in Neuron_architecture.items():
        text.insert(tk.END, f"🔹 Neurone : {nom_neurone}\n")
        text.insert(
            tk.END,
            f"   ↳ Entrées : {', '.join(connexions['presynaptiques']) or 'aucune'}\n",
        )
        text.insert(
            tk.END,
            f"   ↳ Sorties : {', '.join(connexions['postsynaptiques']) or 'aucune'}\n\n",
        )


# === Interface principale ===
root = tk.Tk()
root.title("Création de neurones et synapses")

frame = tk.Frame(root)
frame.pack(pady=10)

btn_neurone = tk.Button(frame, text="Ajouter un neurone", command=neuron)
btn_synapse = tk.Button(frame, text="Ajouter une synapse", command=synapse)
btn_architecture = tk.Button(
    frame, text="Affiche l'architecture", command=DisplayArchitecture
)
btn_spindle = tk.Button(frame, text="Spindle", command=spindle)

btn_neurone.grid(row=0, column=0, padx=10)
btn_synapse.grid(row=0, column=1, padx=10)
btn_architecture.grid(row=0, column=2, padx=10)
btn_spindle.grid(row=1, column=0, columnspan=3, pady=10)

root.mainloop()
