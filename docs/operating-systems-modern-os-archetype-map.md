# Operating Systems Curriculum Archetype Map

Source reference: user-provided Andrew S. Tanenbaum, *Modern Operating Systems* PDF.

Use rule: use this map for concept coverage, misconceptions, and difficulty targets only. Do not copy textbook wording, exercises, diagrams, or explanations verbatim.

## Areas
- `os-foundations-and-interfaces`: Operating-system roles, hardware context, system calls, APIs, kernel boundaries, and structural design.

- `os-processes-concurrency`: Processes, threads, IPC, synchronization, scheduling, and deadlock reasoning.

- `os-memory-storage-io`: Address spaces, memory allocation, virtual memory, file systems, and device I/O.

- `os-virtualization-parallel-security`: Virtual machines, cloud abstractions, multiprocessor systems, and security mechanisms.

- `os-case-studies-and-design`: UNIX/Linux/Android, Windows, and operating-system design tradeoffs.

## Topic Map
### Introduction and System Calls (`os-introduction-system-calls`)
- Source chapter focus: 1 Introduction
- Assessments: `os-introduction-system-calls-concept-lesson`, `os-introduction-system-calls-glossary`, `os-introduction-system-calls-recall`, `os-introduction-system-calls-quiz`, `os-introduction-system-calls-test`
- Core concepts:
  - Operating system roles: An operating system presents useful abstractions while allocating shared hardware resources fairly and safely. Misconception to test: Treating the OS as only a user interface misses its resource-management role.
  - Kernel and user mode: Privileged operations run in kernel mode so ordinary programs cannot directly damage devices, memory, or other processes. Misconception to test: If user code could execute privileged instructions directly, protection would collapse.
  - System call boundary: A system call is the controlled transition where user code asks the kernel to perform protected work. Misconception to test: A library API may wrap a system call, but the two are not identical.
  - Hardware context: CPUs, memory, disks, buses, and interrupts shape what the OS can abstract and what it must protect. Misconception to test: Ignoring hardware leads to wrong mental models for performance and protection.
  - Process, address space, file: Processes, address spaces, and files are foundational abstractions used to organize execution, memory, and persistent data. Misconception to test: These are not just names; they define protection and sharing boundaries.
  - OS families: Different OS types prioritize different constraints, such as throughput, responsiveness, real-time deadlines, embedded size, or server reliability. Misconception to test: A design that works for a desktop may fail for a real-time controller.
- Core terms: kernel, system call, user mode, kernel mode, process, address space, shell, resource manager

### Operating System Structure and Design (`os-structure-design`)
- Source chapter focus: 1.7 and 12 OS Structure and Design
- Assessments: `os-structure-design-concept-lesson`, `os-structure-design-glossary`, `os-structure-design-recall`, `os-structure-design-quiz`, `os-structure-design-test`
- Core concepts:
  - Monolithic kernel: A monolithic kernel keeps many OS services in one privileged address space for fast internal calls. Misconception to test: Monolithic does not mean unorganized; it means services share privileged space.
  - Layered design: Layering limits which components may depend on which other components, making reasoning easier at the cost of flexibility. Misconception to test: A layer violation can make the design harder to maintain.
  - Microkernel: A microkernel keeps only minimal mechanisms in the kernel and moves many services to user space. Misconception to test: Microkernels trade direct-call speed for isolation and modularity.
  - Client-server model: OS services can be represented as servers that respond to client requests through message passing. Misconception to test: The model is about structure, not necessarily network distribution.
  - Virtual machines: A virtual machine presents a hardware-like interface so multiple isolated systems can share one physical host. Misconception to test: A VM is not just an application window; it virtualizes a machine boundary.
  - Mechanism versus policy: Mechanism provides what can be done; policy decides which choice should be made. Misconception to test: Mixing policy into mechanism makes later change harder.
- Core terms: monolithic kernel, microkernel, layered system, client-server model, virtual machine, exokernel, mechanism, policy

