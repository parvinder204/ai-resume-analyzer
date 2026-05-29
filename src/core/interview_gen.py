from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class QuestionType(str, Enum):
    TECHNICAL     = "Technical"
    BEHAVIOURAL   = "Behavioural"
    SITUATIONAL   = "Situational"
    CULTURE_FIT   = "Culture Fit"
    ROLE_SPECIFIC = "Role-Specific"


@dataclass
class InterviewQuestion:
    question:   str
    type:       QuestionType
    difficulty: str           # "Easy" | "Medium" | "Hard"
    skill_tag:  Optional[str] = None
    tip:        Optional[str] = None


_BEHAVIOURAL: list[dict] = [
    {"q": "Tell me about a time you had to learn a new technology quickly under deadline pressure.",
     "d": "Medium", "tip": "Use STAR method: Situation, Task, Action, Result."},
    {"q": "Describe a challenging project you led. What obstacles did you face and how did you overcome them?",
     "d": "Hard", "tip": "Quantify the outcome — e.g., 'shipped 2 weeks early', 'reduced cost by 30%'."},
    {"q": "Give an example of a time you disagreed with a technical decision. How did you handle it?",
     "d": "Medium", "tip": "Focus on constructive resolution, not conflict."},
    {"q": "Tell me about a time you failed. What did you learn?",
     "d": "Medium", "tip": "Authenticity matters — show growth mindset."},
    {"q": "Describe a situation where you had to work with a difficult teammate.",
     "d": "Medium", "tip": "Emphasise empathy and communication."},
    {"q": "Give an example of a time you proactively improved a process or workflow.",
     "d": "Easy", "tip": "Concrete metrics make this answer shine."},
    {"q": "Tell me about a project where you had to juggle multiple priorities. How did you manage?",
     "d": "Medium", "tip": "Mention tools used (Jira, kanban) and how you communicated progress."},
    {"q": "Describe a time you had to deliver bad news to a stakeholder or manager. How did you approach it?",
     "d": "Medium", "tip": "Show ownership, clarity, and a solution-first mindset."},
    {"q": "Tell me about a situation where you took ownership of a problem that wasn't originally yours.",
     "d": "Medium", "tip": "Emphasise initiative and accountability over blame."},
    {"q": "Describe a time when you had to influence a decision without having direct authority.",
     "d": "Hard", "tip": "Use data and storytelling — persuasion beats position."},
    {"q": "Tell me about a time you had to onboard onto a large, unfamiliar codebase. What was your strategy?",
     "d": "Medium", "tip": "Mention reading docs, tests, pairing with teammates, and tracing key paths."},
    {"q": "Describe a project where the requirements changed significantly mid-way. How did you adapt?",
     "d": "Hard", "tip": "Show flexibility while still managing scope creep."},
    {"q": "Give an example of when you mentored a junior colleague. What was your approach?",
     "d": "Easy", "tip": "Focus on empowering, not just solving for them."},
    {"q": "Tell me about a time you went above and beyond what was asked to deliver a great result.",
     "d": "Easy", "tip": "Be specific — vague answers feel hollow."},
    {"q": "Describe a situation where you had to make a decision with incomplete information.",
     "d": "Hard", "tip": "Show your risk framework: what data you had, what you assumed, and how you validated."},
    {"q": "Tell me about a time you received critical feedback. How did you respond?",
     "d": "Medium", "tip": "Show that you listened, reflected, and acted — not defended."},
    {"q": "Give an example of a time you had to advocate for a user or customer during a technical decision.",
     "d": "Medium", "tip": "Bridges the gap between engineering and empathy."},
    {"q": "Describe a time you had to debug a production issue under severe time pressure.",
     "d": "Hard", "tip": "Walk through your systematic debugging approach: isolate, hypothesise, test."},
    {"q": "Tell me about the most technically complex project you've worked on. What made it hard?",
     "d": "Hard", "tip": "Pick something genuinely complex — show depth, not just buzzwords."},
    {"q": "Describe a time you identified a risk in a project early. What did you do about it?",
     "d": "Medium", "tip": "Risk identification + proactive communication = senior-level signal."},
]

