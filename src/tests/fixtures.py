"""Test fixtures for the research system"""

MOCK_SEARCH_RESULTS = [
    {"link": "https://example.com/1", "title": "Python Basics", "snippet": "Learn Python"},
    {"link": "https://example.com/2", "title": "Advanced Python", "snippet": "Master Python"}
]

MOCK_HTML_CONTENT = """
<html>
<body>
<h1>Python Programming</h1>
<p>Python is a great language.</p>
</body>
</html>
"""

MOCK_OPENAI_RESPONSES = {
    "supervisor": "Test research plan",
    "synthesis": "Test synthesis",
    "content": "Test content",
    "summary": "Test summary"
}
