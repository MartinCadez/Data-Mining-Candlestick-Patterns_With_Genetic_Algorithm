[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Not Financial Advice](https://img.shields.io/badge/Not_Financial_Advice-Important-red)](https://www.youtube.com/watch?v=CXrD4rAHZyE)
[![Python Compatibility](https://img.shields.io/badge/Python-3.6%2B-blue)](https://www.python.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

<!-- I will add this one when I the badge is ready -->
<!-- [![PyGAD](https://img.shields.io/badge/genetic-algorithm-pygad-blue)](https://pygad.readthedocs.io/en/stable/) -->

# [![Genetic-algo-photo-1.png](https://i.postimg.cc/Y2nxWK01/Genetic-algo-photo-1.png)](https://postimg.cc/0rSST4pQ)

<div align="center">
<h2>🧬 Data Mining Candlestick Patterns With Genetic Algorithm 🧬</h2>
</div>

_Project aims to discover and refine candlestick patterns within financial datasets using a genetic algorithm, with the approach designed to be applicable across various markets._

**🔴 Disclaimer:** This project is for research purposes only and should not be considered financial advice.

- **What is candlestick pattern?** <br>
  It's charting method encapsulating open, high, low, and close prices of a security or asset over a specific period.<br>

  - 📑 You can find more [here](https://www.investopedia.com/articles/active-trading/092315/5-most-powerful-candlestick-patterns.asp)

- **How does genetics algorithm work?** <br>
  It's an optimization technique inspired by natural selection. It evolves a population over multiple generations by applying selection, crossover, and mutation operations to find the best solution to a problem. <br>
  - 📑 Link to wikipedia [here](https://www.wikiwand.com/en/articles/Genetic_algorithm) <br>
  - 📚 Detailed explanation about operational mechanics of genetic algorithms is covered from pages 7 to 22 in the book by David E. Goldberg, [Genetic Algorithms in Search, Optimization, and Machine Learning](http://www2.fiit.stuba.sk/~kvasnicka/Free%20books/Goldberg_Genetic_Algorithms_in_Search.pdf)

## 🛠️ Setup Guide

This guide outlines the steps to configure the project on your local machine. Before you begin, ensure you have the following installed and correctly added to your system's environment paths:

- 📋**Pre-requisites:**

  - [Git 2.20+](https://git-scm.com/downloads)
  - [Python 3.6+](https://www.python.org/downloads/)

- 📥**Clone the Repository**

  ```bash
  git clone https://github.com/MartinCadez/Data-Mining-Candlestick-Patterns-With-Genetic-Algorithm.git
  ```

- 🔧 **Environment Configuration**

1. **Setup Virtual Environment** (Command Prompt or Terminal) :

   - 🌱*Create the environment* :
     ```bash
     python -m venv Py312_GA_env
     ```
   - ⚡*Activate* : <br>
     On Windows :
     ```bash
     Py312_GA_env\Scripts\activate
     ```
     On Linux/macOS :
     ```bash
     source Py312_GA_env/bin/activate
     ```
   - 📦*Install Required Dependencies* :
     ```bash
     pip install -r requirements.txt
     ```

2. **Anaconda/Miniconda Environment Setup** (Anaconda Prompt or Terminal) :
   - 🌱*Set Up Environment and Install Dependencies* :
     ```bash
     conda env create -f environment.yml
     ```
   - 💥*Mamba users* :
     ```bash
     mamba env create -f environment.yml
     ```
   - ⚡*Activate conda Environment* :
     ```bash
     conda activate Py312_GA_env
     ```

## 🔍 Project Features

Learn about the unique aspects of this project and how they benefit its functionality. <br>

- **Candlestick Patterns Generator**
  - 📊 Need to update
- **Evaluation of Candlestick Pattern**
  - 📊 Need to update
- **Genetic Algorithm for Data Mining Candlestick Patterns**
  - 📊 Need to update
- **Example of Use on Bitcoin Dataset**
  - 📊 Need to update

## 📈 How to Use

- 📊 Need to update
  Run from the main file in project directory. Use yaml file to configure the genetic algorithm parameters.
  ```bash
  python main.py
  ```

## 💡 Discussion & Contributions

Contributions from the community are highly appreciated, especially as the project seeks to advance the analytical methods used in trading research. Pull requests are welcome if you identify opportunities for improvement in areas such as:

- 🖋️**Code Enhancements**: Optimizing or refactoring code to improve performance and readability.
- 🐛**Bug Fixes**: Identifying and resolving issues to increase the project's stability.
- ✨**Feature Development**: Proposing and implementing new features that align with the project’s objectives.
- 📄**Documentation**: Improving documentation to ensure clarity and comprehensiveness.

Your ideas and alternative solutions are also valued. For any questions or to discuss contributions, feel free to contact me via email at [martin.cadez0@gmail.com](mailto:martin.cadez0@gmail.com).

## 🏆 Acknowledgments & Credits

- **Neurotrader** : Youtube video [Data Mining Candlestick Patterns With a Genetic Algorithm](https://www.youtube.com/watch?v=2XQ3PsZActM) from his channel inspired the development of this project. For more of his work, visit [Neurotrader's GitHub](https://github.com/neurotrader888).

- **Ahmed Gad** : His PyGAD library was essential for implementing genetic algorithm. For more information, visit the [PyGAD Documentation](https://pygad.readthedocs.io/en/stable/).

- **David E. Goldberg** : His book _[Genetic Algorithms in Search, Optimization, and Machine Learning](https://archive.org/details/geneticalgorithm0000gold/page/420/mode/2up)_ (1989) was crucial in broadening my understanding of genetic algorithms and their applications.

- **Murray A. Ruggiero, Jr.** : His seminal work, _[Cybernetic Trading Strategies: Developing a Profitable Trading System with State-of-the-Art Technologies](https://archive.org/details/cybernetictradin0000rugg/page/n5/mode/2up)_ (1997, Wiley), has been a cornerstone in understanding the intersection of genetics algorithms and trading systems.
