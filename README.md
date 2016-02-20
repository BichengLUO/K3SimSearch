[![Build Status](https://travis-ci.org/BichengLUO/K3SimSearch.svg?branch=master)](https://travis-ci.org/BichengLUO/K3SimSearch)
# ![K3SimSearch](./k3simsearch.png) K3SimSearch

[中文](./README_zh.md)

K3SimSearch is a simple Python script as a dictionary in which you can look up a GRE word and find its similar words (**not synonyms but visual similarity**). It works as a small tool for helping students to prepare for GRE.

<a href="https://asciinema.org/a/36899" target="_blank"><img src="https://asciinema.org/a/36899.png" width="589" /></a>

**Example**

After typing `python K3SimSearch.py` in the working directory in which `K3SimSearch.py` is located and waiting for several minutes for loading cache, you will get this in your console:

```
[Info] Dictionary loaded!
[Info] Start reading matrix from local cache...
[Info] Reading matrix done!
[Info] Matrix established!
Enter the word:
```

Enter such word as `feckless` to find its definitions and similar words:

```
Enter the word: feckless
============= Visually Similar ===============

feckless,  reckless

Press Enter to show definitions...
```
After showing that, you have a chance to do an exercise to review these visually similar words and to press Enter to show their definitions.
```
Press Enter to show definitions...
=============== Definitions ==================
[0] feckless
无成果的，没有价值的：having no worth；粗心不负责任的：careless
-----------------------------------
[1] reckless
不考虑后果的，大胆鲁莽的：careless
-----------------------------------
```
If you made a typo in your word, it's all right for the script to find the most similar word from our dictionary. Try enter `caramity`:

```
Enter the word: caramity
[Error] We can't find caramity in the dictionary
[Info] Are you looking for calamity?
============= Visually Similar ===============

calamity,  clarity

Press Enter to show definitions...
```
The script will retrieve `calamity` as the word you're looking for.

K3GraphGen
------------
`K3GraphGen.py` is a piece of script for generating [GEXF](https://gephi.org/gexf/format/) file of GRE words according to their visual similarity. In order to open GEXF, you should install Gephi. [Gephi](https://gephi.org/) is an open source tool for visualizing big graph and doing a lot of other things about graph.

After importing GEXF file to Gephi, we can visualize the graph of words in different layouts. Furthermore, we also provided a GEPHI file (`k3.gephi`) which acts as the project file of Gephi to see the graph more clearly.

![k3.gephi](./k3.gif)
