# Agent Framework Integration Guide

Complete documentation for all agent and RAG frameworks integrated with Phoenix Custom-Evals.

---

## 🎯 Overview

Phoenix Custom-Evals provides comprehensive integration with 17+ agent frameworks, enabling developers to evaluate agent outputs across multiple platforms with consistent quality metrics.

**Evaluation Metrics**:
- **Coherence** (threshold: ≥ 0.7) - Logical flow and consistency
- **Relevance** (threshold: ≥ 0.7) - Query-response relevance
- **Correctness** (threshold: ≥ 0.7) - Factual accuracy
- **Toxicity** (threshold: ≤ 0.2) - Harmful content detection

---

## 📦 Agent Frameworks

### Cloud Platform Frameworks

#### 1. **AWS Strands Agents** 🆕
**Provider**: AWS  
**Models**: Claude (via Bedrock)  
**Best For**: AWS cloud applications, Bedrock integration  

```bash
pip install strands boto3
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export AWS_REGION="us-east-1"
```

- **Documentation**: [AWS Strands Guide](frameworks/aws-strands.md)
- **Example**: `examples/aws_strands_agents_example.py`
- **Features**: Multi-agent orchestration, AWS Bedrock integration, Claude models
- **Test Suites**: 5 comprehensive tests

---

#### 2. **Google ADK (Agent Development Kit)** 🆕
**Provider**: Google  
**Models**: Gemini 1.5 Flash, Gemini 1.5 Pro  
**Best For**: Google Cloud applications, Gemini integration  

```bash
pip install google-adk
export GOOGLE_API_KEY="your-google-key"
```

- **Documentation**: [Google ADK Guide](frameworks/google-adk.md)
- **Example**: `examples/google_adk_example.py`
- **GitHub**: https://github.com/google/adk-python
- **Features**: Function decorators, AgentRunner, multi-agent support
- **Test Suites**: 5 comprehensive tests

---

#### 3. **Databricks Agent Bricks SDK** 🆕
**Provider**: Databricks  
**Models**: OpenAI, others  
**Best For**: Data workflows, ML pipelines, MLflow integration  

```bash
pip install databricks-agents mlflow
export OPENAI_API_KEY="your-key"
```

- **Documentation**: [Databricks Agent Bricks Guide](frameworks/databricks-agent-bricks.md)
- **Example**: `examples/databricks_agent_bricks_example.py`
- **Features**: MLflow tracking, data tools, multi-agent workflows
- **Test Suites**: 5 comprehensive tests
- **Special**: Native MLflow experiment tracking

---

### Microsoft Ecosystem

#### 4. **Microsoft Agent Framework** 🆕
**Provider**: Microsoft  
**Models**: OpenAI (GPT-4, GPT-3.5)  
**Best For**: Enterprise agents, production deployments  

```bash
pip install microsoft-agents
export OPENAI_API_KEY="your-key"
```

- **Documentation**: [Microsoft Agent Framework Guide](frameworks/microsoft-agent-framework.md)
- **Example**: `examples/microsoft_agent_framework_example.py`
- **Features**: AgentConfig, AgentRuntime, tool system
- **Test Suites**: 5 comprehensive tests

---

#### 5. **Semantic Kernel** 🆕
**Provider**: Microsoft  
**Models**: OpenAI, Azure OpenAI  
**Best For**: Plugin ecosystems, multi-step planning  

```bash
pip install semantic-kernel
export OPENAI_API_KEY="your-key"
```

- **Documentation**: [Semantic Kernel Guide](frameworks/semantic-kernel.md)
- **Example**: `examples/semantic_kernel_example.py`
- **Features**: Plugin system, SequentialPlanner, kernel architecture
- **Test Suites**: 5 comprehensive tests

---

#### 6. **Autogen (Microsoft)**
**Provider**: Microsoft  
**Models**: OpenAI, others  
**Best For**: Multi-agent conversations, code execution  

```bash
pip install pyautogen
export OPENAI_API_KEY="your-key"
```

