

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

__all__ = ['plot_project_stat_cap', 'plot_plant_type_cap',  'plot_sunburst', 'plot_timelines', 'plot_conn_capa_dist_by_status_host']


def plot_project_stat_cap(df):
    status_proj_cap = df.groupby(["Project Status", "HOST TO"]).agg({"Connection Cap (MW)": "sum",
                                                                     "Project Name": "count"})
    
    
    
    
    
def plot_conn_capa_dist_by_status_host(df: pd.DataFrame):
    """
    Plot the distribution of connection capacity by project status and HOST TO using pie charts.

    Parameters:
    
        df (DataFrame): A dataframe containing at least the following columns:
                       'Connection Cap (MW)', 'Project Status', and 'HOST TO'.

    Returns:
    
        plotly.graph_objs.Figure: A Plotly figure containing two pie charts:
                               one for Connection capacity by project status and
                               another for connection capacity by HOST TO.
    """
    def create_hover_text(row, primary_col, secondary_col):
        hover_text = f"<b>{row[primary_col]}</b><br>"
        hover_text += f"<b>Total:</b> {row['Total']:.2f} MW<br>"
        for status in sorted(df[secondary_col].unique()):
            if status in row.index and row[status] > 0:  # Only show non-zero values
                hover_text += f"<b>{status}:</b> {row[status]:.2f} MW<br>"
        return hover_text

    def create_pie_df(primary_col: str, secondary_col: str):
        # Prepare the df for the pie chart
        proj_cap = df.groupby(primary_col)['Connection Cap (MW)'].sum().reset_index()
        proj_cap = proj_cap.rename(columns={'Connection Cap (MW)': 'Total'})

        # Create a pivot table for secondary df
        secondary_df = df.pivot_table(values='Connection Cap (MW)',
                                        index=primary_col,
                                        columns=secondary_col,
                                        aggfunc='sum',
                                        fill_value=0)

        # Merge the pivot table with proj_cap
        proj_cap = pd.merge(proj_cap, secondary_df, left_on=primary_col, right_index=True)

        # Create hover text
        proj_cap['hover_text'] = proj_cap.apply(lambda row: create_hover_text(row, primary_col, secondary_col), axis=1)

        return proj_cap

    # Create df for both pie charts
    status_df = create_pie_df('Project Status', 'HOST TO')
    host_to_df = create_pie_df('HOST TO', 'Project Status')

    # Create subplots
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                        subplot_titles=('Connection Capacity by Project Status', 'Connection Capacity by HOST TO'))

    # Add traces for both pie charts
    fig.add_trace(go.Pie(labels=status_df['Project Status'], 
                        values=status_df['Total'], 
                         rotation=-110,
                        name='Project Status',
                        hole=0.45,
                        hoverinfo='text',
                        text=status_df['hover_text'],
                        textinfo='percent+label',
                        hovertemplate='%{text}<extra></extra>'), 1, 1)

    fig.add_trace(go.Pie(labels=host_to_df['HOST TO'], 
                        values=host_to_df['Total'], 
                        name='HOST TO',
                        hole=0.45,
                        hoverinfo='text',
                        text=host_to_df['hover_text'],
                        textinfo='percent+label',
                        hovertemplate='%{text}<extra></extra>'), 1, 2)

    # Update layout
    fig.update_layout(
        title_text='Connection Capacity Distribution',
        width=1000,
        height=600,
        legend=dict(orientation='h', yanchor='bottom', y=-0.1, xanchor='center', x=0.5),
    )

    # Update trace settings
    fig.update_traces(textposition='auto', textfont_size=10)

    return fig


