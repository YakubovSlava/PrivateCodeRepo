import math
import numpy as np
import sys

class Poly:
    a, b = 1., 1.
    def __init__(self , a, b):
        self.a, self.b = a, b

class Segment:
    f_idx, g_idx, l, r = 0, 0, 0, 0
    def __init__(self, f_idx, g_idx, l, r):
        self.f_idx, self.g_idx, self.l, self.r = f_idx, g_idx, l, r

f, f_board, g, g_board = [], [], [], []
ab=Poly(0., 0.)
intersect = 1e10

def integrate(seg):
    f_cur = f[seg.f_idx]
    g_cur = g[seg.g_idx]
    global ab
    ab = Poly(f_cur.a - g_cur.a, f_cur.b - g_cur.b)
    if ab.a < 0:
        ab.a *= -1
        ab.b *= -1
        global intersect
        intersect = 1e10
    if ab.a != 0:
        intersect = -ab.b / ab.a
    else :
        if ab.b == 0:
            return 0.
        if seg.l < intersect < seg.r:
            lm_int=ab.a/2*(pow(intersect, 2)-pow(seg.l, 2))+\
            ab.b/1*(pow(intersect, 1)-pow(seg.l, 1))
            fm_int = ab.a / 2 * (pow(seg.r, 2) - pow(intersect , 2)) + \
ab.b / 1 ∗ (pow(seg.r, 1) − pow(intersect , 1)) return abs(lm_int) + abs(fm_int)
3
else :
lr_int = ab.a / 2 ∗ (pow(seg.r, 2) − pow(seg.l, 2)) + \
ab.b / 1 ∗ (pow(seg.r, 1) − pow(seg.l, 1)) return abs(lr_int)
def main():
with open(’input.txt’) as reader:
l = list(map(int, reader.readline().split())) n, m= l[0], l[1]
global f_board
f_board = list (map(int , reader . readline (). split ())) global f
for i in range(n):
c = list (map(int , reader . readline (). split ()))
f.append(Poly(c[0], c[1])) global g_board
g_board = list (map(int , reader . readline (). split ())) global g
for i in range(m):
c = list (map(int , reader . readline (). split ()))
g.append(Poly(c[0] , c[1])) f_p, g_p = 1, 1
merged = list(np.unique(f_board + g_board)) calc = []
for i in range(len(merged) − 1):
calc .append(Segment(f_p − 1, g_p − 1, merged[ i ] , merged[ i + 1])) if merged[i + 1] == f_board[f_p]:
f_p += 1
if merged[i + 1] == g_board[g_p]:
g_p += 1
ans = 0.
for i in calc :
ans += integrate ( i ) print ( ans )
if __name__ == "__main__": main()