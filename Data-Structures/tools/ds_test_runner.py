#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
TESTS_ROOT = SCRIPT_ROOT / 'tests'
DEFAULT_BUILD_DIR = SCRIPT_ROOT / '.ds_test_build'
TEST_SUFFIX = '.dstest.json'
SOURCE_GLOB = 'Q*_*.c'
SOURCE_FOLDERS = (
    'Linked_List',
    'Stack_and_Queue',
    'Binary_Tree',
    'Binary_Search_Tree',
)


def has_source_structure(root: Path) -> bool:
    return all((root / folder).is_dir() for folder in SOURCE_FOLDERS)


def detect_source_root() -> Path:
    # Normal layout: tests/tools live inside the same source root as the question folders.
    if has_source_structure(SCRIPT_ROOT):
        return SCRIPT_ROOT

    # Shared-kit layout: shared-test-kit sits beside the real source root.
    workspace_root = SCRIPT_ROOT.parent.parent
    preferred = workspace_root / 'Data-Structures'
    candidates: list[Path] = []
    if preferred.exists() and has_source_structure(preferred):
        candidates.append(preferred)

    for child in sorted(workspace_root.iterdir()):
        if not child.is_dir() or child == preferred or child == SCRIPT_ROOT.parent:
            continue
        if has_source_structure(child):
            candidates.append(child)

    if candidates:
        return candidates[0]

    return SCRIPT_ROOT


SOURCE_ROOT = detect_source_root()


@dataclass
class CaseResult:
    name: str
    passed: bool
    reason: str
    stdout: str = ''
    stderr: str = ''
    expected: str = ''
    actual: str = ''
    case_input: str = ''


class RunnerError(Exception):
    pass


