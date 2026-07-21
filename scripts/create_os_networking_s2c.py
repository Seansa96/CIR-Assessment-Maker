import yaml
import os
from pathlib import Path

ROOT = Path(r"C:\Users\SeanS\Downloads\cir_app")
MANIFESTS = ROOT / "docs" / "assessment-reference" / "content-manifests"
BLUEPRINTS = ROOT / "docs" / "assessment-reference" / "question-blueprints"
ASSESSMENTS = ROOT / "data" / "assessments"

def dump(path, data):
    path.write_text(yaml.safe_dump(data, sort_keys=False, indent=2), encoding="utf-8")

# 1. Create Manifest
manifest = {
    "schemaVersion": 1,
    "id": "os-distributed-systems-networking-manifest",
    "categoryId": "operating-systems",
    "topicId": "os-distributed-systems-networking",
    "objectiveId": "os-obj-distributed-networking",
    "sourceId": "src-20260721024701-fa0a84f6c8",
    "reviewState": "approved",
    "artifacts": [
        {
            "assessmentId": "os-distributed-systems-networking-concept-lesson",
            "objectiveIds": ["os-obj-distributed-networking"],
            "sourceChunkIds": [],
            "requiresVisual": True
        }
    ]
}
dump(MANIFESTS / "os-distributed-systems-networking.yaml", manifest)

# 2. Create Blueprints
blueprints = [
    {
        "id": "os-networking-rpc-flow",
        "objectiveId": "os-obj-distributed-networking",
        "archetype": "rpc-flow",
        "questionType": "multipleChoice",
        "givens": ["An RPC architecture diagram or scenario"],
        "unknown": "The purpose of the client/server stub",
        "requiresDiagram": True,
        "governingPrinciple": "Stubs marshal and unmarshal parameters to abstract network communication.",
        "methodSteps": [
            "Identify the local procedure call.",
            "Identify the stub that marshals data.",
            "Understand that the network transmits packets."
        ],
        "likelyMisconception": "Thinking the network directly calls the function.",
        "difficultyEvidence": "Requires understanding layers of abstraction.",
        "answerVerificationMethod": "text-reference",
        "variationAxes": ["Client vs Server stub focus", "Failure modes"],
        "reasoningSignature": "Abstracting communication via local proxies."
    },
    {
        "id": "os-networking-middleware-layers",
        "objectiveId": "os-obj-distributed-networking",
        "archetype": "middleware-layers",
        "questionType": "multipleChoice",
        "givens": ["Heterogeneous OS environments"],
        "unknown": "The role of middleware",
        "requiresDiagram": True,
        "governingPrinciple": "Middleware sits logically between applications and the OS to provide a uniform abstraction.",
        "methodSteps": [
            "Observe different underlying operating systems.",
            "Note the application layer needs a unified view.",
            "Identify middleware as the bridging software."
        ],
        "likelyMisconception": "Confusing middleware with the OS kernel.",
        "difficultyEvidence": "Conceptualizing logical layers.",
        "answerVerificationMethod": "text-reference",
        "variationAxes": ["Document-based vs Object-based", "OS heterogeneity"],
        "reasoningSignature": "Providing unified interfaces over distributed, heterogeneous hardware."
    }
]
dump(BLUEPRINTS / "os-networking-blueprints.yaml", blueprints)

