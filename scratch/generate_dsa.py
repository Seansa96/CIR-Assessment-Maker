import os
import yaml

class multiline_str(str): pass

def multiline_representer(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(multiline_str, multiline_representer)

def save(filename, data):
    path = os.path.join(r"c:\Users\SeanS\Downloads\cir_app\data\assessments", filename)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, width=1000)

hashmap_lesson = {
    "schemaVersion": 1,
    "id": "dsa-hashmap-concept-lesson",
    "title": "Hashmaps: Fast Key-Value Storage",
    "assessmentType": "conceptLesson",
    "categoryId": "dsa",
    "subcategoryIds": ["dsa-hashmaps"],
    "modeDefault": "learn",
    "lesson": {
        "introduction": "An in-depth look at Hashmaps (or Hash Tables), one of the most powerful and widely used data structures for achieving O(1) average time complexity for lookups, insertions, and deletions.",
        "sections": [
            {
                "id": "hashmap-basics",
                "title": "What is a Hashmap?",
                "content": multiline_str("A **Hashmap** (or Hash Table) is a data structure that implements an associative array abstract data type, a structure that can map keys to values.\n\nAt its core, a hashmap uses a **hash function** to compute an index (also called a hash code) into an array of buckets or slots, from which the desired value can be found.\n\n### Key Characteristics:\n- **Keys must be unique** (and usually immutable, like strings or integers).\n- **Values can be anything** (and can be duplicated).\n- Offers on average **O(1)** time complexity for search, insert, and delete operations.\n\nWhen you think of a hashmap, think of a real-world dictionary: you have a word (the key) and you use its alphabetical position to quickly find its definition (the value)."),
                "check": {
                    "id": "hashmap-q1",
                    "type": "multipleChoice",
                    "prompt": "What is the average time complexity for looking up a value in a hashmap by its key?",
                    "choices": [
                        {"id": "a", "text": "O(N)"},
                        {"id": "b", "text": "O(log N)"},
                        {"id": "c", "text": "O(1)"}
                    ],
                    "answer": {"choiceId": "c"},
                    "explanation": "Hashmaps achieve O(1) average time complexity because the hash function directly computes the memory location of the value without needing to iterate."
                }
            },
            {
                "id": "hash-functions-collisions",
                "title": "Hash Functions and Collisions",
                "content": multiline_str("A perfect hash function assigns every key to a unique bucket. However, since the number of possible keys usually vastly exceeds the number of buckets (the array size), two distinct keys can produce the same hash index. This is called a **collision**.\n\n### Handling Collisions\nThere are two primary methods for resolving collisions:\n\n1. **Chaining (Separate Chaining):** \n   Each bucket in the array points to a linked list (or another dynamic data structure). When multiple keys hash to the same index, their key-value pairs are stored in the linked list at that index. During a lookup, the hashmap traverses the linked list to find the matching key.\n\n2. **Open Addressing:** \n   If a collision occurs, the hashmap probes for the next available empty bucket in the array. Common probing techniques include linear probing (checking the next slot), quadratic probing, and double hashing.\n\n### Load Factor\nThe performance of a hashmap degrades if it becomes too full. The **load factor** is the ratio of the number of stored items to the number of buckets (`n/k`). When the load factor exceeds a certain threshold (e.g., 0.75), the hashmap automatically resizes its internal array (usually doubling it) and rehashes all existing keys."),
                "check": {
                    "id": "hashmap-q2",
                    "type": "multipleChoice",
                    "prompt": "What happens in a hashmap using 'chaining' when two different keys hash to the same index?",
                    "choices": [
                        {"id": "a", "text": "The hashmap crashes or throws an exception."},
                        {"id": "b", "text": "The new key-value pair overwrites the old one."},
                        {"id": "c", "text": "Both key-value pairs are stored in a linked list at that index."},
                        {"id": "d", "text": "The hashmap linearly searches for the next empty array slot."}
                    ],
                    "answer": {"choiceId": "c"},
                    "explanation": "In chaining, collisions are resolved by storing multiple elements in a linked list attached to the bucket index."
                }
            }
        ]
    }
}

