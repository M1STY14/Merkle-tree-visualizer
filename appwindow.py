import sys
import json
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from merkle_tree import MerkleTree
from ui_merkle_tree import Ui_MainWindow

app = QApplication(sys.argv)
screen = app.primaryScreen()
screenGeometry = screen.geometry()
screenWidth = screenGeometry.width()
screenHeight = screenGeometry.height()

# window settings
windowWidth = 1000
windowHeight = 700


class MerkleTreeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.central_widget = self.findChild(QWidget, "centralwidget")
        self.setWindowTitle("Merkle Tree Visualizer")
        self.setGeometry((screenWidth - windowWidth) / 2,
                         (screenHeight - windowHeight) / 2,
                         windowWidth,
                         windowHeight)

        self.merkle_tree = MerkleTree()
        self.initUI()

        # Varijable omogucavanje pomjeranja 
        self.pan_start_x = None
        self.pan_start_y = None
        self.axes = None

        # Varijabla za zumiranje
        self.zoom_scale = 1.1

        # Varijable za objasnjenja
        self.explanation_steps = []
        self.current_step = -1  # -1 jer nije aktivno
        self.highlighted_nodes = set()
        self.explanations = [
            "First, hash each data block to create the leaf nodes.",
            "Next, we combine pairs of sibling nodes(marked in purple) and hashing them to get a parent node(marked in yellow).",
            "Finally, after combining and hashing the last two nodes(the children of the root) we get the Merkle root: {}",
            "Tree has only 1 node so after hashing it we get Merkle root of: {}"
        ]

    def initUI(self):
        # GUI
        self.canvas_placeholder = self.ui.canvas_placeholder
        self.load_button = self.ui.menuLoad_tree
        self.input_box = self.ui.input_box
        self.add_button = self.ui.add_button
        self.input_box_remove = self.ui.input_box_remove
        self.remove_button = self.ui.remove_button
        self.explain_button = self.ui.explain_button
        self.explanation_box = self.ui.explanation_text
        self.next_button = self.ui.next_button
        self.prev_button = self.ui.prev_button
        # explain
        self.explain_button.clicked.connect(self.start_explanation)
        self.next_button.clicked.connect(self.next_explanation_step)
        self.prev_button.clicked.connect(self.prev_explanation_step)
        # Mathplotlib canvas
        self.canvas = FigureCanvas()
        canvas_layout = QVBoxLayout(self.canvas_placeholder)
        canvas_layout.addWidget(self.canvas)
        self.canvas_placeholder.setLayout(canvas_layout)
        # Add i remove button povezivanje
        self.add_button.clicked.connect(self.add_data)
        self.remove_button.clicked.connect(self.remove_data)

        self.update_merkle_root()
        self.visualize_tree()

        # Dogadaji za pomicanje i zumiranje
        self.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        self.canvas.mpl_connect('scroll_event', self.on_mouse_wheel)

        # Load data button u meniu
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        load_action = file_menu.addAction("Load Tree")
        load_action.triggered.connect(self.load_data_from_json)

        # Prikazivanje root hash-a u explain box-u
        root_hash = self.merkle_tree.get_root()
        self.explanation_box.setText(f"Root hash: {root_hash}" if root_hash else "Merkle root: None")

    def on_mouse_press(self, event):
        if event.inaxes:
            self.pan_start_x = event.xdata
            self.pan_start_y = event.ydata
            self.axes = event.inaxes

    def on_mouse_move(self, event):
        if event.inaxes and self.pan_start_x is not None and self.pan_start_y is not None:
            dx = event.xdata - self.pan_start_x
            dy = event.ydata - self.pan_start_y
            self.axes.set_xlim([self.axes.get_xlim()[0] - dx, self.axes.get_xlim()[1] - dx])
            self.axes.set_ylim([self.axes.get_ylim()[0] - dy, self.axes.get_ylim()[1] - dy])
            self.canvas.draw_idle()

    def on_mouse_release(self, event):
        self.pan_start_x = None
        self.pan_start_y = None
        self.axes = None

    def on_mouse_wheel(self, event):
        if event.inaxes:
            ax = event.inaxes
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            # xdata i ydata lokacije misa
            xdata = event.xdata
            ydata = event.ydata
            # up - zoom in, down - zoom out
            if event.button == 'up':
                scale_factor = 1 / self.zoom_scale
            elif event.button == 'down':
                scale_factor = self.zoom_scale
            else:
                scale_factor = 1

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

            ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * (relx)])
            ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * (rely)])
            self.canvas.draw_idle()

    """
    Ucitavanje podataka iz JSON file-a.
    """
    def load_data_from_json(self):
        file_path, _ = QFileDialog.getOpenFileName(self,
            "Open JSON File",
            "",
            "JSON Files (*.json)")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                data_blocks = data.get("data_blocks", [])
                if not isinstance(data_blocks, list):
                    raise ValueError("Invalid JSON format: 'data_blocks' must be a list.")
                self.merkle_tree = MerkleTree()
                for block in data_blocks:
                    self.merkle_tree.add_data(block)
                self.update_merkle_root()
                self.visualize_tree()
            except (json.JSONDecodeError, ValueError) as e:
                self.explanation_box.setText(f"Error loading JSON: {e}")

    """
    Uklanjanje podataka iz Merkle stabla.
    """
    def remove_data(self):
        if not self.merkle_tree.tree:
            self.explanation_box.setText("Merkle root: Tree is empty!")
            return

        data_to_remove = self.input_box_remove.text()
        try:
            index_to_remove = None
            for i, data in enumerate(self.merkle_tree.data_blocks):
                # kada se nadje data za uklanjanje, break
                if data == data_to_remove:
                    index_to_remove = i
                    break

            if index_to_remove is not None:
                self.merkle_tree.remove_data(index_to_remove)
                self.update_merkle_root()
                self.visualize_tree()
            else:
                QMessageBox.warning(self, "Data Not Found", f"Data '{data_to_remove}' not found in the tree.")
                self.explanation_box.setText(f"Data '{data_to_remove}' not found in the tree.")

        except ValueError:
            self.explanation_box.setText("Invalid input.")

    def add_data(self):
        user_input = self.input_box.text()
        self.merkle_tree.add_data(user_input)
        self.visualize_tree()
        self.update_merkle_root()

    def visualize_tree(self, highlighted_nodes=None, highlighted_children=None):
        if not self.merkle_tree.tree:
            self.explanation_box.setText("Merkle root: Tree is empty!")
            return

        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.margins(0.1)
        self.merkle_tree.visualize(ax, highlighted_nodes=highlighted_nodes,
                                   highlighted_children=highlighted_children)
        self.canvas.figure.tight_layout()
        self.canvas.draw()

    def update_merkle_root(self):
        root = self.merkle_tree.get_root()
        self.explanation_box.setText(f"Root hash: {root}" if root else "Merkle root: None")

    def start_explanation(self):
        if not self.merkle_tree.tree:
            self.explanation_box.setText("No tree to explain.")
            return

        self.current_step = 0
        self.update_explanation()
        self.prev_button.setEnabled(False)
        if len(self.merkle_tree.data_blocks) == 1:
            self.next_button.setEnabled(False)
        else:
            self.next_button.setEnabled(True)

    def next_explanation_step(self):
        if self.current_step < len(self.merkle_tree.tree) - 1:
            self.current_step += 1
            self.update_explanation()
            self.prev_button.setEnabled(True)
        if self.current_step == len(self.merkle_tree.tree) - 1:
            self.next_button.setEnabled(False)

    def prev_explanation_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_explanation()
            self.next_button.setEnabled(True)
        if self.current_step == 0:
            self.prev_button.setEnabled(False)

    def update_explanation(self):
        tree = self.merkle_tree.tree
        data_blocks = self.merkle_tree.data_blocks
        # za oznacavanje cvorova - roditelja i djece
        self.highlighted_nodes = set()
        self.highlighted_children = set()
        level_index = self.current_step
        number_of_nodes_on_level = len(tree[level_index]) if level_index < len(tree) else 0

        # u slucaju 1 cvora
        if len(data_blocks) == 1:
            root_hash = self.merkle_tree.get_root()
            self.highlighted_nodes.add("L0_N0")
            self.explanation_box.setText(self.explanations[3].format(root_hash))
        else:
            level_index = self.current_step
            number_of_nodes_on_level = len(tree[level_index]) if level_index < len(tree) else 0

            if self.current_step == 0:
                for i in range(len(data_blocks)):
                    node_name = f"L{0}_N{i}"
                    self.highlighted_nodes.add(f"L{0}_N{i}")
                self.explanation_box.setText(self.explanations[0])

            elif 0 < self.current_step < len(tree) - 1:
                # oznacavanje cvorova koji nisu na nivou listova
                for i in range(number_of_nodes_on_level):
                    node_name = f"L{level_index}_N{i}"
                    self.highlighted_nodes.add(node_name)

                    # oznacavanje djece cvorova
                    child_level_index = level_index - 1
                    child_1_index = i * 2
                    child_2_index = i * 2 + 1

                    if child_level_index >= 0:

                        child_1_name = f"L{child_level_index}_N{child_1_index}"
                        self.highlighted_children.add(child_1_name)

                        if child_2_index < len(tree[child_level_index]):
                            child_2_name = f"L{child_level_index}_N{child_2_index}"
                            self.highlighted_children.add(child_2_name)

                self.explanation_box.setText(self.explanations[1])

            elif self.current_step == len(tree) - 1:
                # Oznacavanje root-a u zadnjem koraku
                root_hash = self.merkle_tree.get_root()
                for i in range(number_of_nodes_on_level):
                    node_name = f"L{len(tree) - 1}_N{0}"
                    self.highlighted_nodes.add(node_name)

                    child_level_index = level_index - 1
                    child_1_index = i * 2
                    child_2_index = i * 2 + 1

                    if child_level_index >= 0:

                        child_1_name = f"L{child_level_index}_N{child_1_index}"
                        self.highlighted_children.add(child_1_name)

                        if child_2_index < len(tree[child_level_index]):
                            child_2_name = f"L{child_level_index}_N{child_2_index}"
                            self.highlighted_children.add(child_2_name)

                    self.explanation_box.setText(self.explanations[2].format(root_hash))

        self.visualize_tree(highlighted_nodes=self.highlighted_nodes,
                            highlighted_children=self.highlighted_children)


# window aplikacije
if __name__ == "__main__":
    window = MerkleTreeApp()
    window.show()
    sys.exit(app.exec())
