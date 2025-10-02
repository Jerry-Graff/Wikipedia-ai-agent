import os
from datetime import datetime
import re


class FileService:
    def __init__(self, output_dir: str = "Research_output"):
        self.output_dir = output_dir
        self._ensure_directory_exists()

    def _ensure_directory_exists(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f" 📂 Created directory: {self.output_dir}")

    def _create_filename(self, query: str) -> str:
        """Create a filename based on user query"""
        filename = query.lower()
        filename = re.sub(r'[^a-z0-9\s]', '', filename)
        filename = filename.replace(' ', '-')
        filename = re.sub(r'-+', '-', filename)
        filename = filename[:50].strip('-')
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        return f"{filename}-{timestamp}.txt"

    def _convert_markdown_to_text(self, markdown_text: str) -> str:
        """
        Convert markdown formating to plain text for readbility.
        Removes # headers **bold, etc - keeps structure.
        """
        text = markdown_text
        lines = text.split('\n')
        formatted_lines = []

        for line in lines:
            # H1 headers (#)
            if line.startswith('# '):
                title = line.lstrip('# ').strip()
                formatted_lines.append('\n' + '='*80)
                formatted_lines.append(title.upper())
                formatted_lines.append('='*80)

            # H2 headers (## )
            elif line.startswith('## '):
                title = line.lstrip('# ').strip()
                formatted_lines.append('\n' + title.upper())
                formatted_lines.append('-'*len(title))

            # H3 headers (### )
            elif line.startswith('### '):
                title = line.lstrip('# ').strip()
                formatted_lines.append('\n' + title)
                formatted_lines.append('~'*len(title))

            else:
                # Remove bold/italic markdown
                line = line.replace('**', '').replace('__', '')
                line = line.replace('*', '').replace('_', '')
                formatted_lines.append(line)

        return '\n'.join(formatted_lines)
