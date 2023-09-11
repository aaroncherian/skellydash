import json
import dash
import plotly.express as px
from dash import dcc

# Function to determine the selected marker based on the inputs
def get_selected_marker(input_id, clickData, selected_marker):
    # If a marker button was clicked, use its index as the selected marker
    if 'marker-button' in input_id:
        marker = json.loads(input_id)['index']
    # If a marker was clicked in the main graph, use its ID as the selected marker
    elif clickData is not None and 'points' in clickData and len(clickData['points']) > 0 and 'id' in clickData['points'][0]:
        #check if click data exists, and that click data contains the 'points' key, and the 'id' key
        marker = clickData['points'][0]['id']
    # Otherwise, use the currently selected marker
    else:
        marker = selected_marker
    
    return marker

def update_marker_buttons(marker, button_ids, hoverData):
    # Check if hoverData is valid and contains point information
    hover_condition = (hoverData is not None and 'points' in hoverData and  
                       len(hoverData['points']) > 0 and 'id' in hoverData['points'][0])
    
    # Use list comprehension to construct updated_classnames
    updated_classnames = [
        'btn btn-warning' if button_id['index'] == marker else
        'btn btn-info' if hover_condition and button_id['index'] == hoverData['points'][0]['id'] else
        'btn btn-dark'
        for button_id in button_ids
    ]
    
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