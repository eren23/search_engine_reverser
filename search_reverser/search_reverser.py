import time
from typing import Dict, List, Any
from .analyzers import ResultAnalyzer
from .collectors import DataCollector
from .utils import measure_timing
from .adaptive import AdaptiveQueryStrategy


class SearchReverseEngineer:
    def __init__(self):
        self.results_database = {}
        self.analyzer = ResultAnalyzer()
        self.collector = DataCollector()
        self.adaptive_strategy = AdaptiveQueryStrategy()

    def collect_sample(self, query: str, results: List[Any]) -> Dict:
        """Store and analyze a search query and its results"""
        analysis = {
            "results": results,
            "timestamp": time.time(),
            "characteristics": self.analyzer.analyze_results(results),
            "timing": measure_timing(lambda: results),  # Measure response time
        }
        self.results_database[query] = analysis
        return analysis

    def run_test_suite(self, target_url: str) -> Dict:
        """Run an adaptive test suite against a search endpoint"""
        results = {}

        # Initial exploration phase
        test_cases = self.adaptive_strategy.generate_next_queries({})

        for test in test_cases:
            query = test["query"]
            search_results = self.collector.perform_search(target_url, query)
            results[query] = self.collect_sample(query, search_results)

            # Update adaptive strategy with results
            self.adaptive_strategy.analyze_response(query, search_results)

            # Generate next batch of queries based on learning
            next_queries = self.adaptive_strategy.generate_next_queries(results)
            if next_queries:
                for test in next_queries:
                    query = test["query"]
                    search_results = self.collector.perform_search(target_url, query)
                    results[query] = self.collect_sample(query, search_results)
                    self.adaptive_strategy.analyze_response(query, search_results)

        return {**self.generate_hypothesis(results), "learning_status": self.adaptive_strategy.get_learning_status()}

    def generate_hypothesis(self, results: Dict) -> Dict:
        """Generate hypothesis about the search algorithm based on collected data"""
        return {
            "likely_algorithm": self.analyzer.determine_algorithm_type(results),
            "confidence_score": self.analyzer.calculate_confidence(results),
            "observed_patterns": self.analyzer.analyze_patterns(results),
        }