### Processes and Threads (`os-processes-threads`)
- Source chapter focus: 2 Processes and Threads
- Assessments: `os-processes-threads-concept-lesson`, `os-processes-threads-glossary`, `os-processes-threads-recall`, `os-processes-threads-quiz`, `os-processes-threads-test`
- Core concepts:
  - Process model: A process is an executing program with registers, memory context, open resources, and scheduling state. Misconception to test: The program file and the running process are different objects.
  - Process states: Processes move among running, ready, and blocked states depending on CPU availability and waiting conditions. Misconception to test: Blocked means waiting for an event, not merely waiting for CPU time.
  - Process creation: Operating systems create new execution contexts through controlled mechanisms that assign identifiers and resources. Misconception to test: Creation is not just loading bytes; it establishes management state.
  - Thread model: Threads share a process address space but have their own program counters, stacks, and scheduling state. Misconception to test: Threads share memory, so they reduce isolation while enabling cheaper concurrency.
  - User versus kernel threads: User-level threads can be fast to manage, while kernel-level threads give the OS direct scheduling awareness. Misconception to test: Neither implementation is universally best.
  - Thread safety: Single-threaded assumptions often fail when shared data can be accessed concurrently. Misconception to test: Adding threads without redesigning shared state creates subtle bugs.
- Core terms: process, thread, ready state, blocked state, process table, context switch, user-level thread, kernel-level thread

### IPC and Synchronization (`os-ipc-synchronization`)
- Source chapter focus: 2.3 Interprocess Communication
- Assessments: `os-ipc-synchronization-concept-lesson`, `os-ipc-synchronization-glossary`, `os-ipc-synchronization-recall`, `os-ipc-synchronization-quiz`, `os-ipc-synchronization-test`
- Core concepts:
  - Race condition: A race condition occurs when correctness depends on the timing of unsynchronized concurrent actions. Misconception to test: Races are not solved by hoping one thread is usually faster.
  - Critical region: A critical region is code that touches shared state and must not be executed concurrently by conflicting actors. Misconception to test: Only protecting some accesses still leaves a race.
  - Mutual exclusion: Mutual exclusion ensures only one actor enters a critical region at a time. Misconception to test: Mutual exclusion is a tool, not a full correctness proof.
  - Semaphore: A semaphore coordinates access through an integer count changed by atomic operations. Misconception to test: A semaphore is not the same as a mutex, though it can sometimes act like one.
  - Monitor: A monitor packages shared data with procedures and condition synchronization. Misconception to test: Condition variables require careful waiting and signaling discipline.
  - Message passing: Message passing coordinates processes by sending data instead of sharing memory directly. Misconception to test: Message passing can still block and still requires protocol design.
- Core terms: race condition, critical region, mutex, semaphore, monitor, barrier, message passing, busy waiting

### Scheduling (`os-scheduling`)
- Source chapter focus: 2.4 Scheduling
- Assessments: `os-scheduling-concept-lesson`, `os-scheduling-glossary`, `os-scheduling-recall`, `os-scheduling-quiz`, `os-scheduling-test`
- Core concepts:
  - Scheduler goal: A scheduler chooses which runnable work gets CPU time according to goals such as throughput, response time, fairness, or deadlines. Misconception to test: There is no single best schedule without knowing the workload goal.
  - Batch scheduling: Batch systems emphasize throughput and turnaround, often tolerating less interactivity. Misconception to test: Optimizing throughput can conflict with short response times.
  - Interactive scheduling: Interactive systems prioritize responsiveness so users perceive progress quickly. Misconception to test: Responsiveness may require preemption.
  - Real-time scheduling: Real-time scheduling focuses on meeting timing constraints rather than average speed. Misconception to test: A real-time system is about deadlines, not merely being fast.
  - Policy versus mechanism: Scheduling mechanisms enable switching; policies decide who runs next. Misconception to test: Changing policy should not require rewriting all low-level switching machinery.
  - Thread scheduling: Thread scheduling depends on whether threads are visible to the kernel and how user runtimes cooperate. Misconception to test: User-level thread scheduling can conflict with kernel-level CPU allocation.
- Core terms: scheduler, preemption, turnaround time, response time, throughput, fairness, real-time deadline, quantum

