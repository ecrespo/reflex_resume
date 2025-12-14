"""Blog data loading module using flexdown."""
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import re

import flexdown
from flexdown.document import Document


# Path to blog posts directory
POSTS_PATH = "content/posts/"
IMAGES_PATH = "content/images/"


def parse_pelican_metadata(content: str) -> tuple[dict, str]:
    """
    Parse Pelican-style metadata from markdown content.
    
    Pelican format uses lines like:
    Title: My Post Title
    Date: 2023-01-01 10:00
    Category: General
    Tags: tag1, tag2
    Authors: Author Name
    Summary: Post summary text
    Slug: post-slug
    
    Returns:
        Tuple of (metadata dict, remaining content)
    """
    lines = content.split('\n')
    metadata = {}
    content_start = 0
    
    # Metadata patterns
    metadata_pattern = re.compile(r'^([A-Za-z_]+):\s*(.+)$')
    
    for i, line in enumerate(lines):
        if line.strip() == '':
            # Empty line marks end of metadata
            content_start = i + 1
            break
        
        match = metadata_pattern.match(line)
        if match:
            key = match.group(1).lower()
            value = match.group(2).strip()
            metadata[key] = value
            content_start = i + 1
        else:
            # Non-metadata line, content starts here
            content_start = i
            break
    
    remaining_content = '\n'.join(lines[content_start:])
    return metadata, remaining_content


def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string to datetime object."""
    formats = [
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d',
        '%Y/%m/%d %H:%M',
        '%Y/%m/%d',
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None


def sanitize_slug(slug: str) -> str:
    """Sanitize slug to only contain valid route characters (a-z, 0-9, _, -)."""
    import unicodedata
    # Normalize unicode and convert to ASCII
    slug = unicodedata.normalize('NFKD', slug).encode('ascii', 'ignore').decode('ascii')
    # Convert to lowercase, replace spaces with hyphens
    slug = slug.lower().replace(' ', '-')
    # Remove any characters that aren't alphanumeric, underscore, or hyphen
    slug = re.sub(r'[^a-z0-9_-]', '', slug)
    # Remove multiple consecutive hyphens
    slug = re.sub(r'-+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug or 'untitled'


class BlogPost:
    """Represents a parsed blog post."""
    
    def __init__(self, filepath: str, metadata: dict, content: str):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.metadata = metadata
        self.content = content
        
        # Extract key fields with defaults
        self.title = metadata.get('title', 'Untitled')
        self.date_str = metadata.get('date', '')
        self.date = parse_date(self.date_str) or datetime.now()
        self.category = metadata.get('category', 'General')
        self.tags = [t.strip() for t in metadata.get('tags', '').split(',') if t.strip()]
        self.author = metadata.get('authors', 'Unknown')
        self.summary = metadata.get('summary', '')
        # Sanitize slug to ensure valid route
        raw_slug = metadata.get('slug', self._generate_slug())
        self.slug = sanitize_slug(raw_slug)
        self.lang = metadata.get('lang', 'es')
        
    def _generate_slug(self) -> str:
        """Generate slug from filename if not provided."""
        # Remove year prefix and .md extension
        name = os.path.basename(self.filepath)
        name = re.sub(r'^\d{4,8}-?', '', name)  # Remove date prefix
        name = name.replace('.md', '')
        return name.lower().replace(' ', '-')
    
    @property
    def formatted_date(self) -> str:
        """Return formatted date string."""
        return self.date.strftime('%B %d, %Y')
    
    def to_dict(self) -> dict:
        """Convert to dictionary for state management."""
        return {
            'title': self.title,
            'date': self.date_str,
            'formatted_date': self.formatted_date,
            'category': self.category,
            'tags': self.tags,
            'author': self.author,
            'summary': self.summary,
            'slug': self.slug,
            'filename': self.filename,
            'content': self.content,
        }


def get_markdown_files(directory: str) -> list[Path]:
    """Get all markdown files in directory."""
    path = Path(directory)
    if not path.exists():
        return []
    return sorted(path.glob('*.md'), reverse=True)


def load_blog_post(filepath: Path) -> Optional[BlogPost]:
    """Load a single blog post from file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        metadata, post_content = parse_pelican_metadata(content)
        
        # Skip files without title (likely not blog posts)
        if not metadata.get('title'):
            return None
            
        return BlogPost(str(filepath), metadata, post_content)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


def get_blog_data() -> Dict[str, BlogPost]:
    """
    Load all blog posts from the posts directory.
    
    Returns:
        Dictionary mapping slug to BlogPost object
    """
    posts = {}
    markdown_files = get_markdown_files(POSTS_PATH)
    
    for filepath in markdown_files:
        post = load_blog_post(filepath)
        if post:
            posts[post.slug] = post
    
    return posts


def get_sorted_posts(posts: Dict[str, BlogPost]) -> list[BlogPost]:
    """Get posts sorted by date descending."""
    return sorted(posts.values(), key=lambda p: p.date, reverse=True)


# Load blog data at module level
blog_data = get_blog_data()
sorted_posts = get_sorted_posts(blog_data)


def get_post_by_slug(slug: str) -> Optional[BlogPost]:
    """Get a specific post by its slug."""
    return blog_data.get(slug)


def get_posts_page(page: int = 1, per_page: int = 10) -> tuple[list[BlogPost], int]:
    """
    Get paginated posts.
    
    Returns:
        Tuple of (posts list, total pages)
    """
    total = len(sorted_posts)
    total_pages = (total + per_page - 1) // per_page
    
    start = (page - 1) * per_page
    end = start + per_page
    
    return sorted_posts[start:end], total_pages
