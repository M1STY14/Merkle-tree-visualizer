import hashlib

import networkx as nx

def hash_function(data):
    # hashanje podataka, potrebno encodiranje
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def construct_merkle_tree(data_blocks):
    # izrada leafova, hashanje svakog bloka
    leaf_nodes = [hash_function(block) for block in data_blocks]

    # pocetak stabla sa listovima
    # Alice(hash), Bob(hash), Charlie(hash), David(hash), A + B(hash), C + D(hash), root(hash)
    tree = [leaf_nodes]

    # pocetak
    current_level = leaf_nodes

    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            # provjera parova
            if i + 1 < len(current_level):
                sum_hash = hash_function(current_level[i] +
                                         current_level[i + 1])
            # ako je neparno, hashaj zadnji leaf sa samim sobom
            else:
                sum_hash = hash_function(current_level[i] +
                                         current_level[i])
            next_level.append(sum_hash)
        # dodavanje razine stablu
        tree.append(next_level)
        current_level = next_level

    # povrat stabla
    return tree

def get_proof(tree, position):
    proof = []
    for level in tree[:-1]:  # preskoci root razinu
        # XOR, koristi se za pronalazak siblinga na istom nivou
        sibling_position = position ^ 1
        if sibling_position < len(level):
            proof.append(level[sibling_position])
        # pozicija roditelja
        # integer division of position by 2
        position //= 2
    return proof

class MerkleTree:
    def __init__(self):
        self.data_blocks = []
        self.tree = []

    def add_data(self, data):
        self.data_blocks.append(data)
        self.tree = construct_merkle_tree(self.data_blocks)

    def remove_data(self, position):
        # ne smije biti negativna pozicija
        if 0 <= position < len(self.data_blocks):
            self.data_blocks.pop(position)
            self.tree = construct_merkle_tree(self.data_blocks)

    def get_root(self):
        # [-1][0] pozicija roota
        return self.tree[-1][0] if self.tree else None

    def get_proof(self, position):
        if position < len(self.data_blocks):
            return get_proof(self.tree, position)
        else:
            return ValueError("Wrong index!")

    def visualize(self, ax, highlighted_nodes=None, highlighted_children=None):
        if not self.tree:
            raise ValueError("The Merkle tree is empty.")

        G = nx.DiGraph()  # usmjereni graf
        pos = {}  # pozicije cvorova
        y_offset = 0  # vertikalni pomak izmedu razina

        # dodavanje cvorova i bridova
        for level_index, level in enumerate(reversed(self.tree)):  # reversed jer se pocinje od dna
            x_offset = -len(level) / 2  # Horizontal alignment of nodes

            for i, hash_value in enumerate(level):
                node_name = f"L{len(self.tree) - 1 - level_index}_N{i}"  # Node name includes level

                # prikaz podataka za listove
                if level_index == len(self.tree) - 1:  # Leaf level
                    data = self.data_blocks[i] if i < len(self.data_blocks) else "(dup)"
                    label = f"{data} ({hash_value[:8]})"  # data + skraceni hash value

                else:
                    label = hash_value[:8]  # prikaz samo hasheva za cvorove koji nisu root ili leafs

                G.add_node(node_name, label=label)
                pos[node_name] = (x_offset + i, y_offset)

                if highlighted_nodes and node_name in highlighted_nodes:
                    #  Crtanje pravokutnika za oznavanje cvorova u zutu
                    bbox_props = dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.5)
                    ax.text(pos[node_name][0], pos[node_name][1], label, bbox=bbox_props, ha='center', va='center', fontsize=10)

                elif highlighted_children and node_name in highlighted_children:
                    # Crtanje pravokutnika iza teksta cvora u ljubicastu
                    bbox_props = dict(boxstyle="round,pad=0.3", facecolor="purple", alpha=0.5)
                    ax.text(pos[node_name][0], pos[node_name][1], label, bbox=bbox_props, ha='center', va='center', fontsize=10)

                else:
                    ax.text(pos[node_name][0], pos[node_name][1], label, ha='center', va='center', fontsize=10)

                # Ako je neparan broj listova, napraviti da je zadnji list duplikat
                if level_index == len(self.tree) - 1 and i == len(level) - 1 and len(level) % 2 != 0:
                    # u slucaju da je jedan podatak
                    # koji je tehnicki root
                    # ne treba napraviti duplikat
                    if len(level) == 1:
                        continue

                    duplicate_name = f"{node_name}_dup"
                    duplicate_data = data
                    G.add_node(duplicate_name, label=f"{duplicate_data} ({hash_value[:8]})(dup)")
                    # pozicija duplikata
                    pos[duplicate_name] = (x_offset + len(level), y_offset)

                    # dodaj brid duplikata istom roditelju kao i originalan
                    if level_index > 0:  # provjera ako postoji parent razina
                        parent_index = i // 2
                        parent_name = f"L{len(self.tree) - level_index}_N{parent_index}"
                        G.add_edge(duplicate_name, parent_name)

                # povezivanje trenutnog cvora s roditeljem
                if level_index > 0:
                    parent_index = i // 2
                    parent_name = f"L{len(self.tree) - level_index}_N{parent_index}"
                    G.add_edge(node_name, parent_name)  # originalni child usmjerava prema roditelju

            y_offset -= 1  # prelazak na novu razinu

            # Crtanje grafa
            nx.draw(G, pos, with_labels=True,
                    labels=nx.get_node_attributes(G, 'label'),
                    node_size=2000, font_size=10, ax=ax)

            min_x = min(x for x, y in pos.values())
            max_x = max(x for x, y in pos.values())
            ax.set_xlim(min_x - 0.5, max_x + 0.5)
