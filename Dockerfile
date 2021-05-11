FROM python:3.8.2

ADD main.py .
ADD swear_words.txt .
ADD word2vec.model .
ADD word2vec.model.trainables.syn1neg.npy .
ADD word2vec.model.wv.vectors.npy .

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "./main.py"]