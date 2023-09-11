import json
import dash
import plotly.express as px
from dash import dcc

def get_selected_marker(input_id, clickData, hoverData, selected_marker):
    if 'marker-button' in input_id:
        marker = json.loads(input_id)['index']
    elif clickData is not None and 'points' in clickData and len(clickData['points']) > 0 and 'id' in clickData['points'][0]:
        marker = clickData['points'][0]['id']
    else:
        marker = selected_marker
    
    return marker

def update_marker_buttons(marker, button_ids, hoverData):
    updated_classnames = []
    for button_id in button_ids:
        if button_id['index'] == marker:
            updated_classnames.append('btn btn-warning')
        elif hoverData is not None and 'points' in hoverData and len(hoverData['points']) > 0 and 'id' in hoverData['points'][0] and button_id['index'] == hoverData['points'][0]['id']: 
            updated_classnames.append('btn btn-info')  
        else:
            updated_classnames.append('btn btn-dark')
    
    return updated_classnames

def create_trajectory_plots(marker, dataframe_of_3d_data, color_of_cards):
    df_marker = dataframe_of_3d_data[dataframe_of_3d_data.marker == marker]
    
    trajectory_plot_height = 350
    # Your plotting code here. For demonstration, using placeholders.
    fig_x = px.line(df_marker, x='frame', y='x', color='system', color_discrete_map={'freemocap': 'blue', 'qualisys': 'red'})
    fig_y = px.line(df_marker, x='frame', y='y', color='system', color_discrete_map={'freemocap': 'blue', 'qualisys': 'red'})
    fig_z = px.line(df_marker, x='frame', y='z', color='system', color_discrete_map={'freemocap': 'blue', 'qualisys': 'red'})

    fig_x.update_xaxes(title_text='', showticklabels=False)
    fig_x.update_yaxes(title_text='X', title_font=dict(size=18))
    fig_x.update_layout(paper_bgcolor=color_of_cards)

    fig_y.update_xaxes(title_text='', showticklabels=False)
    fig_y.update_yaxes(title_text='Y', title_font=dict(size=18))
    fig_y.update_layout(paper_bgcolor=color_of_cards, height=trajectory_plot_height)

    fig_z.update_xaxes(title_text='Frame', title_font=dict(size=18))
    fig_z.update_yaxes(title_text='Z', title_font=dict(size=18))
    fig_z.update_layout(paper_bgcolor=color_of_cards, height=trajectory_plot_height)

    # Return the list of Plotly figures
    return [dcc.Graph(figure=fig_x), dcc.Graph(figure=fig_y), dcc.Graph(figure=fig_z)]