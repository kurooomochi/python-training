def summation(num):
  sum_val = 0
  for x in range(0, num + 1):
    sum_val += x
  return sum_val
  

print(summation(3))