from math import ceil, floor, sqrt, log10

def main():
    test_path = "./test.txt"
    data_path = "./data.txt"
    t,r = [tuple(map(int,l.split(":")[1].strip().split())) for l in open(data_path)]
    s = 1
    # Pt 2
    def join_numbers(n):
        t = n[0]
        for num in n[1:]:
            t *= 10**(int(log10(num))+1)
            t += num
        return [t]
    tr = zip(t, r) if False else zip(*tuple(map(join_numbers, [t, r])))
    for T, R in tr:
        sl, sr = (T-sqrt(T**2-4*R))/2, (T+sqrt(T**2-4*R))/2
        if sl%1<1e-10: # The exact solution doesn't count, we wanna win!
            sl += 1
        if sr%1<1e-10:
            sr -= 1
        s*=floor(sr)-ceil(sl)+1
    print(s)
        

if __name__ == "__main__":
    main()
