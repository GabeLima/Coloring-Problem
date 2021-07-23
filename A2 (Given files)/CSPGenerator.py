import sys
import random
# random.seed(0)

def CSPGenerator(N, M, K, output_file_path):
    colors = range(K)
    variables = [(i, random.choice(colors)) for i in range(N)]

    variables_by_color = []
    for c in colors:
        vars = [v for v in variables if v[1] == c]
        variables_by_color.append(vars)

    valid_colors = [v[0][1] for v in variables_by_color if len(v) > 0]
    if len(valid_colors) <= 1 and M>0:
        return False

    valid_csps = []
    for c1 in valid_colors:
        for c2 in valid_colors:
            if c1>=c2:
                continue
            for var1 in variables_by_color[c1]:
                for var2 in variables_by_color[c2]:
                    valid_csps.append([var1[0], var2[0]])

    if len(valid_csps) < M:
        return False
    csps = random.sample(valid_csps, M)
    with open(output_file_path, 'w') as f:
        f.write('{} {} {}'.format(N,M,K))
        if len(csps) > 0:
            for csp in csps:
                f.write('\n{} {}'.format(csp[0], csp[1]))
    return True

if __name__ == "__main__":
    N = int(sys.argv[1])
    M = int(sys.argv[2])
    K = int(sys.argv[3])
    output_file_path = sys.argv[4]
    solvable = 1

    if len(sys.argv) > 5:
        solvable = int(sys.argv[5])

    if solvable == 0:
        with open(output_file_path, 'w') as f:
            f.write('{} {} {}'.format(N, M, K))
            for m in range(M):
                csp = random.sample(range(N), 2)
                f.write('\n{} {}'.format(csp[0], csp[1]))
    else:
        trial = 1000

        for t in range(trial):
            status = CSPGenerator(N, M, K, output_file_path)
            if status:
                break

        if not status:
            print("failed to create csp for input parameters")