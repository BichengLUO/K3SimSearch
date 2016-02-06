![K3SimSearch](./k3simsearch.png)
K3SimSearch
==================
[中文](./README_zh.md)

K3SimSearch is a simple Python script as a dictionary in which you can look up a GRE word and find its similar words (**not synonyms but visual similarity**). It works as a small tool for helping students to prepare for GRE.

[![asciicast](https://asciinema.org/a/35666.png)](https://asciinema.org/a/35666)

**Example**

After typing `python K3SimSearch.py` in the working directory in which `K3SimSearch.py` is located and waiting for several minutes for loading cache, you will get this in your console:

```
Dictionary loaded!
Start reading matrix from local cache...
Reading matrix done!
Matrix established!
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
We can't find caramity in the dictionary
Are you looking for calamity?
[0] calamity
大灾难：disastrous event
-----------------------------------
[2] clarity
清晰，清楚：clear, lucidity; 清澈透明:easily seen through
-----------------------------------
```
The script will retrieve `calamity` as the word you're looking for.
