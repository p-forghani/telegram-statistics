from pathlib import Path
import json
from typing import Union
from collections import Counter
from hazm import Normalizer, word_tokenize, stopwords_list
from wordcloud import WordCloud
import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib.pyplot as plt
from src.data import DATA_DIR

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
        self.stopwords = list(map(self.normalizer.normalize, stopwords_list()))
    
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