

class NaturalLanguageProcessor:


    def __init__(self, input: str=None):
        # init list of useless word
        self._ignore_words = ['à', 'a', '?', '!', 'de ', 'la', 'le', 'du', 'des', 'sur', 'un', 'une']
        # init input
        self.input = input



    def find_equality(self, pattern: str=None, threshold: float=75) -> bool:

        # transform float with no '.'
        threshold = self.__conform_float(threshold)

        # first split the patter,
        pattern = self.__split_pattern(pattern)

        # count matched word
        martched_word_count = self.__get_matched_word(pattern)

        # find percent of word matched
        matched_percent = self.__calcul_percent(martched_word_count, len(pattern))

        # modify threshold for len input
        if self.__get_len_input() == 1:
            threshold = 33.0
        elif self.__get_len_input() == 2:
            threshold = 66.0
        else:
            pass

        # return if threshold or more is found
        if matched_percent >= threshold:
            return True
        else:
            return False

    def extract_slot(self, pattern: str=None) -> str:
        pattern = self.__split_pattern(pattern)
        _input = self.input

        for word_in_pattern in pattern:
            for word_in_input in _input.split():

                if word_in_input in self._ignore_words:
                    _input = _input.replace(word_in_input, "")

                if word_in_input == word_in_pattern:
                    _input = _input.replace(word_in_input, "")

        _input = self.__remove_space(_input)
        if _input == "":
            return None
        else:
            return _input



    def __remove_space(self, string: str) -> str:
        return string.replace(" ", "")

    def __get_len_input(self) -> int:
        return len(self.input.split(" "))

    def __get_matched_word(self, pattern: list) -> int:
        # get matched word count
        martched_word_count = 0
        for word_in_pattern in pattern:
            if word_in_pattern in self.input:
                martched_word_count += 1
        return martched_word_count

    def __split_pattern(self, pattern: str) -> list:
        return pattern.split()

    def __calcul_percent(self, partial: int, total: int) -> float:
        # (X * 100) / Y
        return float(100 * partial / total)

    def __conform_float(self, float: float) -> float:
        # transform float with no '.'
        if "." not in str(float):
            float = float + .0
        return float

    def __calcul_is_good_word(self, word: str, word_pattern: str):
        """
        calcul le nombre de lettre dun mot et retourne un pourcentage de probabilité que sa soit le bon mot
        """
        pass
