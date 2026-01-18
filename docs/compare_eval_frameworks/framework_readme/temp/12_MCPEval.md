# MCPEval: Protocol-Level Tool & Function Calling Evaluation

**Type**: Python Framework | **License**: Open Source | **Year**: 2025

---

## Quick Overview

MCPEval is an **open-source automated evaluation framework for LLM agents** that leverages the Model Context Protocol (MCP) to assess tool-augmented systems. It's specifically designed for evaluating function calling accuracy, tool usage patterns, and agent behavior in interactive environments with standardized, reproducible benchmarks.

### At a Glance

| Aspect | Details |
|--------|---------|
| **Focus** | Tool/function calling evaluation |
| **Setup Time** | ⚡ 10-15 minutes |
| **Learning Curve** | Medium |
| **Dependencies** | MCP protocol, LLM APIs |
| **Cost** | Free (OSS) + LLM API costs |
| **Best For** | Agent developers, tool evaluators |

---

## Key Strengths

### ✅ Advantages

1. **Protocol-Level Evaluation**
   - Built on Model Context Protocol (MCP) standard
   - Vendor-agnostic tool evaluation
   - Standardized tool specifications
   - Universal protocol support
   - MCP server integration

2. **Automated Task Generation**
   - Queries MCP servers for tool specifications
   - Auto-generates test cases from tool schemas
   - Reduces manual test creation
   - Domain-flexible benchmarking
   - Scalable test generation

3. **Dual-Perspective Evaluation**
   - **Granular tool call matching**: Exact execution comparison
   - **Rubric-based LLM judging**: Holistic quality assessment
   - Combines precision with nuanced evaluation
   - Both quantitative and qualitative metrics
   - Complementary evaluation approaches

4. **Comprehensive Tool Metrics**
   - **Tool call names**: Correct function selection
   - **Parameters**: Accurate argument passing
   - **Sequencing**: Logical tool order
   - **Execution flow**: Step-by-step validation
   - **Context sensitivity**: Appropriate tool usage

5. **Iterative Task Verification**
   - Revalidation step improves task quality
   - Analyzes actual tool conversations
   - Refines task descriptions
   - Higher-quality evaluation datasets
   - Better task clarity

6. **Extensive Research Validation**
   - 5,000+ trajectory records analyzed
   - 5,000+ completion records evaluated
   - 50 model-domain combinations tested
   - 10 models evaluated (open & closed source)
   - 5 real-world domains: Healthcare, Finance, Airbnb, Sports, Parks
   - Most extensive LLM tool-use evaluation to date

7. **Multi-Domain Support**
   - Healthcare systems
   - Financial applications
   - Booking platforms (Airbnb)
   - Sports analytics
   - Geographic information (National Parks)
   - Easily extensible to new domains

### ⚠️ Limitations

1. **MCP Protocol Dependency**
   - Requires MCP server setup
   - Tool systems must implement MCP
   - Learning curve for MCP protocol
   - Not all tools support MCP yet
   - Protocol overhead

2. **Tool-Only Focus**
   - Specialized for tool/function calling
   - No general text generation metrics
   - Limited RAG evaluation capabilities
   - Not suitable for non-tool applications
   - Narrow use case focus

3. **Relatively New (2025)**
   - Limited production deployments
   - Smaller community
   - Fewer examples and tutorials
   - Documentation still growing
   - Less battle-tested

4. **Complexity**
   - Three-stage workflow (generation, verification, evaluation)
   - Requires understanding of MCP protocol
   - More setup than simple eval frameworks
   - Multiple components to manage
   - Steeper learning curve

5. **LLM API Dependency**
   - Requires LLM for judging
   - API costs for evaluation
   - No offline evaluation mode
   - Dependent on external providers
   - Cost scales with usage

6. **Limited Observability**
   - No built-in dashboard
   - No real-time monitoring
   - Basic reporting
   - Manual trace analysis
   - No production monitoring features

---

## vs Other Frameworks

### vs Custom-Evals

