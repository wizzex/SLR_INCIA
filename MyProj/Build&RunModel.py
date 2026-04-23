
"""

This script allow to create a neuromusculoskeltal model using the class model: 

Here you have a GUI allowing to:
- Create an instance of Model
- Save a model 
- Load a model 
- Change the general parameters of the simulation (total time, step time etc.) 
- Display the model architecture 
- Run a simulation and testing different set of parameters/stimulations 
- Visualize the outcome of your simulation with plots
- Visualize your simulation with the musculoskeltal model using pyorerun (biorbd, Pierre Puchaud)  ########## A faire ??? ou bien ###########

The model instance is saved as a .json file 

The outcome for pyorerun visualization is saved as a csv file 




Important naming rules 

for synapses: 
if 2 neurons are linked via synapses 
neuronA and neuronB
the synapse name HAS to be 
neuronA_neuronB

for motoneurons: 
motoneurons innervating the muscle name FlxMuscle 
HAS to be named FlxAlpha

what we call function at the moment are either Flx or Ext for Flexor and Extensor 

for muscles:
must be function of the muscle + Muscle  ex: ExtMuscle

for spindles:
function + Spindle ex: FlxSpindle

With the current version only two muscles model work, name of muscle are FlxMuscle and ExtMuscle


"""

import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import json
import csv
#from components import *
from components import *
from Model import * 
import bardisbanian_visualizer as bardis