_SITUATIONAL: list[dict] = [
    {"q": "If you inherited a codebase with no documentation and tight deadlines, how would you approach it?",
     "d": "Hard", "tip": "Mention: reading tests, talking to stakeholders, incremental refactoring."},
    {"q": "Imagine your deployment fails in production 30 minutes before a major demo. What do you do?",
     "d": "Hard", "tip": "Show calm, systematic debugging: rollback → diagnose → fix."},
    {"q": "How would you handle a situation where a key dependency has a critical security vulnerability?",
     "d": "Medium", "tip": "CVE triage, patching strategy, stakeholder communication."},
    {"q": "You're asked to estimate a project but realise the scope is too vague. What's your approach?",
     "d": "Medium", "tip": "Requirements gathering, MVP scoping, range estimates."},
    {"q": "Your team is three sprints behind schedule with no signs of catching up. What do you do?",
     "d": "Hard", "tip": "Scope reduction, stakeholder alignment, and velocity analysis — not just 'work harder'."},
    {"q": "A colleague's code passes all tests but you spot a subtle logic error in review. They push back. What now?",
     "d": "Medium", "tip": "Data + patience. Write a failing test that proves the bug."},
    {"q": "You're the only engineer who understands a critical legacy system that's about to fail. How do you handle the knowledge transfer?",
     "d": "Hard", "tip": "Pair programming, documentation sprints, and video walkthroughs."},
    {"q": "A non-technical stakeholder keeps adding scope to a project mid-sprint. How do you manage this?",
     "d": "Medium", "tip": "Redirect to the backlog process — protect the team without burning bridges."},
    {"q": "You discover that a shipped feature has a data privacy issue affecting real users. What do you do?",
     "d": "Hard", "tip": "Escalate immediately, assess impact, patch and disclose — never bury it."},
    {"q": "Two senior engineers on your team fundamentally disagree on the architecture for a critical system. You need a decision this week. How do you resolve it?",
     "d": "Hard", "tip": "Time-box the debate, use data or spikes, then decide and commit."},
    {"q": "You're asked to build a feature you believe is technically wrong or will harm users. What do you do?",
     "d": "Medium", "tip": "Voice concerns with evidence, propose alternatives — then respect the final call."},
    {"q": "Your team is asked to adopt a new framework that none of you have experience with, starting immediately. How do you plan the transition?",
     "d": "Medium", "tip": "POC first, learning budget, incremental adoption, not a big-bang rewrite."},
    {"q": "A client's system is down in production and they're losing revenue every minute. You're on-call. Walk me through your response.",
     "d": "Hard", "tip": "Communication first (status page), then systematic isolation, then fix or rollback."},
    {"q": "You're halfway through a two-week task and realise your estimate was wildly wrong — it'll take two months. What do you do?",
     "d": "Hard", "tip": "Surface it immediately, bring a revised plan, don't wait until the deadline."},
    {"q": "You notice a teammate is consistently overworked and heading toward burnout. What do you do?",
     "d": "Easy", "tip": "Empathy first, then escalation to the manager if needed — don't just ignore it."},
    {"q": "Your manager asks you to implement a solution you think is technically inferior. How do you handle it?",
     "d": "Medium", "tip": "Present the trade-offs clearly, suggest alternatives, and respect the decision."},
]


_CULTURE_FIT: list[dict] = [
    {"q": "What does your ideal engineering team culture look like?",
     "d": "Easy", "tip": "Research the company's values and align your answer authentically."},
    {"q": "How do you keep your technical skills sharp outside of work?",
     "d": "Easy", "tip": "Mention side projects, open source, courses, communities."},
    {"q": "What motivates you most: building new things, fixing hard bugs, or mentoring others?",
     "d": "Easy", "tip": "Be honest — misalignment leads to unhappiness."},
    {"q": "How do you approach giving and receiving code review feedback?",
     "d": "Medium", "tip": "Empathy + specificity + growth mindset."},

    {"q": "How do you balance moving fast versus writing maintainable, well-tested code?",
     "d": "Medium", "tip": "Neither extreme is right — context matters. Show your nuance."},
    {"q": "Describe your ideal relationship with your engineering manager.",
     "d": "Easy", "tip": "Autonomy with support — show you can manage up as well as be managed."},
    {"q": "What's your philosophy on technical debt? When is it acceptable?",
     "d": "Medium", "tip": "Debt is a tool — taken consciously and paid back intentionally."},
    {"q": "How do you handle ambiguity in your day-to-day work?",
     "d": "Easy", "tip": "Show you can make progress without perfect clarity — and know when to escalate."},
    {"q": "What's the most important quality in a strong engineering team, and why?",
     "d": "Easy", "tip": "Psychological safety, trust, and clear ownership are strong answers."},
    {"q": "How do you think about documentation — is it a chore or a feature?",
     "d": "Easy", "tip": "Best answer: it's a product for future engineers, including your future self."},
    {"q": "How do you decide when something is 'good enough' to ship?",
     "d": "Medium", "tip": "Risk × impact × reversibility — show you think in trade-offs."},
    {"q": "Describe a time your values were challenged at work. How did you respond?",
     "d": "Hard", "tip": "Authenticity counts — don't give a textbook answer here."},
]

