from collections import Counter

def main():
    path = "./data.txt"
    # Part 1
    strength0, strength1 = "AKQJT98765432"[::-1], "AKQT98765432J"[::-1]
    def value(s):
        c_counts = Counter(Counter(s).values()) # Number of times each number comes up
        return sorted(c_counts.items(), reverse=True)
    data = sorted([(value(s),tuple(map(strength0.index, s)),int(b)) for s,b in map(str.split,open(path))])
    print(sum(d[-1]*(i+1) for i, d in enumerate(data)))

    # Part 2
    def value(s):
        most_common = "J"
        if s.count("J") < 5:
            most_common = max(Counter(s.replace("J","")).items(), key=lambda s: s[1])[0]
        c_counts = Counter(Counter(s.replace("J", most_common)).values()) # Number of times each number comes up
        return sorted(c_counts.items(), reverse=True)
    data = sorted([(value(s),tuple(map(strength1.index, s)),int(b)) for s,b in map(str.split,open(path))])
    print(sum(d[-1]*(i+1) for i, d in enumerate(data)))
    return 0

if __name__ == "__main__":
    main()
