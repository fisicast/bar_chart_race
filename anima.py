#Iniciando Bibliotecas
import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML
from datetime import datetime
import matplotlib
import matplotlib.animation as animation
from matplotlib import rcParams
import numpy as np

#organizando o dataframe
def arruma_data(df):
    for i in range(len(df)):
        str_date = df['Time (UTC)'][i]
        url = re.sub(str_date[-9:], '', str_date)
        date = datetime.strptime(url, '%m/%d/%Y').date()
        df.at[i, 'Time (UTC)'] = date

    return df
def organiza(dados, df):
    for i in range(len(dados)):
        for j in range(len(df)):
            if dados['Time'][i] == df['Time (UTC)'][j]:
                return i
                
                
df = pd.read_csv("#001.csv", names = None)
df = arruma_data(df)
dados = pd.DataFrame(df['Time (UTC)'].values, columns = ['Time'])


for index in range(33):
    if index < 9:
        filename = '#00'+ str(index+1)
    else:
        filename = '#0' + str(index+1)
        
    d = pd.read_csv(filename + '.csv', names = None)
    d = arruma_data(d)
    i = organiza(dados, d)

    dados.at[i:, filename] = d['Plays'].values

#Titulo dos episodios
epi_name = ['3 minutos (p1)', '3 minutos (p2)','3 minutos (p3)',
           'Teoria Atômica', '1ª Lei de Newton', '2ª Lei de Newton',
           '3ª Lei de Newton', 'Cinemática (p1)', 'Cinemática (p2)',
           'Teorema de Noether', 'Especial dia do Físico', 'Estatística',
           'Física de Partículas (p1)', 'Física de Partículas (p2)',
           'Eletromagnetismo (p1)', 'Relatividade Geral (p1)','Eletromagnetismo (p2)',
           'Motivos', 'Chernobyl', 'Nobel','Termodinâmica', 
            "Financiamento", "Mecânica Quântica", 'Graduação', "Relatividade Geral (p2)",
           'O Fim do Universo', 'Colab FMC', 'Mulheres na Física', 'Físicos no Mercado',
            "Nanotecnologia",'Covid','Estrutura da Matéria','Divulgação']
			
#dados semanais			
dates = df['Time (UTC)']
dados=dados.fillna(0)
orig = dados
dados = dados.transpose()
dados.rename(columns = dados.iloc[0], inplace = True)
dados.drop(['Time'], inplace = True)
dados.at[:,'Episodio'] = epi_name
dados.reset_index(inplace = True)

#dados semanais cumulativos
o = orig.drop(columns=['Time'])
s_dados = o.cumsum()
s_dados = s_dados.transpose()
s_dados.rename(columns = dates, inplace = True)
s_dados.at[:,'Episodio'] = epi_name
s_dados.reset_index(inplace = True)

#lista de cores
c = ['lightblue','#7CB9E8','#C0E8D5','#B284BE','#72A0C1','#EDEAE0',
'#F0F8FF','#C46210','#EFDECD','#E52B50','#9F2B68','#F19CBB',
'#AB274F','#D3212D','#3B7A57','#FFBF00','#FF7E00','#9966CC',
'#A4C639','#CD9575','#665D1E','#915C83','#841B2D','#FAEBD7',
'#008000','#8DB600','#FBCEB1','#00FFFF','#7FFFD4','#D0FF14',
'#4B5320','#8F9779','C0']

colores = dict(zip(epi,c))


#função para fazer o gráfico
epi = dados['index'].values.tolist()
mes = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']

def draw_barchart(date):
    matplotlib.rcParams.update({'font.size': 22})
    rcParams['font.family'] = 'serif'
#    rcParams['font.sans-serif'] = ['Lucida Grande']
    ax.clear()
    dff = s_dados.sort_values(by=date, ascending=False)
    dff.reset_index(drop=True, inplace = True)
    x = dff[:10]
    x = x[::-1]

    idx = dates.index[dates == date]
    cor = [0 for i in range(10)]
    for c in range(10):
        #print(x['index'][c],colores[x['index'][c]])
        cor[c] = colores[x['index'][c]]
    
    ax.barh(x['index'], x[date], color = cor[::-1], alpha = 0.5)
    #ax.text(1, 0.6, 'Semana '+ str(idx.values[0]+1),  transform=ax.transAxes, color='#777777', size=46, ha='right', weight=800)
    ax.text(1, 0.5, mes[date.month-1] + ' ' + str(date.year),  transform=ax.transAxes, color='#777777', size=46, ha='right', weight=800)
    ax.text(0, 1.08, 'Evolução do número total de plays por episódio',
            transform=ax.transAxes, size=24, weight=600, ha='left')
    for i, (value, number,name) in enumerate(zip(x[date], x['Episodio'],x['index'])):
        if value != 0:
            ax.text(value, i,   name + ": " + number,size=16, weight=600, ha='right', va='center')  # Tokyo: name
            #ax.text(value, i,   name ,size=16, weight=500, ha='right', va='bottom')  # Tokyo: name
            ax.text(value, i,     '  '+ str(value),  size=14, ha='left',  va='top')   # 38194.2: value

    
    ax.set_xlabel('Plays', fontsize =  25)
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=15)
    ax.set_yticks([])
    plt.box(False)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)

#animação
fig, ax = plt.subplots(figsize=(15, 8))
Writer = animation.writers['ffmpeg']
writer = Writer(fps=1, metadata=dict(artist='Me'), bitrate=1800)


animator = animation.FuncAnimation(fig, draw_barchart, frames=dates) #dates são todas as datas
animator.save('im.mp4', writer=writer)
HTML(animator.to_jshtml())
# or use animator.to_html5_video() or animator.save()
