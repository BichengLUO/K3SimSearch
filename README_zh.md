# ![K3SimSearch](./k3simsearch.png) K3SimSearch

[English](./README.md)

K3SimSearch是用来帮助查找和搜索外形相近（**不是释义相近**）的GRE单词的一段简单Python脚本。它可以作为GRE备考小工具，帮助你更好地记忆单词。

[![asciicast](https://asciinema.org/a/35666.png)](https://asciinema.org/a/35666)

**示例**

在`K3SimSearch.py`所在目录下的控制台输入`python K3SimSearch.py`来运行这段脚本。耐心等待数秒，编辑距离缓存加载完毕以后，你将看到如下控制台提示：

```
[Info] Dictionary loaded!
[Info] Start reading matrix from local cache...
[Info] Reading matrix done!
[Info] Matrix established!
Enter the word:
```

你可以查询任意一个单词，例如`feckless`：

```
Enter the word: feckless
============= Visually Similar ===============

feckless,  reckless

Press Enter to show definitions...
```
显示了这个以后，你可以花几秒钟回忆一下这些视觉上相似的单词的意思分别是什么，然后按回车来显示他们的释义。如下面所示：
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
如果你查询单词时候，出现了细微的拼写错误，我们的脚本将会返回给你最相近的词条解释。例如，我们输入`caramity`:

```
Enter the word: caramity
[Error] We can't find caramity in the dictionary
[Info] Are you looking for calamity?
============= Visually Similar ===============

calamity,  clarity

Press Enter to show definitions...
```
脚本在搜索不到`caramity`这个单词的同时，会返回一个最接近的单词`calamity`，并以这个单词作为你要查询的单词进行相似性搜索。
