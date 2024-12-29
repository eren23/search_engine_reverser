import logging
from pathlib import Path
from typing import List, Dict
from search_reverser import SearchReverseEngineer
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_server_connection(url: str) -> bool:
    """Test if the server is accessible"""
    try:
        response = requests.get(url.rsplit("/search", 1)[0])
        response.raise_for_status()
        logger.info("Server connection test successful")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Cannot connect to server: {e}")
        return False


def analyze_search_behavior(reverser: SearchReverseEngineer, results: Dict) -> Dict:
    """Analyze specific search engine behaviors"""
    behaviors = {
        "case_sensitive": False,
        "uses_fuzzy_matching": False,
        "removes_stop_words": False,
        "considers_word_order": False,
        "boosts_by_popularity": False,
        "considers_recency": False,
    }

    # Analyze learning status
    learning_status = results.get("learning_status", {})
    learned_patterns = learning_status.get("learned_patterns", {})

    # Update behavior analysis based on learned patterns
    if learned_patterns:
        behaviors["uses_fuzzy_matching"] = any(pattern == "fuzzy" for pattern in results.get("success_rates", {}))
        behaviors["removes_stop_words"] = "stop_words" in learned_patterns.get("ineffective_terms", set())
        behaviors["considers_word_order"] = learning_status.get("phase") == "optimization"

    return behaviors


def print_analysis_report(results: Dict, behaviors: Dict) -> None:
    """Print a detailed analysis report"""
    print("\nSearch Algorithm Analysis Report")
    print("=" * 40)

    # Print learning status
    learning_status = results.get("learning_status", {})
    print(f"\nLearning Phase: {learning_status.get('phase', 'unknown')}")
    print(f"Exploration Progress: {learning_status.get('exploration_progress', 'N/A')}")

    # Print detected behaviors
    print("\nDetected Behaviors:")
    for behavior, detected in behaviors.items():
        print(f"- {behavior.replace('_', ' ').title()}: {'Yes' if detected else 'No'}")

    # Print learned patterns
    print("\nLearned Patterns:")
    learned_patterns = learning_status.get("learned_patterns", {})
    for pattern, value in learned_patterns.items():
        print(f"- {pattern}: {value}")

    # Print success rates
    print("\nQuery Success Rates:")
    success_rates = learning_status.get("success_rates", {})
    for query_type, stats in success_rates.items():
        success_rate = stats["success"] / max(stats["total"], 1) * 100
        print(f"- {query_type}: {success_rate:.1f}% ({stats['success']}/{stats['total']})")


def main():
    # Initialize the reverse engineer
    reverser = SearchReverseEngineer()

    # Point to our mock search endpoint
    target_url = "http://localhost:8000/search"

    # Test server connection first
    if not test_server_connection(target_url):
        logger.error("Cannot proceed with analysis - server not accessible")
        return

    logger.info("Starting comprehensive search algorithm analysis...")

    # Run the adaptive test suite
    results = reverser.run_test_suite(target_url)

    # Analyze behaviors based on results
    behaviors = analyze_search_behavior(reverser, results)

    # Print detailed report
    print_analysis_report(results, behaviors)


if __name__ == "__main__":
    main()
