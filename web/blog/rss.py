import os
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import sys

# Add parent directory to path to allow imports
sys.path.append(os.getcwd())

from web.blog.paths import sorted_posts

def generate_rss_feed():
    """Generate Atom feed for the blog using standard library."""
    
    # Root element
    feed = ET.Element('feed', xmlns='http://www.w3.org/2005/Atom')
    
    # Feed Metadata
    ET.SubElement(feed, 'title').text = 'Blog de Seraph/Lille'
    
    link_self = ET.SubElement(feed, 'link')
    link_self.set('href', 'https://blog.seraph.to/feeds/all.atom.xml')
    link_self.set('rel', 'self')
    
    link_alt = ET.SubElement(feed, 'link')
    link_alt.set('href', 'https://blog.seraph.to')
    link_alt.set('rel', 'alternate')
    
    ET.SubElement(feed, 'id').text = 'https://blog.seraph.to/'
    
    # Updated time (use latest post or now)
    updated_time = datetime.now(timezone.utc)
    if sorted_posts:
        latest_post = sorted_posts[0]
        if latest_post.date.tzinfo is None:
             updated_time = latest_post.date.replace(tzinfo=timezone.utc)
        else:
             updated_time = latest_post.date
    
    ET.SubElement(feed, 'updated').text = updated_time.isoformat()
    
    author = ET.SubElement(feed, 'author')
    ET.SubElement(author, 'name').text = 'Ernesto Crespo'
    ET.SubElement(author, 'email').text = 'ecrespo@gmail.com'

    # Entries
    for post in sorted_posts:
        entry = ET.SubElement(feed, 'entry')
        
        ET.SubElement(entry, 'title').text = post.title
        
        post_url = f"https://blog.seraph.to/blog/{post.slug}"
        link = ET.SubElement(entry, 'link')
        link.set('href', post_url)
        
        ET.SubElement(entry, 'id').text = post_url
        
        dt = post.date
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
            
        ET.SubElement(entry, 'published').text = dt.isoformat()
        ET.SubElement(entry, 'updated').text = dt.isoformat()
        
        ET.SubElement(entry, 'summary').text = post.summary
        
        author_entry = ET.SubElement(entry, 'author')
        ET.SubElement(author_entry, 'name').text = post.author
        
        if post.category:
             cat = ET.SubElement(entry, 'category')
             cat.set('term', post.category)
             
        for tag in post.tags:
             t_elem = ET.SubElement(entry, 'category')
             t_elem.set('term', tag)

    # Convert to string and write
    xml_str = ET.tostring(feed, encoding='utf-8', method='xml')
    
    # Ensure assets directory exists
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        
    output_path = os.path.join(assets_dir, 'feed.xml')
    
    with open(output_path, 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
        f.write(xml_str)
        
    print(f"Atom feed generated successfully at {output_path}")

if __name__ == "__main__":
    generate_rss_feed()
