import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import json
from Model import Model

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

# Dictionnaires globaux
dic = {
    "neuron": {},
    "synapse": {},
    "spindle": {},
    "muscle": {},
    "mechmodel": {},
    "globals_parameters": {},
    "stims": {},
}


# === Fonctions d'ajout ===


def neuron():
    fenetre = tk.Toplevel(root)
    fenetre.title("Ajouter ou modifier un neurone")

    # Choix du neurone
    tk.Label(fenetre, text="Neurone:").grid(row=0, column=0)
    options = ["<Nouveau>"] + list(dic["neuron"].keys())
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

            dic["neuron"][nom] = {"V_rest": V_rest, "tau": tau, "Rm": Rm}

            messagebox.showinfo("Succès", f"neurone '{nom}' ajouté ou modifié.")
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
    options = ["<Nouveau>"] + list(dic["synapse"].keys())
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
        if choix != "<Nouveau>" and choix in dic["synapse"]:
            props = dic["synapse"][choix]
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

            dic["synapse"][nom] = {
                "Veq": Veq,
                "g_max": g_max,
                "V_thr": V_thr,
                "V_sat": V_sat,
            }
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
        if nom in dic.get("spindle", {}):
            for fibre in fibres:
                for param in parametres:
                    try:
                        val = dic["spindle"][nom][fibre][param]
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
            dic.setdefault("spindle", {})[nom] = {}
            for fibre in fibres:
                dic["spindle"][nom][fibre] = {
                    param: float(entries[fibre][param].get()) for param in parametres
                }
            messagebox.showinfo("Succès", f"spindle '{nom}' ajouté ou modifié.")
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


def display_architecture():
    fenetre = tk.Toplevel(root)
    fenetre.title("Architecture complète du modèle")

    fenetre.state("zoomed")

    frame = tk.Frame(fenetre)
    frame.pack(fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text = tk.Text(frame, yscrollcommand=scrollbar.set)
    text.pack(fill=tk.BOTH, expand=True)

    def afficher_contenu(obj, indent=0):
        espace = "    " * indent
        if isinstance(obj, dict):
            for cle, val in obj.items():
                text.insert(tk.END, f"{espace}{cle}:\n")
                afficher_contenu(val, indent + 1)
        else:
            text.insert(tk.END, f"{espace}{obj}\n")

    text.insert(tk.END, "📦 Architecture du dictionnaire `dic` :\n\n")
    afficher_contenu(dic)


def sauvegarder_dic():
    filepath = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Fichiers JSON", "*.json")],
        title="Enregistrer sous",
    )
    if not filepath:
        return  # L'utilisateur a annulé

    try:
        with open(filepath, "w") as f:
            json.dump(dic, f, indent=4)
        messagebox.showinfo(
            "Sauvegarde réussie", f"Dictionnaire enregistré dans\n{filepath}"
        )
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue :\n{e}")


def charger_dic():
    filepath = filedialog.askopenfilename(
        defaultextension=".json",
        filetypes=[("Fichiers JSON", "*.json")],
        title="Ouvrir un fichier de configuration",
    )
    if not filepath:
        return

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            dic.update(data)
        messagebox.showinfo(
            "Chargement réussi", f"Configuration chargée depuis\n{filepath}"
        )
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de charger le fichier :\n{e}")


def mise_a_jour_pre_post():
    for synapse_name in dic["synapse"]:
        try:
            pre, post = synapse_name.split("_", 1)

            dic["synapse"][synapse_name]["neuron_pre"] = pre
            dic["synapse"][synapse_name]["neuron_post"] = post

            if dic["neuron"][post]["input_synapse"] is None:
                dic["neuron"][post]["input_synapse"] = []

            # Ajout du nom de la synapse à la liste
            if synapse_name not in dic["neuron"][post]["input_synapse"]:
                dic["neuron"][post]["input_synapse"].append(synapse_name)

        except ValueError:
            print(f"Nom de synapse invalide : {synapse_name} (il manque un '_')")

    for muscle_name in dic["muscle"]:  # a améliorer
        if "Flx" in muscle_name:
            dic["muscle"][muscle_name]["neuron_pre"] = "FlxAlpha"
        else:
            dic["muscle"][muscle_name]["neuron_pre"] = "ExtAlpha"