| Aspect | MCPEval | Custom-Evals |
|--------|---------|--------------|
| **Tool Evaluation** | ✅✅ Best-in-class | ✅ Good |
| **MCP Protocol** | ✅✅ Native | ❌ No |
| **Auto Task Gen** | ✅✅ Yes | ❌ No |
| **General Eval** | ❌ Limited | ✅✅ Comprehensive |
| **Multi-Framework** | MCP-only | 17+ providers |
| **RAG Metrics** | ❌ No | ✅ Yes |
| **Setup Complexity** | Higher | Lower |

**Choose MCPEval if**: You're building MCP-based agents with complex tool usage

**Choose Custom-Evals if**: You need comprehensive evaluation beyond tools

---

### vs Google ADK

| Aspect | MCPEval | Google ADK |
|--------|---------|------------|
| **Tool Focus** | ✅✅ Core | ✅✅ Core |
| **Protocol** | MCP standard | Gemini-specific |
| **Auto Task Gen** | ✅ Yes | ⚠️ Manual |
| **Vendor Lock-in** | ❌ Agnostic | ⚠️ Google |
| **CLI Tools** | Basic | ✅✅ Excellent |
| **Web UI** | ❌ No | ✅ Yes |
| **Research Backing** | ✅✅ Strong | ⚠️ Limited |

**Choose MCPEval if**: Need protocol-level, vendor-agnostic tool evaluation

**Choose Google ADK if**: Building Gemini agents, want CLI/UI tools

---

### vs DeepEval

| Aspect | MCPEval | DeepEval |
|--------|---------|----------|
| **Tool Evaluation** | ✅✅ Deep | ⚠️ Basic |
| **MCP Support** | ✅✅ Native | ✅ Integrated |
| **Auto Task Gen** | ✅ Yes | ❌ No |
| **General Metrics** | ❌ Limited | ✅✅ Many |
| **Pytest** | ⚠️ Basic | ✅✅ Native |
| **Scope** | Tool-only | Multi-purpose |
| **Research** | ✅✅ Strong | ⚠️ Limited |

**Choose MCPEval if**: Need research-grade tool evaluation with MCP

**Choose DeepEval if**: Want comprehensive testing framework with pytest

---

## When to Choose MCPEval

### ✅ Perfect For

1. **MCP-Based Agent Systems**
   - Applications using Model Context Protocol
   - MCP server implementations
   - Protocol-compliant tools
   - Standardized tool interfaces
   - Universal agent platforms

2. **Tool Calling Accuracy Testing**
   - Function name selection validation
   - Parameter passing correctness
   - Tool sequencing logic
   - Execution flow analysis
   - Context-aware tool usage

3. **Research & Benchmarking**
   - Academic research on tool usage
   - Standardized agent benchmarks
   - Cross-model comparisons
   - Tool-use capability studies
   - Publication-quality evaluation

4. **Multi-Domain Tool Systems**
   - Healthcare applications
   - Financial systems
   - Booking platforms
   - Data analytics tools
   - Geographic information systems

5. **Automated Test Generation**
   - Large tool suites
   - Rapidly evolving tool sets
   - Minimal manual test creation
   - Scalable evaluation needs
   - Dynamic tool ecosystems

### ❌ Not Ideal For

1. **Non-MCP Systems**
   - Custom tool implementations
   - Proprietary protocols
   - Non-standardized interfaces
   - Legacy systems
   - Simple function calls

2. **General LLM Evaluation**
   - Text generation quality
   - RAG systems without tools
   - Simple Q&A applications
   - Content creation
   - Translation tasks

3. **Production Monitoring**
   - Real-time observability
   - Live trace collection
   - Alert systems
   - Dashboard requirements
   - Long-term metric storage

4. **Simple Use Cases**
   - Basic function calling
   - Single-tool applications
   - Non-interactive systems
   - Straightforward workflows
   - Minimal tool complexity

5. **Rapid Prototyping**
   - Quick evaluation needs
   - Minimal setup time
   - Simple metrics only
   - No MCP infrastructure
   - Fast iteration requirements

---

## Pricing

### Cost Breakdown

| Component | Cost |
|-----------|------|
| **MCPEval Framework** | 💰 **Free** (Open Source) |
| **MCP Servers** | Free (self-hosted) |
| **LLM Judge API** | ~$0.01-0.05 per evaluation |
| **Infrastructure** | Local or cloud hosting |

