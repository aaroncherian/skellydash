from .create_card import create_card
from dash import dcc

def get_joint_rmse_plot_card(joint_rmse_figure, color_of_cards):
    content = [dcc.Graph(id='joint-rmse-figure', figure=joint_rmse_figure)]
    return create_card("Joint RMSE", content, color_of_cards)