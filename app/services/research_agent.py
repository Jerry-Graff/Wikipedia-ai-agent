from app.services.claude_services import ClaudeService
from app.services.wikipedia_services import WikipediaService
from typing import Dict
import wikipedia


class ResearchAgent:
    def __init__(self):
        """Initalize agent with Claude and Wiki services."""
        self.claude = ClaudeService()
        self.wiki = WikipediaService()

    def get_full_article_content(self, title: str) -> Dict[str, str]:
        """
        Get full wikipedia content - not just a summary.

        Args:
            title: Wikipedia page

        Returns:
            Dictionary with title and full content.
        """
        try:
            page = wikipedia.page(title, auto_suggest=False)
            return {
                "title": title,
                "content": page.content,
                "url": page.url,
                "word_count": len(page.content.split())
            }
        except wikipedia.exceptions.DisambiguationError as e:
            # If ambiguous, try first option
            return self.get_full_article_content(e.options[0])
        except wikipedia.exceptions.PageError:
            return None
        except Exception as e:
            print(f"Error getting article {title}: {e}")
            return None

    def conduct_research(self, user_query: str, num_searches: int = 3) -> Dict:
        """
        Main research workflow:
        1. Generate search queries with Claude
        2. Search Wikipedia for each query
        3. Retrieve full article content
        4. Return all gathered information

        Args:
            user_query: The user's research question
            num_searches: Number of Wikipedia searches to perform

        Returns:
            Dictionary containing all research data
        """
        print(f"\n 🔍 Starting research for: {user_query}")

        # Step 1: Generate search queries
        print("\n📋 Step 1: Generating search queries with Claude...")
        search_queries = self.claude.generate_search_queries(user_query, num_queries=num_searches)
        print(f"Generated queries: {search_queries}")

        # Step 2: Search Wikipedia
        print("\n🔎 Step 2: Searching Wikipedia...")
        all_articles = []

        for query in search_queries:
            print(f"    Searching for: {query}")
            titles = self.wiki.search_titles(query, max_results=2)

            for title in titles:
                article = self.get_full_article_content(title)
                if article:
                    print(f"    ✓ Retrieved: {article['title']} ({article['word_count']} words)")
                    all_articles.append(article)

        print(f"\n✅ Research complete! Gathered {len(all_articles)} articles")

        return {
            "user_query": user_query,
            "search_queries": search_queries,
            "articles": all_articles,
            "total_articles": len(all_articles),
            "total_words": sum(word['word_count'] for word in all_articles)
        }