### Memory Management (`os-memory-management`)
- Source chapter focus: 3 Memory Management
- Assessments: `os-memory-management-concept-lesson`, `os-memory-management-glossary`, `os-memory-management-recall`, `os-memory-management-quiz`, `os-memory-management-test`
- Core concepts:
  - No abstraction problem: Without memory abstraction, programs can interfere with each other and must know physical placement details. Misconception to test: Raw physical memory is not a safe multiprogramming interface.
  - Address space: An address space gives a process a private memory view independent of physical memory layout. Misconception to test: Virtual-looking addresses need translation and protection.
  - Swapping: Swapping moves process memory between main memory and backing storage to manage limited RAM. Misconception to test: Swapping is coarse compared with demand paging.
  - Free memory management: The OS tracks free and allocated memory using structures such as bitmaps or free lists. Misconception to test: Fragmentation can make free memory hard to use even when total free space seems large.
  - Relocation and protection: Relocation lets programs run at different memory locations, while protection prevents illegal access. Misconception to test: Relocation without protection is not enough for safe sharing.
  - Segmentation idea: Segmentation divides memory by logical units such as code, stack, and data. Misconception to test: Segments are logical regions, not fixed-size pages.
- Core terms: physical address, address space, relocation, protection, swapping, free list, fragmentation, segment

### Virtual Memory (`os-virtual-memory`)
- Source chapter focus: 3.3-3.7 Virtual Memory
- Assessments: `os-virtual-memory-concept-lesson`, `os-virtual-memory-glossary`, `os-virtual-memory-recall`, `os-virtual-memory-quiz`, `os-virtual-memory-test`
- Core concepts:
  - Paging: Paging divides virtual and physical memory into fixed-size units so pages can be mapped independently. Misconception to test: Pages are fixed-size chunks; segments are logical variable-size regions.
  - Page table: A page table records how virtual pages map to physical frames and with what permissions. Misconception to test: A page table entry is not the page data itself.
  - TLB: A TLB caches recent address translations to avoid frequent page-table walks. Misconception to test: A TLB miss is not necessarily a page fault.
  - Page fault: A page fault occurs when a needed virtual page is not currently accessible as required. Misconception to test: The OS must determine whether the access is valid before loading data.
  - Replacement algorithm: When memory is full, a replacement policy chooses which page to evict. Misconception to test: Optimal replacement is a benchmark, not implementable without future knowledge.
  - Working set: The working set approximates the pages a process actively needs in a recent time window. Misconception to test: If working sets do not fit in memory, thrashing can occur.
- Core terms: page, frame, page table, TLB, page fault, LRU, working set, thrashing

### File Systems (`os-file-systems`)
- Source chapter focus: 4 File Systems
- Assessments: `os-file-systems-concept-lesson`, `os-file-systems-glossary`, `os-file-systems-recall`, `os-file-systems-quiz`, `os-file-systems-test`
- Core concepts:
  - File abstraction: A file abstracts persistent data behind names, attributes, operations, and access rules. Misconception to test: A file is not only bytes; metadata and operations matter.
  - Directory hierarchy: Directories organize file names into a navigable namespace. Misconception to test: Path names describe traversal through the namespace, not physical disk layout directly.
  - File allocation: File systems must map logical file blocks onto disk blocks. Misconception to test: Contiguous, linked, and indexed allocation have different tradeoffs.
  - Directory implementation: Directories are data structures mapping names to file metadata references. Misconception to test: A directory entry is not necessarily the entire file metadata.
  - Journaling: A journal records intended metadata operations to support recovery after crashes. Misconception to test: Journaling improves consistency, not necessarily every performance metric.
  - Virtual file system: A VFS layer lets different file-system implementations present a common interface. Misconception to test: The VFS is an abstraction layer, not a particular disk format.
- Core terms: file, directory, path name, inode, journaling, VFS, block, free-space map

### Input and Output (`os-input-output`)
- Source chapter focus: 5 Input/Output
- Assessments: `os-input-output-concept-lesson`, `os-input-output-glossary`, `os-input-output-recall`, `os-input-output-quiz`, `os-input-output-test`
- Core concepts:
  - I/O stack: I/O moves through applications, system calls, device-independent OS layers, drivers, controllers, and devices. Misconception to test: A read call does not talk to hardware directly from user mode.
  - Interrupts: Interrupts let devices notify the CPU that attention is needed. Misconception to test: Interrupt-driven I/O avoids constant polling but introduces asynchronous control flow.
  - DMA: Direct memory access lets a device controller transfer data to or from memory with less CPU copying. Misconception to test: DMA still needs OS setup and protection.
  - Device drivers: Drivers translate general OS requests into device-specific commands. Misconception to test: A driver bug can compromise kernel reliability.
  - Device-independent I/O: The OS hides many device differences behind common naming, buffering, error handling, and protection rules. Misconception to test: Uniform interfaces do not erase hardware-specific behavior.
  - Disk performance: Seek time, rotational delay, transfer time, caching, and scheduling influence storage performance. Misconception to test: Disk speed is not explained by transfer rate alone.
