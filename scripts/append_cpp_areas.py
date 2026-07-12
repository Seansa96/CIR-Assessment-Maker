import yaml

AREAS_FILE = 'data/areas.yaml'

NEW_AREAS = [
    {
        "id": "cpp-basics",
        "title": "C++ Basics",
        "description": "Introduction to C++, variables, and basic input/output.",
        "subcategories": [
            {
                "id": "cpp-hello-world",
                "title": "Hello, World!",
                "description": "Compiling, running, and writing to the screen."
            },
            {
                "id": "cpp-variables-input",
                "title": "Variables and Keyboard Input",
                "description": "Declaring variables, character input, and detecting input problems."
            }
        ]
    },
    {
        "id": "cpp-control-flow-containers",
        "title": "Control Flow and Basic Containers",
        "description": "Loops, arrays, vectors, and handling exceptions.",
        "subcategories": [
            {
                "id": "cpp-exceptions",
                "title": "Exceptions and Expectations",
                "description": "Throwing and handling exceptions with try/catch blocks."
            },
            {
                "id": "cpp-loops-arrays-vectors",
                "title": "Loops, Arrays, and Vectors",
                "description": "Sequential containers, while loops, and initializer lists."
            }
        ]
    },
    {
        "id": "cpp-algorithms-lambdas",
        "title": "Algorithms and Lambdas",
        "description": "Standard library algorithms, lambdas, and the Ranges library.",
        "subcategories": [
            {
                "id": "cpp-std-algorithms",
                "title": "Using Standard Library Algorithms",
                "description": "Analyzing numbers using predicates and iterators."
            },
            {
                "id": "cpp-lambdas-ranges",
                "title": "Lambdas and the Ranges Library",
                "description": "Using lambdas, std::function, and the Ranges view."
            }
        ]
    },
    {
        "id": "cpp-files-strings",
        "title": "Files, Strings, and Formatting",
        "description": "Working with the filesystem, standard strings, and formatting.",
        "subcategories": [
            {
                "id": "cpp-random-numbers",
                "title": "Random Numbers",
                "description": "Generating random numbers and normal distributions."
            },
            {
                "id": "cpp-working-with-files",
                "title": "Working with Files",
                "description": "File modes, bitwise operators, and the Filesystem Library."
            },
            {
                "id": "cpp-strings-formatting",
                "title": "Strings and Formatting",
                "description": "C-style string literals, std::string, and std::format."
            }
        ]
    },
    {
        "id": "cpp-classes-memory",
        "title": "Classes and Memory Management",
        "description": "Object-oriented programming and smart pointers.",
        "subcategories": [
            {
                "id": "cpp-classes-basics",
                "title": "Classes: Member Variables and Functions",
                "description": "Simple classes, access specifiers, constructors, and destructors."
            },
            {
                "id": "cpp-move-semantics",
                "title": "Classes: Special Member Functions and Move Semantics",
                "description": "Copying and moving objects, move constructors, and assignments."
            },
            {
                "id": "cpp-unique-ptr",
                "title": "Memory Management with std::unique_ptr",
                "description": "Smart pointers, custom deleters, and memory safety."
            },
            {
                "id": "cpp-virtual-functions-inheritance",
                "title": "Classes: Virtual Functions and Inheritance",
                "description": "Abstract base classes, derived classes, and virtual destructors."
            }
        ]
    },
    {
        "id": "cpp-advanced-stl",
        "title": "Advanced C++ and STL",
        "description": "Templates, variant, unordered_map, and advanced STL features.",
        "subcategories": [
            {
                "id": "cpp-variant-visit",
                "title": "Using std::variant and std::visit",
                "description": "Type-safe unions and handling potential problems with variants."
            },
            {
                "id": "cpp-templates-unordered-map",
                "title": "Templates and std::unordered_map",
                "description": "Writing templates, specializing std::hash, and associative containers."
            },
            {
                "id": "cpp-stl-numerics",
                "title": "STL Numerics and Math",
                "description": "Standard numerical limits, complex numbers, and math functions."
            },
            {
                "id": "cpp-stl-containers",
                "title": "STL Containers",
                "description": "Sequence containers, associative containers, and container adaptors."
            },
            {
                "id": "cpp-stl-iterators",
                "title": "STL Iterators",
                "description": "Iterator categories, adaptors, and operations."
            },
            {
                "id": "cpp-stl-utilities",
                "title": "STL Utilities",
                "description": "Pairs, tuples, type traits, and functional utilities."
            },
            {
                "id": "cpp-stl-concurrency",
                "title": "STL Concurrency",
                "description": "Threads, mutexes, condition variables, and futures."
            }
        ]
    }
]

def main():
    try:
        with open(AREAS_FILE, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        data = {"areas": []}

    existing_ids = {area['id'] for area in data.get('areas', [])}

    added = 0
    for new_area in NEW_AREAS:
        if new_area['id'] not in existing_ids:
            data.setdefault('areas', []).append(new_area)
            added += 1

    with open(AREAS_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)
    
    print(f"Added {added} C++ areas to {AREAS_FILE}")

if __name__ == '__main__':
    main()
