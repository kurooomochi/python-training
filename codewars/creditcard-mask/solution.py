# return masked string
def maskify(cc):
    masked_cc = ""
    length = len(cc)
    for i, num in enumerate(cc):
        if i < length - 4: masked_cc += "#"
        else: masked_cc += num
    return masked_cc

print(maskify("18"))