- Core terms: interrupt, polling, DMA, device driver, controller, buffering, spooling, seek time

### Deadlocks (`os-deadlocks`)
- Source chapter focus: 6 Deadlocks
- Assessments: `os-deadlocks-concept-lesson`, `os-deadlocks-glossary`, `os-deadlocks-recall`, `os-deadlocks-quiz`, `os-deadlocks-test`
- Core concepts:
  - Deadlock condition: Deadlock occurs when a set of processes cannot proceed because each waits for resources held by others. Misconception to test: Deadlock is not just slowness or contention.
  - Coffman conditions: Mutual exclusion, hold-and-wait, no preemption, and circular wait must all hold for deadlock. Misconception to test: Breaking any one condition can prevent deadlock.
  - Resource allocation graph: A resource graph visualizes processes, resources, holdings, and requests. Misconception to test: A cycle is suspicious, but interpretation depends on resource instance counts.
  - Deadlock detection: Detection allows deadlock to happen, then identifies it for recovery. Misconception to test: Detection requires a recovery policy.
  - Deadlock prevention: Prevention structurally denies at least one necessary condition. Misconception to test: Prevention can reduce resource utilization or flexibility.
  - Deadlock avoidance: Avoidance uses runtime knowledge to stay in safe states. Misconception to test: Avoidance needs information that may not be available.
- Core terms: deadlock, mutual exclusion, hold and wait, no preemption, circular wait, safe state, deadlock detection, deadlock avoidance

### Virtualization and the Cloud (`os-virtualization-cloud`)
- Source chapter focus: 7 Virtualization and the Cloud
- Assessments: `os-virtualization-cloud-concept-lesson`, `os-virtualization-cloud-glossary`, `os-virtualization-cloud-recall`, `os-virtualization-cloud-quiz`, `os-virtualization-cloud-test`
- Core concepts:
  - Virtualization goal: Virtualization lets multiple isolated environments share physical hardware while appearing to have their own machine. Misconception to test: Virtualization is about isolation and abstraction, not only convenience.
  - Hypervisor: A hypervisor manages virtual machines and mediates access to CPU, memory, and I/O. Misconception to test: A hypervisor sits below guest OSes, not inside each ordinary application.
  - Trap and emulate: Privileged guest operations may be trapped and emulated or otherwise handled safely by the virtualization layer. Misconception to test: Not every instruction can be handled identically on all hardware.
  - Containers versus VMs: Containers share a kernel while virtual machines generally run separate guest OS kernels. Misconception to test: Containers are lighter but have a different isolation boundary.
  - Cloud abstraction: Cloud platforms package compute, storage, and networking as provisioned resources with elastic management. Misconception to test: Cloud is not magic hardware; it is managed virtualization plus operational tooling.
  - Isolation tradeoff: Stronger isolation often costs overhead, while lighter isolation may require more trust in the shared kernel. Misconception to test: Performance and isolation must be reasoned together.
- Core terms: virtual machine, hypervisor, guest OS, host OS, container, elasticity, snapshot, isolation boundary

### Multiple Processor Systems (`os-multiprocessor-systems`)
- Source chapter focus: 8 Multiple Processor Systems
- Assessments: `os-multiprocessor-systems-concept-lesson`, `os-multiprocessor-systems-glossary`, `os-multiprocessor-systems-recall`, `os-multiprocessor-systems-quiz`, `os-multiprocessor-systems-test`
- Core concepts:
  - Parallel hardware: Multiprocessor systems run work on more than one CPU or core, creating opportunities and coordination costs. Misconception to test: More processors do not automatically mean proportional speedup.
  - Shared memory: Shared-memory multiprocessors let processors access a common address space. Misconception to test: Shared memory increases communication ease but makes synchronization essential.
  - Cache coherence: Cache coherence keeps processors from seeing incompatible cached values for shared memory. Misconception to test: Coherence is not the same as correct locking.
  - Multiprocessor scheduling: The scheduler must consider processor affinity, load balancing, and cache effects. Misconception to test: Moving a task can balance load but disrupt cache locality.
  - Scalability: A design scales when added processors continue to improve useful throughput. Misconception to test: Global locks can destroy scalability.
  - Distributed systems contrast: Distributed systems communicate across machines and often lack shared memory. Misconception to test: Network delay and partial failure change the design problem.
