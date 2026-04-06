# Shared Test Kit

`shared-test-kit` 폴더를 실제 `Data-Structures/` 폴더와 같은 루트 경로에 두면 바로 테스트를 실행할 수 있습니다.

## 빠른 설치

1. `shared-test-kit/` 폴더를 `Data-Structures/` 옆에 둡니다.
2. 아래 명령을 한 번 실행합니다.

```bash
./shared-test-kit/install.sh
```

3. 그 다음부터는 아래처럼 간단히 사용할 수 있습니다.

```bash
./test list 1
./test queue 3
```

여기서 마지막 숫자는 문제 번호입니다.
- `./test list 1` 의 `1`은 Linked List 1번 문제입니다.
- `./test queue 3` 의 `3`은 Stack and Queue 3번 문제입니다.

## 자주 쓰는 명령

```bash
./test list
./test list 1
./test list 5
./test queue 3
./test tree 4
./test bst 2
```

위 예시에서도 마지막 숫자는 각 자료구조 그룹의 문제 번호입니다.
- `./test list 5` 의 `5`는 Linked List 5번 문제입니다.
- `./test queue 3` 의 `3`은 Stack and Queue 3번 문제입니다.
- `./test tree 4` 의 `4`는 Binary Tree 4번 문제입니다.
- `./test bst 2` 의 `2`는 Binary Search Tree 2번 문제입니다.

그룹 별칭:
- `list` = `Linked_List`
- `queue` = `Stack_and_Queue`
- `tree` = `Binary_Tree`
- `bst` = `Binary_Search_Tree`

문제 번호와 파일명 대응 예시:
- `./test list 5` 에서 `5`는 Linked List의 5번 문제 번호입니다.
- 이 명령은 테스트 정의 파일 `Q5_A_LL.dstest.json`을 선택해 실행합니다.
- 이 테스트는 실제 소스 파일 `Data-Structures/Linked_List/Q5_A_LL.c`를 컴파일해서 검사합니다.
- 즉 `list`는 `Linked_List`, `5`는 문제 번호, `Q5_A_LL.c`는 그에 대응하는 C 파일이라고 보면 됩니다.

## 포함 파일

- `README.md`
- `test`
- `install.sh`
- `run_ds_tests.sh`
- `Data-Structures/`
- `Data-Structures/tools/ds_test_runner.py`
- `Data-Structures/tests/`

## 자료구조별 테스트 파일 정리

테스트 정의 파일은 모두 `shared-test-kit/Data-Structures/tests/` 아래에 있습니다.

### Linked List

- 총 7개
- `Q1_A_LL.dstest.json`
- `Q2_A_LL.dstest.json`
- `Q3_A_LL.dstest.json`
- `Q4_A_LL.dstest.json`
- `Q5_A_LL.dstest.json`
- `Q6_A_LL.dstest.json`
- `Q7_A_LL.dstest.json`

실행 예시:
```bash
./test list 1
./test list 7
```

### Stack and Queue

- 총 7개
- `Q1_C_SQ.dstest.json`
- `Q2_C_SQ.dstest.json`
- `Q3_C_SQ.dstest.json`
- `Q4_C_SQ.dstest.json`
- `Q5_C_SQ.dstest.json`
- `Q6_C_SQ.dstest.json`
- `Q7_C_SQ.dstest.json`

실행 예시:
```bash
./test queue 1
./test queue 7
```

### Binary Tree

- 총 8개
- `Q1_E_BT.dstest.json`
- `Q2_E_BT.dstest.json`
- `Q3_E_BT.dstest.json`
- `Q4_E_BT.dstest.json`
- `Q5_E_BT.dstest.json`
- `Q6_E_BT.dstest.json`
- `Q7_E_BT.dstest.json`
- `Q8_E_BT.dstest.json`

실행 예시:
```bash
./test tree 1
./test tree 8
```

### Binary Search Tree

- 총 5개
- `Q1_F_BST.dstest.json`
- `Q2_F_BST.dstest.json`
- `Q3_F_BST.dstest.json`
- `Q4_F_BST.dstest.json`
- `Q5_F_BST.dstest.json`

