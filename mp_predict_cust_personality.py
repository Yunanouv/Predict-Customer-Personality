# -*- coding: utf-8 -*-
"""MP-Predict Cust Personality.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UEiDhzP4yP01hpUbINuTVzQI0qu3YYQZ
"""

!pip install dython

"""# **Predict Customer Personality to Boost Marketing Campaign**"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
from matplotlib import rcParams
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from scipy import stats
import calendar
import matplotlib.dates as mdates
from datetime import datetime, timedelta

import warnings
warnings.filterwarnings('ignore')

"""---


---

# Data Exploration

---



---
"""

rawdf = pd.read_csv('https://drive.google.com/uc?export=download&id=1WY7_EYEtJ2-ZfTTTnOGAZf4oKMzGsJgc', low_memory=False)
rawdf.info()

rawdf.sample(5)

"""| Feature Name | Description |
| --- | --- |
***CUSTOMERS ATTRIBUTES***
|**Unnamed : 0** | Index number |
|**ID** | Customer's unique identifier |
|**Year_Birth** | Customer's birth year|  
|**Education** |Customer's education level |
|**Marital_Status** | Customer's marital status|
|**Income** | Customer's yearly household income |
|**Kidhome**| Number of children in customer's household |
|**Teenhome** | Number of teenagers in customer's household  |
|**Dt_Customer** |Date of customer's enrollment with the company  |
|**Recency** | Number of days since customer's last purchase |
|**Complain** | 1 if the customer complained in the last 2 years, 0 otherwise |  
***PRODUCTS ATTRIBUTES***
|**MntCoke** | Amount spent on coke in last 2 years |
|**MntFruits** | Amount spent on fruits in last 2 years |
|**MntMeatProducts** | Amount spent on meat in last 2 years |  
|**MntFishProducts** | Amount spent on fish in last 2 years |
|**MntSweetProducts** | Amount spent on sweets in last 2 years|
|**MntGoldProds** | Amount spent on gold in last 2 years |
***PROMOTION ATTRIBUTES***
|**NumDealsPurchases** |Number of purchases made with a discount|
|**AcceptedCmp1** |1 if customer accepted the offer in the 1st campaign, 0 otherwise|
|**AcceptedCmp2** |1 if customer accepted the offer in the 2nd campaign, 0 otherwise|
|**AcceptedCmp3** |1 if customer accepted the offer in the 3rd campaign, 0 otherwise|
|**AcceptedCmp4** |1 if customer accepted the offer in the 4th campaign, 0 otherwise|
|**AcceptedCmp5** |1 if customer accepted the offer in the 5th campaign, 0 otherwise|
|**Response** |1 if customer accepted the offer in the last campaign, 0 otherwise|
***PLACE ATTRIBUTES***
|**NumWebPurchases** |Number of purchases made through the company’s website|  
|**NumCatalogPurchases** |Number of purchases made using a catalogue|
|**NumStorePurchases** |Number of purchases made directly in stores|  
|**NumWebVisitsMonth** |Number of visits to company’s website in the last month|
|**Z_CostContact** | Cost to contact a customer |
|**Z_Revenue** |Revenue after client accepting campaign|

"""

# Check duplicated rows
rawdf.duplicated().sum()

"""Hasil :
1. Hanya ada 1 kolom dengan null value yaitu kolom Income (24 null values)  
2. Tipe data untuk kolom Dt_Customers perlu diubah ke datetime  
3. Tidak ada data duplikat
"""

# Descriptive statistic

num_cols = rawdf.select_dtypes(exclude='object').columns.tolist()
cat_cols = rawdf.select_dtypes(include='object').columns.tolist()

pd.set_option('display.float_format', lambda x: '%.3f' % x)
rawdf[num_cols].describe().T

rawdf[cat_cols].describe()

"""## Feature Extraction"""

# Age - we can't use year birth as indicator, so need to be converted to age
rawdf['Age'] = 2023 - rawdf['Year_Birth']
rawdf['Children'] = rawdf['Kidhome'] + rawdf['Teenhome']
rawdf['TotalSpending'] = rawdf.filter(regex='Mnt', axis=1).sum(axis=1)
rawdf['TotalTrx'] = rawdf.filter(regex='Purchases', axis=1).sum(axis=1)
rawdf['TotalAccCmp'] = rawdf.filter(regex='Cmp', axis=1).sum(axis=1)