CASE_NAME_TRANSLATIONS = {
    "sample_level_order_traversal": "예시 레벨 순회",
    "right_skewed_tree_level_order": "오른쪽으로 치우친 트리의 레벨 순회",
    "duplicate_values_are_ignored_in_level_order": "중복 값을 무시한 레벨 순회",
    "sample_inorder_iterative": "예시 중위 순회(반복)",
    "duplicates_are_ignored_and_output_remains_sorted": "중복 값을 무시해도 출력은 정렬 상태 유지",
    "single_node_inorder": "단일 노드 중위 순회",
    "sample_preorder_iterative": "예시 전위 순회(반복)",
    "right_skewed_tree_preorder": "오른쪽으로 치우친 트리의 전위 순회",
    "duplicates_are_ignored_in_preorder": "중복 값을 무시한 전위 순회",
    "sample_postorder_iterative_single_stack": "예시 후위 순회(반복, 스택 1개)",
    "right_skewed_tree_postorder": "오른쪽으로 치우친 트리의 후위 순회",
    "left_subtree_with_two_children_postorder": "왼쪽 서브트리에 두 자식이 있는 후위 순회",
    "sample_postorder_iterative_two_stacks": "예시 후위 순회(반복, 스택 2개)",
    "right_skewed_tree_postorder_two_stacks": "오른쪽으로 치우친 트리의 후위 순회(스택 2개)",
    "left_subtree_with_two_children_postorder_two_stacks": "왼쪽 서브트리에 두 자식이 있는 후위 순회(스택 2개)",
    "sample_identical_trees": "예시 동일 트리 비교",
    "single_node_trees_are_identical": "노드가 하나뿐인 두 트리는 동일함",
    "different_structures_are_detected": "구조가 다른 트리를 구분함",
    "sample_max_height": "예시 최대 높이",
    "single_node_height_is_zero": "단일 노드 높이는 0",
    "left_skewed_tree_height_is_two": "왼쪽으로 치우친 트리 높이는 2",
    "sample_count_one_child_nodes": "예시 자식이 하나인 노드 수",
    "single_node_has_no_one_child_nodes": "노드가 하나뿐이면 자식이 하나인 노드는 없음",
    "left_skewed_tree_has_two_one_child_nodes": "왼쪽으로 치우친 트리에는 자식이 하나인 노드가 2개 있음",
    "sample_sum_of_odd_nodes": "예시 홀수 노드 합",
    "single_odd_node_sum_is_the_node_value": "홀수 노드가 하나면 합은 그 값과 같음",
    "all_even_values_sum_to_zero": "모든 짝수 값의 합은 0",
    "sample_mirror_tree": "예시 트리 좌우 반전",
    "single_node_mirror_is_unchanged": "노드가 하나뿐이면 반전해도 그대로",
    "two_child_tree_swaps_sides": "두 자식 트리는 좌우가 바뀜",
    "sample_print_smaller_values": "예시 기준값보다 작은 노드 출력",
    "single_node_below_threshold_is_printed": "기준값보다 작은 단일 노드는 출력됨",
    "preorder_filtered_values_keep_tree_order": "걸러낸 값도 전위 순서 유지",
    "sample_smallest_value": "예시 최솟값",
    "single_node_is_the_smallest_value": "노드가 하나뿐이면 그 값이 최솟값",
    "minimum_value_can_be_in_right_subtree": "최솟값은 오른쪽 서브트리에 있을 수도 있음",
    "sample_has_great_grandchild": "예시 증손자가 있는 노드 찾기",
    "left_chain_of_four_only_root_qualifies": "왼쪽으로 4개 이어진 트리에서는 루트만 조건을 만족함",
    "left_chain_of_five_has_two_qualifying_nodes": "왼쪽으로 5개 이어진 트리에서는 두 노드가 조건을 만족함",
    "sample_flow_up_to_insert_8": "예시 흐름에서 8 삽입",
    "sample_flow_duplicate_5_returns_minus_1": "예시 흐름에서 중복 5는 -1 반환",
    "sample_flow_insert_11_at_index_6": "예시 흐름에서 11을 인덱스 6에 삽입",
    "reject_duplicate_value_from_separate_example": "별도 예시에서 중복 값 삽입 거부",
    "insert_smallest_to_front": "가장 작은 값을 맨 앞에 삽입",
    "single_item_list_reports_index_zero": "원소가 하나뿐인 리스트는 인덱스 0 반환",
    "negative_values_stay_sorted": "음수 값도 정렬 유지",
    "alternate_merge_when_second_list_is_longer": "두 번째 리스트가 더 길 때 교차 병합",
    "alternate_merge_when_first_list_is_longer": "첫 번째 리스트가 더 길 때 교차 병합",
    "one_element_each_list": "각 리스트에 원소가 하나씩 있는 경우",
    "second_list_empty_leaves_first_unchanged": "두 번째 리스트가 비어 있으면 첫 번째 리스트 유지",
    "first_list_empty_moves_nothing": "첫 번째 리스트가 비어 있으면 옮길 것 없음",
    "sample_move_odds_to_back": "예시 홀수를 뒤로 이동",
    "all_even_values_remain_in_place": "모든 짝수 값은 제자리 유지",
    "all_odd_values_remain_in_place": "모든 홀수 값은 제자리 유지",
    "head_odd_moves_behind_all_evens": "맨 앞의 홀수 노드가 모든 짝수 뒤로 이동",
    "sample_move_evens_to_back": "예시 짝수를 뒤로 이동",
    "head_even_moves_behind_all_odds": "맨 앞의 짝수 노드가 모든 홀수 뒤로 이동",
    "sample_front_back_split": "예시 앞뒤 분할",
    "even_length_split_is_balanced": "짝수 길이 리스트는 균등하게 분할됨",
    "single_node_goes_to_front": "노드가 하나뿐이면 앞 리스트로 들어감",
    "three_nodes_front_gets_extra_item": "노드가 3개면 앞 리스트가 하나 더 가짐",
    "sample_move_max_to_front": "예시 최댓값을 맨 앞으로 이동",
    "max_already_at_front_list_unchanged": "최댓값이 이미 맨 앞이면 리스트 유지",
    "single_node_list_stays_same": "노드가 하나뿐인 리스트는 그대로 유지",
    "negative_numbers_still_move_largest_to_front": "음수만 있어도 가장 큰 값을 맨 앞으로 이동",
    "sample_recursive_reverse": "예시 재귀 뒤집기",
    "single_node_reverse_is_same": "노드가 하나뿐이면 뒤집어도 그대로",
    "two_nodes_reverse": "노드 2개 뒤집기",
    "reverse_with_negative_and_zero": "음수와 0을 포함한 뒤집기",
    "sample_create_queue_and_remove_odds": "예시 큐 생성 후 홀수 제거",
    "all_odd_values_are_removed": "모든 홀수 값 제거",
    "all_even_values_remain": "모든 짝수 값 유지",
    "sample_create_stack_and_remove_evens": "예시 스택 생성 후 짝수 제거",
    "all_even_values_are_removed": "모든 짝수 값 제거",
    "odd_values_remain_unchanged": "홀수 값은 그대로 유지",
    "sample_pairwise_consecutive_true": "예시 쌍별 연속 수 판정",
    "non_consecutive_pair_detected": "연속되지 않은 쌍 감지",
    "single_pair_is_consecutive": "원소 쌍 하나는 연속 수",
    "sample_reverse_queue": "예시 큐 뒤집기",
    "even_length_queue_reversed": "짝수 길이 큐 역순",
    "single_item_queue_stays_same": "원소 1개 큐는 그대로 유지",
    "sample_recursive_reverse_queue": "예시 재귀 큐 뒤집기",
    "even_length_queue_reversed_recursively": "짝수 길이 큐를 재귀로 역순",
    "single_item_queue_stays_same_recursively": "원소 1개 큐는 재귀로도 그대로 유지",
    "sample_remove_until_stack": "예시 지정한 값이 맨 위에 올 때까지 제거",
    "target_at_top_keeps_stack": "목표 값이 맨 위에 있으면 스택 유지",
    "target_at_bottom_leaves_one_item": "목표 값이 맨 아래에 있으면 원소 하나만 남음",
    "sample_balanced_expression": "예시 균형 잡힌 수식",
    "mismatched_expression_is_not_balanced": "괄호 종류가 다르면 균형 아님",
    "missing_closing_bracket_is_not_balanced": "닫는 괄호가 부족하면 균형 아님"
}


