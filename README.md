# Merkle-tree-visualizer
An interactive tool for creating, visualizing, and exploring Merkle Trees using Python and PySide6.

Description
This Merkle Tree Visualizer is an educational tool that allows users to create, modify, and visualize Merkle Trees through an intuitive graphical interface. Built with Python and leveraging PySide6 for the GUI and Matplotlib for visualization, this application provides a hands-on way to understand the structure and properties of Merkle Trees.

Features:
  Interactive Visualization: Dynamically create and visualize Merkle Trees.
  Add/Remove Data: Easily add new data blocks or remove existing ones from the tree.
  JSON Import: Load pre-existing Merkle Tree data from JSON files.
  Step-by-Step Explanation: Walk through the Merkle Tree construction process with highlighted nodes and explanations.
  Pan and Zoom: Navigate large trees with pan and zoom functionality.
  Root Hash Display: Always see the current Merkle root hash.

Technical Details:
  Language: Python
  GUI Framework: PySide6, Qt designer
  Visualization: Matplotlib
  Graph Handling: NetworkX

How It Works:
  Data Input: Users can manually add or load data blocks from a JSON file. To load data press File > Load Tree
  Tree Construction: The application constructs the Merkle Tree using SHA-256 hashing.
  Visualization: The tree is rendered using Matplotlib, with nodes showing data and partial hashes.
  Interaction: Users can add/remove data, triggering automatic tree reconstruction and visualization updates. Adding data requires the user to input a data block(example: "Leo") which will be added to the tree. Removing data requires the user to input the data block he wishes to remove(example: "Leo")
  Explanation Mode: Step through the tree construction process with highlighted nodes and descriptive text. To enable explanation mode pressing on the "Explain" button is required.

Getting Started:
  To run the program download the repository and extract files to any folder.
  Run the executable file in the "dist" folder.

Recommendations:
  Use Windows 10 for the best experience. Windows 11 gives GUI issues.