### Detailed Cost Analysis

#### Per Evaluation Cost (with LLM Judge)

**Using GPT-4o-mini**:
- Task generation: ~$0.005
- Tool matching: Free (local)
- LLM judging: ~$0.01-0.02
- **Total per eval**: ~$0.015-0.025

**Using GPT-4**:
- Task generation: ~$0.02
- Tool matching: Free (local)
- LLM judging: ~$0.05-0.10
- **Total per eval**: ~$0.07-0.12

#### Monthly Cost Estimates

| Evaluations/Month | GPT-4o-mini | GPT-4 |
|-------------------|-------------|-------|
| 1,000 | $15-25 | $70-120 |
| 10,000 | $150-250 | $700-1,200 |
| 100,000 | $1,500-2,500 | $7,000-12,000 |

### Cost Optimization Tips

1. **Use local matching first** - Free exact matching
2. **Sample your tests** - Evaluate subsets for quick feedback
3. **Cache task generation** - Reuse generated tasks
4. **Use cheaper judge models** - GPT-4o-mini vs GPT-4
5. **Batch evaluations** - More efficient API usage

---

## Quick Start

### Prerequisites

```bash
# Install MCPEval
pip install mcpeval

# Install MCP SDK (for servers)
pip install mcp

# Set up LLM API key (for judging)
export OPENAI_API_KEY=your-api-key
```

### 5-Minute Example

```python
# 1. Define MCP server with tools
from mcp import MCPServer, tool

server = MCPServer(name="calculator")

@tool(server)
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@tool(server)
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@tool(server)
def divide(a: int, b: int) -> float:
    """Divide two numbers."""
    return a / b

# 2. Start MCP server
server.start()

# 3. Run MCPEval
from mcpeval import evaluate_agent

results = evaluate_agent(
    agent_model="gpt-4o-mini",
    mcp_server_url="http://localhost:8000",
    num_test_cases=10,  # Auto-generate 10 test cases
    evaluation_metrics=[
        "tool_name_accuracy",
        "parameter_accuracy",
        "execution_flow",
        "rubric_based_quality"
    ]
)

# 4. View results
print(f"Tool Name Accuracy: {results.tool_name_accuracy:.2%}")
print(f"Parameter Accuracy: {results.parameter_accuracy:.2%}")
print(f"Execution Flow Score: {results.execution_flow_score:.2f}/5")
print(f"Overall Quality: {results.overall_quality:.2f}/5")
```

**Output:**
```
Tool Name Accuracy: 95.00%
Parameter Accuracy: 92.00%
Execution Flow Score: 4.3/5
Overall Quality: 4.5/5

✓ Generated 10 test cases automatically
✓ Evaluated across 4 metrics
✓ Total time: 45 seconds
```

---

## Advanced Usage Examples

### 1. Healthcare Domain Tool Evaluation

```python
from mcp import MCPServer, tool
from mcpeval import evaluate_agent, HealthcareBenchmark

# Healthcare MCP server
server = MCPServer(name="healthcare_system")

@tool(server)
def lookup_patient(patient_id: str) -> dict:
    """Look up patient information."""
    return {"id": patient_id, "name": "John Doe", "age": 45}

@tool(server)
def check_allergies(patient_id: str) -> list:
    """Check patient allergies."""
    return ["penicillin", "peanuts"]

@tool(server)
def prescribe_medication(patient_id: str, medication: str, dosage: str) -> bool:
    """Prescribe medication to patient."""
    # Check allergies first, then prescribe
    return True

@tool(server)
def schedule_appointment(patient_id: str, date: str, doctor: str) -> str:
    """Schedule appointment."""
    return f"Appointment scheduled for {date} with Dr. {doctor}"

# Evaluate healthcare agent
results = evaluate_agent(
    agent_model="gpt-4o",
    mcp_server_url="http://localhost:8000",
    benchmark=HealthcareBenchmark(),  # Pre-defined healthcare scenarios
    evaluation_criteria={
        "tool_trajectory": {
            "check_order": True,  # Must check allergies before prescribing
            "required_tools": ["lookup_patient", "check_allergies", "prescribe_medication"]
        },
        "safety": {
            "rubric": "Agent must verify allergies before any medication prescription"
        },
        "completeness": {
            "rubric": "Agent should gather all necessary patient information"
        }
    }
)

print(f"\nHealthcare Agent Evaluation:")
print(f"  Safe Tool Usage: {results.safety_score:.2f}/5")
print(f"  Correct Sequencing: {results.trajectory_score:.2%}")
print(f"  Completeness: {results.completeness_score:.2f}/5")

if results.safety_score < 4.0:
    print(f"\n⚠️ WARNING: Safety concerns detected!")
    for issue in results.safety_issues:
        print(f"  - {issue}")
```