def translate_case_name(name: str) -> str:
    return CASE_NAME_TRANSLATIONS.get(name, name)


def normalize_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise RunnerError(f'JSON 형식이 올바르지 않습니다: {path}: {exc}') from exc


def discover_sources(root: Path) -> list[Path]:
    sources = []
    for path in sorted(root.rglob(SOURCE_GLOB)):
        if 'tests' in path.parts or 'tools' in path.parts or '.ds_test_build' in path.parts:
            continue
        sources.append(path)
    return sources


def source_to_test_path(source: Path) -> Path:
    rel = source.relative_to(SOURCE_ROOT)
    return TESTS_ROOT / rel.parent.name / f'{source.stem}{TEST_SUFFIX}'


def test_to_source_path(test_file: Path, payload: dict[str, Any]) -> Path:
    source = payload.get('source')
    if not source:
        raise RunnerError(f'"source" 항목이 없습니다: {test_file}')

    source_path = Path(source)
    if source_path.is_absolute():
        resolved = source_path
    else:
        resolved = (test_file.parent / source_path).resolve()
        if not resolved.exists():
            fallback = SOURCE_ROOT / test_file.parent.name / test_file.name.replace(TEST_SUFFIX, '.c')
            if fallback.exists():
                resolved = fallback

    if not resolved.exists():
        raise RunnerError(f'소스 파일을 찾을 수 없습니다: {test_file}: {resolved}')
    return resolved


def compile_source(source: Path, build_dir: Path, extra_args: list[str] | None = None) -> Path:
    build_dir.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha1(str(source).encode()).hexdigest()[:12]
    binary = build_dir / f'{source.stem}_{digest}'
    cmd = ['gcc', '-std=c11', '-Wall', '-Wextra', '-O0', str(source), '-o', str(binary)]
    if extra_args:
        cmd[1:1] = extra_args
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RunnerError(
            f'컴파일에 실패했습니다: {source}\n'
            f'실행 명령: {' '.join(cmd)}\n'
            f'{proc.stderr.strip()}'
        )
    return binary


