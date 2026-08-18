import plotly.express as px
import plotly.graph_objects as go

def plot_allocation(labels, values):
    fig = px.pie(
        names=labels, 
        values=values, 
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        showlegend=True
    )
    return fig

def plot_gains_losses(tickers, pnl_values):
    colors = ['green' if val >= 0 else 'red' for val in pnl_values]
    
    fig = go.Figure(data=[
        go.Bar(
            x=tickers,
            y=pnl_values,
            marker_color=colors,
            text=[f"${v:.2f}" for v in pnl_values],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        margin=dict(t=20, b=20, l=0, r=0),
        xaxis_title="Stock",
        yaxis_title="Profit/Loss ($)",
        template="plotly_white"
    )
    return fig
