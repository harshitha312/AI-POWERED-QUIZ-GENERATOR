import wikipedia

def fetch_topic_text(topic, sentences=10):
    try:
        print(f"Fetching Wikipedia content for topic: {topic}")
        page = wikipedia.page(topic)
        content = page.content
        summary = '. '.join(content.split('. ')[:sentences])
        print(f"Fetched content length: {len(summary)} characters")
        return summary
    except Exception as e:
        print(f"Error fetching Wikipedia page for topic '{topic}': {e}")
        return ""