def plot_timelines(df):
    """
    Create a scatter plot showing the timeline of connection capacity, projects, plant types, and MW change.

    Parameters:
    
        df (pd.DataFrame): A DataFrame containing at least the following columns:
                       'Connection Date', 'HOST TO', 'Connection Cap (MW)', 
                       'Project Name', 'Plant Type', and 'MW Change'.

    Returns:
        
        plotly.express.scatter: A Plotly scatter plot visualizing the data over time.
    """
    # Grouping the df by 'Connection Date'
    time_group = df.groupby(['Connection Date', 'HOST TO']).agg({
                                                                'Connection Cap (MW)': 'sum',
                                                                'Project Name': 'count',
                                                                'Plant Type': 'nunique',
                                                                'MW Change': 'sum'
                                                            }).reset_index()

    # Create a scatter plot
    timeline_plot = px.scatter(data_frame=time_group,
                               x='Connection Date',
                               y='Connection Cap (MW)',
                               size='Project Name',  
                               hover_name='Connection Date', 
                               color='HOST TO',
                               hover_data={
                                    'Project Name': True,
                                    'Plant Type': True,
                                    'MW Change': True},
                                
                                title='Timeline of Connection Capacity, Projects, Plant Types, and MW Change',
                                labels={
                                    'Connection Cap (MW)': 'Total Entry Capacity (MW)',
                                    'MW Change': 'Total MW Change',
                                    'Project Name': 'Number of Projects',
                                    'Plant Type': 'Unique Plant Type'
                                },
                                template='plotly_white'
                            )

    # Update layout for improved aesthetics
    timeline_plot.update_layout(yaxis_title='Total Connection Capacity (MW)',
                                xaxis_title='Connection Date',
                                legend_title='HOST TO',
                                showlegend=True
                              )
    return timeline_plot





def plot_sunburst(df):
    """
    Create a sunburst chart to visualize connection capacity by HOST TO, plant type, and project status.

    Parameters:
        
        df (pd.DataFrame): A DataFrame containing at least the following columns:
                       'Connection Cap (MW)', 'HOST TO', 'Plant Type', 
                       'Project Status', and 'Project Name'.

    Returns:
        
        plotly.express.sunburst: A Plotly sunburst chart visualizing connection capacity.
    """
    colors = ["#800080", "#2B5D18", "#FFD700", "#2CFF05"]
    sun = px.sunburst(
                    data_frame=df,
                    values="Connection Cap (MW)",
                    color="HOST TO",
                    color_discrete_sequence=colors * (df.shape[0] // 4 + 1),
                    path=["HOST TO", "Plant Type", "Project Status"],
                    hover_data=["Project Name", "Connection Cap (MW)"],
                    width=800,
                    height=800,
                    title="Connection Capacity by Host TO, Plant Type, and Project Status. (click to Expand)",
                )

    return sun



def plot_plant_type_cap(df: pd.DataFrame):
    """
    Create a bar chart visualizing connection capacity by plant type and HOST TO.

    Parameters:
        
        df (pd.DataFrame): A DataFrame containing at least the following columns:
                       'Plant Type', 'HOST TO', and 'Connection Cap (MW)'.

    Returns:
        
        plotly.graph_objs.Figure: A Plotly bar chart showing the distribution of connection capacity.
    """
    capacity_by_TO_plant = df.pivot_table(
                                        index="Plant Type",
                                        columns="HOST TO",
                                        values="Connection Cap (MW)",
                                        fill_value=0,
                                        aggfunc="sum",
                                        )
    
    unpivot_capacity_by_TO_plant = (capacity_by_TO_plant
                                    .reset_index()
                                    .melt(id_vars="Plant Type",
                                        value_name="Connection Cap (MW)",
                                        var_name="HOST TO"))
    
    fig = px.bar(data_frame=unpivot_capacity_by_TO_plant.sort_values(by="HOST TO"),
                 x="Plant Type",
                 y="Connection Cap (MW)",
                 color="HOST TO",
                color_continuous_scale=px.colors.diverging.RdBu_r,
                height=900,
    )
    
    fig.update_layout(
        title={
            'text': "Connection Capacity by Plant Type and Host TO",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24}
        }
    )
    return fig