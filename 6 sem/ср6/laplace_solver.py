import sys
import math
import numpy as np

def solve():
    line1 = sys.stdin.readline().split()
    M = int(line1[0])
    epsilon = float(line1[1])

    if M <= 1:
        for _ in range(4):
            sys.stdin.readline()
        print()
        return

    g1_vals = list(map(float, sys.stdin.readline().split()))
    g2_vals = list(map(float, sys.stdin.readline().split()))
    g3_vals = list(map(float, sys.stdin.readline().split()))
    g4_vals = list(map(float, sys.stdin.readline().split()))

    u = np.zeros((M + 1, M + 1), dtype=float)

    u[0, :] = g3_vals
    u[M, :] = g4_vals
    u[:, 0] = g1_vals
    u[:, M] = g2_vals

    h = 1.0 / M
    omega = 2.0 / (1.0 + math.sin(math.pi * h))

    tolerance = max(epsilon, 1e-15)

    max_iter = 100000
    iter_count = 0
    converged = False

    for iter_count in range(max_iter):
        max_diff = 0.0

        for j in range(1, M):
            for i in range(1, M):
                u_old = u[j, i]
                gs_val = 0.25 * (u[j, i + 1] + u[j, i - 1] + u[j + 1, i] + u[j - 1, i])
                u[j, i] = (1.0 - omega) * u_old + omega * gs_val
                max_diff = max(max_diff, abs(u[j, i] - u_old))

        if max_diff < tolerance:
            converged = True
            break

    if not converged:
         print(f"Warning: Maximum iterations ({max_iter}) reached. Max diff = {max_diff:.4E}", file=sys.stderr)


    interior_points = u[1:M, 1:M]
    output_values = interior_points.flatten()
    output_string = " ".join(f"{val:.10f}" for val in output_values)
    print(output_string)

if __name__ == "__main__":
    solve()