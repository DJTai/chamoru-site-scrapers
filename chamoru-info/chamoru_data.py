class ChamoruWord:
    """Class used to represent a Chamoru word.

    Attributes:
        word (str): Chamoru word
        type (str): Word type, e.g., noun, adjective, etc.
        definition (str): Definition of word.
        pronunciation (str): Syllable pronunciation of word.
        origin (str): Origin of word, i.e., etymology.
        ch_example (str): Example sentence in Chamoru.
        en_example (str): English translation of ch_example.
        root_word (str): Root word, if applicable.
    """
    
    def __init__(self, word):
        """Constructor.

        Args:
            word (str): word to be created.
        """
        self.word = word
        self.type = None
        self.definition = None
        self.pronunciation = None
        self.origin = None
        self.ch_example = None
        self.en_example = None
        self.root_word = None

    def __str__(self):
        """Prints main attributes of the ChamoruWord.

        Returns:
            str: Word, Type, and Definition
        """
        return "Word: {}\nDef: {}\nCH: {}\nEX: {}".format(self.word, self.definition, self.ch_example, self.en_example)
