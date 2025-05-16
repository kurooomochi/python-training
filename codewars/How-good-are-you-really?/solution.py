def better_than_average(class_points, your_points):
    sum_val = 0
    for point in class_points:
        sum_val += point
    
    avg = sum_val / len(class_points)
    if avg > your_points:
        return False
    else: 
        return True


print(better_than_average([100, 40, 34, 57, 29, 72, 57, 88], 75))