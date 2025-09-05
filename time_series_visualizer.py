import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
# Import dos dados e setagem do índice para a coluna 'date' e conversao da coluna 'date' para datetime
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date') 

# Clean data
#limpeza dos dados removendo os outliers (2.5% mais baixos e 2.5% mais altos) com base nos quarizes dos dados
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15,5)) # cria uma figura e um eixo com tamanho de 15x5
    ax.plot(df.index, df['value'], color='red', linewidth=1) # plota os dados no eixo com linha vermelha e largura 1
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019') # define o título do gráfico
    ax.set_xlabel('Date') # define a label do eixo x
    ax.set_ylabel('Page Views') # define a label do eixo y

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy() # cria uma cópia do DataFrame original
    df_bar['year'] = df_bar.index.year # extrai o ano do índice (data) e cria uma nova coluna 'year'
    df_bar['month'] = df_bar.index.month # extrai o mês do índice (data) e cria uma nova coluna 'month'
    #Faz o agrupamento de todos os dados por ano e mês, calculando a média dos valores de page views para cada grupo
    #Em seguida, reorganiza o DataFrame para que os anos sejam as linhas e os meses sejam as colunas através do método unstack()
    #Esse método "desempilha" o nível do índice especificado (neste caso, 'month') e o transforma em colunas.
    df_bar = df_bar.groupby(["year", "month"])["value"].mean().unstack()

    # Draw bar plot

    fig = df_bar.plot(kind='bar', figsize=(10,7)).figure # cria um gráfico de barras a partir do DataFrame df_bar com tamanho 10x7
    plt.xlabel('Years') # define a label do eixo x
    plt.ylabel('Average Page Views') # define a label do eixo y
    
    # Adiciona uma legenda com os nomes dos meses
    plt.legend(title='Months', labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    plt.title('Average Daily Page Views per Month') # define o título do gráfico
    plt.tight_layout() # ajusta o layout para evitar sobreposição de elementos

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))       # 1- Cria uma figura com 2 subplots lado a lado

    # boxplot por ano (Trend)
    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])  # 2 - define o primeiro subplot como um boxplot de 'year' vs 'value'
    axes[0].set_title("Year-wise Box Plot (Trend)")       # 3 - define o título do primeiro subplot
    axes[0].set_xlabel("Year")                            # 4 - define o rótulo do eixo x do primeiro subplot
    axes[0].set_ylabel("Page Views")                      # 5 - define o rótulo do eixo y do primeiro subplot

    # boxplot por mês (Seasonality)
    # quando o Seaborn faz o boxplot, ele ordena os meses alfabeticamente (Apr, Aug, Dec, …),
    # ou mantém a ordem como aparecem no DataFrame e nesse caso está começando em Maio porque os dados começam em 2016-05.

    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] # definindo a ordem correta dos meses

    # 6 - define o segundo subplot como um boxplot de 'month' vs 'value'
    sns.boxplot(x="month", y="value", data=df_box, ax=axes[1], order=month_order)
    axes[1].set_title("Month-wise Box Plot (Seasonality)")     # 7 - define o título do segundo subplot
    axes[1].set_xlabel("Month")                                # 8 - define o rótulo do eixo x do segundo subplot
    axes[1].set_ylabel("Page Views")                           # 9 - define o rótulo do eixo y do segundo subplot

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