big_o_lesson = {
    "schemaVersion": 1,
    "id": "dsa-big-o-concept-lesson",
    "title": "Big O Notation: Analyzing Complexity",
    "assessmentType": "conceptLesson",
    "categoryId": "dsa",
    "subcategoryIds": ["dsa-complexity"],
    "modeDefault": "learn",
    "lesson": {
        "introduction": "An in-depth guide to Big O Notation, the mathematical language used to describe the efficiency and scalability of algorithms in computer science.",
        "sections": [
            {
                "id": "big-o-basics",
                "title": "What is Big O?",
                "content": multiline_str("**Big O Notation** describes how the runtime or memory requirements of an algorithm grow as the input size (`N`) grows. It provides an upper bound, focusing on the worst-case scenario and the fundamental scaling behavior rather than exact hardware execution time.\n\n### Why do we drop constants and lower-order terms?\nWhen analyzing an algorithm, we might find its exact runtime is `3N^2 + 5N + 10` operations. \nAs `N` becomes very large (e.g., millions), the `N^2` term completely dominates the growth. The constant multiplier `3` and the smaller terms `5N + 10` become mathematically insignificant to the overall shape of the growth curve. \nThus, `O(3N^2 + 5N + 10)` simplifies directly to **`O(N^2)`**.\n\nBig O is about the *trend*, answering the question: \"If I double the input size, how much longer does it take?\""),
                "check": {
                    "id": "big-o-q1",
                    "type": "multipleChoice",
                    "prompt": "Which of the following correctly simplifies the expression `O(4N + N^3 + 100)`?",
                    "choices": [
                        {"id": "a", "text": "O(N)"},
                        {"id": "b", "text": "O(N^3)"},
                        {"id": "c", "text": "O(4N + N^3)"}
                    ],
                    "answer": {"choiceId": "b"},
                    "explanation": "We drop constants and lower order terms. The highest order term is `N^3`, so the overall complexity is `O(N^3)`."
                }
            },
            {
                "id": "common-complexities",
                "title": "Common Time Complexities",
                "content": multiline_str("Here are the most common time complexities, ordered from fastest (best) to slowest (worst):\n\n- **O(1) Constant:** The runtime is exactly the same regardless of the input size. Example: Array lookup by index, Hashmap lookup.\n- **O(log N) Logarithmic:** The runtime grows very slowly. The algorithm typically cuts the problem size in half each step. Example: Binary Search.\n- **O(N) Linear:** The runtime grows directly proportionally to the input size. Example: Iterating through an array once.\n- **O(N log N) Linearithmic:** Slightly worse than linear. Example: Efficient sorting algorithms like Merge Sort or Quick Sort.\n- **O(N^2) Quadratic:** The runtime grows quadratically. Usually indicates nested loops over the data. Example: Bubble Sort, Selection Sort.\n- **O(2^N) Exponential:** Runtime doubles with each addition to the input data space. Often seen in naive recursive solutions without memoization. Example: Recursive Fibonacci.\n- **O(N!) Factorial:** Runtime grows astronomically fast. Example: Generating all permutations of a string."),
                "check": {
                    "id": "big-o-q2",
                    "type": "multipleChoice",
                    "prompt": "An algorithm repeatedly divides the dataset in half until it finds the target value. What is its time complexity?",
                    "choices": [
                        {"id": "a", "text": "O(N)"},
                        {"id": "b", "text": "O(log N)"},
                        {"id": "c", "text": "O(1)"}
                    ],
                    "answer": {"choiceId": "b"},
                    "explanation": "Algorithms that repeatedly halve the search space, like Binary Search, operate in O(log N) logarithmic time."
                }
            },
            {
                "id": "space-complexity",
                "title": "Space Complexity",
                "content": multiline_str("Big O is not just for time! It is equally important for analyzing **Space (Memory) Complexity**.\n\nSpace complexity measures how much *extra* memory an algorithm needs to run as a function of the input size. \n\n- If you sort an array strictly in-place, the space complexity is **O(1)**.\n- If your algorithm creates a new secondary array of the same size as the input, the space complexity is **O(N)**.\n- A recursive function has a hidden space complexity due to the **Call Stack**. A recursion depth of `N` requires **O(N)** space."),
                "check": {
                    "id": "big-o-q3",
                    "type": "multipleChoice",
                    "prompt": "If a function takes an array of size `N`, and creates a hashmap to store the frequency of every element in that array, what is the worst-case space complexity?",
                    "choices": [
                        {"id": "a", "text": "O(1)"},
                        {"id": "b", "text": "O(log N)"},
                        {"id": "c", "text": "O(N)"}
                    ],
                    "answer": {"choiceId": "c"},
                    "explanation": "In the worst case (all elements are unique), the hashmap will store N key-value pairs, resulting in O(N) extra space used."
                }
            }
        ]
    }
}

