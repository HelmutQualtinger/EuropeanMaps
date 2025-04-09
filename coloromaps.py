import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.colors
import numpy as np

# Get the list of all built-in named continuous colorscales
colorscale_names = plotly.colors.named_colorscales()

# --- Visualization ---

# Create gradient data (a simple ramp from 0 to 1)
gradient = np.linspace(0, 1, 256)
z = np.array([gradient]) # Reshape to 2D for heatmap

# Determine number of rows needed for the subplots
n_rows = len(colorscale_names)//5+1

# Create subplots: one row for each colorscale
fig = make_subplots(rows=n_rows, cols=5,
                    # subplot_titles=colorscale_names, # Option 1: Titles above
                    vertical_spacing=0.00 # Adjust spacing
                   )

# Add a heatmap trace for each colorscale
for i, name in enumerate(colorscale_names):
    fig.add_trace(
        go.Heatmap(
            z=z,
            colorscale=name,
            showscale=False # Hide the individual colorbars for each heatmap
        ),
        row=(i//5) + 1, col=(i%5)+1 # Calculate row and column for the subplot
    )
    # Add the name as an annotation on top of each heatmap
    fig.add_annotation(
        xref=f"x{i+1}", yref=f"y{i+1}", # Reference both axes of the current subplot
        x=0.5,  # Center horizontally within the subplot
        y=0.9,  # Position slightly above the subplot
        text=f"<b>{name}</b>", # The name of the colorscale
        showarrow=False,
        xanchor="center", # Center-align horizontally
        yanchor="bottom", # Bottom-align vertically
        font=dict(size=14)
    )

# Update layout for a cleaner look
fig.update_layout(
    title_text='Built-in Continuous Plotly Colormaps',
    height=70 * n_rows + 50, # Adjust height based on number of colormaps
    width=1400,
    margin=dict(l=150, r=20, t=50, b=20), # Adjust left margin for names
    hovermode=False # Disable hover info for this visualization
)

# Hide all axes ticks and labels for the heatmaps
fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False)
fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False, ticks="")


fig.show()

# Optional: Print the list of names to the console
# print("Available continuous colorscale names:")
# for name in colorscale_names:
#     print(f"- {name}")