import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import warnings
from typing_extensions import Protocol
import pdfplumber

# Lifted from https://stackoverflow.com/questions/18926031/how-to-extract-a-subset-of-a-colormap-as-a-new-colormap-in-matplotlib
def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

def generate_word_cloud(filename, color_map):
	all_content = ""
	with pdfplumber.open(filename) as pdf:
		for page in pdf.pages:
			paragraphs = page.extract_text(x_tolerance=1)
			all_content += paragraphs
			
	# Filter out words not directly related to policy, common terms, and words that add noise to word maps.
	single_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "S"]
	odd_fragments_and_common_terms = ["RE", "ll", "NN", "AANNDD", "TTHHEE", "VE", "CHAPTER", "YEAR", "YEARS", "PLATFORM", "POLICY", "POLICIES", "PEOPLE", "COUNTRY", "NATION", "NATIONAL", "WORLD", "TERM", "WASHINGTON", "FEDERAL", "GOVERNMENT", "INCLUDING", "PARTY", "PRESIDENT", "CONGRESS", "ADMINISTRATION", "WILL", "STATE", "UNITED", "STATES", "AMERICA", "AMERICAN", "AMERICANS"]
	candidates_and_party_names = ["BIDEN", "HARRIS", "TRUMP", "DEMOCRATS", "REPUBLICANS", "DEMOCRAT", "REPUBLICAN"]
	frequent_numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

	for i in range(100):
		frequent_numbers.append(str(i))

	stop_words = single_letters + odd_fragments_and_common_terms + candidates_and_party_names + frequent_numbers + list(STOPWORDS)
	
	cmap = plt.get_cmap(color_map)
	warm_color_map = truncate_colormap(cmap, 0.75, 0.85)
	
	# Word cloud word sizes are based solely on word frequency.
	# Width and height match default PNG size for my computer and should probably be updated.
	wordcloud = WordCloud(width=640, height=475, min_font_size=10, max_words=100, stopwords=stop_words, background_color="white", mode="RGB", relative_scaling=1, collocations=True, colormap=warm_color_map, random_state=42).generate(all_content)

	plt.imshow(wordcloud, interpolation='bilinear')
	plt.axis("off")
	plt.show()


# Democratic: "democratic_2024_platform.pdf", "Blues"
# Republican: "republican_2024_platform.pdf", "Reds"
generate_word_cloud("democratic_2024_platform.pdf", "Blues")
generate_word_cloud("republican_2024_platform.pdf", "Reds")