# 3. Create Concept Lesson
lesson = {
    "schemaVersion": 1,
    "id": "os-distributed-systems-networking-concept-lesson",
    "title": "Distributed Systems and Networking",
    "assessmentType": "conceptLesson",
    "categoryId": "operating-systems",
    "topicId": "os-distributed-systems-networking",
    "modeDefault": "practice",
    "randomizeQuestions": False,
    "navigation": {
        "learningGoal": "learn",
        "activityType": "conceptLesson",
        "tags": ["operating-systems", "networking", "distributed-systems", "rpc", "middleware"]
    },
    "skills": ["os-networking"],
    "lesson": {
        "introduction": "This lesson introduces the fundamentals of distributed systems and networking from an Operating Systems perspective. We will explore how independent systems communicate and how the OS abstracts these boundaries.",
        "sections": [
            {
                "id": "rpc-flow",
                "title": "Remote Procedure Calls (RPC)",
                "required": True,
                "content": "RPC is a powerful abstraction that allows programs to call functions located on other machines as if they were local. The complexity of packing (marshaling) the parameters into a network message is handled by the **stub**.",
                "media": [
                    {
                        "type": "image",
                        "src": "/media/os/rpc-flow.svg",
                        "alt": "Flowchart showing Client, Client Stub, Network, Server Stub, and Server.",
                        "caption": "Information transfer flow in a Remote Procedure Call."
                    }
                ],
                "check": {
                    "id": "rpc-check",
                    "type": "multipleChoice",
                    "prompt": "Based on the RPC flow diagram, what is the primary role of the Client Stub?",
                    "choices": [
                        {"id": "a", "text": "To execute the server function locally."},
                        {"id": "b", "text": "To pack (marshal) the parameters into a message and send it over the network."},
                        {"id": "c", "text": "To manage the OS kernel's memory allocation."},
                        {"id": "d", "text": "To act as the physical network router."}
                    ],
                    "answer": {"choiceId": "b"},
                    "explanation": "The Client Stub intercepts the local call, marshals the arguments, and handles the network transmission to the Server Stub."
                }
            },
            {
                "id": "middleware",
                "title": "Middleware Abstractions",
                "required": True,
                "content": "In a distributed system, different nodes might run different operating systems (e.g., Linux vs Windows). **Middleware** is a software layer that sits above the OS but below the application, providing a common set of services and protocols so applications don't need to worry about OS differences.",
                "media": [
                    {
                        "type": "image",
                        "src": "/media/os/middleware-layers.svg",
                        "alt": "Diagram showing Application layer, Middleware layer, and multiple differing OS layers below.",
                        "caption": "Middleware unifying heterogeneous operating systems."
                    }
                ],
                "check": {
                    "id": "middleware-check",
                    "type": "multipleChoice",
                    "prompt": "Why is a middleware layer necessary in a distributed system?",
                    "choices": [
                        {"id": "a", "text": "To replace the OS kernels on all machines."},
                        {"id": "b", "text": "To provide a unified abstraction layer over different, heterogeneous operating systems."},
                        {"id": "c", "text": "To act as a physical network switch."},
                        {"id": "d", "text": "To enforce single-threaded execution."}
                    ],
                    "answer": {"choiceId": "b"},
                    "explanation": "Middleware hides the heterogeneity of the underlying platforms, making them appear as a single unified system to the application."
                }
            }
        ]
    }
}
dump(ASSESSMENTS / "os-distributed-systems-networking-concept-lesson.yaml", lesson)

# 4. Create Quiz
quiz = {
    "schemaVersion": 1,
    "id": "os-distributed-systems-networking-quiz",
    "title": "Distributed Systems Quiz",
    "assessmentType": "quiz",
    "categoryId": "operating-systems",
    "topicId": "os-distributed-systems-networking",
    "modeDefault": "practice",
    "randomizeQuestions": True,
    "navigation": {
        "learningGoal": "practice",
        "activityType": "focusedPractice",
        "tags": ["operating-systems", "networking"]
    },
    "skills": ["os-networking"],
    "questions": [
        {
            "id": "q001",
            "type": "multipleChoice",
            "skills": ["os-networking"],
            "blueprintId": "os-networking-rpc-flow",
            "prompt": "When a server receives a packet from a client in an RPC system, which component is responsible for unpacking (unmarshaling) the parameters?",
            "choices": [
                {"id": "a", "text": "The Network Router"},
                {"id": "b", "text": "The Client Stub"},
                {"id": "c", "text": "The Server Stub"},
                {"id": "d", "text": "The Application Layer"}
            ],
            "answer": {"choiceId": "c"},
            "explanation": "The Server Stub unmarshals the data received from the network and invokes the actual server function."
        },
        {
            "id": "q002",
            "type": "multipleChoice",
            "skills": ["os-networking"],
            "blueprintId": "os-networking-middleware-layers",
            "prompt": "If an application needs to seamlessly access files across Windows and Linux servers, what type of software layer is typically used to abstract the differences?",
            "choices": [
                {"id": "a", "text": "Network Hardware Layer"},
                {"id": "b", "text": "File-System-Based Middleware"},
                {"id": "c", "text": "Kernel Scheduler"},
                {"id": "d", "text": "Microcode"}
            ],
            "answer": {"choiceId": "b"},
            "explanation": "File-System-Based middleware abstracts the underlying OS differences and provides a common filesystem interface."
        }
    ]
}
dump(ASSESSMENTS / "os-distributed-systems-networking-quiz.yaml", quiz)

print("Created S2C files for OS Networking.")