def cvr(x,y):
    if y == 0:
        return 0
    return x / y

rawdf['CVR'] = round(rawdf.apply(lambda x: cvr(x['TotalTrx'],x['NumWebVisitsMonth']), axis=1), 2)
rawdf['CVR'].value_counts()

rawdf.sample(3)

"""---



---

# Exploratory Data Analysis

---



---
"""

rawdf['Education'].unique()

rawdf['Marital_Status'].unique()

# Graph of Data Distribution
num = ['Age','Income', 'Recency', 'Children', 'TotalSpending', 'TotalTrx', 'TotalAccCmp', 'CVR']

plt.figure(figsize=(12, 5))
for i in range(0, len(num)):
    plt.subplot(2, 4, i+1)
    sns.distplot(rawdf[num[i]], color='red')
    plt.tight_layout()

# Checking Outliers
plt.figure(figsize=(8, 5))
for i in range(0, len(num)):
    plt.subplot(2, 4,  i+1)
    sns.boxplot(rawdf[num[i]], color='red', orient='v')
    plt.title(num[i])
    plt.tight_layout()

"""Jika kita lihat outliers untuk `Age` terlihat bahwa data tersebut kurang masuk akal karena sudah berumur lebih dari 80 tahun sehingga sebaiknya baris ini dihapus agar proses clustering terhindar dari outliers. Begitu juga dengan outliers pada kolom `Income` yang bernilai lebih dari 600.000.000. `TotalSpending`, `TotalTrx`, dan `CVR`juga menunjukkan outliers sehingga perlu penanganan lebih lanjut."""

rawdf['Age'].describe()

rawdf[rawdf['Age'] > 80]

# Drop outliers of age
out_age = rawdf[((rawdf.Age > 80))].index
rawdf = rawdf.drop(out_age)

rawdf['Income'].describe()

# Drop outliers of income
out_income = rawdf[((rawdf.Income > 600000000))].index
rawdf = rawdf.drop(out_income)

# Checking outliers from Total Transactions
rawdf[rawdf['TotalTrx'] > 40]

# Drop outliers of age
out_trx = rawdf[((rawdf.TotalTrx > 40))].index
rawdf = rawdf.drop(out_trx)

biv = ['Age', 'Income', 'TotalTrx', 'TotalSpending']
plt.figure(figsize=(18, 4))
for var in range(0, len(biv)):
    plt.subplot(1, 4, var+1)
    sns.regplot(x=rawdf[biv[var]], y='CVR', data=rawdf, scatter_kws={'s':20, 'alpha':0.3},
                line_kws={'color':'orange'}).set(title=f'Regression plot of {biv[var]} and Conversion Rate')
    plt.tight_layout()

"""## Business Analysis

### 1. CVR Based on Age
"""

df_plot = rawdf.copy()
df_plot.shape

# Age Grouping

def age_group(x):
    if x <= 30:
        return '20-30'
    elif x <= 40:
        return '31-40'
    elif x <= 50:
        return '41-50'
    elif x <= 60:
        return '51-60'
    elif x <= 70:
        return '61-70'
    else:
        return '> 70'

df_plot['Age_Group'] = df_plot['Age'].apply(lambda x : age_group(x))

CVR_age = df_plot.groupby('Age_Group').agg({'ID': 'count','CVR':'mean'}).reset_index().rename(columns = {'ID' : 'Counts'})
CVR_age

# Plotting the Age Group

sns.set(style='whitegrid')
fig, ax = plt.subplots(1,1, figsize=(8,6))
sns.barplot(x='Age_Group', y = 'CVR', width = 0.5, data=CVR_age, palette='RdYlBu', ax=ax)

ax.set_xlabel('Age Group', fontsize=12, fontweight='medium')
ax.set_ylabel('Conversion Rate', fontsize=12, fontweight='bold')
plt.tick_params(axis='both', which='major', labelsize=10)
plt.grid(axis='y', alpha=0.8)
ax.set_axisbelow(True)

