import plotly.express as px
from dash import dcc
import plotly.graph_objects as go

def create_gauge_plot(value, title):
    fig = go.Figure(go.Indicator(
        mode="number",
        value=value,
        title={'text': title},
        ))
    fig.update_layout(margin=dict(l=10, r=10, b=10, t=20))
    return fig

# Function to create a marker figure from a dataframe




def create_3d_scatter_from_dataframe(dataframe_of_3d_data, ax_range=1200):
    x_mean = dataframe_of_3d_data["x"].mean()
    y_mean = dataframe_of_3d_data["y"].mean()
    z_mean = dataframe_of_3d_data["z"].mean()

    fig = px.scatter_3d(dataframe_of_3d_data, x="x", y="y", z="z", 
                        animation_frame="frame",
                        animation_group="marker",
                        color="system",
                        color_discrete_map={'freemocap': 'blue', 'qualisys': 'red'},
                        hover_name="marker",
                        hover_data=["x", "y", "z"],
                        range_x=[x_mean - ax_range, x_mean + ax_range], 
                        range_y=[y_mean - ax_range, y_mean + ax_range],
                        range_z=[z_mean - ax_range, z_mean + ax_range]
    )
    fig.update_layout(
        scene_aspectmode='cube',
        autosize=False,
        height=1000,
        width=1100,
        margin={"t": 1, "b": 1, "l": 1, "r": 1},
    )
    return fig


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



def create_rmse_bar_plot(df):
    dimensions = ['x_error', 'y_error', 'z_error']
    figures = {}
    
    for dim in dimensions:
        filtered_df = df[(df['dimension'] == 'Per Joint') & (df['coordinate'] == dim)]
        fig = go.Figure(data=[
            go.Bar(name=dim, x=filtered_df['marker'], y=filtered_df['RMSE'])
        ])
        fig.update_layout(
            title=f'RMSE for each marker ({dim})',
            xaxis_title='Marker',
            yaxis_title='RMSE Value'
        )
        figures[dim] = fig
    
    return figures


def create_error_plots(marker, absolute_error_dataframe, color_of_cards):
    df_marker = absolute_error_dataframe[absolute_error_dataframe.marker == marker]

    trajectory_plot_height = 500
    
    # Your plotting code for X, Y, and Z error over frames.
    fig_x = px.line(df_marker, x='frame', y='x_error', title='X Error over Time')
    fig_y = px.line(df_marker, x='frame', y='y_error', title='Y Error over Time')
    fig_z = px.line(df_marker, x='frame', y='z_error', title='Z Error over Time')
    
    fig_x.update_xaxes(title_text='', showticklabels=False)
    fig_x.update_yaxes(title_text='X', title_font=dict(size=18))
    fig_x.update_layout(paper_bgcolor=color_of_cards)

    fig_y.update_xaxes(title_text='', showticklabels=False)
    fig_y.update_yaxes(title_text='Y', title_font=dict(size=18))
    fig_y.update_layout(paper_bgcolor=color_of_cards, height=trajectory_plot_height)

    fig_z.update_xaxes(title_text='Frame', title_font=dict(size=18))
    fig_z.update_yaxes(title_text='Z', title_font=dict(size=18))
    fig_z.update_layout(paper_bgcolor=color_of_cards, height=trajectory_plot_height)

    
    return [dcc.Graph(figure=fig_x), dcc.Graph(figure=fig_y), dcc.Graph(figure=fig_z)]