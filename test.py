import os
import subprocess
import sys

# ANSI color codes
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

def assemble_and_link(source_file, executable_file):
    """Compiles and links an assembly source file using gcc."""
    try:
        # Use gcc as the driver to handle both assembly and linking
        compile_command = ["gcc", "-m32", "-no-pie", "-o", executable_file, source_file]
        subprocess.run(compile_command, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during compilation of {source_file}:")
        print(e.stderr)
        return False

def run_test(executable_file, input_file):
    """Runs the executable with the given input file and returns the output."""
    with open(input_file, 'r') as f:
        input_data = f.read()
    
    try:
        result = subprocess.run([f"./{executable_file}"], input=input_data, capture_output=True, text=True, check=True, timeout=5)
        return result.stdout, None
    except subprocess.CalledProcessError as e:
        return e.stdout, f"Execution failed with return code {e.returncode}:\n{e.stderr}"
    except subprocess.TimeoutExpired:
        return "", "Execution timed out."

def compare_output(actual, expected_file):
    """Compares the actual output with the expected output from a file."""
    if not os.path.exists(expected_file):
        return False, f"Expected output file not found: {expected_file}"
        
    with open(expected_file, 'r') as f:
        expected = f.read()
    
    # Normalize line endings and strip trailing whitespace
    actual_normalized = '\n'.join(line.strip() for line in actual.strip().splitlines())
    expected_normalized = '\n'.join(line.strip() for line in expected.strip().splitlines())

    return actual_normalized == expected_normalized, ""

def run_tests_for_task(task_name, executable_file):
    """Runs all tests for a given task."""
    print(f"--- Running tests for {task_name} ---")
    test_dir = os.path.join("tests", task_name)
    if not os.path.isdir(test_dir):
        print(f"Test directory not found: {test_dir}")
        return 0, 0

    total_tests = 0
    passed_tests = 0

    test_categories = sorted([d for d in os.listdir(test_dir) if os.path.isdir(os.path.join(test_dir, d))])

    for category in test_categories:
        category_dir = os.path.join(test_dir, category)
        input_files = sorted([f for f in os.listdir(category_dir) if f.endswith('.in') and 'Zone.Identifier' not in f])
        
        for in_file_name in input_files:
            total_tests += 1
            test_name = f"{category}/{os.path.splitext(in_file_name)[0]}"
            input_file_path = os.path.join(category_dir, in_file_name)
            output_file_path = os.path.join(category_dir, os.path.splitext(in_file_name)[0] + '.out')

            actual_output, error = run_test(executable_file, input_file_path)

            if error:
                print(f"Test {test_name}: {Colors.RED}FAILED{Colors.ENDC} (Execution Error)")
                print(error)
                continue

            is_match, diff_error = compare_output(actual_output, output_file_path)

            if diff_error:
                 print(f"Test {test_name}: {Colors.RED}FAILED{Colors.ENDC} (Comparison Error)")
                 print(diff_error)
                 continue

            if is_match:
                passed_tests += 1
                print(f"Test {test_name}: {Colors.GREEN}PASSED{Colors.ENDC}")
            else:
                print(f"Test {test_name}: {Colors.RED}FAILED{Colors.ENDC}")
                with open(output_file_path, 'r') as f:
                    expected_output = f.read()
                print("Expected:")
                print(expected_output)
                print("Got:")
                print(actual_output)


    return passed_tests, total_tests

def print_summary(passed, total):
    """Prints the test summary with color coding."""
    if total == 0:
        print("No tests were run.")
        return

    percentage = (passed / total) * 100
    
    if percentage == 100:
        color = Colors.GREEN
    elif percentage < 35:
        color = Colors.RED
    else:
        color = Colors.YELLOW
        
    print(f"\nSummary: {color}{passed}/{total} tests passed ({percentage:.2f}%){Colors.ENDC}\n")

def main():
    tasks = {
        "task1": "UnidimentionalSpace.s",
        "task2": "BidimensionalSpace.s"
    }

    overall_passed = 0
    overall_total = 0

    for task, source_file in tasks.items():
        executable = os.path.splitext(source_file)[0]
        if not assemble_and_link(source_file, executable):
            print(f"Could not build {executable}. Skipping tests for {task}.")
            continue
        
        passed, total = run_tests_for_task(task, executable)
        overall_passed += passed
        overall_total += total
        
        if os.path.exists(executable):
            os.remove(executable)

    print("--- Overall Summary ---")
    print_summary(overall_passed, overall_total)

if __name__ == "__main__":
    main()
