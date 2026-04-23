import json
import networkx as nx


def load_model(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    G = nx.MultiDiGraph()

    # ---- Neurons ----
    for neuron in data["neuron"]:
        G.add_node(neuron, kind="neuron")

    # ---- Muscles ----
    for muscle in data["muscle"]:
        G.add_node(muscle, kind="muscle")

    # ---- Spindles (children of muscles) ----
    for spindle in data["spindle"]:
        muscle = spindle[0:3] + "Muscle" #Add muscle to Ext or Flx
        G.add_node(spindle, kind="spindle", parent=muscle)

    # ---- Synapses ----
    for syn_name, syn_data in data["synapse"].items():
        pre, post = syn_name.split("_")
        excitatory = syn_data["params"]["Veq"] >= -15
        weight = syn_data["params"]["g_max"]

        G.add_edge(
            pre,
            post,
            kind="synapse",
            excitatory=excitatory,
            weight=weight
        )

    # ---- Muscle links ----
    for muscle, mdata in data["muscle"].items():
        pre = mdata["neuron_pre"]
        G.add_edge(pre, muscle, kind="muscle_link")

    return G


def export_to_cytoscape(G, out_file="graph.json"):
    elements = []

    # ---- Nodes ----
    for node, data in G.nodes(data=True):
        el = {
            "data": {
                "id": node,
                "kind": data["kind"]
            }
        }
        if "parent" in data:
            el["data"]["parent"] = data["parent"]
        elements.append(el)

    # ---- Edges ----
    for u, v, k, data in G.edges(keys=True, data=True):
        elements.append({
            "data": {
                "id": f"{u}_{v}_{k}",
                "source": u,
                "target": v,
                "kind": data["kind"],
                "weight": data.get("weight", 1),
                "excitatory": data.get("excitatory", True)
            }
        })

    with open(out_file, "w") as f:
        json.dump({"elements": elements}, f, indent=2)


if __name__ == "__main__":
    G = load_model("V1.json")
    export_to_cytoscape(G)
    print("✔ graph.json generated")