---

### 2. Financial Systems Evaluation

```python
from mcpeval import evaluate_agent, FinancialBenchmark

# Financial tools MCP server
server = MCPServer(name="financial_system")

@tool(server)
def get_account_balance(account_id: str) -> float:
    """Get account balance."""
    return 10000.00

@tool(server)
def verify_identity(account_id: str, credentials: dict) -> bool:
    """Verify user identity."""
    return True

@tool(server)
def transfer_funds(from_account: str, to_account: str, amount: float) -> dict:
    """Transfer funds between accounts."""
    return {"status": "success", "transaction_id": "TXN123"}

@tool(server)
def log_transaction(transaction_id: str, details: dict) -> bool:
    """Log transaction for audit."""
    return True

# Evaluate financial agent with strict criteria
results = evaluate_agent(
    agent_model="gpt-4o",
    mcp_server_url="http://localhost:8000",
    benchmark=FinancialBenchmark(),
    evaluation_criteria={
        "security": {
            "rubric": "Agent must verify identity before any financial operations",
            "required_first_tool": "verify_identity"
        },
        "audit_trail": {
            "rubric": "All transactions must be logged",
            "required_final_tool": "log_transaction"
        },
        "accuracy": {
            "check_parameters": True,
            "no_hallucinated_values": True
        }
    }
)

print(f"\nFinancial Agent Evaluation:")
print(f"  Security Compliance: {results.security_score:.2f}/5")
print(f"  Audit Trail: {results.audit_score:.2f}/5")
print(f"  Parameter Accuracy: {results.parameter_accuracy:.2%}")

# Critical checks
if results.security_score < 5.0:
    print(f"\n❌ CRITICAL: Security issues detected - NOT production ready")
else:
    print(f"\n✅ Security checks passed - Production ready")
```

---

### 3. Automated Task Generation & Verification

```python
from mcpeval import TaskGenerator, TaskVerifier

# Step 1: Generate tasks from MCP server
generator = TaskGenerator(mcp_server_url="http://localhost:8000")

generated_tasks = generator.generate_tasks(
    num_tasks=100,
    complexity_levels=["simple", "medium", "complex"],
    coverage_strategy="comprehensive"  # Cover all tool combinations
)

print(f"Generated {len(generated_tasks)} tasks")
print(f"  Simple: {sum(1 for t in generated_tasks if t.complexity == 'simple')}")
print(f"  Medium: {sum(1 for t in generated_tasks if t.complexity == 'medium')}")
print(f"  Complex: {sum(1 for t in generated_tasks if t.complexity == 'complex')}")

# Step 2: Verify task quality
verifier = TaskVerifier(agent_model="gpt-4o-mini")

verified_tasks = []
for task in generated_tasks:
    # Run actual agent on task
    agent_response = run_agent(task)

    # Verify task is well-formed
    verification = verifier.verify_task(
        task=task,
        agent_response=agent_response
    )

    if verification.is_valid:
        # Improve task description based on actual execution
        improved_task = verifier.improve_task_description(
            task=task,
            agent_conversation=agent_response.conversation
        )
        verified_tasks.append(improved_task)

print(f"\nVerified {len(verified_tasks)} high-quality tasks")

# Step 3: Evaluate with verified tasks
results = evaluate_agent(
    agent_model="gpt-4o",
    tasks=verified_tasks,
    evaluation_metrics=["all"]
)
```

---

### 4. Cross-Model Comparison

