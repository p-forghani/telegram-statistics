from pathlib import Path
from typing import Union
from collections import Counter
from hazm import Normalizer, word_tokenize
from wordcloud import WordCloud
from bidi.algorithm import get_display

import arabic_reshaper
import json
import matplotlib.pyplot as plt
import re
import demoji

from src.data import DATA_DIR
from src.utils import io

class ChatStatistics:
    """Generates chat statistics from a Telegram chat json file
    """
    def __init__(self, chat_json: Union[str, Path]):
        """
        Args:
            chat_json (Union[str, Path]): file path of the json file
        """
        # load the data
        with open(chat_json) as f:
            self.data = json.load(f)
        # Initiate and normalize the stopwords
        self.normalizer = Normalizer()
        stop_words = open(DATA_DIR / 'stopwords.txt').readlines()
        stop_words = map(str.strip, stop_words)
        self.stopwords = set(map(self.normalizer.normalize, stop_words))

    def de_emojify(self, text):
        """Removes emojis and some special characters from the text.

        :param text: Text that contains emoji
        """
        regrex_pattern = re.compile(pattern="[\u2069\u2066]+", flags=re.UNICODE)
        text = regrex_pattern.sub('', text)
        return demoji.replace(text, " ")
    
    def generate_wordcloud(self, output_dir: Union[str, Path]):
        """Creates a words cloud to the output file

        Args:
            output_dir (Union[str, Path]): desired file path of the wordcloud file
        """
        # Add the messages to content
        text_content = ''
        for msg in self.data['messages']:
            if type(msg['text']) is str:
                tokens = word_tokenize(msg['text'])
                tokens = filter(lambda item: item not in self.stopwords, tokens)
                text_content += ' '.join(tokens)
        
        # Normalize and reshape the content
        text_content = self.de_emojify(text_content)
        text_content = self.normalizer.normalize(text_content)
        text_content = arabic_reshaper.reshape(text_content)
        
        # this line of code messes up some texts:
        # text_content = get_display(text_content)

        # Generate the wordcloud
        wordcloud = WordCloud(
            font_path=str(DATA_DIR/'NotoNaskhArabic-Regular.ttf')
        ).generate(text_content)
        # Write wordcloud to the file
        WordCloud.to_file(wordcloud, str(Path(output_dir)/'wordcloud.png'))
        print('The wordcloud created in the desired directory!')

if __name__ == "__main__":
    data = ChatStatistics(DATA_DIR / 'result.json')
    data.generate_wordcloud(output_dir=DATA_DIR)