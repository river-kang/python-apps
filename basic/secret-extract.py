f = open("ha.yaml", "r")

for line in f:
    if 'core' in line:
        print(line)