def stims():
    fenetre = tk.Toplevel(root)
    fenetre.title("Stimulations")

    # Initialisation si nécessaire
    if "stimulations" not in dic:
        dic["stimulations"] = {"neuron": {}, "synapse": {}}

    entrees = {}
    row = 0

    # Affichage des neurones
    tk.Label(fenetre, text="📘 Neurones", font=("Arial", 12, "bold")).grid(
        row=row, column=0, columnspan=3, sticky="w"
    )
    row += 1

    for nom in dic.get("neuron", {}):
        tk.Label(fenetre, text=nom).grid(row=row, column=0, sticky="w")
        e1 = tk.Entry(fenetre, width=8)
        e2 = tk.Entry(fenetre, width=8)

        stim = dic["stimulations"]["neuron"].get(nom, {})
        e1.insert(0, str(stim.get("I_set", 0.0)))
        e2.insert(0, str(stim.get("I_go", 0.0)))

        e1.grid(row=row, column=1)
        e2.grid(row=row, column=2)

        entrees[nom] = {"type": "neuron", "I_set": e1, "I_go": e2}
        row += 1

    # Affichage des synapses
    tk.Label(fenetre, text="🔗 Synapses", font=("Arial", 12, "bold")).grid(
        row=row, column=0, columnspan=3, sticky="w"
    )
    row += 1

    for nom in dic.get("synapse", {}):
        tk.Label(fenetre, text=nom).grid(row=row, column=0, sticky="w")
        e1 = tk.Entry(fenetre, width=8)
        e2 = tk.Entry(fenetre, width=8)

        stim = dic["stimulations"]["synapse"].get(nom, {})
        e1.insert(0, str(stim.get("g_set", 0.0)))
        e2.insert(0, str(stim.get("g_go", 0.0)))

        e1.grid(row=row, column=1)
        e2.grid(row=row, column=2)

        entrees[nom] = {"type": "synapse", "g_set": e1, "g_go": e2}
        row += 1

    def appliquer():
        for nom, champs in entrees.items():
            try:
                if champs["type"] == "neuron":
                    I_set = float(champs["I_set"].get())
                    I_go = float(champs["I_go"].get())
                    dic["stimulations"]["neuron"][nom] = {"I_set": I_set, "I_go": I_go}
                elif champs["type"] == "synapse":
                    g_set = float(champs["g_set"].get())
                    g_go = float(champs["g_go"].get())
                    dic["stimulations"]["synapse"][nom] = {"g_set": g_set, "g_go": g_go}
            except ValueError:
                messagebox.showerror("Erreur", f"Valeurs invalides pour '{nom}'")
                return

        messagebox.showinfo(
            "Succès", "Stimulations enregistrées dans dic['stimulations']."
        )
        fenetre.destroy()

    tk.Button(fenetre, text="Appliquer", command=appliquer).grid(
        row=row, column=0, columnspan=3, pady=10
    )


def muscle():
    fenetre = tk.Toplevel(root)
    fenetre.title("Ajouter ou modifier un muscle")

    if "muscles" not in dic:
        dic["muscles"] = {}

    # Liste déroulante pour sélectionner un muscle existant ou nouveau
    tk.Label(fenetre, text="Muscle :").grid(row=0, column=0)
    options = ["<Nouveau>"] + list(dic["muscles"].keys())
    var_choix = tk.StringVar(fenetre)
    var_choix.set("<Nouveau>")
    menu = tk.OptionMenu(fenetre, var_choix, *options)
    menu.grid(row=0, column=1)

    labels = [
        "Nom",
        "L",
        "B",
        "Kpe",
        "Kse",
        "max_active_tension",
        "steepness",
        "x_offset",
        "y_offset",
        "L_rest",
        "L_width",
    ]

    entrees = {}
    for i, label in enumerate(labels):
        tk.Label(fenetre, text=label + " :").grid(row=i + 1, column=0, sticky="w")
        e = tk.Entry(fenetre)
        e.grid(row=i + 1, column=1)
        entrees[label] = e

    def remplir_champs(*args):
        nom = var_choix.get()
        if nom != "<Nouveau>" and nom in dic["muscles"]:
            params = dic["muscles"][nom]
            entrees["Nom"].delete(0, tk.END)
            entrees["Nom"].insert(0, nom)
            for key in labels[1:]:
                entrees[key].delete(0, tk.END)
                entrees[key].insert(0, str(params.get(key, "")))
        else:
            for e in entrees.values():
                e.delete(0, tk.END)

    var_choix.trace("w", remplir_champs)

    def valider():
        try:
            nom = entrees["Nom"].get()
            if not nom:
                raise ValueError("Nom vide.")

            params = {}
            for key in labels[1:]:
                params[key] = float(entrees[key].get())

            dic["muscle"][nom] = params

            messagebox.showinfo("Succès", f"Muscle '{nom}' ajouté ou modifié.")
            fenetre.destroy()
        except Exception as e:
            messagebox.showerror("Erreur", f"Paramètre invalide : {e}")

    tk.Button(fenetre, text="Valider", command=valider).grid(
        row=len(labels) + 1, column=0, columnspan=2, pady=10
    )


