import json
import random
from typing import List, Dict
from datetime import datetime, timedelta

# Constants for generating realistic data
GENRES = [
    "Programming",
    "Data Science",
    "Web Development",
    "Machine Learning",
    "Artificial Intelligence",
    "DevOps",
    "Security",
    "Mobile Development",
    "Game Development",
    "Database Design",
]

TOPICS = [
    "Python",
    "JavaScript",
    "Java",
    "C++",
    "Go",
    "Rust",
    "SQL",
    "NoSQL",
    "React",
    "Angular",
    "Vue",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "TensorFlow",
    "PyTorch",
    "scikit-learn",
    "pandas",
    "numpy",
]

ADJECTIVES = [
    "Advanced",
    "Beginning",
    "Professional",
    "Expert",
    "Complete",
    "Modern",
    "Practical",
    "Essential",
    "Fundamental",
    "Comprehensive",
    "Quick",
    "Deep",
]


def generate_book_data(num_books: int = 1000) -> List[Dict]:
    """Generate fake book data"""
    books = []
    current_date = datetime.now()

    for id in range(1, num_books + 1):
        # Generate basic book info
        topic = random.choice(TOPICS)
        genre = random.choice(GENRES)
        adjective = random.choice(ADJECTIVES)

        # Create title variations
        title_formats = [
            f"{adjective} {topic}",
            f"{topic} {genre}",
            f"{adjective} {genre} with {topic}",
            f"{topic}: A {adjective} Guide",
            f"Learning {topic}",
            f"{topic} in Practice",
        ]

        title = random.choice(title_formats)

        # Generate publication date
        pub_date = (current_date - timedelta(days=random.randint(0, 1825))).strftime("%Y-%m-%d")

        # Generate content description
        content_templates = [
            f"A comprehensive guide to {topic} focusing on {genre} applications.",
            f"Learn {topic} through practical examples in {genre}.",
            f"Master {topic} with this {adjective.lower()} guide to {genre}.",
            f"Everything you need to know about {topic} in {genre}.",
            f"From beginner to expert in {topic} with focus on {genre}.",
        ]

        content = random.choice(content_templates)

        # Generate popularity metrics
        popularity = {"ratings_count": random.randint(0, 1000), "average_rating": round(random.uniform(3.0, 5.0), 1), "sales_rank": random.randint(1, 10000)}

        # Create book entry
        book = {
            "id": id,
            "title": title,
            "genre": genre,
            "topics": [topic] + random.sample(TOPICS, k=random.randint(0, 3)),
            "content": content,
            "publication_date": pub_date,
            "popularity": popularity,
            "price": round(random.uniform(9.99, 99.99), 2),
            "in_stock": random.choice([True, True, True, False]),  # 75% chance of being in stock
        }

        books.append(book)

    return books


def save_mock_data(books: List[Dict], filename: str = "mock_data.json") -> None:
    """Save generated data to JSON file"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"books": books}, f, indent=2)


def main():
    print("Generating mock book data...")
    books = generate_book_data(1000)  # Generate 1000 books
    save_mock_data(books)
    print(f"Generated {len(books)} books and saved to mock_data.json")

    # Print a sample book
    print("\nSample book entry:")
    print(json.dumps(books[0], indent=2))


if __name__ == "__main__":
    main()
