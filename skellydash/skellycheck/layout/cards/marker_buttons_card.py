import dash_bootstrap_components as dbc
from dash import html

from.create_card import create_card

def get_marker_buttons_card(marker_list, color_of_cards):
    content = [
        dbc.Row([
            dbc.Col([
                html.Div(
                    id='marker-list',
                    children=marker_list,
                    style={'display': 'flex', 'flexWrap': 'wrap'}
                )
            ])
        ])
    ]
    return create_card("Marker List", content, color_of_cards)