실행 예시:
```bash
./test bst 1
./test bst 5
```

## 문제별 테스트 입력값과 예상 출력

아래 내용은 각 `.dstest.json`에 정의된 테스트 케이스를 그대로 읽어서 정리한 것입니다.

설명:
- `입력값`은 실제 표준 입력을 보기 쉽게 가로 한 줄로 펼친 것입니다.
- `명령어 제외 값`은 `main` 메뉴 기준으로 명령 숫자를 빼고, 실제 자료구조에 넣은 값만 따로 정리한 것입니다.
- Binary Tree 문제는 `1 <트리 생성 입력값> 2 ... 0` 흐름을 기준으로, 트리 생성에 사용한 입력만 따로 분리합니다.
- `예상 출력`은 JSON의 원본 영어 문구를 바탕으로, README에서는 읽기 쉽게 한국어로 옮겨 적었습니다.
- `케이스 이름`은 보기 쉽게 한국어로 번역해 적고, 원래 JSON의 `name` 값은 괄호 안의 백틱으로 함께 적었습니다.

<details>
<summary><strong>Linked List</strong></summary>

#### `Q1_A_LL.dstest.json`

- 소스 파일: `../../Linked_List/Q1_A_LL.c`
- 케이스 수: 7

케이스 1: 예시 흐름에서 8 삽입 (`sample_flow_up_to_insert_8`)

입력값:
```text
1 2 1 3 1 5 1 7 1 9 1 8 2 3 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 2 3 5 7 9 8
```
예상 출력:
```text
결과 연결 리스트: 2 3 5 7 8 9
인덱스 4에 값 8 삽입
정렬된 결과 연결 리스트: 2 3 5 7 8 9
```

케이스 2: 예시 흐름에서 중복 5는 -1 반환 (`sample_flow_duplicate_5_returns_minus_1`)

입력값:
```text
1 2 1 3 1 5 1 7 1 9 1 8 1 5 2 3 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 2 3 5 7 9 8 5
```
예상 출력:
```text
결과 연결 리스트: 2 3 5 7 8 9
인덱스 -1에 값 5 삽입
정렬된 결과 연결 리스트: 2 3 5 7 8 9
```

케이스 3: 예시 흐름에서 11을 인덱스 6에 삽입 (`sample_flow_insert_11_at_index_6`)

입력값:
```text
1 2 1 3 1 5 1 7 1 9 1 8 1 11 2 3 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 2 3 5 7 9 8 11
```
예상 출력:
```text
결과 연결 리스트: 2 3 5 7 8 9 11
인덱스 6에 값 11 삽입
정렬된 결과 연결 리스트: 2 3 5 7 8 9 11
```

케이스 4: 별도 예시에서 중복 값 삽입 거부 (`reject_duplicate_value_from_separate_example`)

입력값:
```text
1 5 1 7 1 9 1 11 1 15 1 7 2 3 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 5 7 9 11 15 7
```
예상 출력:
```text
인덱스 -1에 값 7 삽입
정렬된 결과 연결 리스트: 5 7 9 11 15
```

케이스 5: 가장 작은 값을 맨 앞에 삽입 (`insert_smallest_to_front`)

입력값:
```text
1 10 1 20 1 30 1 5 2 3 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 10 20 30 5
```
예상 출력:
```text
결과 연결 리스트: 5 10 20 30
인덱스 0에 값 5 삽입
정렬된 결과 연결 리스트: 5 10 20 30
```

케이스 6: 원소가 하나뿐인 리스트는 인덱스 0 반환 (`single_item_list_reports_index_zero`)

입력값:
```text
1 42 2 3 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 42
```
예상 출력:
```text
결과 연결 리스트: 42
인덱스 0에 값 42 삽입
정렬된 결과 연결 리스트: 42
```

케이스 7: 음수 값도 정렬 유지 (`negative_values_stay_sorted`)