class BuildModel:
    def __init__(self):
        # self.dictionnaires globaux
        self.dic = {
            "neuron": {},
            "synapse": {},
            "spindle": {},
            "muscle": {},
            "mechmodel": {},
            "globals_parameters": {},
        }

        self.entries = {
            "neuron": {},
            "synapse": {},
            "spindle": {},
            "muscle": {},
            "mechmodel": {},
            "globals_parameters": {},
        }

    def confirm(self, d, path):
        sub_dic = self.dic
        for key in path:
            sub_dic = sub_dic[key]

        for key, value in d.items():
            sub_dic[key] = float(value.get())

    def neuron(self):
        fenetre = tk.Toplevel(root)
        fenetre.title("Ajouter ou modifier un neurone")

        # neuron_choice
        tk.Label(fenetre, text="Neurone:").grid(row=0, column=0)
        options = ["<New>"] + list(self.dic["neuron"].keys())
        neuron_choice = tk.StringVar(fenetre)
        neuron_choice.set("<New>")
        menu = tk.OptionMenu(fenetre, neuron_choice, *options)
        menu.grid(row=0, column=1)

        # display parameters
        tk.Label(fenetre, text="Nom du neurone:").grid(row=1, column=0)
        tk.Label(fenetre, text="V_rest:").grid(row=2, column=0)
        tk.Label(fenetre, text="tau:").grid(row=3, column=0)
        tk.Label(fenetre, text="Rm:").grid(row=4, column=0)

        e_name = tk.Entry(fenetre)
        e_vrest = tk.Entry(fenetre)
        e_tau = tk.Entry(fenetre)
        e_rm = tk.Entry(fenetre)

        e_name.grid(row=1, column=1)
        e_vrest.grid(row=2, column=1)
        e_tau.grid(row=3, column=1)
        e_rm.grid(row=4, column=1)

        def fill_neuron_params(*args):
            neuron_name = neuron_choice.get()
            if neuron_name != "<Nouveau>" and neuron_name in self.dic["neuron"]:
                param = self.dic["neuron"][neuron_name]["params"]
                e_name.delete(0, tk.END)
                e_name.insert(0, neuron_name)
                e_vrest.delete(0, tk.END)
                e_vrest.insert(0, str(param["V_rest"]))
                e_tau.delete(0, tk.END)
                e_tau.insert(0, str(param["tau"]))
                e_rm.delete(0, tk.END)
                e_rm.insert(0, str(param["Rm"]))
            else:
                e_name.delete(0, tk.END)
                e_vrest.delete(0, tk.END)
                e_tau.delete(0, tk.END)
                e_rm.delete(0, tk.END)

        neuron_choice.trace_add("write", fill_neuron_params)

        def neur_confirm():
            try:
                nom = e_name.get().strip()  # .strip() remove space
                V_rest = float(e_vrest.get())
                tau = float(e_tau.get())
                Rm = float(e_rm.get())

                self.dic["neuron"][nom] = {
                    "params": {"V_rest": V_rest, "tau": tau, "Rm": Rm}
                }

                messagebox.showinfo("Succès", f"neurone '{nom}' ajouté ou modifié.")
                self.pre_post_update()
                fenetre.destroy()
            except ValueError:
                messagebox.showerror("Erreur", "Paramètres invalides.")

        tk.Button(fenetre, text="Valider", command=neur_confirm).grid(
            row=5, column=0, columnspan=2, pady=10
        )

    def synapse(self):
        fenetre = tk.Toplevel(root)
        fenetre.title("Ajouter ou modifier une synapse")

        tk.Label(fenetre, text="Sélectionner une synapse:").grid(row=0, column=0)
        options = ["<New>"] + list(self.dic["synapse"].keys())
        var_choix = tk.StringVar(fenetre)
        var_choix.set("<New>")
        menu = tk.OptionMenu(fenetre, var_choix, *options)
        menu.grid(row=0, column=1)

        tk.Label(fenetre, text="Nom (pre_post):").grid(row=1, column=0)
        tk.Label(fenetre, text="Veq:").grid(row=2, column=0)
        tk.Label(fenetre, text="g_max:").grid(row=3, column=0)
        tk.Label(fenetre, text="V_thr:").grid(row=4, column=0)
        tk.Label(fenetre, text="V_sat:").grid(row=5, column=0)

        e_name = tk.Entry(fenetre)
        e_veq = tk.Entry(fenetre)
        e_gmax = tk.Entry(fenetre)
        e_vthr = tk.Entry(fenetre)
        e_vsat = tk.Entry(fenetre)

        e_name.grid(row=1, column=1)
        e_veq.grid(row=2, column=1)
        e_gmax.grid(row=3, column=1)
        e_vthr.grid(row=4, column=1)
        e_vsat.grid(row=5, column=1)

        def fill_synapse_params(*args):
            choix = var_choix.get()
            if choix != "<New>" and choix in self.dic["synapse"]:
                props = self.dic["synapse"][choix]
                e_name.delete(0, tk.END)
                e_name.insert(0, choix)
                e_veq.delete(0, tk.END)
                e_veq.insert(0, str(props["Veq"]))
                e_gmax.delete(0, tk.END)
                e_gmax.insert(0, str(props["g_max"]))
                e_vthr.delete(0, tk.END)
                e_vthr.insert(0, str(props["V_thr"]))
                e_vsat.delete(0, tk.END)
                e_vsat.insert(0, str(props["V_sat"]))
            else:
                e_name.delete(0, tk.END)
                e_veq.delete(0, tk.END)
                e_gmax.delete(0, tk.END)
                e_vthr.delete(0, tk.END)
                e_vsat.delete(0, tk.END)

        var_choix.trace_add("write", fill_synapse_params)

        def synapse_confirm():
            try:
                nom = e_name.get().strip()
                Veq = float(e_veq.get())
                g_max = float(e_gmax.get())
                V_thr = float(e_vthr.get())
                V_sat = float(e_vsat.get())

                self.dic["synapse"][nom] = {
                    "param": {
                        "Veq": Veq,
                        "g_max": g_max,
                        "V_thr": V_thr,
                        "V_sat": V_sat,
                    }
                }
                messagebox.showinfo("Succès", f"Synapse '{nom}' ajoutée ou modifiée.")
                self.pre_post_update()
                fenetre.destroy()
            except ValueError:
                messagebox.showerror(
                    "Erreur", "Veuillez entrer des valeurs numériques valides."
                )

        tk.Button(fenetre, text="Valider", command=synapse_confirm).grid(
            row=6, column=0, columnspan=2, pady=10
        )

    def spindle(self):
        fenetre = tk.Toplevel(root)
        fenetre.title("Create or modify a spindle")

        self.dic.setdefault("spindle", {})

        # --------------------------
        # Spindle selection
        # --------------------------
        tk.Label(fenetre, text="Select spindle:").grid(row=0, column=0)

        options = ["<New>"] + list(self.dic["spindle"].keys())
        var_choix = tk.StringVar()
        var_choix.set("<New>")

        menu = tk.OptionMenu(fenetre, var_choix, *options)
        menu.grid(row=0, column=1)

        tk.Label(fenetre, text="Spindle name:").grid(row=0, column=2)
        e_name = tk.Entry(fenetre)
        e_name.grid(row=0, column=3)

        # --------------------------
        # Parameters
        # --------------------------
        params = [
            "Ksr","Kpr","tau","beta","beta_dyn","beta_stat",
            "L0pr","L0sr","Lnsr","G","M","R","F_gamma",
            "C_shortening","C_lengthening","a",
            "gamma_freq","freq_to_activation","dt","p",
        ]

        default_values = {
        "Bag1": {
            "Ksr": 10.4649, "Kpr": 0.15, "tau": 0.149,
            "beta": 0.0605, "beta_dyn": 0.2592, "beta_stat": 0.0,
            "L0pr": 0.76, "L0sr": 0.04, "Lnsr": 0.0423,
            "G": 20.0, "M": 0.0002, "R": 0.46,
            "F_gamma": 0.0289,
            "C_shortening": 0.42, "C_lengthening": 1.0,
            "a": 0.3,
            "gamma_freq": 90.0,
            "freq_to_activation": 60.0,
            "dt": 0.0002,
            "p": 2.0
        },
        "Bag2": {
            "Ksr": 10.4649, "Kpr": 0.15, "tau": 0.205,
            "beta": 0.0822, "beta_dyn": 0.0, "beta_stat": -0.046,
            "L0pr": 0.76, "L0sr": 0.04, "Lnsr": 0.0423,
            "G": 20.0, "M": 0.0002, "R": 0.46,
            "F_gamma": 0.0636,
            "C_shortening": 0.42, "C_lengthening": 1.0,
            "a": 0.3,
            "gamma_freq": 50.0,
            "freq_to_activation": 60.0,
            "dt": 0.0002,
            "p": 2.0
        },
        "Chain": {
            "Ksr": 10.4649, "Kpr": 0.15, "tau": 0.205,
            "beta": 0.0822, "beta_dyn": 0.0, "beta_stat": -0.069,
            "L0pr": 0.76, "L0sr": 0.04, "Lnsr": 0.0423,
            "G": 20.0, "M": 0.0002, "R": 0.46,
            "F_gamma": 0.0954,
            "C_shortening": 0.42, "C_lengthening": 1.0,
            "a": 0.3,
            "gamma_freq": 50.0,
            "freq_to_activation": 60.0,
            "dt": 0.0002,
            "p": 2.0
        }
        }

        def fill_with_defaults():
            for fibre in fibers:
                for param in params:
                    entries[fibre][param].delete(0, tk.END)
                    value = default_values[fibre][param]
                    entries[fibre][param].insert(0, str(value))

        fibers = ["Bag1", "Bag2", "Chain"]

        # Store entries here
        entries = {f: {} for f in fibers}

        # Create grid
        for col, fibre in enumerate(fibers):
            tk.Label(fenetre, text=fibre, font=("Arial", 10, "bold")).grid(
                row=1, column=col * 2, columnspan=2
            )

            for i, param in enumerate(params):
                tk.Label(fenetre, text=param).grid(row=i + 2, column=col * 2)
                e = tk.Entry(fenetre, width=10)
                e.grid(row=i + 2, column=col * 2 + 1)
                entries[fibre][param] = e


        def fill_with_defaults():
            for fibre in fibers:
                for param in params:
                    entries[fibre][param].delete(0, tk.END)
                    value = default_values[fibre][param]
                    entries[fibre][param].insert(0, str(value))

        # --------------------------
        # Auto-fill when selecting spindle
        # --------------------------
        def fill_spindle_params(*args):
            choix = var_choix.get()

            # Clear name field
            e_name.delete(0, tk.END)

            if choix != "<New>" and choix in self.dic["spindle"]:
                e_name.insert(0, choix)
                props = self.dic["spindle"][choix]

                for fibre in fibers:
                    for param in params:
                        entries[fibre][param].delete(0, tk.END)
                        try:
                            value = props[fibre]["params"][param]
                            entries[fibre][param].insert(0, str(value))
                        except KeyError:
                            pass
            else:
                fill_with_defaults()
                # Clear all fields
                #for fibre in fibers:
                #    for param in params:
                #        entries[fibre][param].delete(0, tk.END)

        var_choix.trace_add("write", fill_spindle_params)

        # --------------------------
        # Confirm button
        # --------------------------
        def spindle_confirm():
            name = e_name.get().strip()

            if not name:
                messagebox.showerror("Error", "Spindle name required.")
                return

            try:
                self.dic["spindle"][name] = {}

                for fibre in fibers:
                    self.dic["spindle"][name][fibre] = {"params": {}}
                    for param in params:
                        value = float(entries[fibre][param].get())
                        self.dic["spindle"][name][fibre]["params"][param] = value

                messagebox.showinfo("Success", f"Spindle '{name}' added/modified.")
                self.pre_post_update()
                fenetre.destroy()

            except ValueError:
                messagebox.showerror("Error", "All parameters must be numeric.")
        fill_with_defaults()
        # --------------------------
        # Buttons
        # --------------------------
        tk.Button(fenetre, text="Validate", command=spindle_confirm).grid(
            row=len(params) + 3,
            column=0,
            columnspan=6,
            pady=10
        )
    
    def display_architecture(self):
        fenetre = tk.Toplevel(root)
        fenetre.title("Architecture complète du modèle")

        fenetre.state("zoomed")

        frame = tk.Frame(fenetre)
        frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text = tk.Text(frame, yscrollcommand=scrollbar.set)
        text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text.yview)

        def afficher_contenu(obj, indent=0):
            espace = "    " * indent
            if isinstance(obj, dict):
                for cle, val in obj.items():
                    text.insert(tk.END, f"{espace}{cle}:\n")
                    afficher_contenu(val, indent + 1)
            else:
                text.insert(tk.END, f"{espace}{obj}\n")

        text.insert(tk.END, "📦 Architecture du dictionnaire `self.dic` :\n\n")
        afficher_contenu(self.dic)

    def sauvegarder_dic(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Fichiers JSON", "*.json")],
            title="Enregistrer sous",
        )
        if not filepath:
            return  # L'utilisateur a annulé

        try:
            with open(filepath, "w") as f:
                json.dump(self.dic, f, indent=4)
            messagebox.showinfo(
                "Sauvegarde réussie", f"self.dictionnaire enregistré dans\n{filepath}"
            )
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue :\n{e}")

    def charger_dic(self):
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
                self.dic.update(data)
            messagebox.showinfo(
                "Chargement réussi", f"Configuration chargée depuis\n{filepath}"
            )
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le fichier :\n{e}")

    def pre_post_update(self):
        for synapse_name in self.dic["synapse"]:
            try:
                pre, post = synapse_name.split("_", 1)    # Identify pre and post neuron based on synapse name 

                # update pre and post neuron of the synapse

                self.dic["synapse"][synapse_name]["neuron_pre"] = pre
                self.dic["synapse"][synapse_name]["neuron_post"] = post

                # Check wheter pre and post neuron have been created yet 

                if pre not in self.dic["neuron"]:
                    print(f"\n Be careful, neuron {pre} doesn't exist yet")
                if post not in self.dic["neuron"]:
                    print(f"\n Be careful, neuron {post} doesn't exist yet")
                
                # Every neurons must have an input synapse, create this field if it's empty
                # Add synapse to the neuron input list IF it doesn't already exist
                 
                self.dic["neuron"][post].setdefault("input_synapse", [])
                if synapse_name not in self.dic["neuron"][post]["input_synapse"]:
                    self.dic["neuron"][post]["input_synapse"].append(synapse_name)
            except Exception as e:
                print("Problem with neuron pre post update", e)

        for muscle_name in self.dic["muscle"]:
            try:
                alpha_motoneuron = muscle_name.replace(":Muscle", "") + "Alpha"
                self.dic["muscle"][muscle_name]["neuron_pre"] = alpha_motoneuron
            except Exception as e:
                print("Problem with muscle pre post update", e)



                

            except ValueError:
                print(f"Nom de synapse invalide : {synapse_name} (il manque un '_')")

        for muscle_name in self.dic["muscle"]:  # a améliorer
            if "Flx" in muscle_name:
                self.dic["muscle"][muscle_name]["neuron_pre"] = "FlxAlpha"
            else:
                self.dic["muscle"][muscle_name]["neuron_pre"] = "ExtAlpha"

        for spindle_name in self.dic["spindle"]:
            self.dic["globals_parameters"][spindle_name] = spindle_name[:3] + "Muscle"

    def stims(self):
        fenetre = tk.Toplevel(root)
        fenetre.title("Stimulations")

        # Initialisation si nécessaire
        if "stimulations" not in self.dic:
            self.dic["stimulations"] = {"neuron": {}, "synapse": {}, "spindle": {}}
        if "stimulations" not in self.entries:
            self.entries["stimulations"] = {"neuron": {}, "synapse": {}, "spindle": {}}

        for neuron_name in self.dic["neuron"]:
            if neuron_name not in self.dic["stimulations"]["neuron"]:
                self.dic["stimulations"]["neuron"][neuron_name] = {}

            if neuron_name not in self.entries["stimulations"]["neuron"]:
                self.entries["stimulations"]["neuron"][neuron_name] = {}

        neuron_stim = self.dic["stimulations"]["neuron"]
        neuron_stim_entries = self.entries["stimulations"]["neuron"]

        for neuron_name in neuron_stim:
            if "I_set" and "I_go" not in neuron_stim[neuron_name]:
                neuron_stim[neuron_name]["I_set"] = 0
                neuron_stim[neuron_name]["I_go"] = 0
        for neuron_name in neuron_stim_entries:
            if "I_set" and "I_go" not in neuron_stim_entries[neuron_name]:
                neuron_stim_entries[neuron_name]["I_set"] = 0
                neuron_stim_entries[neuron_name]["I_go"] = 0

        synapse_stim = self.dic["stimulations"]["synapse"]
        synapse_stim_entries = self.entries["stimulations"]["synapse"]

        for synapse_name in synapse_stim:
            if "I_set" and "I_go" not in synapse_stim[synapse_name]:
                synapse_stim[synapse_name]["g_max"] = 0
        for synapse_name in synapse_stim_entries:
            if "I_set" and "I_go" not in synapse_stim[synapse_name]:
                synapse_stim_entries[synapse_name]["g_max"] = 0

        

        # Affichage des neurones
        tk.Label(fenetre, text="📘 Neuron", font=("Arial", 12, "bold")).grid(
            row=0, column=0, columnspan=3, sticky="w")
        tk.Label(fenetre, text="SET", font=("Arial", 10, "bold")).grid(
            row=1, column=1, sticky="w")
        tk.Label(fenetre, text="GO", font=("Arial", 10, "bold")).grid(
            row=1, column=2, sticky="w")
        
        row = 2

        for neuron_name in self.dic["neuron"]:
            tk.Label(fenetre, text=neuron_name).grid(row=row, column=0, sticky="w")
            e1 = tk.Entry(fenetre, width=8)
            e2 = tk.Entry(fenetre, width=8)

            I_set = self.dic["stimulations"]["neuron"][neuron_name]["I_set"]
            I_go = self.dic["stimulations"]["neuron"][neuron_name]["I_go"]
            e1.insert(0, str(I_set))
            e2.insert(0, str(I_go))

            e1.grid(row=row, column=1)
            e2.grid(row=row, column=2)

            self.entries["stimulations"]["neuron"][neuron_name] = {
                "I_set": e1,
                "I_go": e2,
            }
            row += 1

        # Affichage des synapses
        tk.Label(fenetre, text="🔗 Synapses", font=("Arial", 12, "bold")).grid(
            row=row, column=0, columnspan=3, sticky="w"
        )
        row += 1

        for synapse_name in self.dic["synapse"]:
            tk.Label(fenetre, text=synapse_name).grid(row=row, column=0, sticky="w")
            e1 = tk.Entry(fenetre, width=8)

            g_value = self.dic["synapse"][synapse_name]["params"]["g_max"]
            e1.insert(0, str(g_value))

            e1.grid(row=row, column=1)

            self.entries["stimulations"]["synapse"][synapse_name] = {"g_max": e1}
            row += 1

        def stim_confirm():
            for neuron_name in self.entries["stimulations"]["neuron"]:
                path = ["stimulations", "neuron", neuron_name]
                self.confirm(self.entries["stimulations"]["neuron"][neuron_name], path)

            for synapse_name in self.entries["stimulations"]["synapse"]:
                path = ["stimulations", "synapse", synapse_name]
                self.confirm(
                    self.entries["stimulations"]["synapse"][synapse_name], path
                )

                path = ["synapse", synapse_name, "params"]
                self.confirm(
                    self.entries["stimulations"]["synapse"][synapse_name], path
                )
            """
        def appliquer():
            for name, champs in self.entries.items():
                try:
                    if champs["type"] == "neuron":
                        I_set = float(champs["I_set"].get())
                        I_go = float(champs["I_go"].get())
                        self.dic["stimulations"]["neuron"][name] = {
                            "I_set": I_set,
                            "I_go": I_go,
                        }
                    elif champs["type"] == "synapse":
                        g_set = float(champs["g_set"].get())
                        g_go = float(champs["g_go"].get())
                        self.dic["stimulations"]["synapse"][name] = {
                            "g_set": g_set,
                            "g_go": g_go,
                        }
                        self.dic["synapse"][synapse_name]["params"]["g_max"] = g_set
                except ValueError:
                    messagebox.showerror("Erreur", f"Valeurs invalides pour '{synapse_name}'")
                    return
             """
            messagebox.showinfo(
                "Succès", "Stimulations enregistrées dans self.dic['stimulations']."
            )
            fenetre.destroy()

        tk.Button(fenetre, text="Confirm", command=stim_confirm).grid(
            row=row, column=0, columnspan=3, pady=10
        )

    def muscle(self):
        fenetre = tk.Toplevel(root)
        fenetre.title("Ajouter ou modifier un muscle")

        if "muscles" not in self.dic:
            self.dic["muscles"] = {}

        # Liste déroulante pour sélectionner un muscle existant ou nouveau
        tk.Label(fenetre, text="Muscle :").grid(row=0, column=0)
        options = ["<Nouveau>"] + list(self.dic["muscles"].keys())
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

        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(fenetre, text=label + " :").grid(row=i + 1, column=0, sticky="w")
            e = tk.Entry(fenetre)
            e.grid(row=i + 1, column=1)
            self.entries[label] = e

        def remplir_champs(*args):
            nom = var_choix.get()
            if nom != "<Nouveau>" and nom in self.dic["muscles"]:
                params = self.dic["muscles"][nom]
                self.entries["Nom"].delete(0, tk.END)
                self.entries["Nom"].insert(0, nom)
                for key in labels[1:]:
                    self.entries[key].delete(0, tk.END)
                    self.entries[key].insert(0, str(params.get(key, "")))
            else:
                for e in self.entries.values():
                    e.delete(0, tk.END)

        var_choix.trace("w", remplir_champs)

        def valider():
            try:
                nom = self.entries["Nom"].get()
                if not nom:
                    raise ValueError("Nom vide.")
                self.dic["muscle"][nom] = {}
                params = {}
                for key in labels[1:]:
                    params[key] = float(self.entries[key].get())

                self.dic["muscle"][nom]["params"] = params

                messagebox.showinfo("Succès", f"Muscle '{nom}' ajouté ou modifié.")
                fenetre.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", f"Paramètre invalide : {e}")

        tk.Button(fenetre, text="Valider", command=valider).grid(
            row=len(labels) + 1, column=0, columnspan=2, pady=10
        )

    def global_parameters(self):
        fenetre = tk.Toplevel(root)
        fenetre.title("Paramètres globaux")

        if "globals_parameters" not in self.dic:
            self.dic["globals_parameters"] = {}

        labels = [
            "dt",
            "masse_avant_bras",
            "L_avant_bras",
            "total_time",
            "I_set_t",
            "I_go_t",
            "FlxSpindle_S",
            "ExtSpindle_S",
        ]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(fenetre, text=label + " :").grid(row=i, column=0, sticky="w")
            e = tk.Entry(fenetre)
            e.grid(row=i, column=1)
            self.entries[label] = e

            # Remplir avec valeur existante si disponible
            if label in self.dic["globals_parameters"]:
                e.insert(0, str(self.dic["globals_parameters"][label]))

        def valider():
            try:
                for label in labels:
                    val = float(self.entries[label].get())
                    self.dic["globals_parameters"][label] = val

                messagebox.showinfo("Succès", "Paramètres globaux enregistrés.")
                fenetre.destroy()
            except ValueError:
                messagebox.showerror(
                    "Erreur", "Tous les champs doivent contenir des nombres."
                )

        tk.Button(fenetre, text="Valider", command=valider).grid(
            row=len(labels), column=0, columnspan=2, pady=10
        )

    def run_model(self):

        self.model = Model(dicModel=self.dic)
        self.model.init_neuromusculoskeletal_model()
        self.model.run_model()
        print("\n model run successfuly \n")


        print ("Do you want to save as csv this movement for visualization? yes = 1 ")

        choice = int(input())

        if choice==1:
            self.save_joint_angle_csv()
    
    def save_joint_angle_csv(self):
        # write to 
        print("\nHow do you want to call this csv")
        csv_name = input()

        with open('csv/'+ csv_name+ '.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['jointangle'])  # optional header
            for angle in self.model.Angle:
                writer.writerow([angle])
        
        print("\n csv file containing joint angles has been saved succesfully \n")

        
    def run_neural_model(self):
        model = Model(dicModel=self.dic)
        model.init_neural_model()
        model.run_neural_model()

    def bardisbanian_architecture(self):
        """ask json filepath"""
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
                self.dic.update(data)
            messagebox.showinfo(
                "Chargement réussi", f"Configuration chargée depuis\n{filepath}"
            )
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le fichier :\n{e}")
        """start bardisbanian procedure"""

        bardis.launch_visualizer(filepath)

if __name__ == "__main__":
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()

    hein = BuildModel()

    btn_neurone = tk.Button(frame, text="Ajouter un neurone", command=hein.neuron)
    btn_synapse = tk.Button(frame, text="Ajouter une synapse", command=hein.synapse)
    btn_architecture = tk.Button(
        frame, text="Affiche l'architecture", command=hein.display_architecture
    )
    btn_bardis_architecture = tk.Button(
        frame, text="Bardis architecutre", command=hein.bardisbanian_architecture
    )
    btn_spindle = tk.Button(frame, text="Spindle", command=hein.spindle)
    btn_save = tk.Button(frame, text="Sauvegarder", command=hein.sauvegarder_dic)
    btn_load = tk.Button(frame, text="Load model", command=hein.charger_dic)
    btn_stim = tk.Button(frame, text="Strimulations", command=hein.stims)
    btn_muscle = tk.Button(frame, text="Muscle", command=hein.muscle)
    btn_global_parameters = tk.Button(
        frame, text="global_parameters", command=hein.global_parameters
    )
    btn_mise_a_jour_post_pre = tk.Button(
        frame, text="MAJ post pre", command=hein.pre_post_update
    )
    btn_run_model = tk.Button(frame, text="run_model", command=hein.run_model)

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
    btn_bardis_architecture.grid(row=0, column=11, padx= 10)
    
    root.mainloop()