plt.text(s="Who Are Our Potential Customers?",
         x=-0.5, y=11.5, fontsize=17, fontweight='bold')
plt.text(s="The minimum age is 27 and maximum is 80 years old\nLate twenty to thirties are our potential customers",
         x=-0.5, y=10.5, fontsize=10)

plt.xlim(-0.5, 6.0)
plt.ylim(0, 10.0)

plt.axvline(0.5, ls='--', color='red')
plt.stackplot(np.arange(-0.5, 1.3, 1), [[10.00]], color='indianred', alpha=0.3)
plt.text(x=-0.3, y=9.0, s='Highest', fontsize=11, color='red')

plt.tight_layout()
plt.savefig('cvr_by_age.png')

"""### 2. CVR Based on Income"""

# Handling missing value from Income
df_plot['Income'].fillna(df_plot['Income'].median(), inplace=True)

# Income Grouping

income = np.where(df_plot['Income']>100000000, 110000000, df_plot['Income'])
income_bins = list(np.arange(0, max(income)+10000000, 10000000))
income_labs = ['{}M-{}M'.format(i*10, (i+1)*10) for i in range(10)] + ['>100M']
df_plot['Income_Group'] = pd.cut(income, bins=income_bins, labels=income_labs)

CVR_income = df_plot.groupby('Income_Group').agg({'ID': 'count', 'CVR': 'mean'}).reset_index().rename(columns = {'ID' : 'Counts'})
CVR_income

# Visualize the data
sns.set(style='darkgrid')
fig, ax = plt.subplots(1, 1, figsize=(10, 6))
sns.lineplot(x=CVR_income.index, y=CVR_income['CVR'], color='#D90429', linewidth=3)
sns.barplot(x='Income_Group', y = 'CVR', width = 0.5, data=CVR_income, palette='Paired', ax=ax)

plt.xlabel('Income_Group')
ax.set_xlabel('Income_Group', fontsize=12, fontweight='medium')
plt.ylabel('CVR')
plt.tick_params(axis='both', which='major', labelsize=10)
plt.ylim(0, 14)

ax.set_title('Conversion Rate Based on Income Group',
             x=0, y=1.06, loc='left', fontweight='bold', fontsize=20)
plt.text(s="Conversion Rate tends to increase\n along with higher income groups",
         x=0.5, y=8.4, fontsize=12, color = 'purple')

plt.tight_layout()
#plt.savefig('cvr_income.png')
plt.show()

"""### 3. CVR Based on Total Spending"""

df_plot['TotalSpending'].describe()

# Total Spending Grouping
def spending_group(x):
    if x <= 500000:
        return '0-0.5M'
    elif x <= 1000000:
        return '0.5M-1M'
    elif x <= 1500000:
        return '1M-1.5M'
    elif x <= 2000000:
        return '1.5M-2M'
    elif x <= 2500000:
        return '2M-2.5M'
    else:
        return '>2.5M'

df_plot['Spending_Group'] = df_plot['TotalSpending'].apply(lambda x : spending_group(x))
CVR_spending = df_plot.groupby('Spending_Group').agg({'ID': 'count', 'CVR': 'mean'}).reset_index().rename(columns = {'ID' : 'Counts'})
CVR_spending = CVR_spending.sort_values('Counts', ascending=False)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
CVR_spending

# Visualize

sns.set(style='white')
fig = px.bar(data_frame=CVR_spending, x='Spending_Group', y= 'CVR',
       color='CVR', color_continuous_scale='RdPu',
       width=800, height=600,
       text_auto=True, title=f'Conversion Rate Based on Spending')

fig.update_layout(plot_bgcolor='white', xaxis_tickangle = 15)
fig.show()

"""---



---

# Data Cleaning

---



---
"""

dfcleaned = df_plot.copy()
dfcleaned.info()

# Fix the noise
# Convert to datetime data type
dfcleaned['Dt_Customer'] = pd.to_datetime(dfcleaned['Dt_Customer'])

