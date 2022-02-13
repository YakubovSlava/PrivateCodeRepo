a = 1
n = 1
while n != 0:
    print('=================')
    n = int(input())
    if n != 0:

        for m in range(1, n+1):
            while n % m == 0 and a % m == 0 and m != 1:
                print(m)
                n /= m
                a /= m
        a *= n
print(a)
