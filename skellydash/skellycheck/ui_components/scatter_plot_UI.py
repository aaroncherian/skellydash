from data_utils.sample_data import subsample_dataframe
from plotting_utils import create_3d_scatter_from_dataframe

def create_3d_figure_from_subsampled_data(dataframe_of_3d_data, frame_skip_interval, color_of_cards):
    """Create marker figure with subsampled data"""
    subsampled_dataframe = subsample_dataframe(dataframe=dataframe_of_3d_data, frame_skip_interval=frame_skip_interval)
    scatter_plot_3d_figure = create_3d_scatter_from_dataframe(dataframe_of_3d_data=subsampled_dataframe)
    scatter_plot_3d_figure.update_layout(paper_bgcolor=color_of_cards, plot_bgcolor=color_of_cards)
    return scatter_plot_3d_figure