# Simplify the value
dfcleaned['Marital_Status'] = dfcleaned['Marital_Status'].replace(['Janda'], 'Cerai')
dfcleaned['Marital_Status'] = dfcleaned['Marital_Status'].replace(['Duda'], 'Cerai')
dfcleaned['Marital_Status'].value_counts()

# Remove unnecessary features
remove_cols = ['Unnamed: 0','Year_Birth', 'Kidhome', 'Teenhome',
               'MntCoke', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts','MntGoldProds',
               'NumDealsPurchases', 'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases',
               'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1', 'AcceptedCmp2',
               'Z_CostContact', 'Z_Revenue', 'Response']
dfcleaned.drop(columns=remove_cols, axis=1, inplace=True)
dfcleaned.shape

import matplotlib
from dython.nominal import associations
fig, ax = plt.subplots(figsize=(10, 8))
plt.tick_params(axis='both', which='major', labelsize=8)
matplotlib.rc('xtick', labelsize=8)
matplotlib.rc('ytick', labelsize=8)
plt.rcParams.update({'font.size': 8})
associations(dfcleaned, ax=ax, plot=False);

"""## Data Preparation"""

dfpre = dfcleaned.copy()

dfpre.info()

categorical_features = dfpre.select_dtypes(include=['object', 'category']).columns.tolist()

for col in categorical_features:
    print(f'value counts of column {col}')
    print(dfcleaned[col].value_counts())
    print('---'*10, '\n')

"""**LRFM Analysis**
Kolom yang akan dipilih berdasarkan LRFM degan metode reduce dimensionality:

L: Length (`DayAsMember`)  
R: Recency  (`Recency`)  
F: Frequency (`TotalTrx`)  
M: Monetary (`TotalSpending`)  
Additional: (`TotalAccCmp`)

## Feature Encoding and Scaling
"""

dfpre2 = dfpre.copy()

# Label Encoder - Education

mapping_education = {'SMA' : 0,
                     'D3' : 1,
                     'S1' : 2,
                     'S2' : 3,
                     'S3' : 4}

dfpre2['Edu_coded'] = dfpre2['Education'].map(mapping_education)

# One Hot Encoder
for cat in ['Marital_Status', 'Age_Group']:
    onehots = pd.get_dummies(dfpre2[cat], prefix=cat)
    dfpre2 = dfpre2.join(onehots)

dfselect = dfpre2.copy()

del_cols = ['ID','Education', 'Marital_Status', 'Dt_Customer', 'Age_Group', 'Income_Group', 'Trx_Group', 'Spending_Group']
dfselect.drop(columns=del_cols, axis=1, inplace=True)

dfselect.info()

from sklearn.preprocessing import StandardScaler

# Standardize the data
scaler    = StandardScaler()
n = dfselect.select_dtypes(["float64", "int64"]).columns
dfselect[n] = scaler.fit_transform(dfselect[n])

dfselect.describe()

dfselect.head(3)

"""## Modeling - Clustering

### Silhouette Score
"""

dfmodel = dfselect.copy()

# PCA and Visualization of Clusters

from sklearn.decomposition import PCA

pca = PCA(n_components=2)
pca.fit(dfmodel)
pcs = pca.transform(dfmodel)

df_pca = pd.DataFrame(data = pcs, columns = ['PC 1', 'PC 2'])
df_pca.head()

"""**Elbow Method**"""

from sklearn.cluster import KMeans

# Calculates inertia values for 2 to 10 clusters
inertia = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=123)
    kmeans.fit(dfmodel)
    inertia.append(kmeans.inertia_)


# Visualize inertia
sns.set_style('white')
plt.figure(figsize= (10, 5))
sns.lineplot(x= range(1, 11), y= inertia, marker='o', color = '#000087', linewidth = 3)
sns.scatterplot(x=range(1, 11), y=inertia, s=300, color='#800000',  linestyle='--')
plt.title('Visualization of Inertia')

# See the difference in inertia percentage for each additional cluster

((pd.Series(inertia) - pd.Series(inertia).shift(-1)) / pd.Series(inertia) * 100).dropna()

# Visualization with Distortion Score
from yellowbrick.cluster import KElbowVisualizer

