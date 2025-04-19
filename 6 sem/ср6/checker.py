import sys
import math
import os

def check(user_out_path, correct_ans_path, input_path):
    try:
        with open(input_path, 'r') as f_in:
            line1 = f_in.readline().split()
            if len(line1) < 2:
                return False, f"Invalid input file format: {input_path}"
            M = int(line1[0])
            epsilon = float(line1[1])
    except Exception as e:
        return False, f"Error reading input file {input_path}: {e}"

    num_expected = (M - 1) * (M - 1) if M > 1 else 0

    try:
        with open(user_out_path, 'r') as f_out:
            user_output_line = f_out.readline().strip()
            if not user_output_line:
                user_vals = []
            else:
                user_vals = [float(x) for x in user_output_line.split()]
                user_vals = [v for v in user_vals if not isinstance(v, str) or v]
    except Exception as e:
        return False, f"Error reading or parsing user output file {user_out_path}: {e}"

    try:
        with open(correct_ans_path, 'r') as f_ans:
            correct_output_line = f_ans.readline().strip()
            if not correct_output_line:
                correct_vals = []
            else:
                correct_vals = [float(x) for x in correct_output_line.split()]
                correct_vals = [v for v in correct_vals if not isinstance(v, str) or v]
    except Exception as e:
        print(f"Internal Error: Could not read or parse correct answer file {correct_ans_path}: {e}", file=sys.stderr)
        return False, f"Internal Error processing answer file {correct_ans_path}"


    if len(user_vals) != num_expected:
        return False, f"Wrong number of output values. Expected {num_expected}, got {len(user_vals)}"

    if len(correct_vals) != num_expected:
        print(f"Internal Error: Correct answer file {correct_ans_path} has wrong number of values. Expected {num_expected}, got {len(correct_vals)}", file=sys.stderr)
        return False, f"Internal Error in answer file {correct_ans_path}"

    if num_expected == 0:
        return True, "OK (M<=1, no interior points)"

    max_rel_err = 0.0
    first_fail_idx = -1
    first_fail_user = 0.0
    first_fail_correct = 0.0
    first_fail_rel_err = 0.0

    all_ok = True
    for i in range(num_expected):
        a = user_vals[i]
        b = correct_vals[i]

        diff = abs(a - b)
        denominator = max(1.0, abs(b))
        rel_err = diff / denominator

        if rel_err > max_rel_err:
             max_rel_err = rel_err

        if rel_err >= epsilon:
            if all_ok:
                first_fail_idx = i
                first_fail_user = a
                first_fail_correct = b
                first_fail_rel_err = rel_err
            all_ok = False


    if all_ok:
        return True, f"OK (MaxRelErr={max_rel_err:.4E} < Eps={epsilon:.4E})"
    else:
        row_idx = first_fail_idx // (M - 1) + 1
        col_idx = first_fail_idx % (M - 1) + 1
        return False, (f"Wrong Answer: First mismatch at index {first_fail_idx} (u[{row_idx}][{col_idx}]). "
                       f"User={first_fail_user:.10f}, Correct={first_fail_correct:.10f}. "
                       f"RelErr={first_fail_rel_err:.4E}, Eps={epsilon:.4E}. MaxRelErr={max_rel_err:.4E}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python checker.py <user_output_file> <correct_answer_file> <input_file>")
        sys.exit(1)

    user_out = sys.argv[1]
    correct_ans = sys.argv[2]
    input_file = sys.argv[3]

    if not os.path.exists(user_out):
        print(f"User output file not found: {user_out}")
        sys.exit(1)
    if not os.path.exists(correct_ans):
        print(f"Correct answer file not found: {correct_ans}")
        sys.exit(1)
    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        sys.exit(1)

    success, message = check(user_out, correct_ans, input_file)

    print(message)
    if success:
        sys.exit(0)
    else:
        sys.exit(1)