big_o_worked_example = {
    "schemaVersion": 1,
    "id": "dsa-big-o-function-worked-example",
    "title": "Finding the Big O of a Function",
    "assessmentType": "workedExample",
    "categoryId": "dsa",
    "subcategoryIds": ["dsa-complexity"],
    "modeDefault": "practice",
    "workedExamples": [
        {
            "id": "we1",
            "title": "Analyzing Nested and Sequential Loops",
            "problem": multiline_str("Consider the following function in Python-like pseudocode. Our goal is to determine its overall **Time Complexity** in Big O notation.\n\n```python\ndef analyze_this(array):\n    n = len(array)\n    \n    # Block 1\n    for i in range(n):\n        print(array[i])\n        \n    # Block 2\n    for i in range(n):\n        for j in range(n):\n            print(array[i], array[j])\n            \n    # Block 3\n    for i in range(10):\n        print(\"Hello!\")\n```\n\nBreak down the complexity of each block, and then determine the final Big O of the entire function."),
            "steps": [
                {
                    "id": "step1",
                    "title": "Analyze Block 1",
                    "instruction": "Determine the time complexity of the first block (a single loop iterating over `array`).",
                    "type": "multipleChoice",
                    "prompt": "What is the Big O of Block 1?",
                    "choices": [
                        {"id": "a", "text": "O(1)"},
                        {"id": "b", "text": "O(N)"},
                        {"id": "c", "text": "O(N^2)"}
                    ],
                    "answer": {"choiceId": "b"},
                    "explanation": "Block 1 iterates from 0 to N-1 exactly once. Therefore, it takes O(N) linear time."
                },
                {
                    "id": "step2",
                    "title": "Analyze Block 2",
                    "instruction": "Determine the time complexity of the second block (the nested loops).",
                    "type": "multipleChoice",
                    "prompt": "What is the Big O of Block 2?",
                    "choices": [
                        {"id": "a", "text": "O(N)"},
                        {"id": "b", "text": "O(N log N)"},
                        {"id": "c", "text": "O(N^2)"}
                    ],
                    "answer": {"choiceId": "c"},
                    "explanation": "Block 2 features an outer loop that runs N times, and an inner loop that also runs N times. N * N = N^2, meaning it takes O(N^2) quadratic time."
                },
                {
                    "id": "step3",
                    "title": "Analyze Block 3",
                    "instruction": "Determine the time complexity of the third block (a loop running 10 times).",
                    "type": "multipleChoice",
                    "prompt": "What is the Big O of Block 3?",
                    "choices": [
                        {"id": "a", "text": "O(1)"},
                        {"id": "b", "text": "O(N)"},
                        {"id": "c", "text": "O(10)"}
                    ],
                    "answer": {"choiceId": "a"},
                    "explanation": "Although it loops 10 times, the number 10 is a constant that does not change as N grows. In Big O, any constant time operation is simply O(1)."
                },
                {
                    "id": "step4",
                    "title": "Combine and Simplify",
                    "instruction": "Now combine the complexities of all three sequential blocks and simplify.",
                    "type": "freeResponse",
                    "prompt": "The total runtime is `O(N) + O(N^2) + O(1)`. What does this simplify to? (Provide just the simplified Big O notation, like 'O(1)')",
                    "answer": {
                        "gradingMode": "selfCheck",
                        "expected": "O(N^2)",
                        "keyPoints": ["O(N^2)"]
                    },
                    "explanation": "When blocks of code execute sequentially, their time complexities are added: `O(N) + O(N^2) + O(1)`. Following the rules of Big O, we drop lower-order terms and constants. `N^2` dominates `N` and `1`, so the overall complexity simplifies to `O(N^2)`."
                }
            ]
        }
    ]
}


save("dsa-hashmap-concept-lesson.yaml", hashmap_lesson)
save("dsa-big-o-concept-lesson.yaml", big_o_lesson)
save("dsa-big-o-function-worked-example.yaml", big_o_worked_example)

print("Generated 3 DSA assessments.")