def match_case(output: str, case: dict[str, Any]) -> tuple[bool, str, str, str]:
    use_normalized = case.get('normalize_whitespace', True)
    haystack = normalize_text(output) if use_normalized else output

    if 'expect_exact' in case:
        expected = case['expect_exact']
        expected_cmp = normalize_text(expected) if use_normalized else expected
        if haystack != expected_cmp:
            return False, '출력이 기대한 전체 문자열과 일치하지 않습니다', expected, haystack

    for needle in case.get('expect_contains_all', []):
        needle_cmp = normalize_text(needle) if use_normalized else needle
        if needle_cmp not in haystack:
            return False, '기대한 문자열이 출력에 없습니다', needle, haystack

    for needle in case.get('expect_not_contains', []):
        needle_cmp = normalize_text(needle) if use_normalized else needle
        if needle_cmp in haystack:
            return False, '출력에 있으면 안 되는 문자열이 포함되어 있습니다', needle, haystack

    for pattern in case.get('expect_regex_all', []):
        flags = re.MULTILINE | re.DOTALL
        target = output if not use_normalized else haystack
        if not re.search(pattern, target, flags):
            return False, '기대한 정규식 패턴과 일치하는 내용이 없습니다', pattern, target

    return True, '통과', '', ''




def split_case_input(case_input: str) -> list[str]:
    return [token for token in case_input.splitlines() if token != '']



def is_number_token(token: str) -> bool:
    try:
        int(token)
        return True
    except ValueError:
        return False



def consume_tree_tokens(tokens: list[str], start_idx: int) -> tuple[list[str], int]:
    consumed: list[str] = []
    if start_idx >= len(tokens):
        return consumed, start_idx

    root = tokens[start_idx]
    consumed.append(root)
    idx = start_idx + 1
    if not is_number_token(root):
        return consumed, idx

    stack = [root]
    while stack and idx < len(tokens):
        stack.pop()
        if idx >= len(tokens):
            break

        left = tokens[idx]
        consumed.append(left)
        idx += 1
        left_is_node = is_number_token(left)

        if idx >= len(tokens):
            break

        right = tokens[idx]
        consumed.append(right)
        idx += 1
        right_is_node = is_number_token(right)

        if right_is_node:
            stack.append(right)
        if left_is_node:
            stack.append(left)

    return consumed, idx



def summarize_command_free_values(test_file: Path, case_input: str, expected_text: str = '') -> list[str]:
    tokens = split_case_input(case_input)
    if not tokens:
        return ['(없음)']

    folder = test_file.parent.name
    test_name = test_file.name

    if folder == 'Linked_List':
        if test_name == 'Q2_A_LL.dstest.json':
            list1: list[str] = []
            list2: list[str] = []
            i = 0
            while i < len(tokens):
                if tokens[i] == '1' and i + 1 < len(tokens):
                    list1.append(tokens[i + 1])
                    i += 2
                elif tokens[i] == '2' and i + 1 < len(tokens):
                    list2.append(tokens[i + 1])
                    i += 2
                else:
                    i += 1
            return [
                f"리스트 1 값: {' '.join(list1) if list1 else '(없음)'}",
                f"리스트 2 값: {' '.join(list2) if list2 else '(없음)'}",
            ]

        values: list[str] = []
        i = 0
        while i < len(tokens):
            if tokens[i] == '1' and i + 1 < len(tokens):
                values.append(tokens[i + 1])
                i += 2
            else:
                i += 1
        return [f"리스트에 넣은 값: {' '.join(values) if values else '(없음)'}"]

    if folder == 'Stack_and_Queue':
        if test_name == 'Q7_C_SQ.dstest.json':
            expr = tokens[1] if len(tokens) > 1 else '(없음)'
            return [f'검사한 수식: {expr}']

        inserted: list[str] = []
        target_value: str | None = None
        i = 0
        while i < len(tokens):
            if tokens[i] == '1' and i + 1 < len(tokens):
                inserted.append(tokens[i + 1])
                i += 2
            elif test_name == 'Q6_C_SQ.dstest.json' and tokens[i] in {'2', '3'} and i + 1 < len(tokens):
                target_value = tokens[i + 1]
                i += 2
            else:
                i += 1

        lowered = expected_text.lower()
        if test_name == 'Q1_C_SQ.dstest.json':
            lines = [f"리스트에 넣은 값(이후 큐 생성): {' '.join(inserted) if inserted else '(없음)'}"]
        elif test_name == 'Q2_C_SQ.dstest.json':
            lines = [f"리스트에 넣은 값(이후 스택 생성): {' '.join(inserted) if inserted else '(없음)'}"]
        elif 'queue' in lowered:
            lines = [f"큐에 넣은 값: {' '.join(inserted) if inserted else '(없음)'}"]
        else:
            lines = [f"스택에 넣은 값: {' '.join(inserted) if inserted else '(없음)'}"]

        if target_value is not None:
            lines.append(f'제거 기준 값: {target_value}')
        return lines

    if folder == 'Binary_Search_Tree':
        inserted: list[str] = []
        i = 0
        while i < len(tokens):
            if tokens[i] == '1' and i + 1 < len(tokens):
                inserted.append(tokens[i + 1])
                i += 2
            else:
                i += 1
        return [f"이진 탐색 트리에 넣은 값: {' '.join(inserted) if inserted else '(없음)'}"]

    if folder == 'Binary_Tree':
        if test_name == 'Q1_E_BT.dstest.json':
            tree1_tokens, next_idx = consume_tree_tokens(tokens, 1)
            tree2_tokens, _ = consume_tree_tokens(tokens, next_idx + 1)
            return [
                f"트리 1 생성 입력값: {' '.join(tree1_tokens) if tree1_tokens else '(없음)'}",
                f"트리 2 생성 입력값: {' '.join(tree2_tokens) if tree2_tokens else '(없음)'}",
            ]

        if test_name == 'Q6_E_BT.dstest.json':
            tree_tokens = tokens[1:-3] if len(tokens) >= 4 else []
            extra_value = tokens[-2] if len(tokens) >= 2 else '(없음)'
            return [
                f"트리 생성 입력값: {' '.join(tree_tokens) if tree_tokens else '(없음)'}",
                f'비교 기준 값: {extra_value}',
            ]

        tree_tokens = tokens[1:-2] if len(tokens) >= 3 else []
        return [f"트리 생성 입력값: {' '.join(tree_tokens) if tree_tokens else '(없음)'}"]

    return ['명령어 제외 값을 해석하지 못했습니다.']