입력값:
```text
1 -3 1 4 1 0 1 -10 2 3 0
```
명령어 제외 값:
```text
리스트에 넣은 값: -3 4 0 -10
```
예상 출력:
```text
결과 연결 리스트: -10 -3 0 4
인덱스 0에 값 -10 삽입
정렬된 결과 연결 리스트: -10 -3 0 4
```

#### `Q2_A_LL.dstest.json`

- 소스 파일: `../../Linked_List/Q2_A_LL.c`
- 케이스 수: 5

케이스 1: 두 번째 리스트가 더 길 때 교차 병합 (`alternate_merge_when_second_list_is_longer`)

입력값:
```text
1 1 1 2 1 3 2 4 2 5 2 6 2 7 3 0
```
명령어 제외 값:
```text
리스트 1 값: 1 2 3
리스트 2 값: 4 5 6 7
```
예상 출력:
```text
결과 연결 리스트 1: 1 4 2 5 3 6
결과 연결 리스트 2: 7
```

케이스 2: 첫 번째 리스트가 더 길 때 교차 병합 (`alternate_merge_when_first_list_is_longer`)

입력값:
```text
1 1 1 5 1 7 1 3 1 9 1 11 2 6 2 10 2 2 2 4 3 0
```
명령어 제외 값:
```text
리스트 1 값: 1 5 7 3 9 11
리스트 2 값: 6 10 2 4
```
예상 출력:
```text
결과 연결 리스트 1: 1 6 5 10 7 2 3 4 9 11
결과 연결 리스트 2: 비어 있음
```

케이스 3: 각 리스트에 원소가 하나씩 있는 경우 (`one_element_each_list`)

입력값:
```text
1 10 2 20 3 0
```
명령어 제외 값:
```text
리스트 1 값: 10
리스트 2 값: 20
```
예상 출력:
```text
결과 연결 리스트 1: 10 20
결과 연결 리스트 2: 비어 있음
```

케이스 4: 두 번째 리스트가 비어 있으면 첫 번째 리스트 유지 (`second_list_empty_leaves_first_unchanged`)

입력값:
```text
1 8 1 9 1 10 3 0
```
명령어 제외 값:
```text
리스트 1 값: 8 9 10
리스트 2 값: (없음)
```
예상 출력:
```text
결과 연결 리스트 1: 8 9 10
결과 연결 리스트 2: 비어 있음
```

케이스 5: 첫 번째 리스트가 비어 있으면 옮길 것 없음 (`first_list_empty_moves_nothing`)

입력값:
```text
2 4 2 5 2 6 3 0
```
명령어 제외 값:
```text
리스트 1 값: (없음)
리스트 2 값: 4 5 6
```
예상 출력:
```text
결과 연결 리스트 1: 비어 있음
결과 연결 리스트 2: 4 5 6
```

#### `Q3_A_LL.dstest.json`

- 소스 파일: `../../Linked_List/Q3_A_LL.c`
- 케이스 수: 4
- 비고: Extended cases for moving odd nodes to the back while preserving relative order.

케이스 1: 예시 홀수를 뒤로 이동 (`sample_move_odds_to_back`)

입력값:
```text
1 2 1 3 1 4 1 7 1 15 1 18 2 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 2 3 4 7 15 18
```
예상 출력:
```text
홀수를 뒤로 이동한 결과 연결 리스트: 2 4 18 3 7 15
```

케이스 2: 모든 짝수 값은 제자리 유지 (`all_even_values_remain_in_place`)

입력값:
```text
1 2 1 4 1 6 1 8 2 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 2 4 6 8
```
예상 출력:
```text
홀수를 뒤로 이동한 결과 연결 리스트: 2 4 6 8
```

케이스 3: 모든 홀수 값은 제자리 유지 (`all_odd_values_remain_in_place`)

입력값:
```text
1 1 1 3 1 5 1 7 2 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 1 3 5 7
```
예상 출력:
```text
홀수를 뒤로 이동한 결과 연결 리스트: 1 3 5 7
```

