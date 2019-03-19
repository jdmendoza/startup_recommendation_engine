#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np


# In[120]:


df = pd.read_csv("cleaned_sf_data.csv")
print(df.shape)
df.head()


# In[118]:


#Used in the project 3 code
#category_df = df[['company_name','company_category_list']].drop_duplicates()
#category_dict = dict(zip(list(category_df.company_name),list(category_df.company_category_list)))


# In[182]:


import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

from sklearn import preprocessing


def clustify(df, k_keywords, k_nums):

    X_keyword = df['company_category_list'].map(lambda x: ' '.join(str(x).lower().split("|")))
    vectorizer = TfidfVectorizer()
    X_vectorized = vectorizer.fit_transform(X_keyword)

    k_keywords = 10
    model = KMeans(n_clusters=k_keywords, init='k-means++', max_iter=100, n_init=1)
    keyword_clusters = model.fit_predict(X_vectorized)

    """
    print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(k_keywords):
        print("Cluster %d:" % i),
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind]),
        print
    """

    keyword_cluster_dict = dict(zip(list(df['company_name']),keyword_clusters))
    df['keyword_clusters'] = df['company_name'].map(keyword_cluster_dict)

    #Cluster the already keyword clustered data
    X_prescaling = df[['total_funding','company_max_round','investor_ratings']]
    X_prescaling.fillna(0)
    X_scaled  = pd.DataFrame(preprocessing.scale(X_prescaling))
    X_scaled['company_name'] = df['company_name']
    X_scaled['keyword_clusters'] = df['keyword_clusters']


    num_clust = KMeans(n_clusters=k_nums)
    num_clusters = num_clust.fit_predict(X_scaled[[0,'keyword_clusters']])

    df['final_cluster'] = num_clusters

    return (df)

    """
    #This section would split each subspace
    for curr_k in range(k_keywords):

        X_scaled_partitioned = X_scaled[X_scaled['keyword_clusters']==curr_k][0]
        num_clust = KMeans(n_clusters=k_nums)
        num_clusters = num_clust.fit_predict(X_scaled_partitioned)
        #num_cluster_dict = dict(zip(list(df['company_name']),keyword_clusters))
        #print (num_clusters)
    """


# In[191]:


clustered_df = clustify(df,40,100)


# In[192]:


clustered_df.columns


# In[205]:


def showTopCompanies(df, enteredCompany):

    company_data = df[df["company_name"]==enteredCompany]
    #print(company_data)
    cluster_group = company_data.iloc[0]['final_cluster']
    #print(cluster_group)

    group = df[df['final_cluster']==cluster_group]

    fig = dashboard(group, enteredCompany)
    return fig, group


# In[204]:


from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

init_notebook_mode(connected=True)

def dashboard(df_plt, company_name):
    '''
    trace1 = go.Table(
        header=dict(values=[1,2],
                    #fill = dict(color='#C2D4FF'),
                    align = ['left'] * 5),
        cells=dict(values=[1,2],
                   #fill = dict(color='#F5F8FF'),
                   align = ['left'] * 5)
    )
    '''
    trace2 = go.Bar(
        x=[x for x in df_plt['company_name']],
        y=list(df_plt['total_funding']),
        #text=['Text A', 'Text B', 'Text C'],
    )

    trace3 = go.Bar(
        name='Test',
        x=[x for x in df_plt['company_name']],
        y=list(df_plt['company_max_round']),
        #text=['Text D', 'Text E', 'Text F'],
    )

    trace4 = go.Bar(
        name='Test',
        x=[x for x in df_plt['company_name']],
        y=list(df_plt['investor_ratings']),
        #text=['Text D', 'Text E', 'Text F'],
    )

    fig = tools.make_subplots(rows=2, cols=2,subplot_titles=('', 'Total Funding', 'Rounds','Investor Rating'))

    #fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)
    fig.append_trace(trace3, 2, 1)
    fig.append_trace(trace4, 2, 2)


    fig['layout'].update(height=600, width=800,showlegend = False, title=f'Companies Similar To *{company_name}*')
    #py.iplot(fig, filename='simple-subplot-with-annotations')
    iplot(fig,filename='basic')

    return fig


# In[206]:


fig, group = showTopCompanies(clustered_df, 'Twitter')


plot(fig, filename='name.html', auto_open=False)

# In[ ]:
