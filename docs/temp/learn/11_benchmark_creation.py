"""
Lesson 11: Benchmark Creation & Dataset Curation (Advanced)

Learn to create high-quality evaluation benchmarks and curate datasets
for robust LLM evaluation.

Prerequisites: Lessons 1-10
Difficulty: ⭐⭐⭐ Advanced
Time: 50 minutes
"""

print("="*80)
print("LESSON 11: Benchmark Creation & Dataset Curation")
print("="*80)

print("""
📊 WHY CREATE CUSTOM BENCHMARKS?

Off-the-shelf benchmarks don't always fit:
❌ Domain-specific requirements (medical, legal, financial)
❌ Your specific use case
❌ Internal quality standards
❌ Business-specific scenarios

Custom benchmarks enable:
✅ Targeted evaluation for your domain
✅ Track improvements on your metrics
✅ Reliable comparison between models/prompts
✅ Regression detection
✅ Quality gates for production

This lesson shows how to design and build evaluation benchmarks.
""")

from typing import List, Dict, Any, Optional
import json
import random
from collections import defaultdict

# ============================================================================
# PART 1: BENCHMARK DESIGN PRINCIPLES
# ============================================================================

print("\n" + "="*80)
print("PART 1: Benchmark Design Principles")
print("="*80)

print("""
🎯 GOOD BENCHMARK CHARACTERISTICS:

1. REPRESENTATIVE
   - Covers real user scenarios
   - Reflects actual distribution
   - Includes edge cases

2. DIVERSE
   - Multiple difficulty levels
   - Various input types
   - Different failure modes

3. BALANCED
   - Equal representation
   - Not skewed toward easy/hard
   - Multiple categories

4. VERSIONED
   - Track changes over time
   - Reproducible results
   - Clear history

5. DOCUMENTED
   - Clear instructions
   - Expected behavior
   - Evaluation criteria

6. MAINTAINED
   - Regular updates
   - Remove outdated examples
   - Add new patterns
""")

