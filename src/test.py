
a = [1, 2, 3, 4]
b = [5, 2]

if(not set(a).isdisjoint(set(b))):
    print("less")

print(a)

a.insert(3,4)

print(a)

if(2 in a) and (8 in a):
    print("yes")