def global_parameters():
    fenetre = tk.Toplevel(root)
    fenetre.title("Paramètres globaux")

    if "globals_parameters" not in dic:
        dic["globals_parameters"] = {}

    labels = [
        "dt",
        "masse_avant_bras",
        "L_avant_bras",
        "total_time",
        "I_set_t",
        "I_go_t",
    ]
    entrees = {}

    for i, label in enumerate(labels):
        tk.Label(fenetre, text=label + " :").grid(row=i, column=0, sticky="w")
        e = tk.Entry(fenetre)
        e.grid(row=i, column=1)
        entrees[label] = e

        # Remplir avec valeur existante si disponible
        if label in dic["globals_parameters"]:
            e.insert(0, str(dic["globals_parameters"][label]))

    def valider():
        try:
            for label in labels:
                val = float(entrees[label].get())
                dic["globals_parameters"][label] = val

            messagebox.showinfo("Succès", "Paramètres globaux enregistrés.")
            fenetre.destroy()
        except ValueError:
            messagebox.showerror(
                "Erreur", "Tous les champs doivent contenir des nombres."
            )

    tk.Button(fenetre, text="Valider", command=valider).grid(
        row=len(labels), column=0, columnspan=2, pady=10
    )


def run_model():
    model = Model(dicModel=dic)
    model.init()
    model.run_model()


if __name__ == "__main__":
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()

    btn_neurone = tk.Button(frame, text="Ajouter un neurone", command=neuron)
    btn_synapse = tk.Button(frame, text="Ajouter une synapse", command=synapse)
    btn_architecture = tk.Button(
        frame, text="Affiche l'architecture", command=display_architecture
    )
    btn_spindle = tk.Button(frame, text="Spindle", command=spindle)
    btn_save = tk.Button(frame, text="Sauvegarder", command=sauvegarder_dic)
    btn_load = tk.Button(frame, text="Load model", command=charger_dic)
    btn_stim = tk.Button(frame, text="Strimulations", command=stims)
    btn_muscle = tk.Button(frame, text="Muscle", command=muscle)
    btn_global_parameters = tk.Button(
        frame, text="global_parameters", command=global_parameters
    )
    btn_mise_a_jour_post_pre = tk.Button(
        frame, text="MAJ post pre", command=mise_a_jour_pre_post
    )
    btn_run_model = tk.Button(frame, text="run_model", command=run_model)

    btn_neurone.grid(row=0, column=0, padx=10)
    btn_synapse.grid(row=0, column=1, padx=10)
    btn_architecture.grid(row=0, column=2, padx=10)
    btn_spindle.grid(row=0, column=3, padx=10)
    btn_save.grid(row=0, column=4, padx=10)
    btn_load.grid(row=0, column=5, padx=10)
    btn_stim.grid(row=0, column=6, padx=10)
    btn_muscle.grid(row=0, column=7, padx=10)
    btn_global_parameters.grid(row=0, column=8, padx=10)
    btn_mise_a_jour_post_pre.grid(row=0, column=9, padx=10)
    btn_run_model.grid(row=0, column=10, padx=10)
    root.mainloop()
