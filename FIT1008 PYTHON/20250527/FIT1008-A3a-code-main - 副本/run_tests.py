当然可以！以下是你提供的测试运行脚本代码的中文注释版本，我已经逐行添加中文注释，并将所有英文 docstring 翻译为中文。

---

```python
"""
用于 Ed 系统的自定义测试运行器，使用 LCG 方法生成随机数。
支持按照任务（task）运行，并输出 JSON 格式的结果供 Ed 使用。
"""

import argparse       # 用于解析命令行参数
import json           # 用于输出 JSON 格式
import os             # 操作系统文件路径
import re             # 正则表达式匹配
import sys            # 系统交互
import unittest       # Python 的单元测试框架
from unittest.runner import TextTestResult  # 引入基础的测试结果类

NUMBER_OF_TASKS_FOR_ASSIGNMENT = 3  # 当前作业一共多少个 task

class SingleTaskTestResult(TextTestResult):
    """
    自定义的测试结果类，用于 Ed 输出格式。

    与默认的 TextTestResult 不同之处在于：
    1. 所有测试结果会保存在列表中而不是打印；
    2. 这些结果可以以 JSON 格式返回给 Ed 系统；
    3. 专为单一 task 设计，若要支持多 task 需自行扩展逻辑。

    支持在测试方法 docstring 中标注：
    - #name(测试名)：用于展示
    - #score(分值)：用于评分
    - #hidden：测试隐藏
    - #private：测试为私有
    - #approach：方法分
    - #hurdle：必须通过，否则该 task 记 0 分
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_results = []  # 所有测试结果列表
        self.any_hurdles_failed = False  # 是否有 hurdle 测试失败
        self.aggregate_results = {}  # 汇总得分 {"tests":..., "approach":...}
        self._task_number = None  # 当前 task 编号

    def addSuccess(self, test):
        self._record_result(test, True, "Well done")  # 成功的测试记录

    def addFailure(self, test, err):
        message = self._exc_info_to_string(err, test)  # 获取错误信息字符串
        self._record_result(test, False, message)

    def addError(self, test, err):
        message = self._exc_info_to_string(err, test)
        self._record_result(test, False, message, ok=True)  # 错误视为未通过，但 ok=True 保证结果能显示

    def _ensure_aggregate_results(self, task_number):
        """
        确保创建了当前任务的 aggregate_results（用于方法分和功能分汇总）。
        """
        if self.aggregate_results:
            if self._task_number != task_number:
                raise ValueError("每个测试文件只能对应一个 Task！")
            return

        self.aggregate_results = {
            "tests": {
                "name": f"[Aggregate] Task {task_number} Tests",
                "score": 0,
                "ok": True,
                "passed": True,
                "feedback": "",
                "hidden": False,
                "private": False,
            },
            "approach": {
                "name": f"[Aggregate] Task {task_number} Approach",
                "score": 0,
                "ok": True,
                "passed": True,
                "feedback": "",
                "hidden": False,
                "private": False,
            },
        }

        self.test_results.append(self.aggregate_results["tests"])
        self.test_results.append(self.aggregate_results["approach"])

        self._task_number = task_number

    def _record_result(self, test, passed, feedback, ok=True):
        docstring = test._testMethodDoc or ""

        task_number_match = re.search(r"[Tt]ask(\d+)", str(test), re.DOTALL)
        task_number = task_number_match.group(1) if task_number_match else "General"

        name_match = re.search(r"#name\((.*?)\)", docstring, re.DOTALL)
        test_name_prefix = f"{'Task ' + task_number}: "
        test_name = f"{test_name_prefix}{name_match.group(1).strip() if name_match else test._testMethodName}"

        score_match = re.search(r"#score\((\d+)\)", docstring, re.DOTALL)
        score = 0 if not passed else (int(score_match.group(1)) if score_match else 1)

        hidden_test = bool(re.search(r"#hidden", docstring))
        private_test = bool(re.search(r"#private", docstring))
        approach_test = bool(re.search(r"#approach", docstring))
        hurdle_test = bool(re.search(r"#hurdle", docstring))

        if hurdle_test and not passed:
            self.any_hurdles_failed = True

        result = {
            "name": test_name,
            "score": 0,
            "ok": ok,
            "passed": passed,
            "feedback": feedback.strip(),
            "hidden": hidden_test,
            "private": private_test,
        }
        self.test_results.append(result)

        self._ensure_aggregate_results(task_number)

        if not hurdle_test:
            if approach_test:
                self.aggregate_results["approach"]["score"] += score
            else:
                self.aggregate_results["tests"]["score"] += score

    def apply_hurdle(self):
        """
        应用 hurdle 测试逻辑：若有任何 hurdle 失败，则功能分和方法分都设为 0。
        """
        if self.any_hurdles_failed:
            self.aggregate_results["tests"]["score"] = 0
            self.aggregate_results["approach"]["score"] = 0


def get_matching_files(regex_pattern):
    """
    返回 tests 文件夹下与 regex_pattern 匹配的文件列表。

    参数:
        regex_pattern: 正则表达式，用于匹配测试文件名。
    """
    test_dir = "tests"
    all_files = os.listdir(test_dir)
    return list(sorted([
        os.path.join(test_dir, f)
        for f in all_files
        if re.fullmatch(regex_pattern, f)
    ]))


def run_tests(file_pattern, running_in_ed=False):
    """
    执行所有匹配 file_pattern 的测试文件。

    参数:
        file_pattern: 正则表达式，用于筛选测试文件；
        running_in_ed: 若为 True，则使用 Ed 格式输出。

    返回:
        若 running_in_ed 为 True，返回 JSON 格式的测试结果；
        否则返回 None。
    """
    if not file_pattern:
        print("未提供文件匹配模式，必须指定匹配模式才能运行测试")
        sys.exit(1)

    test_files = [test_file.replace(".py", "").replace("/", ".").replace("\\", ".")
                  for test_file in get_matching_files(file_pattern)]

    if not test_files:
        print("未找到匹配的测试文件。")
        sys.exit(1)

    loader = unittest.TestLoader()

    if running_in_ed:
        runner = unittest.TextTestRunner(resultclass=SingleTaskTestResult, verbosity=0, buffer=True)
        all_results = []

        for test_file in test_files:
            suite = loader.loadTestsFromName(test_file)
            result: SingleTaskTestResult = runner.run(suite)
            result.apply_hurdle()
            all_results.extend(result.test_results)

        all_results = sorted(all_results, key=lambda x: 1 if "[Aggregate]" in x["name"] else 0)

        ed_output = {
            "testcases": all_results,
        }
        return ed_output

    else:
        runner = unittest.TextTestRunner(verbosity=1)
        for test_file in test_files:
            print("\n\n\033[1m\033[94m" + f"正在运行 {test_file}..." + "\033[0m")
            print("----------------------------------------------------------------------")
            suite = loader.loadTestsFromName(test_file)
            runner.run(suite)

        return None


if __name__ == "__main__":
    p = argparse.ArgumentParser()

    p.add_argument(
        "task",
        help=(
            "你想运行的任务编号。\n"
            "留空则运行所有任务。\n\n"
            "示例: run_tests.py 3\n"
            "将运行 test_task3.py 中的测试。"
        ),
        default="",
        nargs="?",
    )
    p.add_argument(
        "--ed",
        action="store_true",
        help="在 Ed 平台上运行测试。",
    )

    args = p.parse_args()
    task_number = args.task

    if args.ed:
        task_number = None  # 在 Ed 中忽略用户输入，自动运行全部
    else:
        if task_number == '':
            task_number = input(f"请输入任务编号 [1 - {NUMBER_OF_TASKS_FOR_ASSIGNMENT}]，留空则运行所有任务：")

        try:
            task_number = int(task_number)
        except ValueError:
            task_number = None

    if task_number is not None:
        file_pattern = rf"^test_task{task_number}\.py$"
    else:
        file_pattern = rf"^test_task[1-{NUMBER_OF_TASKS_FOR_ASSIGNMENT}]\.py$"

    output = run_tests(file_pattern=file_pattern, running_in_ed=args.ed)

    if args.ed:
        print(json.dumps(output, indent=2))  # 输出 JSON 格式
```

---

这段代码是评测系统运行测试的核心工具，支持 Ed 系统自动评测或本地 CLI 使用。如果你希望我协助你撰写 test\_taskX 的测试文件结构，也可以继续提供模板。需要继续吗？
