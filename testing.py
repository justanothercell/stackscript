l = list(range(10))
print(l)
l, v = l[:-4], l[-4:]
l.append(v)
print(l)