```python
from mcpeval import compare_models

# Compare multiple models on same task set
models_to_evaluate = [
    "gpt-4o",
    "gpt-4o-mini",
    "claude-3-5-sonnet-20241022",
    "claude-3-haiku-20240307",
    "gemini-1.5-pro",
    "gemini-1.5-flash"
]

results = compare_models(
    models=models_to_evaluate,
    mcp_server_url="http://localhost:8000",
    benchmark="comprehensive",
    num_tasks=50
)

print("\nCross-Model Tool Usage Comparison:\n")
print(f"{'Model':<30} {'Accuracy':<12} {'Flow Score':<12} {'Quality':<10}")
print("-" * 70)

for model, scores in results.items():
    print(f"{model:<30} "
          f"{scores.tool_accuracy:.1%}      "
          f"{scores.flow_score:.2f}/5      "
          f"{scores.quality:.2f}/5")

# Find best model
best_model = max(results.items(), key=lambda x: x[1].overall_score)
print(f"\n🏆 Best Model: {best_model[0]}")
print(f"   Overall Score: {best_model[1].overall_score:.2f}/5")
```

**Output:**
```
Cross-Model Tool Usage Comparison:

Model                          Accuracy     Flow Score   Quality
----------------------------------------------------------------------
gpt-4o                         94.0%        4.5/5        4.7/5
gpt-4o-mini                    89.0%        4.2/5        4.3/5
claude-3-5-sonnet-20241022     92.0%        4.4/5        4.6/5
claude-3-haiku-20240307        85.0%        3.9/5        4.0/5
gemini-1.5-pro                 91.0%        4.3/5        4.5/5
gemini-1.5-flash               87.0%        4.0/5        4.2/5

🏆 Best Model: gpt-4o
   Overall Score: 4.7/5
```

---

### 5. Rubric-Based Quality Evaluation

```python
from mcpeval import RubricEvaluator

# Define comprehensive evaluation rubric
booking_agent_rubric = """
Evaluate the booking agent on the following dimensions:

1. Planning Quality (25%)
   - Does agent plan appropriate tool sequence?
   - Are dependencies between tools understood?
   - Is the approach efficient?

2. Execution Flow (25%)
   - Are tools called in logical order?
   - Are all necessary tools used?
   - Are redundant calls avoided?

3. Context Sensitivity (25%)
   - Does agent adapt to user context?
   - Are parameters extracted accurately from conversation?
   - Is conversation history properly used?

4. Requirement Satisfaction (25%)
   - Does agent fulfill user's booking request?
   - Are all booking details confirmed?
   - Is confirmation provided to user?

Score each dimension 1-5.
Provide overall score and detailed justification.
"""

# Evaluate with custom rubric
evaluator = RubricEvaluator(
    rubric=booking_agent_rubric,
    judge_model="gpt-4o"
)

results = evaluator.evaluate_agent(
    agent_model="gpt-4o-mini",
    mcp_server_url="http://localhost:8000",
    test_scenarios=[
        "Book a hotel in San Francisco for next weekend",
        "Find and book a flight from NYC to LA",
        "Reserve a restaurant table for 4 people tonight"
    ]
)

print("\nRubric-Based Evaluation Results:\n")
for scenario, scores in results.items():
    print(f"{scenario}:")
    print(f"  Planning: {scores.planning:.1f}/5")
    print(f"  Execution: {scores.execution:.1f}/5")
    print(f"  Context: {scores.context:.1f}/5")
    print(f"  Satisfaction: {scores.satisfaction:.1f}/5")
    print(f"  Overall: {scores.overall:.1f}/5")
    print(f"  Justification: {scores.justification}\n")
```

---

### 6. Real-World Domain Benchmarks

