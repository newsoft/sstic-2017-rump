# SSTIC 2017 - Rump Session material

## What

This collection of scripts will allow you to train a TensorFlow model using CERTFR publications.

## How

1. Scrape all PDF documents from the Web site, using `scrape.py`.

Files are saved in the current directory. The default time period is 2013-2017.

2. Convert all PDF documents into plain ASCII files using `convert.py`.

This script will first shell out to the `pdf2txt` command, then simplify the resulting UTF-8 document into plain ASCII.

**Please note that you should only use this command against trusted files.**

3. Checkout a slightly modified version of [Martin Gorner's](https://github.com/martin-gorner/tensorflow-rnn-shakespeare) excellent TensorFlow tutorial.
```
$ pip3 install --user tensorflow
$ git clone https://github.com/newsoft/tensorflow-rnn-shakespeare
$ cd tensorflow-rnn-shakespeare/
$ python3 rnn_train.py [directory containing TXT files]
```

Note: this code requires **Python3**.

4. Once the training is completed, you should be able to generate new random files.
```
$ python3 rnn_play.py [META file]
```

Have fun!