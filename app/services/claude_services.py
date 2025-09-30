import os
from anthropic import Anthropic
from dotenv import load_dotenv
from typing import List

load_dotenv()


class ClaudeService:
    def __init__(self):
        """Initalize Claude API client"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set in .env file")

        self.client = Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"

    def generate_search_queries(self, user_query: str, num_queries: int = 3) -> List[str]:
        """
        Given a user's research question, generate optimal Wikipedia search queries.

        Args:
            user_query: The user's original question
            num_queries: Number of search queries to generate

        Returns:
            List of search query strings
        """

        prompt = f""" Given a user question: "{user_query}".
                    Generate {num_queries} specific Wikipedia search queries that would help answer this question.
                    Be dynamic and creative in your approach, try to think outside of the box whilst providing a grounded clear understanding of the root topic.
                 """

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=5000,
                temperature=0.4,
                messages=[
                    {"role": "user",
                     "content": prompt}
                ],
                system="you are a helpful research assistant"
            )

            response_text = message.content[0].text
            queries = [q.strip() for q in response_text.strip().split('\n') if q.strip()]

            print(f"Generated queries: {queries}")
            return queries

        except Exception as e:
            raise Exception(f"Failed to generate search queries: {str(e)}")

    def filter_relevant_articles(self, user_query: str, candidate_articles: list) -> list[str]:
        """
        Given a user query and article summaries, determine which are most relevant.

        Args:
            user_query: The user's research question
            candidate_articles: List of dicts with 'title' and 'summary'

        Returns:
            List of relevant article titles
        """

        # Build the article list for Claude
        articles_text = "\n\n".join([
            f"Title: {article['title']}\nSummary: {article['summary']}"
            for article in candidate_articles
        ])

        prompt = f"""User's research question: "{user_query}"
                    Here are candidate Wikipedia articles:

                    {articles_text}

                    Analyze which articles are MOST relevant to answering the user's question.
                    Return ONLY the titles of relevant articles, one per line.
                    Skip articles that are tangentially related or off-topic.
                    Maximum 5 articles.

                    Return only titles, no explanations."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=300,
                temperature=0.3,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            response_text = message.content[0].text
            relevant_titles = [title.strip() for title in response_text.strip().split('\n') if title.strip()]

            print(f"Filtered to: {relevant_titles}")
            return relevant_titles

        except Exception as e:
            print(f"Filtering failed, using all articles: {e}")
            # Fallback: return first 5
            return [a['title'] for a in candidate_articles[:5]]