- **Documentation**: [Autogen Guide](frameworks/autogen.md)
- **Example**: `examples/autogen_agent_example.py`
- **Features**: Group chat, code execution, multi-agent conversations

---

### LangChain Ecosystem

#### 7. **LangGraph** 🆕
**Provider**: LangChain  
**Models**: OpenAI, others  
**Best For**: Stateful workflows, graph-based agents  

```bash
pip install langgraph langchain langchain-openai
export OPENAI_API_KEY="your-key"
```

- **Documentation**: [LangGraph Guide](frameworks/langgraph.md)
- **Example**: Create `examples/langgraph_example.py`
- **Features**: State graphs, cyclic workflows, checkpointing
- **Test Suites**: Comprehensive state management tests

---

#### 8. **LangChain RAG**
**Provider**: LangChain  
**Models**: OpenAI, others  
**Best For**: RAG applications, document Q&A  

```bash
pip install langchain langchain-openai
export OPENAI_API_KEY="your-key"
```

- **Documentation**: [LangChain RAG Guide](frameworks/langchain-rag.md)
- **Features**: Vector stores, retrievers, document loaders

---

### LlamaIndex Ecosystem

#### 9. **LlamaIndex Workflows** 🆕
**Provider**: LlamaIndex  
**Models**: OpenAI, others  
**Best For**: Event-driven workflows, complex orchestration  

```bash
pip install llama-index llama-index-llms-openai
export OPENAI_API_KEY="your-key"
```

- **Documentation**: [LlamaIndex Workflows Guide](frameworks/llamaindex-workflows.md)
- **Example**: `examples/llamaindex_workflows_example.py`
- **Features**: Event-driven architecture, step decorators, async/await
- **Test Suites**: 5 comprehensive tests

---

#### 10. **LlamaIndex RAG**
**Provider**: LlamaIndex  
**Models**: OpenAI, others  
**Best For**: RAG applications, data indexing  

```bash
pip install llama-index llama-index-llms-openai
export OPENAI_API_KEY="your-key"
```

- **Documentation**: [LlamaIndex RAG Guide](frameworks/llamaindex-rag.md)
- **Features**: Index management, query engines, retrievers

---

### OpenAI Frameworks

#### 11. **OpenAI Agents Framework**
**Provider**: OpenAI  
**Models**: GPT-4, GPT-3.5  
**Best For**: Official OpenAI agent patterns  

```bash
pip install openai
export OPENAI_API_KEY="your-key"
```

- **Documentation**: [OpenAI Agents Framework Guide](frameworks/openai-agents-framework.md)
- **Example**: `examples/openai_agents_framework_example.py`
- **Features**: Native handoffs, function tools, routing

---

#### 12. **OpenAI Agents SDK**
**Provider**: OpenAI  
**Models**: GPT-4, GPT-3.5  
**Best For**: Function calling agents  

```bash
pip install openai
export OPENAI_API_KEY="your-key"
```

- **Documentation**: [OpenAI Agents SDK Guide](frameworks/openai-agents.md)
- **Example**: `examples/openai_agent_example.py`
- **Features**: Function calling, stateless agents

---

#### 13. **OpenAI Assistants API**
**Provider**: OpenAI  
**Models**: GPT-4, GPT-3.5  
**Best For**: Persistent conversations, threads  

```bash
pip install openai
export OPENAI_API_KEY="your-key"
```

- **Documentation**: [OpenAI Assistants Guide](frameworks/openai-assistants.md)
- **Example**: `examples/openai_assistants_example.py`
- **Features**: Thread management, code interpreter, file handling

---

#### 14. **OpenAI Swarm**
**Provider**: OpenAI  
**Models**: GPT-4, GPT-3.5  
**Best For**: Lightweight multi-agent orchestration  

```bash
pip install openai
export OPENAI_API_KEY="your-key"
```

- **Documentation**: [OpenAI Swarm Guide](frameworks/openai-swarm.md)
- **Example**: `examples/openai_swarm_agent_example.py`
- **Features**: Agent handoffs, context passing

---

### Other Frameworks