케이스 4: 맨 앞의 홀수 노드가 모든 짝수 뒤로 이동 (`head_odd_moves_behind_all_evens`)

입력값:
```text
1 9 1 2 1 4 1 7 1 6 2 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 9 2 4 7 6
```
예상 출력:
```text
홀수를 뒤로 이동한 결과 연결 리스트: 2 4 6 9 7
```

#### `Q4_A_LL.dstest.json`

- 소스 파일: `../../Linked_List/Q4_A_LL.c`
- 케이스 수: 4
- 비고: Extended cases for moving even nodes to the back while preserving relative order.

케이스 1: 예시 짝수를 뒤로 이동 (`sample_move_evens_to_back`)

입력값:
```text
1 2 1 3 1 4 1 7 1 15 1 18 2 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 2 3 4 7 15 18
```
예상 출력:
```text
짝수를 뒤로 이동한 결과 연결 리스트: 3 7 15 2 4 18
```

케이스 2: 모든 홀수 값은 제자리 유지 (`all_odd_values_remain_in_place`)

입력값:
```text
1 1 1 3 1 5 1 7 2 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 1 3 5 7
```
예상 출력:
```text
짝수를 뒤로 이동한 결과 연결 리스트: 1 3 5 7
```

케이스 3: 모든 짝수 값은 제자리 유지 (`all_even_values_remain_in_place`)

입력값:
```text
1 2 1 4 1 6 1 8 2 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 2 4 6 8
```
예상 출력:
```text
짝수를 뒤로 이동한 결과 연결 리스트: 2 4 6 8
```

케이스 4: 맨 앞의 짝수 노드가 모든 홀수 뒤로 이동 (`head_even_moves_behind_all_odds`)

입력값:
```text
1 8 1 1 1 3 1 2 1 5 2 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 8 1 3 2 5
```
예상 출력:
```text
짝수를 뒤로 이동한 결과 연결 리스트: 1 3 5 8 2
```

#### `Q5_A_LL.dstest.json`

- 소스 파일: `../../Linked_List/Q5_A_LL.c`
- 케이스 수: 4
- 비고: Extended cases for front/back split with odd, even, and single-node lists.

케이스 1: 예시 앞뒤 분할 (`sample_front_back_split`)

입력값:
```text
1 2 1 3 1 5 1 6 1 7 2 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 2 3 5 6 7
```
예상 출력:
```text
앞 리스트: 2 3 5
뒤 리스트: 6 7
```

케이스 2: 짝수 길이 리스트는 균등하게 분할됨 (`even_length_split_is_balanced`)

입력값:
```text
1 1 1 2 1 3 1 4 1 5 1 6 2 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 1 2 3 4 5 6
```
예상 출력:
```text
앞 리스트: 1 2 3
뒤 리스트: 4 5 6
```

케이스 3: 노드가 하나뿐이면 앞 리스트로 들어감 (`single_node_goes_to_front`)

입력값:
```text
1 99 2 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 99
```
예상 출력:
```text
앞 리스트: 99
뒤 리스트: Empty
```

케이스 4: 노드가 3개면 앞 리스트가 하나 더 가짐 (`three_nodes_front_gets_extra_item`)

입력값:
```text
1 10 1 20 1 30 2 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 10 20 30
```
예상 출력:
```text
앞 리스트: 10 20
뒤 리스트: 30
```

#### `Q6_A_LL.dstest.json`

- 소스 파일: `../../Linked_List/Q6_A_LL.c`
- 케이스 수: 4
- 비고: Extended cases for moving the maximum value to the front.

케이스 1: 예시 최댓값을 맨 앞으로 이동 (`sample_move_max_to_front`)

입력값:
```text
1 30 1 20 1 40 1 70 1 50 2 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 30 20 40 70 50
```
예상 출력:
```text
가장 큰 값을 맨 앞으로 이동한 결과 연결 리스트: 70 30 20 40 50
```

케이스 2: 최댓값이 이미 맨 앞이면 리스트 유지 (`max_already_at_front_list_unchanged`)

