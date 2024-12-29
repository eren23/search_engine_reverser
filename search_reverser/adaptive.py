from typing import Dict, List, Any
from collections import defaultdict
import random


class AdaptiveQueryStrategy:
    def __init__(self):
        self.query_success_rates = defaultdict(lambda: {"success": 0, "total": 0})
        self.learned_patterns = {
            "effective_terms": set(),
            "ineffective_terms": set(),
            "optimal_query_length": 0,
            "best_performing_categories": [],
            "successful_domains": set(),
            "successful_patterns": [],
        }
        self.current_phase = "domain_exploration"
        self.exploration_rounds = 0
        self.max_exploration_rounds = 3

        # Define broader initial domains and specific sub-domains
        self.domains = {
            # Academic/Educational
            "general_academic": ["education", "learning", "study", "course", "tutorial", "guide", "introduction"],
            "science": ["research", "experiment", "theory", "analysis", "methodology", "scientific"],
            "mathematics": ["math", "calculus", "algebra", "statistics", "probability", "equations"],
            # Technology
            "general_tech": ["technology", "digital", "computer", "software", "hardware", "system", "platform"],
            "programming": ["coding", "development", "software", "algorithm", "debugging", "implementation"],
            "languages": ["python", "javascript", "java", "cpp", "rust", "golang", "ruby", "php"],
            "web_dev": ["frontend", "backend", "fullstack", "web", "html", "css", "api", "rest"],
            "data_science": ["analytics", "machine learning", "data mining", "big data", "visualization", "prediction"],
            # Business/Professional
            "business": ["management", "strategy", "planning", "organization", "leadership", "innovation"],
            "marketing": ["advertising", "branding", "marketing", "social media", "content", "seo"],
            "finance": ["investment", "trading", "economics", "financial", "accounting", "market"],
            # Creative
            "design": ["design", "creative", "art", "visual", "graphic", "typography", "layout"],
            "media": ["video", "audio", "multimedia", "animation", "production", "editing"],
            "writing": ["content", "documentation", "technical writing", "blogging", "copywriting"],
            # Industry
            "engineering": ["mechanical", "electrical", "civil", "chemical", "industrial", "engineering"],
            "healthcare": ["medical", "health", "clinical", "patient", "diagnosis", "treatment"],
            "manufacturing": ["production", "assembly", "quality", "automation", "industrial", "process"],
        }

        # Enhanced query patterns
        self.query_patterns = {
            # Basic patterns
            "simple": lambda term: term,
            "quoted": lambda term: f'"{term}"',
            # Compound patterns
            "and_combo": lambda term: f"{term} AND {random.choice(['guide', 'tutorial', 'introduction'])}",
            "or_combo": lambda term: f"{term} OR {random.choice(['course', 'training', 'learning'])}",
            # Specific patterns
            "beginner": lambda term: f"beginner {term}",
            "advanced": lambda term: f"advanced {term}",
            "learn": lambda term: f"learn {term}",
            # Descriptive patterns
            "with": lambda term: f"{term} with {random.choice(['examples', 'practice', 'exercises'])}",
            "for": lambda term: f"{term} for {random.choice(['beginners', 'professionals', 'students'])}",
            # Topic-specific patterns
            "course": lambda term: f"{term} course",
            "tutorial": lambda term: f"{term} tutorial",
            "guide": lambda term: f"complete {term} guide",
        }

        # Add domain weighting to track success rates by domain
        self.domain_weights = {domain: 1.0 for domain in self.domains.keys()}

    def analyze_response(self, query: str, results: List[Dict]) -> None:
        """Analyze search results and update learning patterns"""
        success = bool(results)
        query_type = self._categorize_query(query)
        domain = self._identify_domain(query)

        # Update success rates
        self.query_success_rates[query_type]["total"] += 1
        if success:
            self.query_success_rates[query_type]["success"] += 1
            self.learned_patterns["successful_domains"].add(domain)

            # Extract successful terms and patterns
            successful_terms = set()
            for result in results:
                title_terms = set(result["title"].lower().split())
                query_terms = set(query.lower().split())
                matching_terms = title_terms & query_terms
                successful_terms.update(matching_terms)

                if result.get("score", 0) > 0.7:
                    successful_terms.update(query_terms)
                    # Track successful query pattern
                    pattern = self._identify_query_pattern(query)
                    if pattern and pattern not in self.learned_patterns["successful_patterns"]:
                        self.learned_patterns["successful_patterns"].append(pattern)

            self.learned_patterns["effective_terms"].update(successful_terms)
            current_length = len(query.split())
            self.learned_patterns["optimal_query_length"] = self.learned_patterns["optimal_query_length"] * 0.8 + current_length * 0.2
        else:
            terms = query.split()
            clean_terms = [term for term in terms if term.isalnum() and term.lower() not in {"and", "or", "not"}]
            self.learned_patterns["ineffective_terms"].update(clean_terms)
            self.learned_patterns["ineffective_terms"] -= self.learned_patterns["effective_terms"]

        if success and query_type not in self.learned_patterns["best_performing_categories"]:
            self.learned_patterns["best_performing_categories"].append(query_type)

        # Update domain weights based on success
        if success:
            self.domain_weights[domain] = min(2.0, self.domain_weights[domain] * 1.2)
        else:
            self.domain_weights[domain] = max(0.1, self.domain_weights[domain] * 0.8)

    def generate_next_queries(self, previous_results: Dict[str, Any]) -> List[Dict]:
        """Generate next set of queries based on learned patterns"""
        if self.current_phase == "domain_exploration":
            queries = self._generate_domain_exploration_queries()
            self.exploration_rounds += 1
            if self.exploration_rounds >= self.max_exploration_rounds:
                self.current_phase = "pattern_exploration"
        elif self.current_phase == "pattern_exploration":
            queries = self._generate_pattern_exploration_queries()
            self.exploration_rounds += 1
            if self.exploration_rounds >= self.max_exploration_rounds * 2:
                self.current_phase = "optimization"
        else:
            queries = self._generate_optimized_queries()
        return queries

    def _generate_domain_exploration_queries(self) -> List[Dict]:
        """Generate queries to explore different domains with weighted selection"""
        queries = []
        # Sort domains by weight for prioritization
        weighted_domains = sorted(self.domain_weights.items(), key=lambda x: x[1], reverse=True)

        # Select domains with preference for higher weights
        selected_domains = []
        for domain, weight in weighted_domains:
            if random.random() < weight:
                selected_domains.append(domain)
                if len(selected_domains) >= 3:  # Limit to 3 domains per round
                    break

        # If we haven't selected enough domains, add some randomly
        while len(selected_domains) < 3:
            domain = random.choice(list(self.domains.keys()))
            if domain not in selected_domains:
                selected_domains.append(domain)

        # Generate queries for selected domains
        for domain in selected_domains:
            terms = self.domains[domain]
            term = random.choice(terms)
            queries.append({"query": term, "type": "domain_exploration", "description": f"Testing {domain} domain", "domain": domain})

        return queries

    def _generate_pattern_exploration_queries(self) -> List[Dict]:
        """Generate queries with different patterns in successful domains"""
        queries = []
        successful_domains = self.learned_patterns["successful_domains"] or set(self.domains.keys())

        for domain in random.sample(list(successful_domains), min(2, len(successful_domains))):
            terms = self.domains[domain]
            term = random.choice(terms)
            pattern_type = random.choice(list(self.query_patterns.keys()))
            pattern_func = self.query_patterns[pattern_type]

            queries.append({"query": pattern_func(term), "type": pattern_type, "description": f"Testing {pattern_type} pattern in {domain}", "domain": domain})
        return queries

    def _generate_optimized_queries(self) -> List[Dict]:
        """Generate optimized queries based on learned patterns"""
        queries = []
        successful_patterns = self.learned_patterns["successful_patterns"] or list(self.query_patterns.keys())
        successful_domains = self.learned_patterns["successful_domains"] or set(self.domains.keys())

        for domain in random.sample(list(successful_domains), min(2, len(successful_domains))):
            pattern_type = random.choice(successful_patterns)
            terms = self.domains[domain]
            term = random.choice(terms)
            pattern_func = self.query_patterns[pattern_type]

            queries.append({"query": pattern_func(term), "type": "optimized", "description": f"Optimized {pattern_type} query for {domain}", "domain": domain})

        return queries

    def _identify_domain(self, query: str) -> str:
        """Identify which domain a query belongs to"""
        query_terms = set(query.lower().split())
        for domain, terms in self.domains.items():
            if query_terms & set(term.lower() for term in terms):
                return domain
        return "general"

    def _identify_query_pattern(self, query: str) -> str:
        """Identify the pattern used in a query"""
        query = query.lower()
        if '"' in query:
            return "phrase"
        if " and " in query:
            return "compound"
        if " or " in query:
            return "broad"
        if query.startswith("advanced "):
            return "specific"
        return "simple"

    def _categorize_query(self, query: str) -> str:
        """Categorize query type"""
        categories = {
            "exact": lambda q: len(q.split()) > 2,
            "partial": lambda q: len(q.split()) == 1,
            "fuzzy": lambda q: any(not c.isalnum() and not c.isspace() for c in q),
            "compound": lambda q: " AND " in q or " OR " in q,
        }

        for category, check in categories.items():
            if check(query):
                return category
        return "general"

    def _update_effective_patterns(self, query: str, results: List[Dict]) -> None:
        """Update patterns based on successful queries"""
        terms = query.split()
        self.learned_patterns["effective_terms"].update(terms)
        self.learned_patterns["optimal_query_length"] = self.learned_patterns["optimal_query_length"] * 0.8 + len(terms) * 0.2

    def _update_ineffective_patterns(self, query: str) -> None:
        """Update patterns based on unsuccessful queries"""
        terms = query.split()
        self.learned_patterns["ineffective_terms"].update(terms)

    def get_learning_status(self) -> Dict:
        """Return current learning status"""
        return {
            "phase": self.current_phase,
            "exploration_progress": f"{self.exploration_rounds}/{self.max_exploration_rounds}",
            "learned_patterns": self.learned_patterns,
            "success_rates": dict(self.query_success_rates),
        }