_SKILL_TEMPLATES: dict[str, list[dict]] = {

    "Python": [
        {"q": "Explain the difference between `@staticmethod`, `@classmethod`, and instance methods.",
         "d": "Medium", "tip": "Give a concrete use-case for each."},
        {"q": "How does Python's GIL affect multi-threaded CPU-bound workloads, and how do you work around it?",
         "d": "Hard", "tip": "Mention multiprocessing, concurrent.futures, or C extensions."},
        {"q": "Walk me through Python's memory management and garbage collection.",
         "d": "Hard", "tip": "Cover reference counting + cyclic GC."},
        {"q": "What are Python generators and when would you prefer them over a list?",
         "d": "Medium", "tip": "Lazy evaluation + memory efficiency are the key wins."},
        {"q": "Explain the difference between `deepcopy` and `copy`. When does it matter?",
         "d": "Easy", "tip": "Give an example with a nested dict or list."},
        {"q": "What are Python descriptors? Give a real-world example.",
         "d": "Hard", "tip": "`__get__`, `__set__`, `__delete__` — they power `@property`."},
        {"q": "How would you profile and optimise a slow Python function?",
         "d": "Medium", "tip": "cProfile, line_profiler, memory_profiler — measure before optimising."},
    ],

    "JavaScript": [
        {"q": "Explain the event loop and how it handles async operations.",
         "d": "Medium", "tip": "Cover call stack, task queue, microtask queue."},
        {"q": "What's the difference between `==` and `===`, and when would you use each?",
         "d": "Easy", "tip": "Type coercion is the core issue."},
        {"q": "Describe closures and give a practical use-case.",
         "d": "Medium", "tip": "Module pattern and private state are classic examples."},
        {"q": "What is prototype-based inheritance, and how does it differ from class-based?",
         "d": "Hard", "tip": "ES6 `class` is sugar — the prototype chain is still underneath."},
        {"q": "Explain `Promise.all`, `Promise.race`, `Promise.allSettled`, and `Promise.any`. When would you use each?",
         "d": "Medium", "tip": "Think about error-tolerance and fan-out vs. first-response patterns."},
        {"q": "What are WeakMap and WeakSet used for? Why do they exist?",
         "d": "Hard", "tip": "Garbage-collection-friendly keying — useful for caches and metadata."},
        {"q": "How does `this` binding work in JavaScript? List all the ways it can be set.",
         "d": "Medium", "tip": "Default, implicit, explicit (call/bind/apply), new, arrow function."},
    ],

    "TypeScript": [
        {"q": "What is the difference between `interface` and `type` in TypeScript? When would you choose each?",
         "d": "Medium", "tip": "Interfaces are open; types support unions and mapped types."},
        {"q": "Explain `keyof`, `typeof`, and mapped types. Give a practical example.",
         "d": "Hard", "tip": "Show how you'd build a `Partial<T>` or `Readonly<T>` manually."},
        {"q": "What are TypeScript generics and why are they useful? Show a real example.",
         "d": "Medium", "tip": "Generic constraints with `extends` add a lot of power."},
        {"q": "How does TypeScript's structural typing differ from nominal typing?",
         "d": "Hard", "tip": "Duck typing at compile time — show an example where it surprises people."},
        {"q": "What are discriminated unions and how do they help with type narrowing?",
         "d": "Medium", "tip": "Pattern matching without runtime overhead."},
    ],

    "React": [
        {"q": "Explain the difference between `useMemo`, `useCallback`, and `React.memo`. When would you use each?",
         "d": "Hard", "tip": "All three avoid re-renders/re-computations — but for different things."},
        {"q": "How would you handle global state in a large React app without a state management library?",
         "d": "Medium", "tip": "Context + useReducer can get you far; show when it breaks down."},
        {"q": "Describe how React's reconciliation (diffing) algorithm works.",
         "d": "Hard", "tip": "Key prop importance + O(n) heuristic."},
        {"q": "What are React Server Components and how do they differ from Client Components?",
         "d": "Hard", "tip": "Rendering location, bundle size, and data fetching model differ fundamentally."},
        {"q": "Explain the rules of hooks. Why do they exist?",
         "d": "Medium", "tip": "The linked list of hooks depends on call order — any branching breaks it."},
        {"q": "How would you optimise a React app that re-renders too frequently?",
         "d": "Medium", "tip": "React DevTools Profiler first, then memo / selector patterns."},
    ],

    "Node.js": [
        {"q": "How does Node.js handle concurrency if it's single-threaded?",
         "d": "Medium", "tip": "Event loop + libuv thread pool for I/O — it's not truly single-threaded."},
        {"q": "When would you use a Worker Thread vs. a child process in Node.js?",
         "d": "Hard", "tip": "Worker threads share memory; child processes are isolated."},
        {"q": "Explain how `require` caching works in Node.js.",
         "d": "Easy", "tip": "Modules are cached after the first `require` — singletons by default."},
        {"q": "How would you handle uncaught exceptions and unhandled promise rejections in a production Node app?",
         "d": "Medium", "tip": "`process.on('uncaughtException')` is a last resort — proper error propagation is better."},
        {"q": "What's the difference between `process.nextTick` and `setImmediate`?",
         "d": "Hard", "tip": "`nextTick` fires before I/O callbacks; `setImmediate` fires after."},
    ],

    "Docker": [
        {"q": "What's the difference between an image and a container? Explain layers.",
         "d": "Easy", "tip": "Images are read-only; containers add a writable layer."},
        {"q": "How would you reduce a Docker image from 1.2 GB to under 200 MB?",
         "d": "Medium", "tip": "Multi-stage builds, alpine base, .dockerignore, fewer layers."},
        {"q": "Explain the difference between `CMD` and `ENTRYPOINT` in a Dockerfile.",
         "d": "Medium", "tip": "ENTRYPOINT is the fixed executable; CMD is the default argument."},
        {"q": "How does Docker networking work? Explain bridge, host, and overlay networks.",
         "d": "Hard", "tip": "Bridge = isolated LAN; host = no isolation; overlay = multi-host swarm."},
        {"q": "What are Docker volumes and bind mounts? When would you use each?",
         "d": "Easy", "tip": "Volumes are Docker-managed; bind mounts map a host path."},
    ],

    "Kubernetes": [
        {"q": "Explain the difference between a Deployment, StatefulSet, and DaemonSet.",
         "d": "Medium", "tip": "Stateless vs. stateful vs. per-node workloads."},
        {"q": "What happens when a Pod is scheduled? Walk through the control plane flow.",
         "d": "Hard", "tip": "API server → etcd → scheduler → kubelet → container runtime."},
        {"q": "How do you handle secrets in Kubernetes securely?",
         "d": "Medium", "tip": "Sealed Secrets, Vault agent injector, or cloud-native secret stores."},
        {"q": "Explain Kubernetes resource requests and limits. What happens if you exceed them?",
         "d": "Medium", "tip": "Requests affect scheduling; limits cause throttling (CPU) or OOMKill (memory)."},
        {"q": "How would you perform a zero-downtime rolling deployment in Kubernetes?",
         "d": "Hard", "tip": "Proper liveness/readiness probes + RollingUpdate strategy with minAvailable."},
        {"q": "What is the role of an Ingress controller? How does it differ from a LoadBalancer service?",
         "d": "Medium", "tip": "Ingress is L7 routing; LoadBalancer is L4 — Ingress is more cost-efficient at scale."},
    ],

    "AWS": [
        {"q": "Compare SQS and SNS — when would you use each?",
         "d": "Medium", "tip": "SQS = pull/queue; SNS = push/fan-out. Often used together."},
        {"q": "Explain the difference between an IAM role and an IAM user.",
         "d": "Easy", "tip": "Roles are assumed temporarily; users are persistent identities."},
        {"q": "How would you architect a highly available, fault-tolerant web application on AWS?",
         "d": "Hard", "tip": "Multi-AZ, ALB, Auto Scaling Groups, RDS Multi-AZ, S3 for static assets."},
        {"q": "Explain the difference between S3 storage classes. How would you use lifecycle policies?",
         "d": "Medium", "tip": "Standard → IA → Glacier — automate tiering to cut costs."},
        {"q": "What is the AWS Shared Responsibility Model?",
         "d": "Easy", "tip": "AWS owns security *of* the cloud; you own security *in* the cloud."},
        {"q": "How does VPC peering differ from AWS Transit Gateway?",
         "d": "Hard", "tip": "Peering is 1:1 and non-transitive; TGW is a hub-and-spoke router."},
    ],

    "GCP": [
        {"q": "How does BigQuery differ from a traditional RDBMS, and when would you choose it?",
         "d": "Medium", "tip": "Columnar, serverless, optimised for analytics — not OLTP."},
        {"q": "Explain the difference between Pub/Sub and Cloud Tasks.",
         "d": "Medium", "tip": "Pub/Sub is push/fan-out messaging; Cloud Tasks is a managed task queue."},
        {"q": "What are GCP service accounts and how should they be scoped?",
         "d": "Easy", "tip": "Principle of least privilege — one SA per workload."},
        {"q": "How would you design a scalable data pipeline on GCP?",
         "d": "Hard", "tip": "Pub/Sub → Dataflow → BigQuery is the canonical pattern."},
    ],

    "Azure": [
        {"q": "What is the difference between Azure Service Bus and Azure Event Hub?",
         "d": "Medium", "tip": "Service Bus = message queue; Event Hub = high-throughput event streaming."},
        {"q": "Explain Azure Managed Identities and why they're preferred over service principals with secrets.",
         "d": "Medium", "tip": "No credentials to rotate — identity is bound to the resource."},
        {"q": "How does Azure App Service scale, and what are its limits?",
         "d": "Medium", "tip": "Scale up (bigger VM) vs. scale out (more instances) — know both."},
    ],

    "Machine Learning": [
        {"q": "Explain the bias-variance tradeoff and how you'd diagnose each in a model.",
         "d": "Hard", "tip": "High bias = underfitting; high variance = overfitting."},
        {"q": "How would you handle a highly imbalanced dataset in a classification task?",
         "d": "Medium", "tip": "Resampling (SMOTE), class weights, precision-recall over accuracy."},
        {"q": "Walk me through how you'd design an A/B test to evaluate a new ML model in production.",
         "d": "Hard", "tip": "Traffic split, statistical power, guardrail metrics, holdout period."},
        {"q": "What is feature leakage and how do you prevent it?",
         "d": "Hard", "tip": "Future data in training features — use temporal splits and careful pipeline design."},
        {"q": "Explain the difference between bagging and boosting. Give an algorithm example of each.",
         "d": "Medium", "tip": "Random Forest (bagging) vs. XGBoost/GBM (boosting)."},
        {"q": "How would you monitor a machine learning model in production for drift?",
         "d": "Hard", "tip": "Data drift (input distribution), concept drift (relationship), and prediction drift."},
    ],

    "PyTorch": [
        {"q": "Explain the difference between `model.train()` and `model.eval()` in PyTorch.",
         "d": "Easy", "tip": "Dropout and BatchNorm behave differently in each mode."},
        {"q": "What is gradient accumulation and when would you use it?",
         "d": "Hard", "tip": "Simulates larger batch sizes when GPU memory is limited."},
        {"q": "How does `autograd` work in PyTorch? What is the computational graph?",
         "d": "Hard", "tip": "Dynamic graph built forward, traversed backward during `.backward()`."},
        {"q": "Explain the difference between DataLoader's `pin_memory` and `num_workers`.",
         "d": "Medium", "tip": "Pinned memory speeds up CPU→GPU transfers; workers parallelise data loading."},
    ],

    "LLM": [
        {"q": "Explain how Retrieval-Augmented Generation (RAG) works and when you'd use it over fine-tuning.",
         "d": "Hard", "tip": "RAG = dynamic knowledge; fine-tuning = baked-in behaviour."},
        {"q": "What is the attention mechanism in Transformers, and why did it replace RNNs?",
         "d": "Hard", "tip": "Parallelisable and captures long-range dependencies — RNNs struggle with both."},
        {"q": "What are hallucinations in LLMs, and what strategies reduce them?",
         "d": "Medium", "tip": "Grounding via RAG, temperature control, chain-of-thought prompting."},
        {"q": "Explain prompt engineering techniques: zero-shot, few-shot, chain-of-thought, and ReAct.",
         "d": "Medium", "tip": "Each adds more context/guidance — trade-off is token cost."},
    ],
    "Hugging Face": [
        {"q": "How would you fine-tune a pre-trained Hugging Face model for a text classification task?",
         "d": "Medium", "tip": "AutoModelForSequenceClassification + Trainer API or custom loop."},
        {"q": "Explain the difference between model.generate() strategies: greedy, beam search, sampling.",
         "d": "Hard", "tip": "Greedy = fast; beam = better quality; sampling = diversity."},
        {"q": "How would you optimise a Hugging Face model for inference on a CPU?",
         "d": "Hard", "tip": "Quantisation (int8/fp16), ONNX export, or distillation."},
    ],

    "PostgreSQL": [
        {"q": "Explain the difference between a B-tree and a BRIN index. When would you choose each?",
         "d": "Hard", "tip": "B-tree for selective queries; BRIN for naturally ordered large tables."},
        {"q": "How would you diagnose and fix a slow query in PostgreSQL?",
         "d": "Medium", "tip": "EXPLAIN ANALYZE, then look at Seq Scan on large tables, missing indexes."},
        {"q": "What is MVCC and how does it enable concurrent transactions in PostgreSQL?",
         "d": "Hard", "tip": "Multiple versions coexist — readers don't block writers."},
        {"q": "Explain the difference between INNER JOIN, LEFT JOIN, and a lateral join.",
         "d": "Medium", "tip": "Lateral is a correlated subquery that can reference the outer row — like a for-each."},
        {"q": "What is connection pooling and why is it important for PostgreSQL at scale?",
         "d": "Medium", "tip": "PgBouncer is the standard — PostgreSQL forks a process per connection."},
    ],

    "MongoDB": [
        {"q": "When would you choose MongoDB over PostgreSQL? What trade-offs are you accepting?",
         "d": "Medium", "tip": "Flexible schema vs. ACID guarantees — not a free lunch."},
        {"q": "Explain the aggregation pipeline in MongoDB. Build a stage that groups and sorts.",
         "d": "Medium", "tip": "$match → $group → $sort is the canonical pattern."},
        {"q": "What is a covered query in MongoDB and how do you achieve it?",
         "d": "Hard", "tip": "Query satisfied entirely from the index — no document fetch needed."},
        {"q": "How does MongoDB handle transactions? What are the limitations?",
         "d": "Hard", "tip": "Multi-document ACID since 4.0 — but with performance overhead."},
    ],

    "Redis": [
        {"q": "What persistence options does Redis offer and what are the trade-offs?",
         "d": "Medium", "tip": "RDB (snapshots) vs. AOF (log) vs. both — durability vs. performance."},
        {"q": "How would you implement a distributed rate limiter using Redis?",
         "d": "Hard", "tip": "INCR + EXPIRE, or the sliding window with sorted sets."},
        {"q": "Explain Redis eviction policies. Which would you use for a cache?",
         "d": "Medium", "tip": "`allkeys-lru` is usually right for pure cache workloads."},
        {"q": "What are Redis Streams and how do they compare to Pub/Sub?",
         "d": "Hard", "tip": "Streams are persistent, ordered, and consumer-group aware — Pub/Sub is fire-and-forget."},
    ],

    "Elasticsearch": [
        {"q": "Explain the difference between a `term` query and a `match` query in Elasticsearch.",
         "d": "Medium", "tip": "`term` is exact (keyword); `match` runs through the analyser (text)."},
        {"q": "How does Elasticsearch handle document scoring (relevance)?",
         "d": "Hard", "tip": "BM25 by default — TF-IDF variant with saturation and field-length norms."},
        {"q": "How would you design an index for high write throughput in Elasticsearch?",
         "d": "Hard", "tip": "Reduce replicas during bulk indexing, use bulk API, tune refresh interval."},
    ],

    "Git": [
        {"q": "Explain the difference between `git merge` and `git rebase`. When would you use each?",
         "d": "Medium", "tip": "Merge preserves history; rebase creates a linear history — use rebase for local cleanup."},
        {"q": "What is a fast-forward merge and when does it happen?",
         "d": "Easy", "tip": "No divergence — HEAD can simply move forward."},
        {"q": "How would you recover a commit that was lost after a hard reset?",
         "d": "Hard", "tip": "`git reflog` is your friend here."},
        {"q": "Explain `git bisect`. When would you use it?",
         "d": "Medium", "tip": "Binary search through commit history to find a regression."},
    ],

    "CI/CD": [
        {"q": "What's the difference between Continuous Integration, Continuous Delivery, and Continuous Deployment?",
         "d": "Easy", "tip": "CD (delivery) = manual prod release; CD (deployment) = automatic prod release."},
        {"q": "How would you design a CI/CD pipeline for a microservices architecture?",
         "d": "Hard", "tip": "Independent pipelines per service, shared library for common steps, canary deployments."},
        {"q": "What strategies would you use to make a CI pipeline faster?",
         "d": "Medium", "tip": "Caching, parallelism, test splitting, and failing fast on lint."},
    ],

    "Terraform": [
        {"q": "Explain the Terraform state file. What problems arise if two engineers apply simultaneously?",
         "d": "Medium", "tip": "Remote state + state locking (DynamoDB for AWS) solves this."},
        {"q": "What is the difference between `terraform plan` and `terraform apply`?",
         "d": "Easy", "tip": "Plan is a dry-run; apply executes the change."},
        {"q": "How would you structure a Terraform project for a large organisation with multiple teams?",
         "d": "Hard", "tip": "Workspaces or separate state files per environment, module registry for sharing."},
    ],

    "Linux": [
        {"q": "Explain the difference between a process and a thread at the OS level.",
         "d": "Hard", "tip": "Processes have separate memory spaces; threads share memory within a process."},
        {"q": "How would you troubleshoot high CPU usage on a Linux server?",
         "d": "Medium", "tip": "`top`/`htop`, `perf`, `strace` — find the hot process/syscall."},
        {"q": "What is the difference between `hard link` and `soft (symbolic) link`?",
         "d": "Easy", "tip": "Hard links share the inode; soft links are a pointer to a path."},
        {"q": "How does the Linux kernel handle memory paging and swapping?",
         "d": "Hard", "tip": "Virtual memory, page tables, OOM killer — swapping is a last resort."},
    ],
    "Bash": [
        {"q": "How would you write a Bash script that retries a failing command up to 5 times?",
         "d": "Medium", "tip": "Loop with a counter, sleep between retries, exit on success."},
        {"q": "Explain the difference between `$()` and backticks for command substitution.",
         "d": "Easy", "tip": "`$()` is nestable and modern — always prefer it."},
        {"q": "How would you safely handle errors in a Bash script?",
         "d": "Medium", "tip": "`set -euo pipefail` at the top — fail fast, fail loud."},
    ],

    "Swift": [
        {"q": "Explain Swift's `ARC` (Automatic Reference Counting). What causes retain cycles?",
         "d": "Hard", "tip": "`weak` and `unowned` references break cycles — know when to use each."},
        {"q": "What is the difference between a `struct` and a `class` in Swift?",
         "d": "Medium", "tip": "Value semantics vs. reference semantics — structs are copied, classes are shared."},
        {"q": "Explain Swift's `async/await` and how it compares to completion handlers.",
         "d": "Medium", "tip": "Structured concurrency — cleaner call stack and error propagation."},
    ],
    
    "Kotlin": [
        {"q": "Explain the difference between `val` and `var`, and `const val`.",
         "d": "Easy", "tip": "`const val` is a compile-time constant; `val` is runtime immutable."},
        {"q": "What are Kotlin coroutines and how do they differ from Java threads?",
         "d": "Hard", "tip": "Coroutines are lightweight and cooperative; they don't block OS threads."},
        {"q": "Explain Kotlin's null safety system. How does it prevent NPEs?",
         "d": "Medium", "tip": "Nullable types (`?`) must be explicitly unwrapped — compiler enforces it."},
    ],

    "Agile": [
        {"q": "What's the difference between Scrum and Kanban? When would you choose each?",
         "d": "Easy", "tip": "Scrum = time-boxed sprints; Kanban = continuous flow with WIP limits."},
        {"q": "How do you handle technical stories and refactoring work within a Scrum sprint?",
         "d": "Medium", "tip": "Include tech debt as first-class backlog items — not hidden work."},
        {"q": "What makes a good user story? What is the INVEST criteria?",
         "d": "Easy", "tip": "Independent, Negotiable, Valuable, Estimable, Small, Testable."},
    ],

    "scikit-learn": [
        {"q": "Explain the difference between `fit`, `transform`, and `fit_transform` in scikit-learn.",
         "d": "Easy", "tip": "`fit` learns parameters; `transform` applies them — never `fit` on test data."},
        {"q": "How would you build a reproducible ML pipeline using scikit-learn's Pipeline API?",
         "d": "Medium", "tip": "Chaining preprocessors + estimator prevents data leakage from cross-validation."},
        {"q": "What cross-validation strategy would you use for time-series data and why?",
         "d": "Hard", "tip": "`TimeSeriesSplit` — standard k-fold would leak future data."},
    ],

    "FastAPI": [
        {"q": "How does FastAPI use Pydantic for request validation? What happens on validation failure?",
         "d": "Easy", "tip": "422 Unprocessable Entity with a detailed error body."},
        {"q": "Explain FastAPI's dependency injection system. Give a real-world use-case.",
         "d": "Medium", "tip": "Database sessions, auth, config — anything you want scoped per-request."},
        {"q": "How would you implement background tasks and async endpoints in FastAPI?",
         "d": "Medium", "tip": "`BackgroundTasks` for fire-and-forget; `async def` endpoints for I/O-bound work."},
    ],

    "Django": [
        {"q": "Explain Django's ORM N+1 problem and how to fix it.",
         "d": "Medium", "tip": "`select_related` (FK joins) and `prefetch_related` (reverse FK / M2M)."},
        {"q": "How does Django's middleware stack work?",
         "d": "Medium", "tip": "Onion model — each middleware wraps the view. Order matters."},
        {"q": "What is Django signals and when would you use (or avoid) them?",
         "d": "Hard", "tip": "Decoupled side effects — but hard to test and trace. Use sparingly."},
    ],

    "default": [
        {"q": "Walk me through a complex technical problem you solved recently.",
         "d": "Medium", "tip": "Emphasise your debugging process, not just the solution."},
        {"q": "How do you ensure code quality on your team?",
         "d": "Easy", "tip": "PR reviews, linting, testing culture, and automated CI checks."},
        {"q": "What's your approach to system design when starting a new project from scratch?",
         "d": "Hard", "tip": "Clarify requirements → define constraints → API design → data model → scalability."},
        {"q": "How do you stay current with best practices in your field?",
         "d": "Easy", "tip": "Newsletter, papers, open-source contribution, conferences."},
        {"q": "Explain the CAP theorem and how it influences database choice.",
         "d": "Hard", "tip": "Consistency, Availability, Partition tolerance — pick two in a network."},
        {"q": "How do you approach writing tests? What's the right balance between unit, integration, and E2E?",
         "d": "Medium", "tip": "Testing pyramid — many fast unit tests, fewer slow E2E tests."},
        {"q": "What's the most important thing you look for when reviewing someone else's code?",
         "d": "Easy", "tip": "Correctness first, then clarity, then performance — in that order."},
        {"q": "How would you explain a complex technical concept to a non-technical stakeholder?",
         "d": "Easy", "tip": "Analogy + impact, not jargon. Know your audience."},
        {"q": "Describe your approach to designing a RESTful API from scratch.",
         "d": "Medium", "tip": "Resource naming, HTTP verbs, versioning, pagination, error contracts."},
        {"q": "What is eventual consistency and when is it acceptable?",
         "d": "Hard", "tip": "DNS, shopping carts, social counts — where stale reads are tolerable."},
        {"q": "How do you think about observability in a production system?",
         "d": "Medium", "tip": "Logs, metrics, traces — the three pillars. Show you understand the difference."},
        {"q": "Walk me through how you'd debug a memory leak in a long-running service.",
         "d": "Hard", "tip": "Heap snapshots, metric trends, profiling tools — isolate before patching."},
    ],
}