입력값:
```text
1 90 1 20 1 30 1 40 2 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 90 20 30 40
```
예상 출력:
```text
가장 큰 값을 맨 앞으로 이동한 결과 연결 리스트: 90 20 30 40
```

케이스 3: 노드가 하나뿐인 리스트는 그대로 유지 (`single_node_list_stays_same`)

입력값:
```text
1 5 2 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 5
```
예상 출력:
```text
가장 큰 값을 맨 앞으로 이동한 결과 연결 리스트: 5
```

케이스 4: 음수만 있어도 가장 큰 값을 맨 앞으로 이동 (`negative_numbers_still_move_largest_to_front`)

입력값:
```text
1 -10 1 -3 1 -20 1 -7 2 0
```
명령어 제외 값:
```text
리스트에 넣은 값: -10 -3 -20 -7
```
예상 출력:
```text
가장 큰 값을 맨 앞으로 이동한 결과 연결 리스트: -3 -10 -20 -7
```

#### `Q7_A_LL.dstest.json`

- 소스 파일: `../../Linked_List/Q7_A_LL.c`
- 케이스 수: 4
- 비고: Extended cases for recursively reversing a linked list.

케이스 1: 예시 재귀 뒤집기 (`sample_recursive_reverse`)

입력값:
```text
1 1 1 2 1 3 1 4 1 5 2 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 1 2 3 4 5
```
예상 출력:
```text
연결 리스트를 뒤집은 결과: 5 4 3 2 1
```

케이스 2: 노드가 하나뿐이면 뒤집어도 그대로 (`single_node_reverse_is_same`)

입력값:
```text
1 42 2 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 42
```
예상 출력:
```text
연결 리스트를 뒤집은 결과: 42
```

케이스 3: 노드 2개 뒤집기 (`two_nodes_reverse`)

입력값:
```text
1 8 1 9 2 0
```
명령어 제외 값:
```text
리스트에 넣은 값: 8 9
```
예상 출력:
```text
연결 리스트를 뒤집은 결과: 9 8
```

케이스 4: 음수와 0을 포함한 뒤집기 (`reverse_with_negative_and_zero`)

입력값:
```text
1 -1 1 0 1 4 1 10 2 0
```
명령어 제외 값:
```text
리스트에 넣은 값: -1 0 4 10
```
예상 출력:
```text
연결 리스트를 뒤집은 결과: 10 4 0 -1
```

</details>
<details>
<summary><strong>Stack and Queue</strong></summary>

#### `Q1_C_SQ.dstest.json`

- 소스 파일: `../../Stack_and_Queue/Q1_C_SQ.c`
- 케이스 수: 1
- 비고: Sample case based on Stack and Queues Questions.pdf examples

케이스 1: create_queue_and_remove_odds (`create_queue_and_remove_odds`)

입력값:
```text
1 1 1 2 1 3 1 4 1 5 2 3 0
```
명령어 제외 값:
```text
리스트에 넣은 값(이후 큐 생성): 1 2 3 4 5
```
예상 출력:
```text
결과 큐: 1 2 3 4 5
홀수를 제거한 결과 큐: 2 4
```

#### `Q2_C_SQ.dstest.json`

- 소스 파일: `../../Stack_and_Queue/Q2_C_SQ.c`
- 케이스 수: 1
- 비고: Sample case based on Stack and Queues Questions.pdf examples

케이스 1: create_stack_and_remove_evens (`create_stack_and_remove_evens`)

입력값:
```text
1 1 1 3 1 5 1 6 1 7 2 3 0
```
명령어 제외 값:
```text
리스트에 넣은 값(이후 스택 생성): 1 3 5 6 7
```
예상 출력:
```text
결과 스택: 7 6 5 3 1
짝수를 제거한 결과 스택: 7 5 3 1
```

#### `Q3_C_SQ.dstest.json`

- 소스 파일: `../../Stack_and_Queue/Q3_C_SQ.c`
- 케이스 수: 1
- 비고: Sample case taken from Stack and Queues Questions.pdf