```python
from mcpeval.benchmarks import (
    HealthcareBenchmark,
    FinanceBenchmark,
    AirbnbBenchmark,
    SportsAnalyticsBenchmark,
    NationalParksBenchmark
)

# Run agent across multiple real-world domains
domains = [
    ("Healthcare", HealthcareBenchmark()),
    ("Finance", FinanceBenchmark()),
    ("Airbnb", AirbnbBenchmark()),
    ("Sports", SportsAnalyticsBenchmark()),
    ("Parks", NationalParksBenchmark())
]

print("Multi-Domain Agent Evaluation:\n")

for domain_name, benchmark in domains:
    results = evaluate_agent(
        agent_model="gpt-4o",
        benchmark=benchmark,
        mcp_server_url=f"http://localhost:8000/{domain_name.lower()}"
    )

    print(f"{domain_name}:")
    print(f"  Tool Accuracy: {results.tool_accuracy:.1%}")
    print(f"  Flow Score: {results.flow_score:.2f}/5")
    print(f"  Domain Quality: {results.domain_quality:.2f}/5")
    print()

# Overall cross-domain performance
print(f"Average Cross-Domain Performance: {avg_score:.2f}/5")
```

---

## Architecture Highlights

### Design Principles

1. **Protocol-Level**: Built on MCP standard for universal compatibility
2. **Automated**: Generate tests from tool specifications
3. **Dual Evaluation**: Combine exact matching with LLM judging
4. **Research-Grade**: Extensively validated across domains and models
5. **Iterative**: Task verification improves quality over time

### Three-Stage Evaluation Workflow

#### Stage 1: Task Generation
```
MCP Server → Tool Specs → LLM Generation → Test Tasks
```
- Query MCP server for available tools
- Extract tool specifications and schemas
- Use LLM to generate realistic usage scenarios
- Create diverse test cases automatically

#### Stage 2: Task Verification
```
Test Tasks → Agent Execution → Conversation Analysis → Refined Tasks
```
- Run agent on generated tasks
- Analyze actual tool conversations
- Identify task ambiguities or issues
- Improve task descriptions for clarity
- Filter out invalid or problematic tasks

#### Stage 3: Evaluation & Reporting
```
Refined Tasks → Dual Evaluation → Metrics → Report
```
- **Strict Matching**: Exact tool call comparison
- **Flexible Matching**: Allow reasonable variations
- **LLM Judging**: Holistic quality assessment
- Generate comprehensive evaluation report

### Evaluation Metrics Explained

#### Granular Matching Metrics

**Tool Name Accuracy**:
- Percentage of correct tool selections
- Binary match: right tool or wrong tool
- Score: 0-100%

**Parameter Accuracy**:
- Correct parameter extraction and passing
- Checks all required parameters
- Validates parameter types and values
- Score: 0-100%

**Execution Sequence**:
- Tool calls in correct order
- Dependencies respected
- No unnecessary calls
- Score: 0-100%

#### LLM Judge Metrics

**Planning Quality** (1-5):
- Appropriate tool selection strategy
- Understanding of task requirements
- Efficient approach planning

**Execution Flow** (1-5):
- Logical step-by-step progression
- Proper tool orchestration
- Handling of dependencies

**Context Sensitivity** (1-5):
- Adapts to conversation context
- Uses information appropriately
- Maintains conversation state

**Requirement Satisfaction** (1-5):
- Fulfills user's request
- Complete task execution
- Appropriate final response

---

## Comparison Summary

### Unique Advantages

1. ⭐ **MCP Protocol Native** - Standardized, universal evaluation
2. 🤖 **Automated Task Generation** - Minimal manual test creation
3. 🔬 **Research-Grade** - Extensively validated (5K+ records)
4. 🎯 **Dual Evaluation** - Exact + LLM judging
5. 📊 **Multi-Domain** - 5+ real-world benchmarks
6. 🔄 **Iterative Verification** - Improving task quality

### Trade-offs

1. MCP protocol dependency
2. Tool-only focus (no general eval)
3. Relatively new (2025)
4. Higher complexity than simple frameworks
5. LLM API costs for judging
6. No built-in observability

### MCPEval vs The Competition

| Feature | MCPEval | Custom-Evals | Google ADK | DeepEval | LangSmith |
|---------|---------|--------------|------------|----------|-----------|
| **MCP Protocol** | ✅✅ | ❌ | ❌ | ✅ | ❌ |
| **Auto Task Gen** | ✅✅ | ❌ | ❌ | ❌ | ❌ |
| **Tool Focus** | ✅✅ | ✅ | ✅✅ | ⚠️ | ✅ |
| **Research Grade** | ✅✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| **General Eval** | ❌ | ✅✅ | ⚠️ | ✅✅ | ✅ |
| **Observability** | ❌ | ⚠️ | ⚠️ | ⚠️ | ✅✅ |

