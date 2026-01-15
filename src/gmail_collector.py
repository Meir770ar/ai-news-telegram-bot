"""
Gmail Newsletter Collector - Collects AI news from email newsletters
"""
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
from typing import List, Optional
import re
from bs4 import BeautifulSoup


class NewsletterItem:
    """Represents a newsletter item/article"""
    def __init__(self, title: str, url: str, source: str, description: str = "", date: str = ""):
        self.title = title
        self.url = url
        self.source = source
        self.description = description
        self.date = date
        self.score = 100  # High priority for newsletters
        self.is_tool = True  # Newsletters usually feature tools
        self.id = self._generate_id()
    
    def _generate_id(self) -> str:
        return str(hash(self.url + self.title))
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "source": self.source,
            "description": self.description,
            "score": self.score,
            "is_tool": self.is_tool
        }


class GmailNewsletterCollector:
    """Collect AI news from Gmail newsletters"""
    
    # Newsletter senders configuration
    NEWSLETTER_SENDERS = {
        "dharmesh": {
            "name": "Dharmesh (Agent.AI)",
            "search": "dharmesh",
            "priority": 1
        },
        "superhuman": {
            "name": "Superhuman AI",
            "search": "superhuman",
            "priority": 1
        },
        "rundown": {
            "name": "The Rundown AI", 
            "search": "rundown",
            "priority": 1
        },
        "bensbites": {
            "name": "Ben's Bites",
            "search": "bensbites",
            "priority": 1
        },
        "thecode": {
            "name": "The Code by Superhuman",
            "search": "thecode",
            "priority": 2
        }
    }
    
    # Skip these junk titles
    SKIP_TITLES = [
        "upgrade to paid", "subscribe", "read in app", "view in browser",
        "unsubscribe", "manage preferences", "click here", "learn more",
        "read more", "sign up", "join now", "get started", "try free",
        "advertisement", "sponsored", "ad:", "promo", "discount",
        "little video", "video walkthrough", "watch now", "see more"
    ]
    
    def __init__(self, email_address: str, app_password: str):
        self.email = email_address
        self.password = app_password
        self.mail = None
    
    def connect(self) -> bool:
        """Connect to Gmail via IMAP"""
        try:
            self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
            self.mail.login(self.email, self.password)
            return True
        except Exception as e:
            print(f"Gmail connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from Gmail"""
        if self.mail:
            try:
                self.mail.logout()
            except:
                pass
    
    def collect(self, days_back: int = 2, limit_per_source: int = 1) -> List[NewsletterItem]:
        """Collect newsletter items from the last X days"""
        items = []
        
        if not self.connect():
            print("❌ Failed to connect to Gmail")
            return items
        
        try:
            self.mail.select('"[Gmail]/All Mail"')
            date_since = (datetime.now() - timedelta(days=days_back)).strftime("%d-%b-%Y")
            
            print(f"📬 Searching newsletters from {date_since}...")
            
            for sender_key, sender_config in self.NEWSLETTER_SENDERS.items():
                try:
                    search_term = sender_config["search"]
                    status, messages = self.mail.search(
                        None, 
                        f'FROM "{search_term}"', 
                        f'SINCE {date_since}'
                    )
                    
                    if status == "OK" and messages[0]:
                        msg_ids = messages[0].split()
                        print(f"  📧 {sender_config['name']}: {len(msg_ids)} emails")
                        
                        # Get the latest emails
                        for msg_id in msg_ids[-limit_per_source:]:
                            newsletter_items = self._extract_from_email(
                                msg_id, 
                                sender_config['name']
                            )
                            items.extend(newsletter_items)
                    else:
                        print(f"  📧 {sender_config['name']}: No recent emails")
                        
                except Exception as e:
                    print(f"  ❌ Error with {sender_config['name']}: {e}")
            
        except Exception as e:
            print(f"Gmail error: {e}")
        finally:
            self.disconnect()
        
        # Filter out junk items
        items = self._filter_items(items)
        
        print(f"📬 Total newsletter items: {len(items)}")
        return items
    
    def _filter_items(self, items: List[NewsletterItem]) -> List[NewsletterItem]:
        """Filter out junk/irrelevant items"""
        filtered = []
        seen_titles = set()
        
        for item in items:
            title_lower = item.title.lower().strip()
            
            # Skip if title matches skip patterns
            skip = False
            for skip_pattern in self.SKIP_TITLES:
                if skip_pattern in title_lower:
                    skip = True
                    break
            
            if skip:
                continue
            
            # Skip very short titles
            if len(item.title) < 15:
                continue
            
            # Skip if no URL
            if not item.url or not item.url.startswith("http"):
                continue
            
            # Skip duplicates
            if title_lower in seen_titles:
                continue
            seen_titles.add(title_lower)
            
            # Must contain some AI-related keyword or be from trusted source
            ai_keywords = ["ai", "gpt", "claude", "gemini", "llm", "agent", "model", 
                          "openai", "anthropic", "google", "microsoft", "copilot",
                          "chatbot", "automation", "neural", "machine learning"]
            
            has_ai_keyword = any(kw in title_lower or kw in item.description.lower() 
                                for kw in ai_keywords)
            
            # Accept if has AI keyword OR has good description
            if has_ai_keyword or len(item.description) > 50:
                filtered.append(item)
        
        return filtered
    
    def _extract_from_email(self, msg_id: bytes, source_name: str) -> List[NewsletterItem]:
        """Extract news items from a single email"""
        items = []
        
        try:
            status, msg_data = self.mail.fetch(msg_id, '(RFC822)')
            
            if status != "OK":
                return items
            
            msg = email.message_from_bytes(msg_data[0][1])
            
            # Get subject for context
            subject = self._decode_header(msg["Subject"])
            
            # Get email body
            body = self._get_email_body(msg)
            
            if not body:
                return items
            
            # Parse HTML content to find links and news items
            soup = BeautifulSoup(body, 'html.parser')
            
            # Look for article-like structures
            links_found = []
            
            # Method 1: Find links with good text
            for a_tag in soup.find_all('a', href=True):
                href = a_tag.get('href', '')
                text = a_tag.get_text(strip=True)
                
                if self._is_relevant_link(href, text):
                    # Get surrounding context
                    context = self._get_link_context(a_tag)
                    
                    links_found.append({
                        "url": href,
                        "title": text,
                        "context": context
                    })
            
            # Method 2: Look for headings followed by links
            for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'strong', 'b']):
                heading_text = heading.get_text(strip=True)
                
                if len(heading_text) > 20 and len(heading_text) < 200:
                    # Find nearby link
                    link = heading.find('a', href=True) or heading.find_next('a', href=True)
                    
                    if link and self._is_relevant_link(link.get('href', ''), heading_text):
                        context = self._get_link_context(heading)
                        
                        links_found.append({
                            "url": link.get('href', ''),
                            "title": heading_text,
                            "context": context
                        })
            
            # Create items from best links
            seen_urls = set()
            for link in links_found[:8]:  # Top 8 links per email
                url = link["url"]
                
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                
                title = link["title"]
                
                # Clean up title
                title = re.sub(r'\s+', ' ', title).strip()
                
                if len(title) > 15:
                    item = NewsletterItem(
                        title=title[:250],
                        url=url,
                        source=f"Newsletter: {source_name}",
                        description=link["context"][:400]
                    )
                    items.append(item)
        
        except Exception as e:
            print(f"    Error extracting from email: {e}")
        
        return items
    
    def _get_link_context(self, element) -> str:
        """Get text context around a link element"""
        context_parts = []
        
        # Get parent paragraph/div text
        parent = element.parent
        for _ in range(3):  # Go up 3 levels max
            if parent:
                text = parent.get_text(strip=True)
                if len(text) > 50 and len(text) < 500:
                    context_parts.append(text)
                    break
                parent = parent.parent
        
        # Get next sibling text
        next_sib = element.find_next_sibling(string=True)
        if next_sib:
            context_parts.append(str(next_sib).strip())
        
        return ' '.join(context_parts)[:400]
    
    def _decode_header(self, header_value: str) -> str:
        """Decode email header"""
        if not header_value:
            return ""
        
        decoded_parts = decode_header(header_value)
        result = ""
        
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                try:
                    result += part.decode(encoding or 'utf-8')
                except:
                    result += part.decode('utf-8', errors='ignore')
            else:
                result += part
        
        return result.strip()
    
    def _get_email_body(self, msg) -> str:
        """Extract email body (prefer HTML)"""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                
                if content_type == "text/html":
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
                    except:
                        pass
                elif content_type == "text/plain" and not body:
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    except:
                        pass
        else:
            try:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            except:
                pass
        
        return body
    
    def _is_relevant_link(self, url: str, text: str) -> bool:
        """Check if a link is relevant AI news/tool"""
        if not url or not text:
            return False
        
        # Skip common non-content links
        skip_url_patterns = [
            "unsubscribe", "mailto:", "twitter.com/intent", "facebook.com/sharer",
            "linkedin.com/share", "instagram.com", "manage", "preferences",
            "beehiiv.com", "substack.com/subscribe", "joinsuperhuman",
            "mail.", "/settings", "/account", "youtube.com/watch",
            "#", "javascript:", "tel:", "sms:"
        ]
        
        skip_text_patterns = [
            "unsubscribe", "view in browser", "manage preferences",
            "click here", "read more", "learn more", "subscribe",
            "upgrade", "sign up", "join", "download app", "get the app"
        ]
        
        url_lower = url.lower()
        text_lower = text.lower()
        
        for pattern in skip_url_patterns:
            if pattern in url_lower:
                return False
        
        for pattern in skip_text_patterns:
            if text_lower.startswith(pattern) or text_lower == pattern:
                return False
        
        # Must be a real URL
        if not url.startswith("http"):
            return False
        
        # Text should be meaningful
        if len(text) < 15:
            return False
        
        return True


def collect_from_gmail(email_address: str, app_password: str, days_back: int = 2) -> List[NewsletterItem]:
    """Convenience function to collect from Gmail"""
    collector = GmailNewsletterCollector(email_address, app_password)
    return collector.collect(days_back=days_back)
