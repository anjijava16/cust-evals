"""
Custom Text Evaluation Framework
Compares model outputs against ground truth using multiple metrics
"""

from typing import List, Dict, Any, Callable
import re
from difflib import SequenceMatcher
from collections import Counter
import json


class TextEvaluator:
    """
    A flexible evaluation framework for comparing text outputs against ground truth.
    Supports multiple evaluation metrics and custom scoring functions.
    """
    
    def __init__(self):
        self.results = []
        self.metrics = {
            'exact_match': self._exact_match,
            'case_insensitive_match': self._case_insensitive_match,
            'normalized_match': self._normalized_match,
            'sequence_similarity': self._sequence_similarity,
            'word_overlap': self._word_overlap,
            'contains_match': self._contains_match,
            'length_similarity': self._length_similarity,
        }
    
    def _exact_match(self, output: str, ground_truth: str) -> Dict[str, Any]:
        """Exact string matching"""
        match = output == ground_truth
        return {
            'score': 1.0 if match else 0.0,
            'passed': match,
            'details': 'Exact match' if match else 'Strings differ'
        }
    
    def _case_insensitive_match(self, output: str, ground_truth: str) -> Dict[str, Any]:
        """Case-insensitive matching"""
        match = output.lower() == ground_truth.lower()
        return {
            'score': 1.0 if match else 0.0,
            'passed': match,
            'details': 'Case-insensitive match' if match else 'Strings differ (ignoring case)'
        }
    
    def _normalized_match(self, output: str, ground_truth: str) -> Dict[str, Any]:
        """Normalized matching (lowercase, stripped, whitespace normalized)"""
        def normalize(text):
            text = text.lower().strip()
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'[^\w\s]', '', text)
            return text
        
        normalized_output = normalize(output)
        normalized_gt = normalize(ground_truth)
        match = normalized_output == normalized_gt
        
        return {
            'score': 1.0 if match else 0.0,
            'passed': match,
            'details': f'Normalized: "{normalized_output}" vs "{normalized_gt}"'
        }
    
    def _sequence_similarity(self, output: str, ground_truth: str) -> Dict[str, Any]:
        """Calculate sequence similarity ratio (0.0 to 1.0)"""
        ratio = SequenceMatcher(None, output, ground_truth).ratio()
        return {
            'score': ratio,
            'passed': ratio >= 0.8,  # 80% similarity threshold
            'details': f'Similarity: {ratio:.2%}'
        }
    
    def _word_overlap(self, output: str, ground_truth: str) -> Dict[str, Any]:
        """Calculate word-level overlap (Jaccard similarity)"""
        def get_words(text):
            return set(re.findall(r'\w+', text.lower()))
        
        output_words = get_words(output)
        gt_words = get_words(ground_truth)
        
        if not output_words and not gt_words:
            score = 1.0
        elif not output_words or not gt_words:
            score = 0.0
        else:
            intersection = len(output_words & gt_words)
            union = len(output_words | gt_words)
            score = intersection / union if union > 0 else 0.0
        
        return {
            'score': score,
            'passed': score >= 0.7,  # 70% word overlap threshold
            'details': f'Word overlap: {score:.2%} ({len(output_words & gt_words)}/{len(output_words | gt_words)} words)'
        }
    
    def _contains_match(self, output: str, ground_truth: str) -> Dict[str, Any]:
        """Check if ground truth is contained in output or vice versa"""
        contains = ground_truth.lower() in output.lower() or output.lower() in ground_truth.lower()
        return {
            'score': 1.0 if contains else 0.0,
            'passed': contains,
            'details': 'One text contains the other' if contains else 'No containment'
        }
    
    def _length_similarity(self, output: str, ground_truth: str) -> Dict[str, Any]:
        """Compare text lengths"""
        len_output = len(output)
        len_gt = len(ground_truth)
        
        if len_gt == 0:
            score = 1.0 if len_output == 0 else 0.0
        else:
            ratio = min(len_output, len_gt) / max(len_output, len_gt)
            score = ratio
        
        return {
            'score': score,
            'passed': score >= 0.8,
            'details': f'Length ratio: {score:.2%} ({len_output} vs {len_gt} chars)'
        }
    
    def add_custom_metric(self, name: str, func: Callable[[str, str], Dict[str, Any]]):
        """
        Add a custom evaluation metric.
        
        Args:
            name: Name of the metric
            func: Function that takes (output, ground_truth) and returns dict with 'score', 'passed', 'details'
        """
        self.metrics[name] = func
    
    def evaluate_single(self, 
                       input_text: str,
                       output: str, 
                       ground_truth: str,
                       metrics: List[str] = None,
                       metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate a single output against ground truth.
        
        Args:
            input_text: The input that generated the output
            output: Model/system output
            ground_truth: Expected/correct output
            metrics: List of metric names to use (uses all if None)
            metadata: Additional metadata to store with results
            
        Returns:
            Dictionary containing evaluation results
        """
        if metrics is None:
            metrics = list(self.metrics.keys())
        
        result = {
            'input': input_text,
            'output': output,
            'ground_truth': ground_truth,
            'metadata': metadata or {},
            'metric_results': {},
            'overall_passed': True,
            'overall_score': 0.0
        }
        
        scores = []
        for metric_name in metrics:
            if metric_name not in self.metrics:
                raise ValueError(f"Unknown metric: {metric_name}")
            
            metric_result = self.metrics[metric_name](output, ground_truth)
            result['metric_results'][metric_name] = metric_result
            scores.append(metric_result['score'])
            
            # If any metric fails, overall fails
            if not metric_result['passed']:
                result['overall_passed'] = False
        
        # Average score across all metrics
        result['overall_score'] = sum(scores) / len(scores) if scores else 0.0
        
        return result
    
    def evaluate_batch(self,
                      data: List[Dict[str, str]],
                      metrics: List[str] = None,
                      save_results: bool = True) -> Dict[str, Any]:
        """
        Evaluate multiple examples.
        
        Args:
            data: List of dicts with 'input', 'output', 'ground_truth' (and optional 'metadata')
            metrics: List of metric names to use
            save_results: Whether to save results to self.results
            
        Returns:
            Summary statistics and detailed results
        """
        results = []
        
        for idx, item in enumerate(data):
            result = self.evaluate_single(
                input_text=item.get('input', ''),
                output=item['output'],
                ground_truth=item['ground_truth'],
                metrics=metrics,
                metadata=item.get('metadata', {'index': idx})
            )
            results.append(result)
        
        if save_results:
            self.results.extend(results)
        
        # Calculate summary statistics
        summary = self._calculate_summary(results, metrics or list(self.metrics.keys()))
        
        return {
            'summary': summary,
            'detailed_results': results
        }
    
    def _calculate_summary(self, results: List[Dict], metrics: List[str]) -> Dict[str, Any]:
        """Calculate summary statistics from results"""
        total = len(results)
        passed = sum(1 for r in results if r['overall_passed'])
        
        summary = {
            'total_examples': total,
            'passed': passed,
            'failed': total - passed,
            'pass_rate': passed / total if total > 0 else 0.0,
            'average_score': sum(r['overall_score'] for r in results) / total if total > 0 else 0.0,
            'metric_breakdown': {}
        }
        
        # Per-metric statistics
        for metric in metrics:
            metric_scores = [r['metric_results'][metric]['score'] for r in results if metric in r['metric_results']]
            metric_passed = sum(1 for r in results if metric in r['metric_results'] and r['metric_results'][metric]['passed'])
            
            summary['metric_breakdown'][metric] = {
                'average_score': sum(metric_scores) / len(metric_scores) if metric_scores else 0.0,
                'passed': metric_passed,
                'pass_rate': metric_passed / total if total > 0 else 0.0
            }
        
        return summary
    
    def print_report(self, summary: Dict[str, Any], show_failures_only: bool = False):
        """Print a formatted evaluation report"""
        print("\n" + "="*80)
        print("EVALUATION REPORT")
        print("="*80)
        
        s = summary['summary'] if 'summary' in summary else summary
        
        print(f"\nOverall Statistics:")
        print(f"  Total Examples: {s['total_examples']}")
        print(f"  Passed: {s['passed']} ({s['pass_rate']:.1%})")
        print(f"  Failed: {s['failed']}")
        print(f"  Average Score: {s['average_score']:.3f}")
        
        print(f"\nMetric Breakdown:")
        for metric, stats in s['metric_breakdown'].items():
            print(f"  {metric}:")
            print(f"    Average Score: {stats['average_score']:.3f}")
            print(f"    Pass Rate: {stats['pass_rate']:.1%} ({stats['passed']}/{s['total_examples']})")
        
        if 'detailed_results' in summary and not show_failures_only:
            print("\n" + "-"*80)
            print("DETAILED RESULTS")
            print("-"*80)
            
            for idx, result in enumerate(summary['detailed_results']):
                self._print_single_result(idx, result)
        
        elif 'detailed_results' in summary and show_failures_only:
            failures = [r for r in summary['detailed_results'] if not r['overall_passed']]
            if failures:
                print("\n" + "-"*80)
                print(f"FAILURES ({len(failures)} examples)")
                print("-"*80)
                
                for idx, result in enumerate(failures):
                    self._print_single_result(idx, result)
    
    def _print_single_result(self, idx: int, result: Dict[str, Any]):
        """Print a single evaluation result"""
        status = "✓ PASS" if result['overall_passed'] else "✗ FAIL"
        print(f"\n[Example {idx}] {status} (Score: {result['overall_score']:.3f})")
        print(f"  Input: {result['input'][:100]}{'...' if len(result['input']) > 100 else ''}")
        print(f"  Output: {result['output'][:100]}{'...' if len(result['output']) > 100 else ''}")
        print(f"  Ground Truth: {result['ground_truth'][:100]}{'...' if len(result['ground_truth']) > 100 else ''}")
        
        for metric, metric_result in result['metric_results'].items():
            status_icon = "✓" if metric_result['passed'] else "✗"
            print(f"    {status_icon} {metric}: {metric_result['score']:.3f} - {metric_result['details']}")
    
    def export_results(self, filepath: str, format: str = 'json'):
        """Export evaluation results to file"""
        if format == 'json':
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        print(f"Results exported to {filepath}")


# Example usage and demonstration
if __name__ == "__main__":
    # Create evaluator
    evaluator = TextEvaluator()
    
    # Sample data
    test_data = [
        {
            'input': 'What is the capital of France?',
            'output': 'Paris',
            'ground_truth': 'ParisABC'
        },
        # {
        #     'input': 'What is 2+2?',
        #     'output': 'The answer is 4',
        #     'ground_truth': '4'
        # },
        # {
        #     'input': 'Translate "hello" to Spanish',
        #     'output': 'Hola',
        #     'ground_truth': 'hola'
        # },
        # {
        #     'input': 'Name a primary color',
        #     'output': 'Red is a primary color',
        #     'ground_truth': 'red'
        # },
    ]
    
    # Run evaluation
    results = evaluator.evaluate_batch(test_data)
    
    # Print report
    evaluator.print_report(results)
    
    # Show only failures
    print("\n\n")
    evaluator.print_report(results, show_failures_only=True)