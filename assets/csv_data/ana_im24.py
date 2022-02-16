#libraries
from pyexpat.errors import XML_ERROR_ABORTED
from winreg import QueryInfoKey
from numpy import true_divide
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore
from scipy import stats
import re

def quartiles (data,a,b):
   
    Q2 = np.quantile(data,float(a))
    Q3 = np.quantile(data,float(b))
    IQR = Q3 - Q2 
    return print('El Q2 es = {}, el Q3 es = {} y el IQR es ={}'.format(Q2,Q3,IQR))

#importing data
df = pd.read_csv('/Users/victorsoplat/Documents/2022/TBD/Scrapy_IM24/data/1001_im24_ii.csv')
# cleaning columns
df = df.replace('\n','',regex=True)
df = df.replace('\n\t\n\t\t','',regex=True)
df = df.replace('\n\t\n\t\t\n\n\t\t\t\n\n\t\t\t','',regex=True)
df = df.replace('\t\t\t','',regex=True)
df = df.replace('\t','',regex=True)
#cleaning the precio,superficie  column
precio = df['Precio'].str.split(' ',expand=True)
precio = precio.replace(',','', regex=True)
sup = df['Superficie'].str.split(' ',expand=True)
recamaras = df['Recamaras'].str.split(' ',expand=True)
df['Recamaras'] = recamaras[0]
df['sup'] = sup[0]
df['moneda'] = precio[0]
df['precio'] = precio[1]
# droping a column Precio
df.drop('Precio',axis=1,inplace=True)
df.drop('Palabras_clave',axis=1,inplace=True)
df.drop('publisherlogo_URL',axis=1,inplace=True)
#df.drop(df[df['precio']>70000],axis=1,inplace=True)
# tipo de anuncio 
df.rename(columns={'postingpills':'cat_anuncio','postingcardexpenses':'mantenimiento'},inplace=True)
# llenado de NaN
df['cat_anuncio']= df['cat_anuncio'].fillna('normal')
df['sup'] = df['sup'].fillna(0)
df['Recamaras'] = df['Recamaras'].fillna(0)
df['Info']= df['Info'].fillna('normal')
df['mantenimiento'] = df['mantenimiento'].fillna(0)
#cleaning mantenimiento columna
df['mantenimiento'] = df['mantenimiento'].replace('Mantenimiento','',regex=True)
df['mantenimiento'] = df['mantenimiento'].replace('\+ MN','',regex=True)
df['mantenimiento'] = df['mantenimiento'].replace(',','',regex=True)
df['Baños'] = df['Baños'].replace('baños','baño', regex=True)
df['Baños'] = df['Baños'].replace('None', 'nan', regex=True)
# changing data type 
df['precio'] = df.precio.astype(int)
df['mantenimiento'] = df.mantenimiento.astype(int)
df['sup'] = df.sup.astype(int)
df['Recamaras'] = df.Recamaras.astype(int)
# creating new column
df['$/sup'] = df['precio']/df['sup']

# Propiedades solo en MN - peso
df_mxn = df[df['moneda']=='MN']

quartiles_mxn = quartiles(df_mxn,0.25,0.75)



df_mxn['z_score']=stats.zscore(df_mxn['precio'])
df_mxn['z_score_sup']=stats.zscore(df_mxn['sup'])

df_mxn_outliers = df_mxn.loc[(df_mxn['z_score'].abs()<=3)&(df_mxn['z_score_sup'].abs()<=3)]

df_mxn_outliers.info()

df_mxn_out_iqr_sup = df_mxn_outliers[(df_mxn_outliers.sup>=70)&(df_mxn_outliers.sup<=215)]

colonias_interesadas = [' Granjas del Marqués, Acapulco de Juárez', ' Fraccionamiento Playa Diamante, Acapulco de Juárez',' Alfredo V Bonfil, Acapulco de Juárez',' Fraccionamiento Real Diamante, Acapulco de Juárez',' Plan de los Amates, Acapulco de Juárez',' Fraccionamiento Costa Azul, Acapulco de Juárez',' Fraccionamiento Granjas del Márquez, Acapulco de Juárez','Alfredo V Bonfil, Acapulco de Juárez','Fraccionamiento Real Diamante, Acapulco de Juárez','Fraccionamiento Playa Diamante, Acapulco de Juárez','Fraccionamiento Granjas del Márquez, Acapulco de Juárez','Fraccionamiento Costa Azul, Acapulco de Juárez','Granjas del Marqués, Acapulco de Juárez','Fraccionamiento Las Brisas, Acapulco de Juárez','Plan de los Amates, Acapulco de Juárez','Fraccionamiento Copacabana, Acapulco de Juárez','Fraccionamiento Club Deportivo, Acapulco de Juárez','Brisas del Marqués, Acapulco de Juárez','Fraccionamiento Marina Brisas, Acapulco de Juárez','Fraccionamiento Mayan Island, Acapulco de Juárez','La Cima, Acapulco de Juárez','Fraccionamiento Playa Guitarrón, Acapulco de Juárez','Fraccionamiento Farallón, Acapulco de Juárez','Renacimiento, Acapulco de Juárez' 'Miguel Alemán, Acapulco de Juárez','Icacos, Acapulco de Juárez','Fraccionamiento Puente del Mar, Acapulco de Juárez','Ejido Viejo, Acapulco de Juárez' 'Niños Héroes, Acapulco de Juárez','Club de golf 3 Vidas, Acapulco de Juárez','Fraccionamiento Puerto Marqués, Acapulco de Juárez','Fraccionamiento Pichilingue, Acapulco de Juárez','Lomas de Costa Azul, Acapulco de Juárez']

mercado_renta = df_mxn[df_mxn['Localización'].isin(colonias_interesadas)]

mercado_renta.describe()

mercado_renta.precio.hist(bins=50)
plt.show()

Q1_mer = np.quantile(mercado_renta.precio, 0.25)
Q3_mer = np.quantile(mercado_renta.precio, 0.75)
IQR_mer = Q3_mer - Q1_mer
print(Q1_mer,Q3_mer, IQR_mer)

# GRAPHIC EDA
_= sns.boxplot(x='precio',data=mercado_renta)
_= plt.xlabel('Precio')
plt.show()

_= sns.scatterplot(x='precio',y='sup',data=mercado_renta, alpha = 0.2)

_=plt.xlabel('Precio de renta')
_=plt.ylabel('m2 de departamentos')
_= plt.show()

quartiles(mercado_renta.sup,0.25,0.75)
quartiles(mercado_renta.precio,0.25,0.75)