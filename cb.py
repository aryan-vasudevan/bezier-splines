import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Global variables to store control points and state
control_points = np.array([
    [1.0, 1.0],   # P0
    [2.0, 3.0],   # P1
    [4.0, 3.0],   # P2
    [5.0, 1.0]    # P3
])

# Variables for dragging functionality
dragging_point = None
point_circles = []


def de_casteljau(p0, p1, p2, p3, t):    
    # First level
    # These are points on the three line segments of the control polygon
    q0 = (1 - t) * p0 + t * p1  # Point on line P0-P1
    q1 = (1 - t) * p1 + t * p2  # Point on line P1-P2
    q2 = (1 - t) * p2 + t * p3  # Point on line P2-P3
    
    # Second level
    # These are points on the two line segments formed by q0, q1, q2
    r0 = (1 - t) * q0 + t * q1  # Point on line Q0-Q1
    r1 = (1 - t) * q1 + t * q2  # Point on line Q1-Q2
    
    # Third level
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


def draw_scene(ax):
    ax.clear()
    
    # Extract control points for easier access
    p0, p1, p2, p3 = control_points
    
    # Draw the control polygon (straight lines connecting control points)
    control_x = [p0[0], p1[0], p2[0], p3[0]]
    control_y = [p0[1], p1[1], p2[1], p3[1]]
    ax.plot(control_x, control_y, 'b--', linewidth=1, alpha=0.5, label='Control Polygon')
    
    # Generate and draw the Bézier curve
    curve = generate_bezier_curve(p0, p1, p2, p3, num_points=100)
    ax.plot(curve[:, 0], curve[:, 1], 'r-', linewidth=2, label='Bézier Curve')
    
    # Draw control points as circles
    point_circles.clear()
    colors = ['green', 'blue', 'blue', 'green']  # Endpoints in green, control points in blue
    labels = ['P0', 'P1', 'P2', 'P3']
    
    for i, (point, color, label) in enumerate(zip(control_points, colors, labels)):
        # Draw the point
        circle = ax.plot(point[0], point[1], 'o', color=color, 
                        markersize=10, picker=5)[0]
        point_circles.append(circle)
        
        # Add label
        ax.text(point[0], point[1] + 0.2, label, 
               ha='center', fontsize=10, fontweight='bold')
    
    # Set axis properties
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 4)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right')
    ax.set_title('Cubic Bézier Curve Playground', 
                fontsize=12, fontweight='bold')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    
    plt.draw()


def on_press(event):
    global dragging_point
    
    if event.inaxes is None:
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
    
    # Only process if we're dragging a point and mouse is in the axes
    if dragging_point is None or event.inaxes is None:
        return
    
    # Update the position of the dragged control point
    control_points[dragging_point] = [event.xdata, event.ydata]
    
    # Redraw the scene with updated control points
    draw_scene(event.inaxes)


def on_release(event):
    global dragging_point
    dragging_point = None


# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Draw initial scene
draw_scene(ax)

# Connect event handlers for interactivity
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)

# Show the interactive plot
plt.show()