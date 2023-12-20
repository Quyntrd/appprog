from tracemalloc import stop
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torchvision
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import os
import sys
import nltk
from nltk.tokenize import word_tokenize
from nltk import PorterStemmer
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

sys.path.insert(1, "D:/AppProgPython/appprog/Lab4")
from df_functions import make_dataframe
from preprocess import preprocess_text


def change_label(data:pd.DataFrame, rate: int) -> pd.DataFrame:
    data.dropna(inplace=True)
    labels = lambda x: 1 if x == rate else 0
    data['label'] = data['Рейтинг'].apply(labels)
    return data


def load_data(file_path: str) -> pd.DataFrame:
    data = make_dataframe(file_path)
    data = preprocess_text(data)
    return data


def vectorizer(df: pd.DataFrame) -> torch.Tensor:
    cv = CountVectorizer(max_features=10000, stop_words=stopwords.words('russian'))
    sparse_matrix = cv.fit_transform(df["Текст отзыва"]).toarray()
    return sparse_matrix


def split_data(all_data: torch.Tensor, df:pd.DataFrame) -> (torch.utils.data.Dataset,\
                                                            torch.utils.data.Dataset, torch.utils.data.Dataset, torch.utils.data.Dataset):
    text = pd.array(df["label"])
    x_train, x_test, y_train, y_test = train_test_split(all_data, text)
    return x_train, x_test, y_train, y_test


class LogisticRegression(nn.Module):
    def __init__(self):
        super(LogisticRegression, self).__init__()
        self.linear1 = nn.Linear(10000, 100)
        self.linear2 = nn.Linear(100, 10)
        self.linear3 = nn.Linear(10, 2)
        
    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        x = self.linear3(x)
        return x



    
df = load_data('D:/AppProgPython/appprog/csv/final1.csv')

changed = change_label(df, 1)
vec = vectorizer(changed)
print(split_data(vec, changed))