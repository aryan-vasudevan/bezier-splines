import numpy as np
import matplotlib.pyplot as plt


def de_casteljau_general(control_points, t):
    points = [np.array(p) for p in control_points]
    num_levels = len(points) - 1
    
    for level in range(num_levels):
        next_level_points = []
        for i in range(len(points) - 1):
            new_point = (1 - t) * points[i] + t * points[i + 1]
            next_level_points.append(new_point)
        points = next_level_points
    
    return points[0]


def generate_bezier_curve(control_points, num_points=100):
    curve_points = []
    for i in range(num_points):
        t = i / (num_points - 1)
        point = de_casteljau_general(control_points, t)
        curve_points.append(point)
    return np.array(curve_points)


def run_local_control_experiment(max_degree=15, vertical_shift=1.0, num_curve_points=100):
    degrees = []
    influence_percentages = []
    
    for degree in range(1, max_degree + 1):
        num_control_points = degree + 1
        baseline_y = 2.0
        control_points_original = []
        
        for i in range(num_control_points):
            x = float(i)
            y = baseline_y
            control_points_original.append(np.array([x, y]))
        
        control_points_shifted = [np.array(p) for p in control_points_original]
        control_points_shifted[0][1] += vertical_shift
        
        original_curve = generate_bezier_curve(control_points_original, num_curve_points)
        shifted_curve = generate_bezier_curve(control_points_shifted, num_curve_points)
        
        vertical_displacements = np.abs(shifted_curve[:, 1] - original_curve[:, 1])
        average_displacement = np.mean(vertical_displacements)
        
        # Calculate what percentage of the original shift propagated to the average curve point
        influence_percentage = (average_displacement / vertical_shift) * 100
        
        degrees.append(degree)
        influence_percentages.append(influence_percentage)
        
        print(f"Degree {degree}: Average influence = {influence_percentage:.2f}% of P0 shift")
    
    return degrees, influence_percentages


def plot_results(degrees, influence_percentages):
    plt.figure(figsize=(12, 7))
    
    plt.plot(degrees, influence_percentages, 'bo-', linewidth=2, markersize=8, label='P0 Influence on Average Curve Point')
    
    plt.grid(True, alpha=0.3)
    plt.xlabel('Degree of Bézier Curve', fontsize=12, fontweight='bold')
    plt.ylabel('Average Influence (%)', fontsize=12, fontweight='bold')
    plt.title('Local Control Effect in Bézier Curves of Varying Degrees\n' +
              'Measurement: % of P0 vertical shift that affects the average curve point',
              fontsize=13, fontweight='bold')
    plt.legend(loc='upper right', fontsize=11)
    
    # Add horizontal reference line at 50%
    plt.axhline(y=50, color='gray', linestyle='--', alpha=0.5, label='50% influence')
    
    max_idx = np.argmax(influence_percentages)
    
    
    plt.ylim(0, 105)
    plt.tight_layout()
    plt.show()


# Run the experiment
print("Running Local Control Effect Experiment on Bézier Curves")
print("=" * 60)
print()

degrees, influence_percentages = run_local_control_experiment(
    max_degree=15,
    vertical_shift=1.0,
    num_curve_points=100
)

print()
print("=" * 60)
print("Experiment Complete")
print()

plot_results(degrees, influence_percentages)