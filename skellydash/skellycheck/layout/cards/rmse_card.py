from dash import html
from .create_card import create_card

def get_rmse_card(gauges):
    content = [
        html.Div(
            id='rmse-gauges',
            children=gauges,
            style={'display': 'flex'}
        )
    ]
    return create_card("RMSE", content, None)