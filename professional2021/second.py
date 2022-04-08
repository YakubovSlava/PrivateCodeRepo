import sys
from sys import stdout , stdin

def ask(n):
    print(f'? {n}')
    stdout.flush()
    ans = int(input())
    stdin.flush()
    return ans

def print_answer(a, b):
    print(f"! {a} {b}")

def main():
    for i in range(1, 1001):
        answer = ask(i)
        if answer == 2:
            a=i
            b=i
            print_answer (a , b)
            return
        if answer == 1:
            a=i
        for j in range(i + 1, 1001):
            answer = ask(j)
            expected_answer = 0
            if j % a == 0:
                expected_answer = j // a
            if answer != expected_answer:
                b = j
                print_answer(a,b)
                return