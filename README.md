K3SimSearch
==================

K3SimSearch is a simple Python script as a dictionaray in which you can look up a GRE word and find its similar words (**not synonyms but visiually similarity**). It works as a small tool for helping students to prepare for GRE.

>**Example**
>
>After typing `python K3SimSearch.py` in the working directory in which `K3SimSearch.py` is located and waiting for several minutes for loading cache, you will get this in your console:
>
```
Dictionary loaded!
Start reading matrix from local cache...
Reading matrix done!
Matrix established!
Enter the word:
```
>
>Enter such word as `feckless` to find its definitions and similar words:
>
```
Enter the word: feckless
[0] feckless
无成果的，没有价值的：having no worth；粗心不负责任的：careless
-----------------------------------
[1] reckless
不考虑后果的，大胆鲁莽的：careless
-----------------------------------
```
>If you made a typo in your word, it's all right for the script to find the most similar word from our dictionary. Try enter `caramity`:
>
```
Enter the word: caramity
[0] calamity
大灾难：disastrous event
-----------------------------------
[2] clarity
清晰，清楚：clear, lucidity; 清澈透明:easily seen through
-----------------------------------
```
>The script will retrieve `calamity` as the word you're looking for.

K3SimSearch
==================

K3SimSearch是用来帮助查找和搜索外形相近（**不是释义相近**）的GRE单词的一段简单Python脚本。它可以作为GRE备考小工具，帮助你更好地记忆单词。

>**Example**
>
>在`K3SimSearch.py`所在目录下的控制台输入`python K3SimSearch.py`来运行这段脚本。耐心等待数秒，编辑距离缓存加载完毕以后，你将看到如下控制台提示：
>
```
Dictionary loaded!
Start reading matrix from local cache...
Reading matrix done!
Matrix established!
Enter the word:
```
>
>你可以查询任意一个单词，例如`feckless`：
>
```
Enter the word: feckless
[0] feckless
无成果的，没有价值的：having no worth；粗心不负责任的：careless
-----------------------------------
[1] reckless
不考虑后果的，大胆鲁莽的：careless
-----------------------------------
```
>如果你查询单词时候，出现了细微的拼写错误，我们的脚本将会返回给你最相近的词条解释。例如，我们输入`caramity`:
>
```
Enter the word: caramity
[0] calamity
大灾难：disastrous event
-----------------------------------
[2] clarity
清晰，清楚：clear, lucidity; 清澈透明:easily seen through
-----------------------------------
```
>脚本在搜索不到`caramity`这个单词的同时，会返回一个最接近的单词`calamity`，并以这个单词作为你要查询的单词进行相似性搜索。