def generate_questions(
    skills: list[str],
    job_title: str = "",
    num_questions: int = 10,
) -> list[InterviewQuestion]:
    questions: list[InterviewQuestion] = []

    tech_target = max(num_questions // 2, 3)
    tech_added  = 0
    random.shuffle(skills)

    for skill in skills:
        if tech_added >= tech_target:
            break
        templates = _SKILL_TEMPLATES.get(skill, [])
        if templates:
            q_data = random.choice(templates)
            questions.append(InterviewQuestion(
                question   = q_data["q"],
                type       = QuestionType.TECHNICAL,
                difficulty = q_data["d"],
                skill_tag  = skill,
                tip        = q_data.get("tip"),
            ))
            tech_added += 1

    while tech_added < tech_target:
        q_data = random.choice(_SKILL_TEMPLATES["default"])
        questions.append(InterviewQuestion(
            question   = q_data["q"],
            type       = QuestionType.TECHNICAL,
            difficulty = q_data["d"],
        ))
        tech_added += 1

    behav_target = max(num_questions // 4, 2)
    for q_data in random.sample(_BEHAVIOURAL, min(behav_target, len(_BEHAVIOURAL))):
        questions.append(InterviewQuestion(
            question   = q_data["q"],
            type       = QuestionType.BEHAVIOURAL,
            difficulty = q_data["d"],
            tip        = q_data.get("tip"),
        ))

    sit_target = max(num_questions // 6, 1)
    for q_data in random.sample(_SITUATIONAL, min(sit_target, len(_SITUATIONAL))):
        questions.append(InterviewQuestion(
            question   = q_data["q"],
            type       = QuestionType.SITUATIONAL,
            difficulty = q_data["d"],
            tip        = q_data.get("tip"),
        ))

    for q_data in random.sample(_CULTURE_FIT, min(1, len(_CULTURE_FIT))):
        questions.append(InterviewQuestion(
            question   = q_data["q"],
            type       = QuestionType.CULTURE_FIT,
            difficulty = q_data["d"],
            tip        = q_data.get("tip"),
        ))

    random.shuffle(questions)
    return questions[:num_questions]