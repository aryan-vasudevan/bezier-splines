import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Global variables to store control points and state
# Start with cubic Bézier (degree 3 = 4 control points)
control_points = [
    np.array([1.0, 1.0]),
    np.array([2.0, 3.0]),
    np.array([4.0, 3.0]),
    np.array([5.0, 1.0])
]

# Variables for dragging functionality
dragging_point = None
point_circles = []

# Store references to matplotlib objects
fig = None
ax = None
increase_button_ax = None
decrease_button_ax = None
increase_button = None
decrease_button = None


def de_casteljau_general(control_points, t):
    # Make a copy of control points to avoid modifying the original
    # We'll work with this list and reduce it level by level
    points = [np.array(p) for p in control_points]
    
    # Number of levels we need = number of control points - 1
    # For cubic (4 points): 3 levels
    # For quadratic (3 points): 2 levels
    # For linear (2 points): 1 level
    num_levels = len(points) - 1
    
    # Perform de Casteljau's algorithm level by level
    for level in range(num_levels):
        # Create a new list for the next level
        next_level_points = []
        
        # The current level has (len(points)) points
        # The next level will have (len(points) - 1) points
        # We get each new point by linear interpolation between consecutive pairs
        for i in range(len(points) - 1):
            # Linear interpolation between points[i] and points[i+1]
            # Formula: new_point = (1 - t) * point_a + t * point_b
            new_point = (1 - t) * points[i] + t * points[i + 1]
            next_level_points.append(new_point)
        
        # Move to the next level
        points = next_level_points
    
    # After all levels, we should have exactly one point
    # This is the point on the Bézier curve at parameter t
    return points[0]


def generate_bezier_curve(control_points, num_points=100):
    curve_points = []
    
    # Generate points by varying t from 0 to 1
    for i in range(num_points):
        t = i / (num_points - 1)  # Parameter from 0 to 1
        point = de_casteljau_general(control_points, t)
        curve_points.append(point)
    
    return np.array(curve_points)


def get_degree():
    return len(control_points) - 1


def draw_scene():
    ax.clear()
    
    degree = get_degree()
    
    # Draw the control polygon (straight lines connecting control points)
    control_x = [p[0] for p in control_points]
    control_y = [p[1] for p in control_points]
    ax.plot(control_x, control_y, 'b--', linewidth=1, alpha=0.5, label='Control Polygon')
    
    # Generate and draw the Bézier curve
    curve = generate_bezier_curve(control_points, num_points=100)
    ax.plot(curve[:, 0], curve[:, 1], 'r-', linewidth=2, label=f'Bézier Curve (degree {degree})')
    
    # Draw control points as circles
    point_circles.clear()
    
    for i, point in enumerate(control_points):
        # Endpoints in green, internal control points in blue
        if i == 0 or i == len(control_points) - 1:
            color = 'green'
            marker_size = 12
        else:
            color = 'blue'
            marker_size = 10
        
        # Draw the point
        circle = ax.plot(point[0], point[1], 'o', color=color, 
                        markersize=marker_size, picker=5)[0]
        point_circles.append(circle)
        
        # Add label showing the point index
        ax.text(point[0], point[1] + 0.2, f'P{i}', 
               ha='center', fontsize=10, fontweight='bold')
    
    # Set axis properties
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 4)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right')
    
    # Create title with degree information
    degree_name = {
        1: "Linear",
        2: "Quadratic", 
        3: "Cubic",
        4: "Quartic",
        5: "Quintic",
        6: "Sextic",
        7: "Septic",
        8: "Octic"
    }
    curve_type = degree_name.get(degree, f"Degree {degree}")
    
    ax.set_title(f'{curve_type} Bézier Curve ({len(control_points)} control points)\n' +
                'Drag points to modify | Use buttons to change degree', 
                fontsize=11, fontweight='bold')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    
    plt.draw()


def increase_degree(event):
    # Get the current last point
    last_point = control_points[-1]
    second_last_point = control_points[-2]
    
    # Insert a new control point before the last point
    # Position it as an average of the last two points, slightly offset
    new_point = (second_last_point + last_point) / 2.0
    new_point[1] += 0.5  # Offset upward slightly
    
    # Insert the new point before the last control point
    control_points.insert(-1, new_point)
    
    # Redraw the scene
    draw_scene()


def decrease_degree(event):
    # Need at least 2 points for a curve (degree 1, linear)
    if len(control_points) <= 2:
        print("Cannot decrease degree below 1 (minimum 2 control points)")
        return
    
    # Remove the second-to-last control point
    # This keeps the endpoints intact
    control_points.pop(-2)
    
    # Redraw the scene
    draw_scene()

def on_press(event):
    global dragging_point
    
    if event.inaxes != ax:
        return
    
    # Check which point (if any) was clicked
    for i, point in enumerate(control_points):
        # Calculate distance from click to point
        distance = np.sqrt((event.xdata - point[0])**2 + (event.ydata - point[1])**2)
        
        # If click is close enough to a point, start dragging it
        if distance < 0.2:
            dragging_point = i
            break


def on_motion(event):
    global dragging_point
    
    # Only process if we're dragging a point and mouse is in the correct axes
    if dragging_point is None or event.inaxes != ax:
        return
    
    # Update the position of the dragged control point
    control_points[dragging_point][0] = event.xdata
    control_points[dragging_point][1] = event.ydata
    
    # Redraw the scene with updated control points
    draw_scene()


def on_release(event):
    global dragging_point
    dragging_point = None

# Create figure and main axis for the Bézier curve
fig = plt.figure(figsize=(12, 7))

# Main plotting area (leave space at bottom for buttons)
ax = plt.subplot2grid((10, 1), (0, 0), rowspan=9)

# Draw initial scene
draw_scene()

# Create button axes at the bottom
# Decrease degree button (left)
decrease_button_ax = plt.subplot2grid((10, 1), (9, 0))
decrease_button_ax.set_position([0.25, 0.02, 0.15, 0.04])
decrease_button = Button(decrease_button_ax, 'Decrease Degree', 
                        color='lightcoral', hovercolor='salmon')
decrease_button.on_clicked(decrease_degree)

# Increase degree button (right)
increase_button_ax = plt.subplot2grid((10, 1), (9, 0))
increase_button_ax.set_position([0.6, 0.02, 0.15, 0.04])
increase_button = Button(increase_button_ax, 'Increase Degree', 
                        color='lightgreen', hovercolor='lightblue')
increase_button.on_clicked(increase_degree)

# Connect event handlers for interactivity
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)

# Show the interactive plot
plt.show()