def narcissistic( value ):
    num_arr = list(str(value))
    digits = len(num_arr)
    total = 0
    for num in num_arr: total += int(num)**digits
    if total == value: return True
    return False

print(narcissistic(1938))