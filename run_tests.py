import subprocess
import csv
import re


def get_error_message(full_message):
    start_index = full_message.find("Error Message")
    if start_index != -1:
        error_message_substring = full_message[start_index:]
        final_indx = error_message_substring.find("\n\n\n")
        if final_indx != -1:
            return error_message_substring[0:final_indx].replace('\r\n', '\\n').replace('\n', '\\n')
        
        return error_message_substring.replace('\r\n', '\\n').replace('\n', '\\n')
    else:
        return "Error Message not found!"


def parse_test_results(output):
    # Matches lines like: 'Passed TestName [x s]' or 'Failed TestName [x s]'
    results = {}
    for line in output.splitlines():
        print(line, flush=True)
        match = re.match(r'^\s*(Passed|Failed|Skipped)\s+([^\s\[]+)', line)
        if match:
            status, test_name = match.groups()
            # Normaliza para 'PASS', 'FAIL', 'SKIP'
            if status == 'Failed':
                results[test_name] = 'FAIL'
            elif status == 'Skipped':
                results[test_name] = 'SKIP'
            else:
                results[test_name] = 'PASS'
    return results




def run_all_tests_with_retry(max_retries=3):
    attempt = 0
    all_results = {}
    tests_to_run = set()
    # Primeira execução: roda todos os testes
    command = 'dotnet test --logger "console;verbosity=detailed"'
    print(f"Running all tests, attempt 1", flush=True)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout + '\n' + result.stderr
    test_results = parse_test_results(result.stdout)
    print(test_results, flush=True)

    # Só reexecuta os que falharam (não os skipped)
    tests_to_run = {test for test, status in test_results.items() if status == 'FAIL'}
    for test, status in test_results.items():
        if status == 'PASS':
            all_results[test] = {'Status': 'Passed', 'Attempt Passed': 1, 'Fail reason': ''}
        elif status == 'FAIL':
            all_results[test] = {'Status': 'Failed', 'Attempt Passed': 1, 'Fail reason': get_error_message(output)}
        else:
            all_results[test] = {'Status': 'Skipped', 'Attempt Passed': 1, 'Fail reason': 'Test was skipped'}
    attempt = 1
    # Próximas execuções: só os que falharam
    while attempt < max_retries and tests_to_run:
        filter_str = '|'.join([f'Name~{name}' for name in tests_to_run])
        command = f'dotnet test --filter "{filter_str}"'
        print(f"Retrying failed tests: {tests_to_run}, attempt {attempt + 1}", flush=True)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout + '\n' + result.stderr
        test_results = parse_test_results(output)
        next_tests_to_run = set()
        for test in tests_to_run:
            # Só atualiza se ainda não passou ou foi skipped
            if all_results.get(test, {}).get('Status') in ['Passed', 'Skipped']:
                continue
            status = test_results.get(test)
            if status == 'PASS':
                all_results[test]['Status'] = 'Passed'
                all_results[test]['Attempt Passed'] = attempt + 1
                all_results[test]['Fail reason'] = ''
            elif status == 'FAIL':
                all_results[test]['Status'] = 'Failed'
                all_results[test]['Attempt Passed'] = attempt + 1
                all_results[test]['Fail reason'] = get_error_message(output)
                next_tests_to_run.add(test)
            # Não atualiza para Skipped em retries
        tests_to_run = next_tests_to_run
        attempt += 1

    # Se não encontrou nenhum teste
    if not all_results:
        all_results['NO_TESTS_FOUND'] = {'Status': 'Error', 'Attempt Passed': '-', 'Fail reason': 'No tests found or parsing failed'}
    return all_results


def run_test_with_retry(test_name, max_retries=3):
    attempt = 0
    passed = False
    final_test_str = "\n"
    status_line = "I dont know"
    reason = ""
    while attempt < max_retries:
        command = f'dotnet test --filter "Name~{test_name}" --no-build --logger "trx;LogFileName={test_name}_attempt{attempt+1}.trx"'
        print(f"Running {test_name}, attempt {attempt + 1}", flush=True)

        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # check test status
        for line in result.stdout.splitlines():
            if "Failed:" in line and "Passed:" in line and "Skipped:" in line:
                status_line = line
                break

        if status_line.startswith("Passed!"):
            final_test_str += f"{test_name} passed on attempt {attempt + 1}"
            print(final_test_str, flush=True)
            passed = True
            break

        elif status_line.startswith("Failed!"):
            final_test_str += f"{test_name} failed on attempt {attempt + 1}\n"
            print(final_test_str, flush=True)
            reason += f"Fail Reason {attempt+1}:\n" + get_error_message(result.stdout)
            attempt += 1

        else:
            final_test_str += f"{test_name} probably skipped on attempt {attempt + 1}\n{result.stdout} {result.stderr}"
            print(final_test_str, flush=True)
            break

    print(final_test_str, flush=True)
    return passed, attempt + 1 if passed else None, reason


def save_csv_report(results):
    with open('test_report.csv', 'w', newline='') as csvfile:
        fieldnames = ['Test Name', 'Status', 'Attempt Passed', 'Fail reason']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    print("\nTest report written to test_report.csv", flush=True)


def save_stats_report(results):
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r['Status'] == 'Passed')
    failed_tests = sum(1 for r in results if r['Status'] == 'Failed')
    skipped_tests = sum(1 for r in results if r['Status'] == 'Skipped')
    passed_percentage = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    skipped_percentage = (skipped_tests / total_tests * 100) if total_tests > 0 else 0
    failed_percentage = (failed_tests / total_tests * 100) if total_tests > 0 else 0

    passed_in_retry = sum(1 for r in results if r['Attempt Passed'] > 1 and r['Status'] == 'Passed')
    passed_in_retry_percentage = (passed_in_retry / total_tests * 100) if total_tests > 0 else 0


    with open('test_report_stats.md', 'w') as stats_file:
        stats_file.write(f"# Test Report Stats\n\n")
        stats_file.write(f"Total Tests: {total_tests}\n")
        stats_file.write(f" . | . \n")
        stats_file.write(f"---|---\n")
        stats_file.write(f"Passed Tests: {passed_tests} | {str(passed_percentage)}%\n")
        stats_file.write(f"Failed Tests: {failed_tests} | {str(failed_percentage)}%\n")
        stats_file.write(f"Skipped Tests: {skipped_tests}| {str(skipped_percentage)}%\n")
        stats_file.write(f"Passed in retry: {passed_in_retry} |" + str(passed_in_retry_percentage) + "%\n")


    print("\nTest report stats written to test_report_stats.md", flush=True)



def main():
    test_names = [
        # Leave empty to run all tests
        # 'Validate_Github_HomePage',
        # 'This_Test_Shall_Fail'
    ]
    results = []
    if not test_names:  # Run all tests
        all_results = run_all_tests_with_retry(max_retries=3)
        for test_name, res in all_results.items():
            results.append({'Test Name': test_name, **res})
    else:
        for test_name in test_names:
            passed, attempt, reason = run_test_with_retry(test_name, max_retries=3)
            if passed:
                results.append({'Test Name': test_name, 'Status': 'Passed', 'Attempt Passed': attempt, 'Fail reason': ''})
            else:
                results.append({'Test Name': test_name, 'Status': 'Failed', 'Attempt Passed': 'Failed', 'Fail reason': reason})
    # Write CSV report
    try:
        save_csv_report(results)
        save_stats_report(results)
    except Exception as e:
        print(f"Error saving reports: {e}", flush=True)


if __name__ == "__main__":
    main()