- Core terms: multiprocessor, SMP, processor affinity, load balancing, cache coherence, scalability, spin lock, distributed system

### Operating System Security (`os-security`)
- Source chapter focus: 9 Security
- Assessments: `os-security-concept-lesson`, `os-security-glossary`, `os-security-recall`, `os-security-quiz`, `os-security-test`
- Core concepts:
  - Security goals: Confidentiality, integrity, and availability describe what the system must protect. Misconception to test: Security is not only secrecy.
  - Authentication: Authentication establishes who or what is making a request. Misconception to test: Authentication does not by itself decide what is allowed.
  - Authorization: Authorization decides whether an authenticated subject may perform an action on an object. Misconception to test: Authorization without good identity is weak.
  - Access control: Access control lists and capabilities represent permissions from different directions. Misconception to test: ACLs attach permissions to objects; capabilities attach authority to subjects or tokens.
  - Least privilege: A component should receive only the authority needed to do its job. Misconception to test: Running everything as administrator expands damage from mistakes and attacks.
  - Malware and exploits: Malware exploits weaknesses in code, configuration, or users to gain unauthorized effects. Misconception to test: Security design must assume failures and limit blast radius.
- Core terms: confidentiality, integrity, availability, authentication, authorization, ACL, capability, least privilege

### UNIX, Linux, and Android (`os-unix-linux-android`)
- Source chapter focus: 10 UNIX, Linux, and Android
- Assessments: `os-unix-linux-android-concept-lesson`, `os-unix-linux-android-glossary`, `os-unix-linux-android-recall`, `os-unix-linux-android-quiz`, `os-unix-linux-android-test`
- Core concepts:
  - UNIX design idea: UNIX emphasizes files, processes, permissions, and composable tools as system-wide organizing ideas. Misconception to test: The design style matters more than memorizing one command.
  - Everything as file-like: Many UNIX interfaces expose devices and resources through file-like operations. Misconception to test: File-like does not mean every object is stored as ordinary disk data.
  - Fork and exec: UNIX process creation separates copying a process context from replacing its program image. Misconception to test: Fork and exec are distinct steps with different purposes.
  - Permissions: UNIX permissions model access by owner, group, and others with read, write, and execute bits. Misconception to test: Execute on a directory means traversal, not running the directory.
  - Linux kernel: Linux combines UNIX-style abstractions with a large monolithic kernel and loadable modules. Misconception to test: Linux is not the same thing as an entire distribution.
  - Android adaptation: Android builds mobile-focused services and app isolation on top of a Linux kernel base. Misconception to test: Android app sandboxing adds layers beyond ordinary desktop UNIX assumptions.
- Core terms: fork, exec, pipe, inode, permission bits, shell, Linux distribution, Android sandbox

### Windows Case Study (`os-windows-case-study`)
- Source chapter focus: 11 Windows 8 Case Study
- Assessments: `os-windows-case-study-concept-lesson`, `os-windows-case-study-glossary`, `os-windows-case-study-recall`, `os-windows-case-study-quiz`, `os-windows-case-study-test`
- Core concepts:
  - Windows design lens: Windows emphasizes object-based kernel structures, compatibility, security descriptors, and broad device/application support. Misconception to test: A case study is best read for design tradeoffs, not just product trivia.
  - Objects and handles: Windows exposes many kernel-managed resources through object handles. Misconception to test: A handle is a reference with mediated access, not the object itself.
  - Registry: The registry stores structured configuration used by the OS and applications. Misconception to test: The registry is not equivalent to a file system, even though it stores persistent data.
  - Security descriptors: Windows access control uses security descriptors and access tokens to mediate object access. Misconception to test: Permissions depend on token identity and object policy together.
  - Subsystem compatibility: Compatibility layers and subsystems help support different APIs and historical expectations. Misconception to test: Compatibility can constrain design choices.
  - I/O model: The Windows I/O manager and drivers coordinate device requests through layered components. Misconception to test: Application I/O requests pass through OS mediation and driver layers.
- Core terms: handle, object manager, registry, access token, security descriptor, I/O manager, driver stack, compatibility layer