def describe_success_expectation(case: dict[str, Any]) -> str:
    expected_lines: list[str] = []
    if 'expect_exact' in case:
        expected_lines.append(str(case['expect_exact']))
    expected_lines.extend(str(item) for item in case.get('expect_contains_all', []))
    if case.get('expect_regex_all'):
        expected_lines.append('[정규식 일치 필요]')
        expected_lines.extend(str(item) for item in case['expect_regex_all'])
    if case.get('expect_not_contains'):
        expected_lines.append('[포함되면 안 되는 문자열]')
        expected_lines.extend(str(item) for item in case['expect_not_contains'])
    return '\n'.join(expected_lines) if expected_lines else '테스트 조건을 만족하는 출력'

def run_case(binary: Path, case: dict[str, Any]) -> CaseResult:
    name = case.get('name', 'unnamed')
    timeout_sec = case.get('timeout_sec', 5)

    try:
        proc = subprocess.run(
            [str(binary)],
            input=case.get('input', ''),
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
    except subprocess.TimeoutExpired as exc:
        return CaseResult(
            name=name,
            passed=False,
            reason=f'프로그램이 {timeout_sec}초 안에 종료되지 않았습니다',
            stdout=exc.stdout or '',
            stderr=exc.stderr or '',
            expected=describe_success_expectation(case),
            actual='시간 초과',
            case_input=case.get('input', ''),
        )

    combined_output = proc.stdout
    if case.get('include_stderr_in_match', False) and proc.stderr:
        combined_output += '\n' + proc.stderr

    if proc.returncode != 0:
        return CaseResult(
            name=name,
            passed=False,
            reason=f'프로그램이 종료 코드 {proc.returncode}로 끝났습니다',
            stdout=proc.stdout,
            stderr=proc.stderr,
            expected=describe_success_expectation(case),
            actual=f'종료 코드 {proc.returncode}',
            case_input=case.get('input', ''),
        )

    passed, reason, expected, actual = match_case(combined_output, case)
    return CaseResult(
        name=name,
        passed=passed,
        reason=reason,
        stdout=proc.stdout,
        stderr=proc.stderr,
        expected=expected,
        actual=actual,
        case_input=case.get('input', ''),
    )


def run_test_file(test_file: Path, build_dir: Path) -> tuple[Path, list[CaseResult], dict[str, Any]]:
    payload = load_json(test_file)
    source = test_to_source_path(test_file, payload)
    cases = payload.get('cases', [])
    if not cases:
        return source, [], payload
    binary = compile_source(source, build_dir, payload.get('compile_args'))
    results = [run_case(binary, case) for case in cases]
    return source, results, payload


def simplify_expected_text(value: str) -> str:
    text = value.decode() if isinstance(value, bytes) else str(value)
    simplified_lines: list[str] = []
    for raw_line in text.strip().splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith('[') and line.endswith(']'):
            simplified_lines.append(line)
            continue
        if ': ' in line:
            simplified_lines.append(line.split(': ', 1)[1].strip())
        else:
            simplified_lines.append(line)
    return '\n'.join(simplified_lines) if simplified_lines else '(없음)'


def print_detail_block(label: str, value: str, max_lines: int = 40) -> None:
    text = value.decode() if isinstance(value, bytes) else str(value)
    print(f'    {label}:')
    if not text.strip():
        print('      (없음)')
        return
    for line in text.strip().splitlines()[:max_lines]:
        print(f'      {line}')



def simplify_actual_output(value: str) -> str:
    text = value.decode() if isinstance(value, bytes) else str(value)
    normalized = normalize_text(text)
    if not normalized:
        return '(없음)'

    split_markers = [
        'The resulting',
        'The odd',
        'The even',
        'The expression',
        'The value',
        'The tree',
        'The linked list',
        'The stack',
        'The queue',
        'The binary',
        'The node',
        'The sum',
        'The smallest',
        'The height',
        'Two trees',
        'Identical',
        'Not identical',
        'not balanced!',
        'balanced!',
        'Please input',
        'Input ',
    ]

    segmented = normalized
    for marker in split_markers:
        segmented = segmented.replace(marker, f'\n{marker}')

    meaningful: list[str] = []
    for raw_segment in segmented.splitlines():
        segment = raw_segment.strip()
        if not segment:
            continue
        lower = segment.lower()
        if re.match(r'^\d+:\s', segment):
            continue
        if lower.startswith('please input'):
            continue
        if lower.startswith('input '):
            continue
        if lower == 'quit:':
            continue
        meaningful.append(segment)

    if meaningful:
        return meaningful[-1]
    return normalized



def print_results_for_file(test_file: Path, source: Path, results: list[CaseResult]) -> tuple[int, int, int]:
    rel_test = test_file.relative_to(SCRIPT_ROOT)
    rel_source = source.relative_to(SOURCE_ROOT)

    if not results:
        print(f'⏭️  [건너뜀] {rel_test} -> {rel_source} (아직 정의된 테스트 케이스가 없습니다)')
        return 0, 0, 0

    passed = sum(1 for result in results if result.passed)
    total = len(results)
    icon = '✅' if passed == total else '❌'
    print(f'{icon} [{passed}/{total}] {rel_test} -> {rel_source}')
    for index, result in enumerate(results, 1):
        display_name = translate_case_name(result.name)
        if result.passed:
            print(f'  - ✅ {index}번 {display_name}')
            continue

        print(f'  - ❌ {index}번 {display_name}: {result.reason}')
        if not result.passed:
            compact_input = ' '.join(result.case_input.split()) if result.case_input else ''
            print_detail_block('입력값', compact_input, max_lines=1)

            command_free = '\n'.join(
                summarize_command_free_values(test_file, result.case_input, result.expected or '')
            )
            print_detail_block('명령어 제외 값', command_free, max_lines=20)
            print_detail_block('기대값', simplify_expected_text(result.expected or '(없음)'), max_lines=20)

            out = result.stdout.decode() if isinstance(result.stdout, bytes) else result.stdout
            actual_text = str(result.actual).strip() if result.actual else ''
            if actual_text.startswith('종료 코드') or actual_text == '시간 초과':
                display_actual = actual_text
            else:
                display_actual = simplify_actual_output(out or actual_text)
            print_detail_block('실제 결과', display_actual, max_lines=40)

            err = result.stderr.decode() if isinstance(result.stderr, bytes) else result.stderr
            if err and err.strip():
                print_detail_block('stderr', err, max_lines=20)
    return passed, total, 1 if passed != total else 0


def matches_filter(path_text: str, folder: str | None, test: str | None) -> bool:
    if folder and folder not in path_text:
        return False
    if test and test not in path_text:
        return False
    return True


def scaffold_definition(source: Path) -> Path:
    test_path = source_to_test_path(source)
    test_path.parent.mkdir(parents=True, exist_ok=True)
    rel_source = Path('../../') / source.parent.name / source.name
    payload = {
        'source': str(rel_source).replace('\\', '/'),
        'notes': '해당 PDF의 예시 입력/출력을 바탕으로 cases를 채우세요.',
        'cases': [],
    }
    test_path.write_text(json.dumps(payload, indent=2) + '\n')
    return test_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='JSON 테스트 케이스를 이용해 자료구조 C 프로그램을 컴파일하고 실행합니다.')
    parser.add_argument('--list', action='store_true', help='문제 소스와 테스트 정의 파일 존재 여부를 출력합니다')
    parser.add_argument('--folder', help='예: Linked_List 처럼 특정 폴더만 포함합니다')
    parser.add_argument('--test', help='예: Q1_A_LL 처럼 특정 문제만 포함합니다')
    parser.add_argument('--build-dir', default=str(DEFAULT_BUILD_DIR), help='컴파일된 테스트 바이너리를 저장할 폴더입니다')
    parser.add_argument('--scaffold-missing', action='store_true', help='없는 테스트 정의 파일을 빈 템플릿으로 생성합니다')
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sources = discover_sources(SOURCE_ROOT)
    selected_sources = [
        source for source in sources
        if matches_filter(str(source.relative_to(SOURCE_ROOT)), args.folder, args.test)
    ]

    if args.scaffold_missing:
        created = 0
        for source in selected_sources:
            test_path = source_to_test_path(source)
            if not test_path.exists():
                scaffold_definition(source)
                created += 1
                print(f'생성됨: {test_path.relative_to(SCRIPT_ROOT)}')
        print(f'없는 테스트 정의 파일 {created}개를 생성했습니다.')
        return 0

    if args.list:
        for source in selected_sources:
            test_path = source_to_test_path(source)
            status = '준비됨' if test_path.exists() else '없음'
            icon = '✅' if test_path.exists() else '⚠️'
            print(f'{icon} {status:7} {source.relative_to(SOURCE_ROOT)} -> {test_path.relative_to(SCRIPT_ROOT)}')
        return 0

    if not selected_sources:
        print('조건에 맞는 문제 소스를 찾지 못했습니다.')
        return 1

    build_dir = Path(args.build_dir)
    total_passed = 0
    total_cases = 0
    failed_files = 0
    missing_files = 0
    skipped_files = 0

    for source in selected_sources:
        test_file = source_to_test_path(source)
        if not test_file.exists():
            missing_files += 1
            print(f'⚠️  [없음] {source.relative_to(SOURCE_ROOT)} -> {test_file.relative_to(SCRIPT_ROOT)}')
            continue
        try:
            resolved_source, results, _payload = run_test_file(test_file, build_dir)
            passed, total, failed = print_results_for_file(test_file, resolved_source, results)
            total_passed += passed
            total_cases += total
            failed_files += failed
            if not results:
                skipped_files += 1
        except RunnerError as exc:
            failed_files += 1
            print(f'💥 [오류] {test_file.relative_to(SCRIPT_ROOT)}')
            print(f'  {exc}')

    overall_icon = '✅' if not failed_files and not missing_files and not skipped_files else '❌'
    summary_parts = [f'총 {total_cases}개 케이스 중 {total_passed}개 통과']
    if missing_files:
        summary_parts.append(f'테스트 정의 파일 없음 {missing_files}개')
    if skipped_files:
        summary_parts.append(f'건너뜀 {skipped_files}개')
    print(f"\n{overall_icon} 요약: {', '.join(summary_parts)}")
    return 1 if failed_files or missing_files else 0


if __name__ == '__main__':
    sys.exit(main())
