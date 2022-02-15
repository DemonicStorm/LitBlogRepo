import spacy
from spacy_langdetect import LanguageDetector
import en_core_web_sm
from glob import glob

nlp = en_core_web_sm.load()

#nlp = spacy.load('en')
nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)


print(LanguageDetector)