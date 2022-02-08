# N, M = [int(x) for x in input().split()]
N, M = 3,2

# Ftpx = [int(x) for x in input().split()]
Ftpx = [0, 1, 2, 3]


F_a = []
F_b = []
G_a = []
G_b = []


# for i in range(N):
#     a, b = input().split()
#     F_a.append(a)
#     F_b.append(b)

F_a = [1, 1, 1]
F_b = [0, -2, -1]


# Gtpx = [int(x) for x in input().split()]

Gtpx = [0, 1, 3]
# for i in range(M):
#     a, b = input().split()
#     G_a.append(a)
#     G_b.append(b)

G_a = [-1, -1]
G_b = [0, 2]

sums = 0
for i in range(1, N+1):
    l_f = Ftpx[i-1]
    r_f = Ftpx[i]
    a_f = F_a[i-1]
    b_f = F_b[i-1]
    # print(l_f, r_f, a_f, b_f)

    for j in range(1, M+1):
        if ((Gtpx[j-1] >= l_f) and (Gtpx[j-1] < r_f)) or ((Gtpx[j] > l_f) and (Gtpx[j] <= r_f)):
            a_g = G_a[j - 1]
            b_g = G_b[j - 1]
            l_g = max(l_f, Gtpx[j-1])
            r_g = min(Gtpx[j], r_f)

            if l_g != r_g:
                A = abs(((a_f*l_g+b_f) - (a_g*l_g+b_g)))
                B = abs(((a_f * r_g + b_f) - (a_g * r_g + b_g)))

                res = (A+B)/2 * (r_g-l_g)
                # print(A, B, l_g, r_g)
                sums += res

print(sums)

