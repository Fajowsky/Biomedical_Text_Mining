from ppi.models import *


import random



#PROTEIN RECOGNITION AND DEPENENCIES

import numpy as np

import spacy
import scispacy
nlp = spacy.load("en_core_sci_sm")


def word2vec(x):
    return nlp(x).vector


#instance = proteinRecognizerNetwork()

def isProtein(proteinRecognitionNetwork,word):
	return bool(round(proteinRecognitionNetwork.predict(np.array([word2vec(word)]))[0][0]))