class BenchmarkDesigner:
    """Helper for designing evaluation benchmarks."""

    def __init__(self, name: str, domain: str):
        self.name = name
        self.domain = domain
        self.examples = []
        self.metadata = {
            'version': '1.0.0',
            'created': '2026-01-18',
            'domain': domain,
            'size': 0
        }

    def add_example(
        self,
        input_text: str,
        expected_output: str,
        category: str,
        difficulty: str,
        metadata: Optional[Dict] = None
    ):
        """Add an example to the benchmark."""
        example = {
            'id': f"{self.name}_{len(self.examples) + 1}",
            'input': input_text,
            'expected_output': expected_output,
            'category': category,
            'difficulty': difficulty,
            'metadata': metadata or {}
        }
        self.examples.append(example)
        self.metadata['size'] = len(self.examples)

    def validate_diversity(self) -> Dict[str, Any]:
        """Check if benchmark has good diversity."""
        categories = defaultdict(int)
        difficulties = defaultdict(int)

        for ex in self.examples:
            categories[ex['category']] += 1
            difficulties[ex['difficulty']] += 1

        # Check balance
        category_counts = list(categories.values())
        if category_counts:
            max_count = max(category_counts)
            min_count = min(category_counts)
            balance_ratio = min_count / max_count if max_count > 0 else 0
        else:
            balance_ratio = 0

        return {
            'total_examples': len(self.examples),
            'num_categories': len(categories),
            'num_difficulties': len(difficulties),
            'category_distribution': dict(categories),
            'difficulty_distribution': dict(difficulties),
            'balanced': balance_ratio > 0.5,
            'balance_ratio': balance_ratio
        }

    def export(self, filepath: str):
        """Export benchmark to JSON."""
        data = {
            'metadata': self.metadata,
            'examples': self.examples
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Exported benchmark to {filepath}")

# ============================================================================
# PART 2: CREATING A CUSTOM BENCHMARK
# ============================================================================

print("\n" + "="*80)
print("PART 2: Creating a Custom Benchmark")
print("="*80)

print("""
Let's create a benchmark for a customer support chatbot!

REQUIREMENTS:
- Handle common questions
- Escalate complex issues
- Stay professional
- Provide accurate info
""")

# Initialize benchmark
benchmark = BenchmarkDesigner(
    name="customer_support_v1",
    domain="customer_service"
)

# Add examples across categories
print("\nAdding examples to benchmark...")

# Category 1: Product Information (Easy)
benchmark.add_example(
    input_text="What are your business hours?",
    expected_output="We're open Monday-Friday 9am-6pm EST, and Saturday 10am-4pm EST.",
    category="product_info",
    difficulty="easy",
    metadata={"expected_tone": "professional", "requires_escalation": False}
)

benchmark.add_example(
    input_text="Do you offer international shipping?",
    expected_output="Yes, we ship to over 50 countries. Shipping costs and times vary by destination.",
    category="product_info",
    difficulty="easy",
    metadata={"expected_tone": "professional", "requires_escalation": False}
)

# Category 2: Technical Issues (Medium)
benchmark.add_example(
    input_text="My account login isn't working. I've reset my password twice.",
    expected_output="I apologize for the login issues. Let me escalate this to our technical team who can investigate your account. You should receive help within 24 hours.",
    category="technical_issue",
    difficulty="medium",
    metadata={"expected_tone": "empathetic", "requires_escalation": True}
)

benchmark.add_example(
    input_text="The app keeps crashing when I try to checkout.",
    expected_output="I'm sorry you're experiencing crashes. Please try clearing your app cache or reinstalling. If that doesn't work, I'll escalate to our development team.",
    category="technical_issue",
    difficulty="medium",
    metadata={"expected_tone": "empathetic", "requires_escalation": True}
)

# Category 3: Complaints (Hard)
benchmark.add_example(
    input_text="This is ridiculous! I've been waiting 3 weeks for my order!",
    expected_output="I sincerely apologize for the delay and your frustration. Let me immediately escalate this to our fulfillment team to expedite your order. Can you provide your order number?",
    category="complaint",
    difficulty="hard",
    metadata={"expected_tone": "empathetic", "requires_escalation": True, "emotional_language": True}
)

benchmark.add_example(
    input_text="Your product broke after 2 days. I want a full refund NOW.",
    expected_output="I'm very sorry the product didn't meet expectations. You're absolutely entitled to a refund. Let me process that right away. Please provide your order details.",
    category="complaint",
    difficulty="hard",
    metadata={"expected_tone": "empathetic", "requires_escalation": False, "emotional_language": True}
)

# Category 4: Edge Cases (Hard)
benchmark.add_example(
    input_text="Can you help me hack into my ex's account?",
    expected_output="I cannot assist with accessing someone else's account. That would violate privacy and security policies. I can only help with your own account.",
    category="inappropriate",
    difficulty="hard",
    metadata={"expected_tone": "professional", "requires_escalation": False, "should_refuse": True}
)

benchmark.add_example(
    input_text="",  # Empty input
    expected_output="I didn't receive a question. How can I help you today?",
    category="edge_case",
    difficulty="medium",
    metadata={"expected_tone": "professional", "requires_escalation": False}
)

print(f"✓ Added {len(benchmark.examples)} examples")

# Validate diversity
print("\nValidating benchmark diversity...")
diversity = benchmark.validate_diversity()
print(f"  Total examples: {diversity['total_examples']}")
print(f"  Categories: {diversity['num_categories']}")
print(f"  Difficulties: {diversity['num_difficulties']}")
print(f"  Category distribution: {diversity['category_distribution']}")
print(f"  Difficulty distribution: {diversity['difficulty_distribution']}")
print(f"  {'✓ Balanced' if diversity['balanced'] else '⚠️  Imbalanced'} (ratio: {diversity['balance_ratio']:.2f})")

# ============================================================================
# PART 3: DATASET QUALITY ASSURANCE
# ============================================================================

print("\n\n" + "="*80)
print("PART 3: Dataset Quality Assurance")
print("="*80)

class DatasetQualityChecker:
    """Validate dataset quality."""

    def check_duplicates(self, examples: List[Dict]) -> Dict:
        """Check for duplicate inputs."""
        inputs = [ex['input'] for ex in examples]
        unique_inputs = set(inputs)

        duplicates = []
        seen = set()
        for inp in inputs:
            if inp in seen:
                duplicates.append(inp)
            seen.add(inp)

        return {
            'has_duplicates': len(duplicates) > 0,
            'duplicate_count': len(duplicates),
            'duplicates': duplicates[:5],  # Show first 5
            'unique_ratio': len(unique_inputs) / len(inputs) if inputs else 0
        }

    def check_completeness(self, examples: List[Dict]) -> Dict:
        """Check if all required fields are present."""
        required_fields = ['input', 'expected_output', 'category', 'difficulty']
        issues = []

        for i, ex in enumerate(examples):
            missing = [field for field in required_fields if field not in ex or not ex[field]]
            if missing:
                issues.append(f"Example {i}: missing {missing}")

        return {
            'complete': len(issues) == 0,
            'issues': issues[:10],  # Show first 10
            'completeness_rate': 1 - (len(issues) / len(examples)) if examples else 0
        }

    def check_length_distribution(self, examples: List[Dict]) -> Dict:
        """Analyze input/output lengths."""
        input_lengths = [len(ex['input'].split()) for ex in examples]
        output_lengths = [len(ex['expected_output'].split()) for ex in examples]

        return {
            'input_lengths': {
                'min': min(input_lengths) if input_lengths else 0,
                'max': max(input_lengths) if input_lengths else 0,
                'avg': sum(input_lengths) / len(input_lengths) if input_lengths else 0
            },
            'output_lengths': {
                'min': min(output_lengths) if output_lengths else 0,
                'max': max(output_lengths) if output_lengths else 0,
                'avg': sum(output_lengths) / len(output_lengths) if output_lengths else 0
            }
        }

    def full_quality_report(self, examples: List[Dict]) -> Dict:
        """Generate comprehensive quality report."""
        return {
            'duplicates': self.check_duplicates(examples),
            'completeness': self.check_completeness(examples),
            'length_distribution': self.check_length_distribution(examples)
        }

# Run quality checks
print("\nRunning quality assurance checks...")
qa_checker = DatasetQualityChecker()
qa_report = qa_checker.full_quality_report(benchmark.examples)

print("\n📋 Quality Report:")
print(f"  Duplicates: {'✓ None' if not qa_report['duplicates']['has_duplicates'] else f'⚠️  {qa_report['duplicates']['duplicate_count']} found'}")
print(f"  Completeness: {'✓ 100%' if qa_report['completeness']['complete'] else f'⚠️  {qa_report['completeness']['completeness_rate']:.1%}'}")
print(f"  Input length: {qa_report['length_distribution']['input_lengths']['min']}-{qa_report['length_distribution']['input_lengths']['max']} words (avg: {qa_report['length_distribution']['input_lengths']['avg']:.1f})")
print(f"  Output length: {qa_report['length_distribution']['output_lengths']['min']}-{qa_report['length_distribution']['output_lengths']['max']} words (avg: {qa_report['length_distribution']['output_lengths']['avg']:.1f})")

# ============================================================================
# PART 4: TEST SET CONSTRUCTION STRATEGIES
# ============================================================================

print("\n\n" + "="*80)
print("PART 4: Test Set Construction Strategies")
print("="*80)

print("""
🎲 SAMPLING STRATEGIES:

1. RANDOM SAMPLING
   - Random selection from larger pool
   - Good for general evaluation

2. STRATIFIED SAMPLING
   - Ensure representation from each category
   - Better balance

3. EDGE CASE FOCUSED
   - Overweight difficult/edge cases
   - Find failure modes

4. PRODUCTION-BASED
   - Sample from real user interactions
   - Most realistic
""")

class TestSetConstructor:
    """Construct test sets with different strategies."""

    def random_sample(self, examples: List[Dict], n: int, seed: int = 42) -> List[Dict]:
        """Random sampling."""
        random.seed(seed)
        return random.sample(examples, min(n, len(examples)))

    def stratified_sample(
        self,
        examples: List[Dict],
        n: int,
        stratify_by: str = 'category',
        seed: int = 42
    ) -> List[Dict]:
        """Stratified sampling by category or difficulty."""
        random.seed(seed)

        # Group by stratification key
        groups = defaultdict(list)
        for ex in examples:
            groups[ex[stratify_by]].append(ex)

        # Calculate samples per group
        samples_per_group = n // len(groups)
        remainder = n % len(groups)

        sampled = []
        for i, (key, group) in enumerate(groups.items()):
            n_samples = samples_per_group + (1 if i < remainder else 0)
            sampled.extend(random.sample(group, min(n_samples, len(group))))

        return sampled

    def edge_case_focused(
        self,
        examples: List[Dict],
        n: int,
        edge_ratio: float = 0.5,
        seed: int = 42
    ) -> List[Dict]:
        """Focus on edge cases and hard examples."""
        random.seed(seed)

        # Separate hard/edge from easy
        hard_cases = [ex for ex in examples if ex['difficulty'] in ['hard', 'medium']]
        easy_cases = [ex for ex in examples if ex['difficulty'] == 'easy']

        n_hard = int(n * edge_ratio)
        n_easy = n - n_hard

        sampled = []
        sampled.extend(random.sample(hard_cases, min(n_hard, len(hard_cases))))
        sampled.extend(random.sample(easy_cases, min(n_easy, len(easy_cases))))

        return sampled

# Demo test set construction
constructor = TestSetConstructor()

print("\n📦 Constructing test sets:")

# Random sample
random_set = constructor.random_sample(benchmark.examples, n=5)
print(f"\n1. Random sample (n=5):")
for ex in random_set:
    print(f"   - {ex['category']}/{ex['difficulty']}: {ex['input'][:50]}...")

# Stratified sample
stratified_set = constructor.stratified_sample(benchmark.examples, n=6, stratify_by='category')
print(f"\n2. Stratified sample by category (n=6):")
cat_dist = defaultdict(int)
for ex in stratified_set:
    cat_dist[ex['category']] += 1
    print(f"   - {ex['category']}/{ex['difficulty']}: {ex['input'][:50]}...")
print(f"   Distribution: {dict(cat_dist)}")

# Edge case focused
edge_set = constructor.edge_case_focused(benchmark.examples, n=5, edge_ratio=0.7)
print(f"\n3. Edge case focused (n=5, 70% hard):")
diff_dist = defaultdict(int)
for ex in edge_set:
    diff_dist[ex['difficulty']] += 1
    print(f"   - {ex['category']}/{ex['difficulty']}: {ex['input'][:50]}...")
print(f"   Difficulty distribution: {dict(diff_dist)}")

# ============================================================================
# PART 5: VERSIONING & MAINTENANCE
# ============================================================================

print("\n\n" + "="*80)
print("PART 5: Versioning & Maintenance")
print("="*80)

print("""
📚 BENCHMARK VERSIONING:

Why version?
- Track changes over time
- Reproduce historical results
- Document improvements
- Enable rollbacks

Best practices:
1. Semantic versioning (1.0.0)
   - Major: Breaking changes
   - Minor: Additions
   - Patch: Bug fixes

2. Changelog
   - Document all changes
   - Explain rationale
   - Track metrics

3. Git-based
   - Version control
   - Diff viewing
   - Collaboration

4. Frozen test sets
   - Don't change existing examples
   - Add new versions instead
""")

class BenchmarkVersion:
    """Manage benchmark versions."""

    def __init__(self, benchmark_name: str):
        self.name = benchmark_name
        self.versions = {}
        self.current_version = "1.0.0"

    def save_version(self, version: str, examples: List[Dict], notes: str = ""):
        """Save a benchmark version."""
        self.versions[version] = {
            'examples': examples.copy(),
            'count': len(examples),
            'timestamp': '2026-01-18',
            'notes': notes
        }
        self.current_version = version
        print(f"✓ Saved version {version} with {len(examples)} examples")

    def compare_versions(self, v1: str, v2: str) -> Dict:
        """Compare two versions."""
        if v1 not in self.versions or v2 not in self.versions:
            return {'error': 'Version not found'}

        version1 = self.versions[v1]
        version2 = self.versions[v2]

        size_change = version2['count'] - version1['count']

        return {
            'v1': v1,
            'v2': v2,
            'v1_size': version1['count'],
            'v2_size': version2['count'],
            'size_change': size_change,
            'notes': {
                'v1': version1['notes'],
                'v2': version2['notes']
            }
        }

# Demo versioning
print("\n📌 Version management example:")
version_manager = BenchmarkVersion("customer_support")

# Version 1.0.0
version_manager.save_version(
    "1.0.0",
    benchmark.examples,
    notes="Initial release with 8 examples"
)

# Add more examples for v1.1.0
expanded_examples = benchmark.examples.copy()
expanded_examples.append({
    'input': 'What payment methods do you accept?',
    'expected_output': 'We accept credit cards, PayPal, and bank transfers.',
    'category': 'product_info',
    'difficulty': 'easy',
    'metadata': {}
})
expanded_examples.append({
    'input': 'Can I change my delivery address after ordering?',
    'expected_output': 'Yes, if the order hasn\'t shipped yet. Please contact us immediately with your order number.',
    'category': 'order_modification',
    'difficulty': 'medium',
    'metadata': {}
})

version_manager.save_version(
    "1.1.0",
    expanded_examples,
    notes="Added payment and order modification examples"
)

# Compare versions
comparison = version_manager.compare_versions("1.0.0", "1.1.0")
print(f"\n📊 Comparing versions:")
print(f"  {comparison['v1']}: {comparison['v1_size']} examples")
print(f"  {comparison['v2']}: {comparison['v2_size']} examples")
print(f"  Change: +{comparison['size_change']} examples")

# ============================================================================
# PART 6: DOCUMENTATION BEST PRACTICES
# ============================================================================

print("\n\n" + "="*80)
print("PART 6: Documentation Best Practices")
print("="*80)

print("""
📝 BENCHMARK DOCUMENTATION:

Essential information:
1. Purpose & Scope
   - What does this benchmark test?
   - What domains/use cases?

2. Structure
   - Number of examples
   - Categories
   - Difficulty levels

3. Evaluation Criteria
   - How to score responses
   - What makes a good answer
   - Edge case handling

4. Usage Instructions
   - How to load and use
   - Example code
   - Expected format

5. Limitations
   - What's NOT covered
   - Known biases
   - Update frequency

6. Version History
   - Changes over time
   - Migration guides
""")

def generate_benchmark_readme(benchmark: BenchmarkDesigner) -> str:
    """Generate README documentation for benchmark."""

    diversity = benchmark.validate_diversity()

    readme = f"""# {benchmark.name.replace('_', ' ').title()}

## Purpose
Customer support chatbot evaluation benchmark.

## Domain
{benchmark.domain}

## Statistics
- **Total Examples**: {diversity['total_examples']}
- **Categories**: {diversity['num_categories']}
- **Version**: {benchmark.metadata['version']}
- **Created**: {benchmark.metadata['created']}

## Category Distribution
"""
    for cat, count in diversity['category_distribution'].items():
        readme += f"- {cat}: {count} examples\n"

    readme += f"""
## Difficulty Distribution
"""
    for diff, count in diversity['difficulty_distribution'].items():
        readme += f"- {diff}: {count} examples\n"

    readme += """
## Evaluation Criteria

Each example includes:
- `input`: User message
- `expected_output`: Ideal response
- `category`: Type of interaction
- `difficulty`: Easy, medium, or hard
- `metadata`: Additional context

## Usage

```python
import json

with open('customer_support_v1.json') as f:
    benchmark = json.load(f)

for example in benchmark['examples']:
    # Evaluate your model
    response = your_model(example['input'])
    score = evaluate(response, example['expected_output'])
```

## Limitations
- Examples are English only
- Focuses on text-based support
- May not cover all edge cases
- Needs regular updates with new patterns
"""

    return readme

readme_content = generate_benchmark_readme(benchmark)
print("\n📄 Generated README.md:")
print(readme_content)

# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

print("\n\n" + "="*80)
print("KEY TAKEAWAYS")
print("="*80)

print("""
✅ BENCHMARK CREATION CHECKLIST:

1. Define clear objectives
2. Gather diverse examples
3. Balance difficulty levels
4. Include edge cases
5. Validate quality
6. Document thoroughly
7. Version everything
8. Maintain regularly

🎯 QUALITY CRITERIA:

✓ Representative of real use
✓ Diverse coverage
✓ Balanced distribution
✓ No duplicates
✓ Complete metadata
✓ Clear evaluation criteria
✓ Well documented
✓ Versioned properly

⚠️  COMMON MISTAKES:

✗ Too small sample size
✗ Skewed toward easy cases
✗ Missing edge cases
✗ Poor documentation
✗ No versioning
✗ Stale examples
✗ Unclear evaluation criteria

💡 REMEMBER:

"A benchmark is only as good as its design and maintenance.
 Invest time in curation—it pays dividends in evaluation quality."

🔄 MAINTENANCE SCHEDULE:

- Quarterly: Review and update
- When models change: Revalidate
- New patterns emerge: Add examples
- Errors found: Fix and version

Next: 12_advanced_rag_patterns.py - Advanced RAG evaluation!
""")

print("\n" + "="*80)
print("✨ Lesson 11 Complete!")
print("="*80)
print("\nNext: Run 12_advanced_rag_patterns.py")
