from .scatter_plot_UI import create_3d_figure_from_subsampled_data
from .indicators import create_indicators_ui
from .marker_buttons_list import create_marker_buttons
from plotting.rmse_joint_plot import create_rmse_joint_bar_plot


def prepare_dashboard_elements(dataframe_of_3d_data, rmse_error_dataframe, frame_skip_interval, color_of_cards):
    """Prepare the figures and components for the Dash app layout."""
    scatter_3d_figure = create_3d_figure_from_subsampled_data(dataframe_of_3d_data, frame_skip_interval, color_of_cards)
    indicators = create_indicators_ui(rmse_error_dataframe)
    marker_buttons_list = create_marker_buttons(dataframe_of_3d_data)
    joint_rmse_plot = create_rmse_joint_bar_plot(rmse_error_dataframe)

    return scatter_3d_figure, indicators, marker_buttons_list, joint_rmse_plot
