import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Global variables to store control points and state
# Start with one cubic Bézier curve (4 control points: P0, P1, P2, P3)
control_points = [
    np.array([1.0, 2.0]),   # P0
    np.array([2.0, 3.5]),   # P1
    np.array([3.0, 3.5]),   # P2
    np.array([4.0, 2.0])    # P3
]

# Variables for dragging functionality
dragging_point = None
point_circles = []

# Store references to matplotlib objects
fig = None
ax = None
button_ax = None
add_button = None


def de_casteljau(p0, p1, p2, p3, t):
    # First level of linear interpolation
    # These are points on the three line segments of the control polygon
    q0 = (1 - t) * p0 + t * p1  # Point on line P0-P1
    q1 = (1 - t) * p1 + t * p2  # Point on line P1-P2
    q2 = (1 - t) * p2 + t * p3  # Point on line P2-P3
    
    # Second level of linear interpolation
    # These are points on the two line segments formed by q0, q1, q2
    r0 = (1 - t) * q0 + t * q1  # Point on line Q0-Q1
    r1 = (1 - t) * q1 + t * q2  # Point on line Q1-Q2
    
    # Third level of linear interpolation
    # This is the final point on the Bézier curve
    b = (1 - t) * r0 + t * r1   # Point on line R0-R1
    
    return b


def generate_bezier_curve(p0, p1, p2, p3, num_points=100):
    curve_points = []
    
    # Generate points by varying t from 0 to 1
    for i in range(num_points):
        t = i / (num_points - 1)  # Parameter from 0 to 1
        point = de_casteljau(p0, p1, p2, p3, t)
        curve_points.append(point)
    
    return np.array(curve_points)


def get_num_segments():
    return (len(control_points) - 1) // 3


def get_segment_control_points(segment_index):
    # Each segment starts at index = segment_index * 3
    # Segment 0: indices 0, 1, 2, 3
    # Segment 1: indices 3, 4, 5, 6
    # Segment 2: indices 6, 7, 8, 9
    start_idx = segment_index * 3
    
    p0 = control_points[start_idx]
    p1 = control_points[start_idx + 1]
    p2 = control_points[start_idx + 2]
    p3 = control_points[start_idx + 3]
    
    return p0, p1, p2, p3


def draw_scene():
    ax.clear()
    
    num_segments = get_num_segments()
    
    # Define colors for different segments
    segment_colors = ['red', 'green', 'blue', 'orange', 'purple', 'brown']
    
    # Draw each cubic Bézier segment
    for seg_idx in range(num_segments):
        # Get control points for this segment
        p0, p1, p2, p3 = get_segment_control_points(seg_idx)
        
        # Choose color for this segment
        color = segment_colors[seg_idx % len(segment_colors)]
        
        # Draw the control polygon for this segment
        control_x = [p0[0], p1[0], p2[0], p3[0]]
        control_y = [p0[1], p1[1], p2[1], p3[1]]
        ax.plot(control_x, control_y, '--', color=color, 
               linewidth=1, alpha=0.3, label=f'Control Polygon {seg_idx}')
        
        # Generate and draw the Bézier curve for this segment
        curve = generate_bezier_curve(p0, p1, p2, p3, num_points=100)
        ax.plot(curve[:, 0], curve[:, 1], '-', color=color, 
               linewidth=2, label=f'Bézier Segment {seg_idx}')
    
    # Draw all control points as circles
    point_circles.clear()
    
    for i, point in enumerate(control_points):
        # Determine if this is a shared point (endpoint of one segment and start of next)
        # Shared points occur at indices 3, 6, 9, ... (every 3rd point starting from index 3)
        is_shared = (i > 0 and i % 3 == 0 and i < len(control_points) - 1)
        
        # Determine color based on point type
        if i == 0 or i == len(control_points) - 1:
            # First and last points (endpoints of entire piecewise curve)
            color = 'darkgreen'
            marker_size = 12
        elif is_shared:
            # Shared points between segments
            color = 'red'
            marker_size = 12
        else:
            # Regular control points
            color = 'blue'
            marker_size = 10
        
        # Draw the point
        circle = ax.plot(point[0], point[1], 'o', color=color, 
                        markersize=marker_size, picker=5)[0]
        point_circles.append(circle)
        
        # Add label showing the point index
        ax.text(point[0], point[1] + 0.15, f'P{i}', 
               ha='center', fontsize=9, fontweight='bold')
    
    # Set axis properties
    # Dynamically adjust x-axis based on number of points
    max_x = max(p[0] for p in control_points) + 1
    ax.set_xlim(0, max(max_x, 6))
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left', fontsize=8)
    ax.set_title(f'Piecewise Cubic Bézier Curve ({num_segments} segment{"s" if num_segments > 1 else ""})\n',
                fontsize=11, fontweight='bold')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    
    plt.draw()


def add_segment(event):
    # Get the last control point (which will be shared with the new segment)
    last_point = control_points[-1]
    
    # Calculate positions for the three new control points
    # We'll place them to the right of the last point with reasonable offsets
    # This creates a natural-looking continuation
    
    # P(n+1): First new control point - offset right and up
    new_p1 = last_point + np.array([1.0, 0.5])
    
    # P(n+2): Second new control point - offset right and down  
    new_p2 = last_point + np.array([2.0, 0.5])
    
    # P(n+3): Final control point of new segment - offset right, same height
    new_p3 = last_point + np.array([3.0, 0.0])
    
    # Add the three new control points
    control_points.append(new_p1)
    control_points.append(new_p2)
    control_points.append(new_p3)
    
    # Redraw the scene with the new segment
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


# Create figure and main axis for the Bézier curves
fig = plt.figure(figsize=(12, 7))

# Main plotting area (leave space at bottom for button)
ax = plt.subplot2grid((10, 1), (0, 0), rowspan=9)

# Draw initial scene (one cubic Bézier curve)
draw_scene()

# Create button axis at the bottom
button_ax = plt.subplot2grid((10, 1), (9, 0))
button_ax.set_position([0.4, 0.02, 0.2, 0.04])

# Create "Add Segment" button
add_button = Button(button_ax, 'Add Segment', color='lightblue', hovercolor='skyblue')
add_button.on_clicked(add_segment)

# Connect event handlers for interactivity
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)

# Show the interactive plot
plt.show()