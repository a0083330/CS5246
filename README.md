# CS5246

This is the repo to document the group project for NUS CS5246

The standard dataset of choice is Stanford Sentiment Treebank 2:
GLUE data benchmark performance:https://gluebenchmark.com/leaderboard

# SentimentAnalysis-BERT
This repo is developed from: https://github.com/huggingface/pytorch-pretrained-BERT

The model structure for sentence classification could be found in: https://github.com/huggingface/pytorch-pretrained-BERT/blob/master/pytorch_pretrained_bert/modeling.py
Bertforsequenceclassification

Benchmark BERT Model could be run with the following code:
```shell
export GLUE_DIR=/SST-2
export TASK_NAME=SST-2

python run_classifier.py \
  --task_name $TASK_NAME \
  --do_train \
  --do_eval \
  --do_lower_case \
  --data_dir $GLUE_DIR/$TASK_NAME \
  --bert_model bert-base-uncased \
  --max_seq_length 128 \
  --train_batch_size 32 \
  --learning_rate 2e-5 \
  --num_train_epochs 3.0 \
  --output_dir /tmp/$TASK_NAME/
```
Bilstm Model or LSTM could be run with the following code:
```shell
python train_batch.py --m bilstm
```
CNN Model could be run with the following code:
```shell
python cnn_classification.py
```
