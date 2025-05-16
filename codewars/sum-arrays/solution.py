def sum_array(a):
    if len(a) == 0: return 0
    sum_val = 0
    for num in a: sum_val += num
    return sum_val

print(sum_array([1,2,3]))