import unittest
import string

class TestRevRelMethods(unittest.TestCase):
    def test_1word(self):
        self.assertEqual(nb_sentences("test"), 1)
    

    def test_1sentences(self):
        self.assertEqual(nb_sentences("test."), 1)
    

    def test_2sentences(self):
        self.assertEqual(nb_sentences("bonjour. au revoir"), 2)
    
    def test_3sentences(self):
        self.assertEqual(nb_sentences("test. test. test."), 3)
    

def nb_sentences(text):
    """
    Détecte le nombre de phrases "correctement formatées" dans un texte, en utilisant la ponctuation finale
    Un phrase correctement formatée se finit par une ponctuation finale . ? ou !
    On ne tient pas compte des majuscules (souvent il peut ne pas y en avoir, la ponctuation finale semble être le meilleur indicateur)
    """
    sentence_ends = [".", "?", "!"]
    previous_char_is_end = False
    nb = 0

    text = "".join(text.split()) #on supprime tous les caractères non imprimables
    for char in text:
        if char in sentence_ends:
            previous_char_is_end = True
        #else not . ? or !
        elif previous_char_is_end:
            previous_char_is_end = False
            nb += 1
        else :
            previous_char_is_end = False
    
    nb += 1
    
    return nb


def nb_strong_punc(text):
    nb = 0
    for char in text:
        if char in ["?", "!"]:
            nb += 1
    return nb


def nb_weak_punc(text):
    nb = 0
    for char in text:
        if char in [".", ",", ";", ":"]:
            nb += 1
    return nb


def nb_upper(text):
    nb = 0
    for char in text:
        if char in string.ascii_uppercase:
            nb += 1
    return nb


def replace_na_by_void(df):
    return df.fillna("", axis=0)


def drop_column(df, column):
    return df.drop(column, axis=1)