# fit model
model = KMeans(random_state=123)
visualizer = KElbowVisualizer(model, metric='distortion', timings=True, locate_elbow=True)
visualizer.fit(df_pca)
visualizer.show()

"""From the elbow methodabove, it can be seen that the optimal number of clusters is 4 clusters.

### Cluster Evaluation
"""

from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=4, random_state=0).fit(df_pca)

clusters = kmeans.labels_

import matplotlib.pyplot as plt
from yellowbrick.cluster import SilhouetteVisualizer

fig, ax = plt.subplots(3, 2, figsize=(15,8))
for i in [2, 3, 4, 5, 6, 7]:
    '''
    Create KMeans instance for different number of clusters
    '''
    km = KMeans(n_clusters=i, init='k-means++', n_init=10, max_iter=100, random_state=42)
    q, mod = divmod(i, 2)
    '''
    Create SilhouetteVisualizer instance with KMeans instance
    Fit the visualizer
    '''
    visualizer = SilhouetteVisualizer(km, colors='yellowbrick', ax=ax[q-1][mod])
    visualizer.fit(df_pca)

# Visualize the Clusters Using Silhouette Visualizer
from yellowbrick.cluster import SilhouetteVisualizer

model = KMeans(4)
visualizer = SilhouetteVisualizer(model)

visualizer.fit(df_pca)
visualizer.show()

"""From the picture above, it can be seen that all clusters have good coefficient values. This means that the model created is very ideal."""

df_pca['Cluster'] = clusters
df_pca.sample(5)

# Visualization of cluster distribution
sns.set_style('white')
fig, ax = plt.subplots(figsize=(10,6))

sns.scatterplot(
    x='PC 1', y='PC 2',
    hue='Cluster',
    linestyle='--',
    data=df_pca,
    marker = 'o',
    palette=['#E63946', '#023E8A', '#FFBA08', '#03071E'],
    s=50,
    ax=ax
)

"""### Summary"""

# Assign cluster to dataset
dfpre.loc[:,'Cluster'] = kmeans.labels_
dfpre.sample(5)

features = ['Recency','TotalTrx','TotalSpending', 'TotalAccCmp', 'Cluster', 'CVR']
data_summary = dfpre[features]
round(data_summary.groupby('Cluster').agg(['mean', 'median', 'std']),2).round()

def dist_list(lst):
    plt.figure(figsize=[12, 6])
    i = 1
    for col in lst:
        ax = plt.subplot(2, 3, i)
        ax.vlines(dfpre[col].median(), ymin=-1, ymax=4, color='black', linestyle='--')
        g = dfpre.groupby('Cluster')
        x = g[col].median().index
        y = g[col].median().values
        ax.barh(x, y, color=['#003049', '#D62828', '#FCBF49', '#EAE2B7'])
        plt.title(col)
        i = i + 1

dist_list(['Recency','TotalTrx','TotalSpending', 'Income', 'CVR', 'Age'])
plt.tight_layout()
plt.show()

"""It looks like `Recency` doesn't have a big impact on differentiating the cluster because the gap between each cluster is low. We only know that cluster 0 has the biggest recency.  
Meanwhile, `Total Transactions` has a similar mean and median and we can conclude that clusters 0 and 3 are the highest. For other features, all the patterns seem similar where the most potential cluster in order are 0 > 3 > 2 > 1.

### Insight
"""

dfpre['Cluster'].value_counts().to_frame().reset_index().rename(columns={"index": "Cluster", "Cluster": "total_customers"})

cluster_by_age = dfpre.groupby(['Cluster', 'Age_Group'])['CVR'].mean()
cluster_by_age = cluster_by_age.unstack(level=0).fillna(0.0)
cluster_by_age.columns = ['Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3']
cluster_by_age

cluster_by_trx = dfpre.groupby(['Cluster', 'Trx_Group'])['ID'].count()
cluster_by_age = cluster_by_trx.unstack(level=0).fillna(0.0)
cluster_by_trx.columns = ['Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3']
cluster_by_trx

cluster_by_spending = dfpre.groupby(['Cluster', 'Spending_Group'])['ID'].count()
cluster_by_spending.columns = ['Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3']
cluster_by_spending