---

## Resources

### Official Documentation
- **Model Context Protocol**: https://modelcontextprotocol.io/
- **MCPEval Paper**: https://arxiv.org/abs/2507.12806
- **GitHub**: https://github.com/SalesforceAIResearch/MCPEval
- **MCP Eval (LastMile)**: https://github.com/lastmile-ai/mcp-eval

### Integration Guides
- **DeepEval MCP**: https://deepeval.com/docs/getting-started-mcp
- **OpenAI Cookbook**: https://cookbook.openai.com/examples/evaluation/use-cases/mcp_eval_notebook
- **MCP Evals Website**: https://www.mcpevals.io/

### Research & Benchmarks
- **ArXiv Paper**: "MCPEval: Automatic MCP-based Deep Evaluation for AI Agent Models"
- **EmergentMind**: https://www.emergentmind.com/topics/mcpeval
- **VentureBeat Article**: Protocol-level agent testing coverage

### Community
- **GitHub Discussions**: Project-specific discussions
- **MCP Community**: Model Context Protocol community

---

## Verdict

**MCPEval is the cutting-edge choice for developers building MCP-based agent systems who need research-grade, protocol-level evaluation of tool calling accuracy with automated test generation and comprehensive benchmarks.**

**Rating**: ⭐⭐⭐⭐ (4/5 for MCP agents, 2/5 for non-MCP)

### Choose MCPEval if you value:
- ✅ MCP protocol standardization
- ✅ Automated test generation
- ✅ Research-grade validation
- ✅ Tool calling accuracy
- ✅ Multi-domain benchmarks
- ✅ Dual evaluation approach

### Choose alternatives if you need:
- ❌ General LLM evaluation → Custom-Evals, DeepEval
- ❌ RAG-specific metrics → RAGAS
- ❌ Production observability → LangSmith, Phoenix
- ❌ Simple setup → Custom-Evals, RAGAS
- ❌ Non-MCP tools → Google ADK, Custom-Evals
- ❌ Mature ecosystem → Established frameworks

---

## Decision Matrix

### Use MCPEval when:
✅ Building MCP-based agents
✅ Need tool calling validation
✅ Want automated test generation
✅ Require research-grade evaluation
✅ Testing across multiple domains
✅ Need protocol-level standardization

### Don't use MCPEval when:
❌ Non-MCP tool implementations
❌ General LLM applications
❌ RAG-only systems
❌ Need production monitoring
❌ Want simple, quick setup
❌ No tool calling focus

---

## Quick Reference Card

```bash
# Installation
pip install mcpeval mcp

# Set API key
export OPENAI_API_KEY=your-key

# Basic evaluation
from mcpeval import evaluate_agent

results = evaluate_agent(
    agent_model="gpt-4o-mini",
    mcp_server_url="http://localhost:8000",
    num_test_cases=10
)

# Core Metrics
tool_name_accuracy        # Correct tool selection %
parameter_accuracy        # Correct parameters %
execution_flow_score      # Logical sequencing (1-5)
planning_quality         # LLM-judged planning (1-5)
context_sensitivity      # Context awareness (1-5)
requirement_satisfaction # Task fulfillment (1-5)

# Cost: ~$0.015-0.025 per eval (GPT-4o-mini)
#       ~$0.07-0.12 per eval (GPT-4)
```

---

**Next Steps**:
1. [Try the Example Code](mcpeval_example.py)
2. [Compare All Frameworks](Compare_All_Eval_Frameworks.md)
3. [View Framework Index](FRAMEWORKS_INDEX.md)

**Related**:
- [Custom-Evals Comparison](01_Custom_Evals.md)
- [Google ADK Comparison](10_Google_ADK.md)
- [DeepEval Comparison](08_DeepEval.md)

---

*Last Updated: January 2026*
*MCPEval Version: Latest*
*Maintained by: Custom-Evals Team*
