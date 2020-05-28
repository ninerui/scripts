# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import pandas as pd
from tqdm import tqdm

train_df = pd.read_csv(r'D:\data\61\data\train.csv')
test_df = pd.read_csv(r'D:\data\61\data\test.csv')

from textrank4zh import TextRank4Sentence

texts = test_df['article'].values
res = []

for text in tqdm(texts):
    text = text.replace('<Paragraph>', ' ')
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source='no_stop_words')
    key_sentences = tr4s.get_key_sentences(num=1, sentence_min_len=20)
    res.append(key_sentences[0]['sentence'])

sub = pd.DataFrame()
sub['sum'] = res
sub.head()

sub.to_csv('sub.csv', header=None)
