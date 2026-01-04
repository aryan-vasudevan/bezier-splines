import numpy as np
import time


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


def de_casteljau_cubic(p0, p1, p2, p3, t):
    # First level
    q0 = (1 - t) * p0 + t * p1
    q1 = (1 - t) * p1 + t * p2
    q2 = (1 - t) * p2 + t * p3
    
    # Second level
    r0 = (1 - t) * q0 + t * q1
    r1 = (1 - t) * q1 + t * q2
    
    # Third level
    b = (1 - t) * r0 + t * r1
    
    return b


def generate_higher_order_bezier(control_points, num_points=100):
    curve_points = []
    for i in range(num_points):
        t = i / (num_points - 1)
        point = de_casteljau_general(control_points, t)
        curve_points.append(point)
    return np.array(curve_points)


def generate_piecewise_bezier(control_points, num_points=100):
    num_segments = (len(control_points) - 1) // 3
    all_curve_points = []
    
    for seg_idx in range(num_segments):
        start_idx = seg_idx * 3
        p0 = control_points[start_idx]
        p1 = control_points[start_idx + 1]
        p2 = control_points[start_idx + 2]
        p3 = control_points[start_idx + 3]
        
        segment_points = []
        for i in range(num_points):
            t = i / (num_points - 1)
            point = de_casteljau_cubic(p0, p1, p2, p3, t)
            segment_points.append(point)
        
        all_curve_points.extend(segment_points)
    
    return np.array(all_curve_points)


# Create 19 control points
num_control_points = 19
control_points = []
for i in range(num_control_points):
    x = float(i)
    y = 2.0 + np.sin(i * 0.5)  # Add some variation
    control_points.append(np.array([x, y]))

print("=" * 70)
print("Computational Cost Comparison: Higher Order vs Piecewise Bézier")
print("=" * 70)
print(f"\nNumber of control points: {num_control_points}")
print(f"Higher order: Degree {num_control_points - 1} Bézier (1 curve)")
print(f"Piecewise: {(num_control_points - 1) // 3} cubic Bézier segments")
print()

# Number of iterations for timing
num_iterations = 1000
num_curve_points = 100

print(f"Running {num_iterations} iterations with {num_curve_points} points per curve...")
print()

# Time higher order Bézier
start_time = time.time()
for _ in range(num_iterations):
    curve = generate_higher_order_bezier(control_points, num_curve_points)
end_time = time.time()
higher_order_time = end_time - start_time

# Time piecewise Bézier
start_time = time.time()
for _ in range(num_iterations):
    curve = generate_piecewise_bezier(control_points, num_curve_points)
end_time = time.time()
piecewise_time = end_time - start_time

# Results
print("=" * 70)
print("RESULTS")
print("=" * 70)
print(f"Higher Order Bézier (Degree {num_control_points - 1}):")
print(f"  Total time: {higher_order_time:.4f} seconds")
print(f"  Average per iteration: {(higher_order_time / num_iterations) * 1000:.4f} ms")
print()
print(f"Piecewise Bézier ({(num_control_points - 1) // 3} cubic segments):")
print(f"  Total time: {piecewise_time:.4f} seconds")
print(f"  Average per iteration: {(piecewise_time / num_iterations) * 1000:.4f} ms")
print()
print(f"Speed ratio: {higher_order_time / piecewise_time:.2f}x")
print(f"Piecewise is {((higher_order_time - piecewise_time) / higher_order_time * 100):.1f}% faster")
print()

# Complexity analysis
higher_order_ops = (num_control_points * (num_control_points - 1)) // 2  # n(n-1)/2
piecewise_ops = 6 * ((num_control_points - 1) // 3)  # 6n for cubic segments

print("=" * 70)
print("THEORETICAL COMPLEXITY")
print("=" * 70)
print(f"Higher Order: O(n²) = ½n(n-1) = {higher_order_ops} operations per point")
print(f"Piecewise: O(n) = 6m (where m = segments) = {piecewise_ops} operations per point")
print(f"Theoretical ratio: {higher_order_ops / piecewise_ops:.2f}x")
print("=" * 70)