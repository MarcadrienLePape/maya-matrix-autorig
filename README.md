# Matrix AutoRig for Maya

**Matrix AutoRig** is an open-source autorigging framework for Autodesk Maya, designed for artists and TDs who want a fast, modular, and easily extendable rigging pipeline.
Built with flexibility in mind, this tool leverages Maya’s matrix-based transformations to create lightweight, efficient rigs without unnecessary constraints.
This work is based of the incredible teaching of Jean-Paul Tossings oover at https://polderanimation.com/.

**This uses only matrix nodes, no constraints only pure mathimatical calculations for a fast autorig!*

---

## ✨ Features

* ⚙️ **Matrix-based architecture** – Faster and cleaner rigs using Maya’s matrix nodes.
* 🧩 **Modular components** – Build custom rigs with plug-and-play modules (spine, limbs, face, etc.).
* 🚀 **Non-destructive workflow** – Easily update and rebuild rigs while preserving animation data.
* 💡 **Open and extensible** – Simple Python/MEL interface for custom extensions.
* 🧠 **Educational** – A great resource for learning advanced rigging techniques.

---

## 🧰 Requirements

* **Autodesk Maya** 2020+
* **Python 3** (ships with Maya 2022+)
* No external dependencies required

---

## 📦 Installation

1. Clone or download this repository:

   ```bash
   git clone https://github.com/yourusername/matrix-autorig.git
   ```
2. Add the folder to your Maya scripts path.
3. In Maya’s Script Editor, load the main tool:

   ```python
   import matrix_autorig
   matrix_autorig.launch()
   ```

---

## 🧑‍💻 Usage

* Open the **Matrix AutoRig** window from the shelf or via script.
* Choose the components you want (spine, arms, legs, face, etc.).
* Adjust guide placements.
* Build the rig with one click!

---

## 🤝 Contributing

Pull Requests are **welcome and encouraged**!
If you’d like to contribute:

1. Fork the repository
2. Create a new branch (`feature/your-feature-name`)
3. Submit a pull request

We welcome code improvements, new modules, bug fixes, and documentation updates.

---

## 🪪 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute it.

---

## 💬 Contact

* **Author:** [Marc-adrien LE PAPE]
* **Email:** [[marc-adrienlp@outlook.com](mailto:marc-adrienlp@outlook.com)]
* **GitHub:** [@MarcadrienLePape](https://github.com/MarcadrienLePape)

---

## ⭐ Support

If you find this useful, consider giving the repo a ⭐ — it helps others discover the project!