### Operating System Design (`os-operating-system-design`)
- Source chapter focus: 12 Operating System Design
- Assessments: `os-operating-system-design-concept-lesson`, `os-operating-system-design-glossary`, `os-operating-system-design-recall`, `os-operating-system-design-quiz`, `os-operating-system-design-test`
- Core concepts:
  - Design requirements: An OS design starts from goals such as reliability, performance, portability, security, maintainability, and compatibility. Misconception to test: Optimizing one goal often stresses another.
  - Abstraction choice: Good OS abstractions hide accidental hardware complexity while exposing enough control for useful programs. Misconception to test: Hiding too much can block performance or flexibility.
  - Modularity: Modular boundaries make systems easier to reason about, test, and replace. Misconception to test: A boundary that is too chatty can hurt performance.
  - Reliability: Reliability improves when faults are isolated, interfaces are narrow, and recovery paths are designed intentionally. Misconception to test: Reliability is not added only by testing at the end.
  - Performance tradeoffs: Caching, batching, zero-copy paths, and fast common cases improve performance but complicate correctness. Misconception to test: A faster mechanism that breaks isolation is not a good OS tradeoff.
  - Evolution: Operating systems must evolve while preserving compatibility with programs, users, and hardware ecosystems. Misconception to test: Compatibility can dominate otherwise clean design decisions.
- Core terms: abstraction, portability, compatibility, modularity, reliability, maintainability, fast path, tradeoff

## Generated Assessment IDs

- `os-introduction-system-calls-concept-lesson`
- `os-introduction-system-calls-glossary`
- `os-introduction-system-calls-recall`
- `os-introduction-system-calls-quiz`
- `os-introduction-system-calls-test`
- `os-structure-design-concept-lesson`
- `os-structure-design-glossary`
- `os-structure-design-recall`
- `os-structure-design-quiz`
- `os-structure-design-test`
- `os-processes-threads-concept-lesson`
- `os-processes-threads-glossary`
- `os-processes-threads-recall`
- `os-processes-threads-quiz`
- `os-processes-threads-test`
- `os-ipc-synchronization-concept-lesson`
- `os-ipc-synchronization-glossary`
- `os-ipc-synchronization-recall`
- `os-ipc-synchronization-quiz`
- `os-ipc-synchronization-test`
- `os-scheduling-concept-lesson`
- `os-scheduling-glossary`
- `os-scheduling-recall`
- `os-scheduling-quiz`
- `os-scheduling-test`
- `os-memory-management-concept-lesson`
- `os-memory-management-glossary`
- `os-memory-management-recall`
- `os-memory-management-quiz`
- `os-memory-management-test`
- `os-virtual-memory-concept-lesson`
- `os-virtual-memory-glossary`
- `os-virtual-memory-recall`
- `os-virtual-memory-quiz`
- `os-virtual-memory-test`
- `os-file-systems-concept-lesson`
- `os-file-systems-glossary`
- `os-file-systems-recall`
- `os-file-systems-quiz`
- `os-file-systems-test`
- `os-input-output-concept-lesson`
- `os-input-output-glossary`
- `os-input-output-recall`
- `os-input-output-quiz`
- `os-input-output-test`
- `os-deadlocks-concept-lesson`
- `os-deadlocks-glossary`
- `os-deadlocks-recall`
- `os-deadlocks-quiz`
- `os-deadlocks-test`
- `os-virtualization-cloud-concept-lesson`
- `os-virtualization-cloud-glossary`
- `os-virtualization-cloud-recall`
- `os-virtualization-cloud-quiz`
- `os-virtualization-cloud-test`
- `os-multiprocessor-systems-concept-lesson`
- `os-multiprocessor-systems-glossary`
- `os-multiprocessor-systems-recall`
- `os-multiprocessor-systems-quiz`
- `os-multiprocessor-systems-test`
- `os-security-concept-lesson`
- `os-security-glossary`
- `os-security-recall`
- `os-security-quiz`
- `os-security-test`
- `os-unix-linux-android-concept-lesson`
- `os-unix-linux-android-glossary`
- `os-unix-linux-android-recall`
- `os-unix-linux-android-quiz`
- `os-unix-linux-android-test`
- `os-windows-case-study-concept-lesson`
- `os-windows-case-study-glossary`
- `os-windows-case-study-recall`
- `os-windows-case-study-quiz`
- `os-windows-case-study-test`
- `os-operating-system-design-concept-lesson`
- `os-operating-system-design-glossary`
- `os-operating-system-design-recall`
- `os-operating-system-design-quiz`
- `os-operating-system-design-test`
- `operating-systems-cumulative-review-test`
