# SSTIC 2017 - Rump Session material

## What

This collection of scripts will allow you to train a TensorFlow model using CERTFR publications.

## How

1. Extract `CERT*ACT*.txt` files from official archives:
[https://www.cert.ssi.gouv.fr/tar/2004.tar](https://www.cert.ssi.gouv.fr/tar/2004.tar)
[https://www.cert.ssi.gouv.fr/tar/2005.tar](https://www.cert.ssi.gouv.fr/tar/2005.tar)
[https://www.cert.ssi.gouv.fr/tar/2006.tar](https://www.cert.ssi.gouv.fr/tar/2006.tar)
[https://www.cert.ssi.gouv.fr/tar/2007.tar](https://www.cert.ssi.gouv.fr/tar/2007.tar)
[https://www.cert.ssi.gouv.fr/tar/2008.tar](https://www.cert.ssi.gouv.fr/tar/2008.tar)
[https://www.cert.ssi.gouv.fr/tar/2009.tar](https://www.cert.ssi.gouv.fr/tar/2009.tar)
[https://www.cert.ssi.gouv.fr/tar/2010.tar](https://www.cert.ssi.gouv.fr/tar/2010.tar)
[https://www.cert.ssi.gouv.fr/tar/2011.tar](https://www.cert.ssi.gouv.fr/tar/2011.tar)
[https://www.cert.ssi.gouv.fr/tar/2012.tar](https://www.cert.ssi.gouv.fr/tar/2012.tar)
[https://www.cert.ssi.gouv.fr/tar/2013.tar](https://www.cert.ssi.gouv.fr/tar/2013.tar)
[https://www.cert.ssi.gouv.fr/tar/2014.tar](https://www.cert.ssi.gouv.fr/tar/2014.tar)
[https://www.cert.ssi.gouv.fr/tar/2015.tar](https://www.cert.ssi.gouv.fr/tar/2015.tar)
[https://www.cert.ssi.gouv.fr/tar/2016.tar](https://www.cert.ssi.gouv.fr/tar/2016.tar)
[https://www.cert.ssi.gouv.fr/tar/2017.tar](https://www.cert.ssi.gouv.fr/tar/2017.tar)

2. Convert all text files into plain ASCII files using `convert.py`.

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