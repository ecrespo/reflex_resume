
import os
import re
import subprocess
import glob
import sys

# Configuration
CONTENT_DIR = "content/posts"
SLUG_MAP = {}
NORMALIZED_MAP = {}

def get_slug_from_filename(filename):
    """Generate slug from filename similar to the blog module."""
    # Logic matched from web/blog/paths.py
    name = os.path.basename(filename)
    name = re.sub(r'^\d{4,8}-?', '', name)
    name = name.replace('.md', '')
    return name.lower().replace(' ', '-')

def build_slug_map():
    """Map slugs to filenames."""
    print("Building slug map...")
    files = glob.glob(os.path.join(CONTENT_DIR, "*.md"))
    for f in files:
        slug = get_slug_from_filename(f)
        SLUG_MAP[slug] = f
        # Create normalized version (remove hyphens) to match legacy URLs that might have hyphens
        # where the filename doesn't (or vice versa)
        norm_slug = slug.replace('-', '')
        NORMALIZED_MAP[norm_slug] = f
        
    print(f"Mapped {len(SLUG_MAP)} posts.")

def check_url(url):
    """Check if a URL is reachable using curl."""
    try:
        # -I: head only, -L: follow redirects, --fail: fail on error code
        # --max-time 5: 5 seconds timeout
        subprocess.check_call(
            ["curl", "-I", "-L", "--max-time", "5", "--fail", "-s", "-o", "/dev/null", url],
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False
    except Exception as e:
        print(f"Error checking {url}: {e}")
        return False

def process_file(filepath):
    """Process a single markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    # Regex to find links: [text](url)
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    
    def replace_link(match):
        text = match.group(1)
        url = match.group(2)
        
        # 1. Internal Link Fix (seraph.to or blog.crespo.org.ve)
        if "seraph.to" in url or "blog.crespo.org.ve" in url:
            # Clean URL: remove anchor, protocol, domain
            clean_url = url.split('#')[0]
            base = clean_url.split('/')[-1].replace('.html', '')
            
            target_file = None
            if base in SLUG_MAP:
                target_file = SLUG_MAP[base]
            else:
                # Try normalized match
                norm_base = base.replace('-', '')
                if norm_base in NORMALIZED_MAP:
                    target_file = NORMALIZED_MAP[norm_base]
            
            if target_file:
                # Use the slug that the APP expects for this file
                correct_slug = get_slug_from_filename(target_file)
                new_url = f"/blog/{correct_slug}"
                print(f"[{os.path.basename(filepath)}] Replacing internal link: {url} -> {new_url}")
                return f"[{text}]({new_url})"
            else:
                print(f"[{os.path.basename(filepath)}] WARNING: Internal link target not found: {url} (base: {base})")
        
        # 2. External Link Validation
        if url.startswith("http") and "localhost" not in url and "127.0.0.1" not in url:
            # Skip if already marked
            if "(enlace roto)" in text:
                return match.group(0)
                
            print(f"[{os.path.basename(filepath)}] Checking external link: {url}")
            if not check_url(url):
                print(f"[{os.path.basename(filepath)}] BROKEN LINK: {url}")
                return f"[{text} (enlace roto)]({url})"
        
        return match.group(0)

    try:
        new_content = link_pattern.sub(replace_link, content)
    except Exception as e:
        print(f"Error processing regex in {filepath}: {e}")
        return

    if new_content != original_content:
        # Write back (ensure we don't lose data if write fails)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

def main():
    build_slug_map()
    files = glob.glob(os.path.join(CONTENT_DIR, "*.md"))
    
    for f in files:
        process_file(f)

if __name__ == "__main__":
    main()
