import argparse
import re
import sys
from pathlib import Path


def run(source):
    lines = re.split(r"\r?\n|~", source.strip())

    if lines[0] != "레전드 시" or lines[-1] != "아무 맛도 안난다":
        raise ValueError(
            "첫 줄은 '레전드 시', 마지막 줄은 '아무 맛도 안난다'여야 해요."
        )

    variables = {}
    variable_name = r"쓴|쓰으*은"
    repeat_start = "화요알"
    repeat_end = "화요알끝"

    # 실행 전에 반복문의 시작 줄과 끝 줄을 짝지어요.
    loop_ends = {}
    loop_starts = {}
    open_loops = []

    for index, line in enumerate(lines):
        if line == repeat_end:
            if not open_loops:
                raise ValueError(f"{index + 1}번째 줄에 짝이 없는 화요알끝이 있어요.")
            start = open_loops.pop()
            loop_ends[start] = index
            loop_starts[index] = start
        elif line.startswith(repeat_start):
            open_loops.append(index)

    if open_loops:
        line_number = open_loops[-1] + 1
        raise ValueError(f"{line_number}번째 줄의 화요알에 화요알끝이 필요해요.")

    remaining_repeats = {}

    def read_term(term):
        match = re.fullmatch(rf"({variable_name})?([.,]*)", term)
        if match is None:
            raise ValueError(f"잘못된 숫자 표현: {term!r}")

        name, signs = match.groups()
        value = variables.get(name, 0)
        return value + signs.count(".") - signs.count(",")

    def number(expression):
        parts = re.split(r"( +|/)", expression)
        if len(parts) > 1 and not all(parts[::2]):
            raise ValueError("곱셈과 나눗셈 기호 양쪽에 값이 필요해요.")

        result = read_term(parts[0])
        for operator, term in zip(parts[1::2], parts[2::2]):
            value = read_term(term)
            if operator == "/":
                if value == 0:
                    raise ValueError("0으로 나눌 수 없어요.")
                result //= value
            else:
                result *= value

        return result

    def execute(line, next_line):
        if not line:
            return next_line

        if line.startswith("사랑"):
            condition, separator, command = line[len("사랑"):].partition("?")
            if not separator:
                raise ValueError("사랑 뒤에는 조건과 ?가 필요해요.")
            if number(condition) == 0:
                return execute(command, next_line)
            return next_line

        if line.startswith("됬"):
            target = number(line[len("됬"):]) - 1
            if not 0 <= target < len(lines):
                raise ValueError(f"이동할 줄이 없어요: {target + 1}")

            # 이동하면서 빠져나간 반복문의 횟수를 정리해요.
            for start in list(remaining_repeats):
                if not start < target <= loop_ends[start]:
                    del remaining_repeats[start]
            return target

        if line.startswith("심박수!"):
            return None, number(line[len("심박수!"):])

        assignment = re.fullmatch(rf"({variable_name})(.*)", line)
        if assignment:
            name, expression = assignment.groups()
            if expression == "단?":
                variables[name] = int(input())
            else:
                variables[name] = number(expression)
            return next_line

        text_output = re.fullmatch(r'단"([^"]*)"!', line)
        if text_output:
            print(text_output.group(1), end="")
            return next_line

        if line.startswith("단") and line.endswith("!"):
            print(number(line[1:-1]), end="")
            return next_line

        if line.startswith("단") and line.endswith("ㅋ"):
            expression = line[1:-1]
            print(chr(number(expression)) if expression else "\n", end="")
            return next_line

        raise ValueError(f"알 수 없는 명령: {line!r}")

    line_index = 1
    while line_index < len(lines) - 1:
        if line_index == 0:
            line_index = 1
            continue

        if line_index in loop_ends:
            expression = lines[line_index][len(repeat_start):]
            if not expression:
                raise ValueError(f"{line_index + 1}번째 줄의 화요알에 횟수를 써 주세요.")

            count = number(expression)
            if count <= 0:
                line_index = loop_ends[line_index] + 1
            else:
                remaining_repeats[line_index] = count
                line_index += 1
            continue

        if line_index in loop_starts:
            start = loop_starts[line_index]
            count = remaining_repeats.get(start, 0)

            if count > 1:
                remaining_repeats[start] = count - 1
                line_index = start + 1
            else:
                remaining_repeats.pop(start, None)
                line_index += 1
            continue

        result = execute(lines[line_index], line_index + 1)
        if isinstance(result, tuple):
            return result[1]
        line_index = result

    return 0


def main():
    parser = argparse.ArgumentParser(description="쓴랭 소스 파일을 실행해요.")
    default_source = Path(__file__).with_name("example.sseun")
    if not default_source.is_file():
        default_source = default_source.with_suffix(".txt")
    parser.add_argument("source", nargs="?", type=Path, default=default_source)
    args = parser.parse_args()

    try:
        return run(args.source.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError, EOFError) as error:
        print(f"{args.source.name}: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
