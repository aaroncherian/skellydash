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

def update_marker_buttons(marker, button_ids):

    # Use list comprehension to construct updated_classnames
    updated_classnames = [
        'btn btn-info' if button_id['index'] == marker else
        'btn btn-dark'
        for button_id in button_ids
    ]
    
    return updated_classnames

