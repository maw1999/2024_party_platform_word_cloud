import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import warnings
from typing_extensions import Protocol
import pdfplumber

# Democrat: democrat_2024_platform.pdf
# Republican: republican_2024_platform.pdf
print("Input platform PDF file: democrat_2024_platform.pdf or republican_2024_platform.pdf?\n")
filename = input()
print("Loading...\n")

all_content = ""
with pdfplumber.open(filename) as pdf:
	for page in pdf.pages:
		paragraphs = page.extract_text(x_tolerance=1)
		all_content += paragraphs
		
single_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "S"]
odd_fragments_and_common_terms = ["RE", "ll", "PRESIDENT", "CONGRESS", "ADMINISTRATION"]
past_and_present_candidates = ["BIDEN", "HARRIS", "TRUMP"]
frequent_numbers = list()

for i in range(100):
	frequent_numbers.append(str(i))

stop_words = single_letters + odd_fragments_and_common_terms + past_and_present_candidates+ frequent_numbers + list(STOPWORDS)

# Democrat: BuPu
# Republican: RgDy
print("Word cloud color map: BuPu or RdGy?\n")
color_map = input()
wordcloud = WordCloud(width=650, height=475, min_font_size=7, stopwords=stop_words, background_color="white", mode="RGB", relative_scaling=0, collocations=False, colormap=color_map, random_state=42).generate(all_content)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
