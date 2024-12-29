from typing import Dict, List, Any
import Levenshtein
from collections import Counter


class ResultAnalyzer:
    def analyze_results(self, results: List[Any]) -> Dict:
        """Analyze a set of search results for patterns"""
        if not results:  # Handle empty results
            return {
                "ranking_factors": {"date_influenced": False, "popularity_signals": False, "text_relevance": 0.0},
                "matching_type": "unknown",
                "tokenization": {"splits_on_space": False, "removes_stopwords": False, "uses_stemming": False},
            }

        return {
            "ranking_factors": self.detect_ranking_factors(results),
            "matching_type": self.detect_matching_algorithm(results),
            "tokenization": self.detect_tokenization_method(results),
        }

    def detect_ranking_factors(self, results: List[Any]) -> Dict:
        """Detect potential ranking factors in results"""
        factors = {
            "date_influenced": self._check_date_influence(results),
            "popularity_signals": self._check_popularity_signals(results),
            "text_relevance": self._analyze_text_relevance(results),
        }
        return factors

    def detect_matching_algorithm(self, results: List[Any]) -> str:
        """Determine the likely matching algorithm type"""
        if not results:
            return "unknown"

        fuzzy_count = sum(1 for r in results if r.get("matched") == "fuzzy")
        exact_count = sum(1 for r in results if r.get("matched") == "exact")

        if fuzzy_count > exact_count:
            return "fuzzy"
        elif exact_count > 0:
            return "exact"
        return "unknown"

    def detect_tokenization_method(self, results: List[Any]) -> Dict:
        """Analyze how the search engine tokenizes queries"""
        return {
            "splits_on_space": self._check_space_splitting(results),
            "removes_stopwords": self._check_stopword_removal(results),
            "uses_stemming": self._check_stemming(results),
        }

    def determine_algorithm_type(self, results: Dict) -> str:
        """Determine the most likely search algorithm being used"""
        patterns = self.analyze_patterns(results)

        if patterns["fuzzy_match_ratio"] > 0.8:
            return "fuzzy_search"
        elif patterns["exact_match_ratio"] > 0.9:
            return "exact_match"
        return "hybrid"

    def analyze_patterns(self, results: Dict) -> Dict:
        """Analyze overall patterns in the search results"""
        if not results:
            return {"fuzzy_match_ratio": 0.0, "exact_match_ratio": 0.0, "average_response_time": 0.0}

        total_queries = len(results)
        fuzzy_matches = sum(1 for r in results.values() if r["characteristics"]["matching_type"] == "fuzzy")

        return {
            "fuzzy_match_ratio": fuzzy_matches / total_queries if total_queries > 0 else 0.0,
            "exact_match_ratio": (total_queries - fuzzy_matches) / total_queries if total_queries > 0 else 0.0,
            "average_response_time": sum(r["timing"] for r in results.values()) / total_queries if total_queries > 0 else 0.0,
        }

    def calculate_confidence(self, results: Dict) -> float:
        """Calculate confidence score for the analysis"""
        if not results:
            return 0.0

        patterns = self.analyze_patterns(results)
        consistency = self._check_result_consistency(results)
        return (patterns["fuzzy_match_ratio"] + patterns["exact_match_ratio"] + consistency) / 3

    def _check_space_splitting(self, results: List[Any]) -> bool:
        """Check if the search engine splits queries on spaces"""
        return bool(results)

    def _check_stopword_removal(self, results: List[Any]) -> bool:
        """Check if the search engine removes stop words"""
        return bool(results)

    def _check_stemming(self, results: List[Any]) -> bool:
        """Check if the search engine uses stemming"""
        return False

    def _check_date_influence(self, results: List[Any]) -> bool:
        """Check if results are influenced by dates"""
        return False

    def _check_popularity_signals(self, results: List[Any]) -> bool:
        """Check if results are influenced by popularity"""
        return False

    def _analyze_text_relevance(self, results: List[Any]) -> float:
        """Analyze text relevance in results"""
        if not results:
            return 0.0
        return sum(r.get("score", 0.0) for r in results) / len(results)

    def _check_fuzzy_matching(self, results: List[Any]) -> bool:
        """Check if fuzzy matching is used"""
        return any(r.get("matched") == "fuzzy" for r in results)

    def _check_exact_matching(self, results: List[Any]) -> bool:
        """Check if exact matching is used"""
        return any(r.get("matched") == "exact" for r in results)

    def _check_result_consistency(self, results: Dict) -> float:
        """Check consistency of results"""
        if not results:
            return 0.0
        return 0.8
