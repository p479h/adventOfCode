
char_per_signal = 14
for line in open("input.txt", "r").read().splitlines():
    for i, char in enumerate(line, start = 3):
        sequence = set(line[i-char_per_signal+1:i+1])
        if len(sequence) == char_per_signal:
            print(i+1)
            break
