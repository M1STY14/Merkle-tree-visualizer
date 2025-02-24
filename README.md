# Merkle tree visualizer
An interactive tool for creating, visualizing, and exploring Merkle Trees using Python and PySide6.

Description:<br/>
This Merkle tree visualizer is an educational tool that allows users to create, modify, and visualize Merkle Trees through an intuitive graphical interface. Built with Python and leveraging PySide6 for the GUI and Matplotlib for visualization, this application provides a hands-on way to understand the structure and properties of Merkle Trees.

Features:<br/>
  Interactive visualization: Dynamically create and visualize Merkle Trees.<br/>
  Add/Remove data: Easily add new data blocks or remove existing ones from the tree.<br/>
  JSON import: Load pre-existing Merkle Tree data from JSON files.<br/>
  Step-by-Step Explanation: Walk through the Merkle Tree construction process with highlighted nodes and explanations.<br/>
  Pan and zoom: Navigate large trees with pan and zoom functionality.<br/>
  Root hash display: Always see the current Merkle root hash.<br/>

Technical Details:<br/>
  Language: Python<br/>
  GUI framework: PySide6, Qt designer<br/>
  Visualization: Matplotlib<br/>
  Graph handling: NetworkX<br/>

How it works:<br/>
  Data input: Users can manually add or load data blocks from a JSON file. To load data press File > Load Tree<br/>
  Tree construction: The application constructs the Merkle Tree using SHA-256 hashing.<br/>
  Visualization: The tree is rendered using Matplotlib, with nodes showing data and partial hashes.<br/>
  Interaction: Users can add/remove data, triggering automatic tree reconstruction and visualization updates. Adding data requires the user to input a data block(example: "Leo") which will be added to the tree. Removing data requires the user to input the data block he wishes to remove(example: "Leo")<br/>
  Explanation mode: Step through the tree construction process with highlighted nodes and descriptive text. To enable explanation mode pressing on the "Explain" button is required.<br/>

Running the program:<br/>
  To run the program download the repository and extract files to any folder.<br/>
  Run the executable file in the "dist" folder.<br/>

Recommendations:<br/>
  Use Windows 10 for the best experience. Windows 11 gives GUI issues.
