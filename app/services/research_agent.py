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
            page = wikipedia.page(title)
            return {
                "title": page.title,
                "content": page.content,
                "url": page.url,
                "word_count": len(page.content.split())
            }
        except wikipedia.exceptions.DisambiguationError as e:
            # If ambiguous, try first option
            print(f"⚠️ Disambiguation for '{title}', trying: {e.options[0]}")
            return self.get_full_article_content(e.options[0])
        except wikipedia.exceptions.PageError:
            print(f"⚠️ Page not found: '{title}'")
            return None
        except Exception as e:
            print(f"⚠️ Error getting article '{title}': {e}")
            return None

    def conduct_research(self, user_query: str, num_searches: int = 3) -> Dict:
        """
        Main research workflow:
        1. Generate search queries
        2. Get summaries for all results
        3. Use Claude to pick most relevant articles
        4. Only get full content for relevant ones

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

        # Step 2: Get summaries of potential candiates
        print("\n📝 Step 2: Getting article summaries...")
        candidate_articles = []

        for query in search_queries:
            print(f"    Searching for: {query}")
            titles = self.wiki.search_titles(query, max_results=3)

            for title in titles:
                summary = self.wiki.get_page_summary(title, sentences=3)
                if summary:
                    candidate_articles.append({
                        "title": title,
                        "summary": summary,
                        "url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
                    })
                    print(f"  ✓ {title}")

        print(f"\nFound {len(candidate_articles)} candidate articles")

        # Step 3: Use Claude to filter out relevant articles
        print("\n🤖 Step 3: Claude filtering for relevance...")
        relevant_titles = self.claude.filter_relevant_articles(
            user_query=user_query,
            candidate_articles=candidate_articles
        )
        print(f"Claude selected {len(relevant_titles)} relevant articles.")

        # Step 4: Get full content of relevant articles
        print("\n📖 Step 4: Retrieving full content for relevant articles...")
        final_articles = []

        for title in relevant_titles:
            article = self.get_full_article_content(title)
            if article:
                print(f"  ✓ Retrieved full content: {article['title']} ({article['word_count']} words)")
                final_articles.append(article)

        print(f"\n✅ Research complete! {len(final_articles)} articles ready for synthesis")

        # After Step 4, add Step 5:
        print("\n✍️ Step 5: Synthesizing research document with Claude...")
        research_document = self.claude.synthesize_research(
            user_query=user_query,
            articles=final_articles
        )
        print("✅ Document synthesis complete!")

        return {
            "user_query": user_query,
            "search_queries": search_queries,
            "articles": final_articles,
            "total_articles": len(final_articles),
            "total_words": sum(a['word_count'] for a in final_articles),
            "candidates_considered": len(candidate_articles),
            "research_document": research_document
        }
