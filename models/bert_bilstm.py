# -*- coding: utf-8 -*-
# file: BERT_SPC.py
# author: songyouwei <youwei0314@gmail.com>
# Copyright (C) 2019. All Rights Reserved.
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
from torchtext import data


from layers.squeeze_embedding import SqueezeEmbedding
from pytorch_pretrained_bert import BertModel, BertForSequenceClassification, BertForNextSentencePrediction, \
    BertForPreTraining


class BERT_BiLSTM(nn.Module):
    def __init__(self, lstm_opt, bert_opt, variant='bert-base-uncased'):
        #TODO: need to pass in the parameters here
        super(BERT_BiLSTM, self).__init__()

        # BERT layers
        self.bert = BertModel.from_pretrained(variant)
        self.bert_dropout = nn.Dropout(bert_opt.dropout)

        # LSTM layers
        self.use_gpu = lstm_opt['use_gpu']
        self.batch_size = lstm_opt['batch_size']
        self.lstm_dropout = lstm_opt['dropout']
        vectors = self.load_embeddings(lstm_opt)
        self.embeddings = nn.Embedding(lstm_opt['vocab_size'], lstm_opt['embedding_dim'])
        self.bilstm = nn.LSTM(input_size=lstm_opt['embedding_dim'],
                              hidden_size=lstm_opt['hidden_dim'], bidirectional=True)
        self.hidden = self.init_hidden()

        # Linear layers
        self.dense = nn.Linear(bert_opt.bert_dim + lstm_opt['hidden_dim'] * 2, bert_opt.polarities_dim)

    def load_embeddings(self, lstm_opt):
        if lstm_opt["embedding_type"] == "glove":
            text_field = data.Field(lower=True)
            text_field.vocab.load_vectors(lstm_opt['embedding_path'])
            return text_field.vocab.vectors

    def init_hidden(self):
        # first is the hidden h
        # second is the cell c
        if self.use_gpu:
            return (Variable(torch.zeros(2, self.batch_size, self.hidden_dim).cuda()),
                    Variable(torch.zeros(2, self.batch_size, self.hidden_dim).cuda()))
        else:
            return (Variable(torch.zeros(2, self.batch_size, self.hidden_dim)),
                    Variable(torch.zeros(2, self.batch_size, self.hidden_dim)))

    def forward(self, inputs):
        bert_inputs, lstm_inputs = inputs

        text_bert_indices, bert_segments_ids = bert_inputs[0], bert_inputs[1]
        _, pooled_output = self.bert(text_bert_indices, bert_segments_ids, output_all_encoded_layers=False)
        pooled_output = self.bert_dropout(pooled_output)

        lstm_x = self.embeddings(lstm_inputs).view(len(lstm_inputs), self.batch_size, -1)
        lstm_y, self.hidden = self.lstm(lstm_x, self.hidden)

        y = self.dense(torch.cat((pooled_output, lstm_y[-1])))
        log_probs = F.log_softmax(y)
        return log_probs
