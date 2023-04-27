# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 12:48:09 2022

@author: Johan

title: Test af kandidat til dataanalytiker stillingen
"""

import pandas as pd
# import ast
# import numpy as np

# https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
# https://docs.python.org/3/library/codecs.html#error-handlers
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.translate.html
netflix_df = pd.read_csv(r'C:\Users\Johan\opg_dataanalytiker\netflix_titles.csv') # ,encoding(),encoding_errors()

netflix_df
netflix_df.info
netflix_df.size # 105684
netflix_df.shape # (8807, 12)
netflix_df.empty # not empty
netflix_df.index
netflix_df.columns
# =============================================================================
# Index(['show_id', 'type', 'title', 'director', 'cast', 'country', 'date_added',
#        'release_year', 'rating', 'duration', 'listed_in', 'description'],
#       dtype='object')
# =============================================================================
netflix_df.dtypes # mostly objects - convert/parse? https://pandas.pydata.org/docs/reference/series.html#conversion


# =============================================================================
#  opg 1.1 gns antal skuespillere per film/tv-show
# =============================================================================
netflix_df.type.unique() # kun movies og tvshows, dvs. ingen grund til at selektere type
netflix_df.cast # lists of actors

# tæl elementer i cast per række og tag gns

# 1.1.1 find ud af hvordan jeg vælger elementer i lister og tæller antallet
netflix_df.loc[1]
netflix_df.loc[1].cast # der er ca 20 skuespillere i denne udgivelse
netflix_df.cast.str.len() # her tælles 300 elementer i listen; altså tælles antal tegn. enten tæller jeg forkert eller også skal objektet konverteres
type(netflix_df.cast) # series
type(netflix_df.cast[0]) # float NaN
type(netflix_df.cast[1]) # str NOT LIST

# find metode til at konvertere serie/col af serier til serie/col af lister
# netflix_df.cast.transform(ast.literal_eval) # fails
netflix_df.cast = netflix_df.cast.str.split(pat=",") # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.split.html
type(netflix_df.cast[1]) # list

netflix_df.cast.str.len() # ANTAL SKUESPILLERE PER UDGIVELSE
netflix_df.cast.str.len().sum() # samlet antal skuespillere i film = 64126. Der er 8807 film/shows
# GNS ANTAL SKUESPILLERE PER udgivelse
64126.0/8807 # 7 inkl film uden cast
netflix_df.cast.str.len().mean() # 8 eksl NaN

# =============================================================================
# 1.2 gns antal film/tv-show per skuespiller
# =============================================================================

# find alle elementer i lister og tæl frekvensen af hver. 
# https://stackoverflow.com/questions/48707117/count-of-elements-in-lists-within-pandas-data-frame
# https://stackoverflow.com/questions/22391433/count-the-frequency-that-a-value-occurs-in-a-dataframe-column
# http://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.value_counts.html

netflix_df2 = netflix_df[['type','cast']]
netflix_df2.cast.sort_values()

test = netflix_df2.explode('cast').value_counts().to_frame('fq').reset_index().sort_values('fq')
test
test = netflix_df2.explode('cast').value_counts().to_frame('fq').reset_index().sort_values('cast')
test 

#  virker ikke pga NaN's
# test2 = pd.Series([item for sublist in netflix_df2.cast for item in sublist])
# test3 = pd.Series(np.concatenate(netflix_df2.cast))
# test4 = pd.Series(sum([item for item in netflix_df2.cast], [])).value_counts()
# netflix_df2.groupby('cast').size()

netflix_df3 = netflix_df['cast']
netflix_df3.explode().value_counts()
netflix_df3.explode().unique()
netflix_df3.explode().value_counts().mean() # RESULTAT hver medvirkende optræder i gns 1.6 film/shows

netflix_df3.explode().str.lstrip().value_counts().mean() # RESULTAT når vi renser for leadling whitespace er svaret 1.75

netflix_df3.explode().value_counts().unique()
netflix_df3.explode().value_counts().describe()
netflix_df3.explode().value_counts().to_frame('fq').reset_index().sort_values('index')
# er det nødvendigt at parse navnene bedre? kan det samme navn være stavet forskelligt i forskellige udgivelser?
# - fornavn, efternavn; efternavn, fornavn?
# - forkortet mellemnavn; komplet mellemnavn
# evt. kan man tilføje regex for at skelne specielle tilfælde.
# der er også mange udenlandske navne fx kinesiske, dvs. i anden tegn-enkodning https://en.wikipedia.org/wiki/Character_encoding
# Her har jeg antaget at fejl pga. anden enkodning vil opstå på sammen måde, hvorfor jeg godt kan tælle således.

# netflix_df3.explode().value_counts().hist() # er selvfølgelig også fordelt som



# =============================================================================
# 2 histogram over antal film/tv-show per instruktør
# =============================================================================
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.hist.html
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.html
# https://stackoverflow.com/questions/29525120/pandas-creating-a-histogram-from-string-counts
directors = netflix_df['director']
directors.value_counts()
directors.value_counts().unique()
directors.value_counts().hist() # frekvensen går fra 17,5 til 1 i stedet for 19 til 1 (giver ikke mening med halve antal film)
directors.value_counts().hist(legend=True)

directors.value_counts().hist(bins=18).set_xticks([0,1,5,10,15,19,20]) 
# https://matplotlib.org/stable/api/axes_api.html
# skal bygges op med matplotlib for at sætte flere elementer fx .set_xlabel("Film").set_ylabel("Film")
# https://stackoverflow.com/questions/18992086/save-a-pandas-series-histogram-plot-to-file
# https://stackoverflow.com/questions/35484458/how-to-export-to-pdf-a-graph-based-on-a-pandas-dataframe
directors.value_counts().hist(bins=18).get_figure().savefig(r'C:\Users\Johan\opg_dataanalytiker\opg2_histogram.pdf') 
# ligner Poisson, Negative binomial og Pareto distributions - meget skæv. usandsynligt at lave mere end et par film

netflix_df.director = netflix_df.director.str.split(pat=",")
directors = netflix_df['director']
directors2 = directors.explode().str.lstrip()
directors2.value_counts().unique()
dir_pr_no_of_prod = directors2.value_counts().rename_axis('directors').reset_index(name='productions') # max = 22
dir_pr_no_of_prod.hist(column='productions', bins=18)
dir_pr_no_of_prod.plot(kind='hist', bins=18, color='green', legend=False) # , x='productions', rot=0)
dir_pr_no_of_prod.plot(kind='hist', bins=18, color='green', legend=False, title='Instruktører fordelt efter antal produktioner', ylabel='')




# test andre versioner
# import seaborn as sns
import matplotlib.pyplot as plt

# kør plotlinjer sammen
dir_pr_no_of_prod.plot(kind='hist', bins=18, color='green', legend=False
                       , title='Instruktører fordelt efter antal produktioner')
plt.xlabel('Antal produktioner')
plt.ylabel('Antal instruktører')
plt.show()

# dir_pr_no_of_prod.hist(column='productions', bins=18, color='green')


# https://www.geeksforgeeks.org/how-to-change-the-number-of-ticks-in-matplotlib/
# https://www.tutorialspoint.com/how-to-set-x-axis-values-in-matplotlib-python
# https://stackoverflow.com/questions/27491392/set-x-axis-intervalsticks-for-graph-of-pandas-dataframe
# https://stackoverflow.com/questions/24003485/intervals-on-x-axis
# https://stackoverflow.com/questions/58585241/modify-the-x-axis-labels-in-histogram-plot-using-matplotlib
# https://stackoverflow.com/questions/12608788/changing-the-tick-frequency-on-the-x-or-y-axis
# https://stackoverflow.com/questions/12608788/changing-the-tick-frequency-on-the-x-or-y-axis

# =============================================================================
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.len.html
# https://stackoverflow.com/questions/21295334/find-length-of-longest-string-in-pandas-dataframe-column
# # max length of directors name
# # directors.map(len).max() # TypeError: object of type 'float' has no len()
# directors.str.len().to_frame('length').reset_index().sort_values('length')
# directors.str.len().max()
# directors[[directors.str.len().max()]]
# =============================================================================




# =============================================================================
# 3 Beskriv hvad du synes er et andet interessant aspekt af datasættet 
# STATISTISK (f.eks. min, max, gennemsnit, varians) 
# og VISUELT (f.eks. histogrammer og tidslinjer). 
# =============================================================================
# ville forvente ret stort skew i antal film blandt hhv instruktører og medvirkende
# sandsynligheden for at lave mere end 1 er meget lav
# directors.value_counts().describe()

# fordi jeg ikke kender datasættets oprindelse, er det interessant
# at undersøge hvordan det stemmer med en normal/typisk forventning;
# at de fleste film og shows er produceret i USA
netflix_df = pd.read_csv(r'C:\Users\Johan\opg_dataanalytiker\netflix_titles.csv') # ,encoding(),encoding_errors()
netflix_df.country
netflix_df.country.value_counts()
netflix_df.country = netflix_df.country.str.split(pat=",")
country_df = netflix_df['country']
country_df2 = country_df.explode().str.lstrip()
country_df2.value_counts()


# =============================================================================
# how to convert count to df
# df['your_column'].value_counts().to_frame()
# value_counts = df['course_difficulty'].value_counts()
# 
# # converting to df and assigning new names to the columns
# df_value_counts = pd.DataFrame(value_counts)
# df_value_counts = df_value_counts.reset_index()
# df_value_counts.columns = ['unique_values', 'counts for course_difficulty'] # change column names
# df_value_counts
# =============================================================================
# prod_pr_country = country_df2.value_counts().to_frame()
country_df2.value_counts()
prod_pr_country = country_df2.value_counts().rename_axis('countries').reset_index(name='productions')
prod_pr_country.productions.describe() # max = 3690
prod_pr_country[prod_pr_country['countries'] == 'United States'] # 3690
prod_pr_country[prod_pr_country['countries'] == 'China'] # 162 -> dvs der er ca. 25 gange så mange us prod som ch prod
prod_pr_country.loc[prod_pr_country['countries'].isin(['United States','China'])]
prod_pr_country.plot()
us_china = prod_pr_country.loc[prod_pr_country['countries'].isin(['United States','China'])]
us_china 
us_china.plot(kind='bar', color='green', ylabel='Productions', x='countries', rot=0, legend=False, title='Chinese media production trails in Western outlets',xlabel='')

netflix_df.release_year.describe() # det er film der går tilbage til 1925 fra 2021
netflix_df.date_added.value_counts() # flest film tilføjet i 2021
# =============================================================================
# netflix_df.release_year
# netflix_df.date_added
# netflix_df = pd.read_csv(r'C:\Users\Johan\opg_dataanalytiker\netflix_titles.csv',\
#                          parse_dates=[6,7], infer_datetime_format=True)
# =============================================================================


# undersøg fx udviklingen i antal film fra kina (vs rest)
# netflix_df.groupby('release_year').country.value_counts()

# netflix_df.groupby('type').release_year.value_counts()


# =============================================================================
# 4 Hvordan kan vi estimere de mest sete film/tv-shows, uden at have adgang til
#  yderligere Netflix-data? 
#  Er der offentligt tilgængelige data, der kan hjælpe os med denne vurdering?
# =============================================================================

# 4.1 - uden at have adgang til yderligere Netflix-data, dvs. uden en kolonne med "hours watched"

netflix_df.columns
# =============================================================================
# Index(['show_id', 'type', 'title', 'director', 'cast', 'country', 'date_added',
#        'release_year', 'rating', 'duration', 'listed_in', 'description'],
#       dtype='object')
# =============================================================================
netflix_df.listed_in
netflix_df.country
netflix_df.type
netflix_df.description

netflix_df.rating.unique()
netflix_df.rating.value_counts()


netflix_df.release_year
netflix_df.duration
netflix_df.type.value_counts()

netflix_df = pd.read_csv(r'C:\Users\Johan\opg_dataanalytiker\netflix_titles.csv')
netflix_df.dtypes
netflix_df.date_added
netflix_df['date_added'] = pd.to_datetime(netflix_df['date_added'])
netflix_df.date_added

import seaborn as sns