#### 15. **Agno** 🆕
**Provider**: Agno
**Models**: Anthropic Claude, OpenAI, Google Gemini, others
**Best For**: Multi-agent systems at scale, workflow automation

```bash
pip install agno anthropic
export ANTHROPIC_API_KEY="your-key"
```

- **Documentation**: [Agno Guide](frameworks/agno.md)
- **Example**: `examples/agno_example.py`
- **Official Docs**: https://docs.agno.com/
- **GitHub**: https://github.com/agno-agi/agno
- **Features**: Multi-agent Teams, workflow automation, MCP support, knowledge management (RAG), memory persistence, structured I/O, multimodal support, reasoning
- **Test Suites**: 5 comprehensive tests

---

#### 16. **CrewAI**
**Provider**: CrewAI
**Models**: OpenAI, others
**Best For**: Role-based multi-agent systems

```bash
pip install crewai
export OPENAI_API_KEY="your-key"
```

- **Documentation**: [CrewAI Guide](frameworks/crewai.md)
- **Example**: `examples/crewai_agent_example.py`
- **Features**: Role-based agents, sequential/hierarchical processes

---

#### 17. **Pydantic AI**
**Provider**: Pydantic
**Models**: OpenAI, others
**Best For**: Type-safe agents, structured outputs

```bash
pip install pydantic-ai
export OPENAI_API_KEY="your-key"
```

- **Documentation**: [Pydantic AI Guide](frameworks/pydanticai.md)
- **Example**: `examples/pydanticai_agent_example.py`
- **Features**: Pydantic models, type validation, structured outputs

---

## 📊 Framework Comparison

| Framework | Provider | Models | Multi-Agent | Tools | MLflow | Best For |
|-----------|----------|--------|-------------|-------|--------|----------|
| **Agno** | Agno | Claude/GPT+ | ✅ | Decorator/MCP | ❌ | Multi-agent scale |
| **AWS Strands** | AWS | Claude | ✅ | Class | ❌ | AWS apps |
| **Google ADK** | Google | Gemini | ✅ | Decorator | ❌ | Google Cloud |
| **Databricks** | Databricks | OpenAI+ | ✅ | Function | ✅ | Data/ML |
| **Microsoft Agent** | Microsoft | OpenAI | ✅ | Class | ❌ | Enterprise |
| **Semantic Kernel** | Microsoft | OpenAI+ | ✅ | Plugin | ❌ | Plugins |
| **Autogen** | Microsoft | OpenAI+ | ✅ | Function | ❌ | Conversations |
| **LangGraph** | LangChain | OpenAI+ | ✅ | Function | ❌ | Stateful |
| **LlamaIndex Workflows** | LlamaIndex | OpenAI+ | ✅ | Function | ❌ | Events |
| **OpenAI Agents** | OpenAI | GPT-4 | ✅ | Function | ❌ | OpenAI native |
| **OpenAI Swarm** | OpenAI | GPT-4 | ✅ | Function | ❌ | Lightweight |
| **CrewAI** | CrewAI | OpenAI+ | ✅ | Function | ❌ | Role-based |
| **Pydantic AI** | Pydantic | OpenAI+ | ✅ | Function | ❌ | Type-safe |

---

## 🚀 Quick Start Guide

### 1. Choose Your Framework

Select based on your requirements:
- **Multi-Agent at Scale**: Agno
- **AWS/Claude**: AWS Strands
- **Google Cloud/Gemini**: Google ADK
- **Data/ML**: Databricks Agent Bricks
- **Enterprise**: Microsoft Agent Framework
- **Plugins**: Semantic Kernel
- **Stateful Workflows**: LangGraph
- **Event-Driven**: LlamaIndex Workflows
- **Type-Safe**: Pydantic AI

### 2. Install Framework

```bash
pip install [framework-package]
export API_KEY="your-api-key"
```

### 3. Run Example

```bash
python examples/[framework]_example.py
```

### 4. Add Evaluation