케이스 1: 예시 쌍별 연속 수 판정 (`sample_pairwise_consecutive_true`)

입력값:
```text
1 4 1 5 1 10 1 11 1 15 1 16 2 0
```
명령어 제외 값:
```text
스택에 넣은 값: 4 5 10 11 15 16
```
예상 출력:
```text
스택의 각 쌍은 연속된 수입니다.
```

#### `Q4_C_SQ.dstest.json`

- 소스 파일: `../../Stack_and_Queue/Q4_C_SQ.c`
- 케이스 수: 1
- 비고: Sample case taken from Stack and Queues Questions.pdf

케이스 1: 예시 큐 뒤집기 (`sample_reverse_queue`)

입력값:
```text
1 1 1 2 1 3 1 4 1 5 2 0
```
명령어 제외 값:
```text
큐에 넣은 값: 1 2 3 4 5
```
예상 출력:
```text
큐를 뒤집은 결과: 5 4 3 2 1
```

#### `Q5_C_SQ.dstest.json`

- 소스 파일: `../../Stack_and_Queue/Q5_C_SQ.c`
- 케이스 수: 1
- 비고: Sample case taken from Stack and Queues Questions.pdf

케이스 1: 예시 재귀 큐 뒤집기 (`sample_recursive_reverse_queue`)

입력값:
```text
1 1 1 2 1 3 1 4 1 5 2 0
```
명령어 제외 값:
```text
큐에 넣은 값: 1 2 3 4 5
```
예상 출력:
```text
뒤집은 결과 큐: 5 4 3 2 1
```

#### `Q6_C_SQ.dstest.json`

- 소스 파일: `../../Stack_and_Queue/Q6_C_SQ.c`
- 케이스 수: 1
- 비고: Sample case taken from Stack and Queues Questions.pdf

케이스 1: 예시 지정한 값이 맨 위에 올 때까지 제거 (`sample_remove_until_stack`)

입력값:
```text
1 7 1 6 1 5 1 4 1 3 1 2 1 1 3 4 0
```
명령어 제외 값:
```text
스택에 넣은 값: 7 6 5 4 3 2 1
```
예상 출력:
```text
지정한 값이 나올 때까지 제거한 결과 스택: 4 5 6 7
```

#### `Q7_C_SQ.dstest.json`

- 소스 파일: `../../Stack_and_Queue/Q7_C_SQ.c`
- 케이스 수: 1
- 비고: Sample case taken from Stack and Queues Questions.pdf

케이스 1: 예시 균형 잡힌 수식 (`sample_balanced_expression`)

입력값:
```text
1 {[]()[]} 2 0
```
명령어 제외 값:
```text
검사한 수식: {[]()[]}
```
예상 출력:
```text
{[]()[]}
균형 잡힘!
```

</details>
<details>
<summary><strong>Binary Tree</strong></summary>

#### `Q1_E_BT.dstest.json`

- 소스 파일: `../../Binary_Tree/Q1_E_BT.c`
- 케이스 수: 1
- 비고: Sample case taken from Binary Trees Questions.pdf

케이스 1: 예시 동일 트리 비교 (`sample_identical_trees`)

입력값:
```text
1 5 3 7 1 2 a a a a 4 8 a a a a 2 5 3 7 1 2 a a a a 4 8 a a a a 3 0
```
명령어 제외 값:
```text
트리 1 생성 입력값: 5 3 7 1 2 a a a a 4 8 a a a a
트리 2 생성 입력값: 5 3 7 1 2 a a a a 4 8 a a a a
```
예상 출력:
```text
결과 트리 1: 1 3 2 5 4 7 8
결과 트리 2: 1 3 2 5 4 7 8
두 트리는 구조가 같습니다.
```

#### `Q2_E_BT.dstest.json`

- 소스 파일: `../../Binary_Tree/Q2_E_BT.c`
- 케이스 수: 1
- 비고: Sample case taken from Binary Trees Questions.pdf

