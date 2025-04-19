#!/bin/bash

PYTHON_INTERPRETER="python3"
SOURCE_FILE="laplace_solver.py"
CHECKER_SCRIPT="checker.py"
TEST_DIR="."

TEST_CASES=$(find "${TEST_DIR}" -maxdepth 1 -name 'test_*.in' -print0 | xargs -0 -n1 basename | sed 's/\.in$//' | sort)

if ! command -v ${PYTHON_INTERPRETER} &> /dev/null; then
    echo "Error: Python interpreter '${PYTHON_INTERPRETER}' not found."
    exit 1
fi

if [ ! -f "${SOURCE_FILE}" ]; then
    echo "Error: Source file '${SOURCE_FILE}' not found."
    exit 1
fi

if [ ! -f "${CHECKER_SCRIPT}" ]; then
    echo "Error: Checker script '${CHECKER_SCRIPT}' not found."
    exit 1
fi

total_tests=0
passed_tests=0

echo "Starting tests for ${SOURCE_FILE}..."
echo

for test_base in ${TEST_CASES}; do
    total_tests=$((total_tests + 1))
    input_file="${test_base}.in"
    answer_file="${test_base}.ans"
    output_file="${test_base}.out"

    echo "--- Running test $(basename ${test_base}) ---"

    if [ ! -f "${input_file}" ]; then
        echo "  Input file ${input_file} not found. Skipping."
        continue
    fi
     if [ ! -f "${answer_file}" ]; then
        echo "  Answer file ${answer_file} not found. Skipping."
        continue
    fi

    start_time=$(date +%s.%N)
    ${PYTHON_INTERPRETER} "${SOURCE_FILE}" < "${input_file}" > "${output_file}"
    exit_code=$?
    end_time=$(date +%s.%N)
    runtime=$(awk -v t1="$start_time" -v t2="$end_time" 'BEGIN { print t2 - t1 }')

    if [ ${exit_code} -ne 0 ]; then
        echo "  Runtime Error! Exit code: ${exit_code}. Time: ${runtime}s"
        if [ -s "${output_file}" ]; then
            echo "  Output produced before error:"
            head -n 5 "${output_file}"
        fi
        continue
    fi

    echo "  Checking output (Time: ${runtime}s)..."
    ${PYTHON_INTERPRETER} ${CHECKER_SCRIPT} "${output_file}" "${answer_file}" "${input_file}"
    checker_exit_code=$?

    if [ ${checker_exit_code} -eq 0 ]; then
        echo "  Result: PASSED"
        passed_tests=$((passed_tests + 1))
        rm "${output_file}"
    else
        echo "  Result: FAILED"
    fi
    echo
done

echo "===================="
echo "Testing Summary:"
echo "Total Tests: ${total_tests}"
echo "Passed:      ${passed_tests}"
echo "Failed:      $((total_tests - passed_tests))"
echo "===================="

exit $((total_tests - passed_tests))