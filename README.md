# :white_check_mark: :underage: **Swear words filter**

![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

A filter using for recognizing swear words and their various variations. When a word is found, it replaces all word with *.

The algorithm is divided into several stages: 

1. Checking text by regular expressions and difflib library to find obvious swear words and replace them. <br />
Not obvious words go next.
2. If word from current list of swear words is in word2vec model, it is checked by word2vec similarity function. <br />
3. If word from current list of swear words is **NOT** in word2vec model, the word is checked by the Levenshtein distance and token_sort_ratio function from FuzzyWuzzy library. <br />

:file_folder: Word2Vec model was trained on old datasets of negative and positive reviews of movies, series, anime from [Kaggle](https://www.kaggle.com/).
<br />
___

## :tv: **Demo**:
___

## :scroll: **Project stack**:

### **Filter Part**:
+ Python
+ Gensim
+ Word2Vec NLP model
+ FuzzyWuzzy and different metrics 
+ Difflib
+ NumPy
+ Pandas
+ RegExp
### **Web Part**:
+ Flask

### **Deploy**:
+ Docker

___

## :rocket: **Installation**

### :warning: You need Docker to start project easily! 

Run command that will create docker build:

```shell
docker build -t <your build name> . 
```
Then you can start created docker and open it in browser at http://localhost:5000/
```shell
docker run -p 5000:5000 <your build name>
```
