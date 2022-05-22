a = [4,5,7,8,9,9,9,9]
s = list()
for i in range(0,len(a),2):
    b = a[i:i+4]
    print(b)
    s.append(b)


print(s)