```python
from custom.evals import CoherenceEvaluator
from custom.evals.llm import LLM

# Create evaluator
eval_llm = LLM(provider="openai", model="gpt-4o-mini")
evaluator = CoherenceEvaluator(eval_llm)

# Evaluate
score = evaluator.evaluate({"input": query, "output": response})
print(f"Coherence: {score.label} ({score.score:.2f})")
```

---

## 📈 Evaluation Pattern

All frameworks follow this consistent pattern:

```python
from custom.evals import (
    CoherenceEvaluator,
    RelevanceEvaluator,
    CorrectnessEvaluator,
    ToxicityEvaluator
)
from custom.evals.llm import LLM

class EvaluatedAgent:
    def __init__(self):
        # Create agent (framework-specific)
        self.agent = create_agent()

        # Initialize evaluators
        eval_llm = LLM(provider="openai", model="gpt-4o-mini")
        self.evaluators = {
            "coherence": CoherenceEvaluator(eval_llm),
            "relevance": RelevanceEvaluator(eval_llm),
            "correctness": CorrectnessEvaluator(eval_llm),
            "toxicity": ToxicityEvaluator(eval_llm)
        }

    def evaluate(self, query: str, response: str):
        scores = {}
        for name, evaluator in self.evaluators.items():
            score = evaluator.evaluate({"input": query, "output": response})
            scores[name] = score
        return scores
```

---

## ✅ Quality Gates

```python
QUALITY_THRESHOLDS = {
    "coherence": 0.7,
    "relevance": 0.7,
    "correctness": 0.7,
    "toxicity": 0.2  # Lower is better
}

def validate_quality_gates(scores):
    passed = True
    for metric, threshold in QUALITY_THRESHOLDS.items():
        if metric == "toxicity":
            if scores[metric].score > threshold:
                passed = False
        else:
            if scores[metric].score < threshold:
                passed = False
    return passed
```

---

## 📚 Documentation Links

### Complete Framework Documentation
- [Agno](frameworks/agno.md)
- [AWS Strands Agents](frameworks/aws-strands.md)
- [Google ADK](frameworks/google-adk.md)
- [LlamaIndex Workflows](frameworks/llamaindex-workflows.md)
- [Microsoft Agent Framework](frameworks/microsoft-agent-framework.md)
- [Databricks Agent Bricks](frameworks/databricks-agent-bricks.md)
- [Semantic Kernel](frameworks/semantic-kernel.md)
- [LangGraph](frameworks/langgraph.md)
- [Autogen](frameworks/autogen.md)
- [CrewAI](frameworks/crewai.md)
- [Pydantic AI](frameworks/pydanticai.md)
- [OpenAI Agents Framework](frameworks/openai-agents-framework.md)
- [OpenAI Agents SDK](frameworks/openai-agents.md)
- [OpenAI Assistants](frameworks/openai-assistants.md)
- [OpenAI Swarm](frameworks/openai-swarm.md)
- [LangChain RAG](frameworks/langchain-rag.md)
- [LlamaIndex RAG](frameworks/llamaindex-rag.md)

---

## 💡 Best Practices

### 1. Always Evaluate
```python
# ✅ Good: Evaluate every response
result = agent.run(query)
scores = evaluate(query, result)
```

### 2. Use Quality Gates
```python
# ✅ Good: Validate thresholds
if not validate_quality_gates(scores):
    alert_quality_failure(query, scores)
```

### 3. Batch Testing
```python
# ✅ Good: Test multiple scenarios
test_cases = [{"query": "...", "category": "..."}]
results = batch_evaluate(agent, test_cases)
```

### 4. Monitor Metrics
```python
# ✅ Good: Track over time
for metric, score in scores.items():
    log_to_monitoring(metric, score.score)
```

---

## 🎓 Support

- **Documentation**: See framework-specific guides above
- **Examples**: All examples in `examples/` directory
- **GitHub**: Report issues on GitHub
- **Community**: Join discussions

---

**Total Frameworks**: 17+ agent frameworks + RAG integrations
**Custom-Evals**: Fully integrated across all frameworks
**Documentation**: Complete with examples and best practices

**Created**: 2026-01-17
**Last Updated**: 2026-01-17
**Status**: Production Ready
