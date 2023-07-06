import plotly.express as px

#func to plot interactive plot chart

def interactive_plot(df):
    fig = px.line()
    for i in df.columns[1:]:
        fig.add_scatter(x= df['Date'],y=df[i],name = i)
    fig.update_layout(width = 450, margin = dict(l=20,r=20,t=50,b=20),legend = dict(orientation = 'h', yanchor = 'bottom', y = 1.02, xanchor = 'right',x = 1))
    return fig

# func to normalise the prices based on the initail price
def normalise(df_2):
    df = df_2.copy()
    for i in df.columns[1:]:
        df[i]= df[i]/df[i][0]
    return df

#calculate daily returns

def daily_returns(df):
    df_dr = df.copy()
    for i in df.columns[1:]:
        for j in range(1,len(df)):
            df_dr[i][j] = (df[i][j]-df[i][j-1]/df[i][j-1])*100
    df_dr[i][0]=0
    return df_dr

# Calculating beta

def calculate_beta(stocks_daily_return,stock):
    rm = stocks_daily_return['sp500']
     