케이스 1: 예시 최대 높이 (`sample_max_height`)

입력값:
```text
1 4 2 6 1 3 a a a a 5 7 a a a a 2 0
```
명령어 제외 값:
```text
트리 생성 입력값: 4 2 6 1 3 a a a a 5 7 a a a a
```
예상 출력:
```text
결과 이진 트리: 1 2 3 4 5 6 7
이진 트리의 최대 높이: 2
```

#### `Q3_E_BT.dstest.json`

- 소스 파일: `../../Binary_Tree/Q3_E_BT.c`
- 케이스 수: 1
- 비고: Sample case taken from Binary Trees Questions.pdf

케이스 1: 예시 자식이 하나인 노드 수 (`sample_count_one_child_nodes`)

입력값:
```text
1 50 20 60 10 30 a a 55 a a a 80 a a 2 0
```
명령어 제외 값:
```text
트리 생성 입력값: 50 20 60 10 30 a a 55 a a a 80 a a
```
예상 출력:
```text
결과 이진 트리: 10 20 55 30 50 60 80
자식이 정확히 하나인 노드의 개수: 2
```

#### `Q4_E_BT.dstest.json`

- 소스 파일: `../../Binary_Tree/Q4_E_BT.c`
- 케이스 수: 1
- 비고: Sample case taken from Binary Trees Questions.pdf

케이스 1: 예시 홀수 노드 합 (`sample_sum_of_odd_nodes`)

입력값:
```text
1 50 40 60 11 35 a a a a 80 85 b b b b 2 0
```
명령어 제외 값:
```text
트리 생성 입력값: 50 40 60 11 35 a a a a 80 85 b b b b
```
예상 출력:
```text
결과 이진 트리: 11 40 35 50 80 60 85
이진 트리의 모든 홀수 값의 합: 131
```

#### `Q5_E_BT.dstest.json`

- 소스 파일: `../../Binary_Tree/Q5_E_BT.c`
- 케이스 수: 1
- 비고: Sample case taken from Binary Trees Questions.pdf

케이스 1: 예시 트리 좌우 반전 (`sample_mirror_tree`)

입력값:
```text
1 4 5 2 a 6 a a 3 1 a a a a 2 0
```
명령어 제외 값:
```text
트리 생성 입력값: 4 5 2 a 6 a a 3 1 a a a a
```
예상 출력:
```text
결과 이진 트리: 5 6 4 3 2 1
좌우 반전한 이진 트리: 1 2 3 4 6 5
```

#### `Q6_E_BT.dstest.json`

- 소스 파일: `../../Binary_Tree/Q6_E_BT.c`
- 케이스 수: 1
- 비고: Sample case taken from Binary Trees Questions.pdf

케이스 1: 예시 기준값보다 작은 노드 출력 (`sample_print_smaller_values`)

입력값:
```text
1 50 30 60 25 65 a a a a 10 75 a a a a 2 55 0
```
명령어 제외 값:
```text
트리 생성 입력값: 50 30 60 25 65 a a a a 10 75 a a a a
비교 기준 값: 55
```
예상 출력:
```text
결과 이진 트리: 25 30 65 50 10 60 75
55보다 작은 값들: 50 30 25 10
```

#### `Q7_E_BT.dstest.json`

- 소스 파일: `../../Binary_Tree/Q7_E_BT.c`
- 케이스 수: 1
- 비고: Sample case taken from Binary Trees Questions.pdf

케이스 1: 예시 최솟값 (`sample_smallest_value`)

입력값:
```text
1 50 30 60 25 65 a a a a 10 75 a a a a 2 0
```
명령어 제외 값:
```text
트리 생성 입력값: 50 30 60 25 65 a a a a 10 75 a a a a
```
예상 출력:
```text
결과 이진 트리: 25 30 65 50 10 60 75
이진 트리의 최솟값: 10
```

#### `Q8_E_BT.dstest.json`

- 소스 파일: `../../Binary_Tree/Q8_E_BT.c`
- 케이스 수: 1
- 비고: Sample case taken from Binary Trees Questions.pdf

