def count_sheep(n):
    sheeps = ""
    for x in range(1, n + 1):
        currsheep = str(x) + " sheep..."
        sheeps += currsheep
    return sheeps

print(count_sheep(3))