케이스 1: 예시 증손자가 있는 노드 찾기 (`sample_has_great_grandchild`)

입력값:
```text
1 50 30 60 25 65 a a 20 a a a 10 75 a a a 15 a a 2 0
```
명령어 제외 값:
```text
트리 생성 입력값: 50 30 60 25 65 a a 20 a a a 10 75 a a a 15 a a
```
예상 출력:
```text
결과 이진 트리: 25 30 20 65 50 10 60 75 15
증손자가 하나 이상 있는 노드의 값들: 50
```

</details>
<details>
<summary><strong>Binary Search Tree</strong></summary>

#### `Q1_F_BST.dstest.json`

- 소스 파일: `../../Binary_Search_Tree/Q1_F_BST.c`
- 케이스 수: 1
- 비고: Sample case taken from Binary Search Trees Questions.pdf

케이스 1: 예시 레벨 순회 (`sample_level_order_traversal`)

입력값:
```text
1 20 1 15 1 50 1 10 1 18 1 25 1 80 2 0
```
명령어 제외 값:
```text
이진 탐색 트리에 넣은 값: 20 15 50 10 18 25 80
```
예상 출력:
```text
이진 탐색 트리의 레벨 순회 결과: 20 15 50 10 18 25 80
```

#### `Q2_F_BST.dstest.json`

- 소스 파일: `../../Binary_Search_Tree/Q2_F_BST.c`
- 케이스 수: 1
- 비고: Sample case taken from Binary Search Trees Questions.pdf

케이스 1: 예시 중위 순회(반복) (`sample_inorder_iterative`)

입력값:
```text
1 20 1 15 1 50 1 10 1 18 2 0
```
명령어 제외 값:
```text
이진 탐색 트리에 넣은 값: 20 15 50 10 18
```
예상 출력:
```text
이진 탐색 트리의 중위 순회 결과: 10 15 18 20 50
```

#### `Q3_F_BST.dstest.json`

- 소스 파일: `../../Binary_Search_Tree/Q3_F_BST.c`
- 케이스 수: 1
- 비고: Sample case taken from Binary Search Trees Questions.pdf

케이스 1: 예시 전위 순회(반복) (`sample_preorder_iterative`)

입력값:
```text
1 20 1 15 1 50 1 10 1 18 1 25 1 80 2 0
```
명령어 제외 값:
```text
이진 탐색 트리에 넣은 값: 20 15 50 10 18 25 80
```
예상 출력:
```text
이진 탐색 트리의 전위 순회 결과: 20 15 10 18 50 25 80
```

#### `Q4_F_BST.dstest.json`

- 소스 파일: `../../Binary_Search_Tree/Q4_F_BST.c`
- 케이스 수: 1
- 비고: Sample case taken from Binary Search Trees Questions.pdf

케이스 1: 예시 후위 순회(반복, 스택 1개) (`sample_postorder_iterative_single_stack`)

입력값:
```text
1 20 1 15 1 50 1 10 1 18 1 25 1 80 2 0
```
명령어 제외 값:
```text
이진 탐색 트리에 넣은 값: 20 15 50 10 18 25 80
```
예상 출력:
```text
이진 탐색 트리의 후위 순회 결과: 10 18 15 25 80 50 20
```

#### `Q5_F_BST.dstest.json`

- 소스 파일: `../../Binary_Search_Tree/Q5_F_BST.c`
- 케이스 수: 1
- 비고: Sample case taken from Binary Search Trees Questions.pdf

케이스 1: 예시 후위 순회(반복, 스택 2개) (`sample_postorder_iterative_two_stacks`)

입력값:
```text
1 20 1 15 1 50 1 10 1 18 1 25 1 80 2 0
```
명령어 제외 값:
```text
이진 탐색 트리에 넣은 값: 20 15 50 10 18 25 80
```
예상 출력:
```text
이진 탐색 트리의 후위 순회 결과: 10 18 15 25 80 50 20
```

</details>
