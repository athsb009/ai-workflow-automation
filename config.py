import os

# ---------------- SECURITY ----------------
# export OPENAI_API_KEY="sk-..." in your terminal
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-5.1" # Use gpt-4o or gpt-4-turbo

# ---------------- OUTPUT ----------------
OUTPUT_DIR = "outputs"

# ---------------- APP CONTEXTS ----------------
# This is the "knowledge" Agent B needs about specific apps
LINEAR_CONTEXT = {
    "base_url": "https://linear.app",
    "auth_required": True,
    "common_selectors": {
        "issues_link": 'a:has-text("Issues"), a[href*="/issues"]',
        "my_issues": 'a:has-text("My Issues"), button:has-text("My Issues")',
        "projects_link": 'a:has-text("Projects"), button:has-text("Projects")',
        "sidebar": 'nav, [role="navigation"]',
        "issue_list": '[role="list"], .issue-list',
        "filter": 'button:has-text("Filter"), [aria-label*="filter"]',
        "view_options": 'button:has-text("Display"), button:has-text("View")'
    },
    "keyboard_shortcuts": {
        "search": "/",
        "command_menu": "Meta+k"
    },
    "notes": "Linear navigation tasks capture sidebar interactions, view changes, and filter states (non-URL)."
}

NOTION_CONTEXT = {
    "base_url": "https://notion.so",
    "auth_required": True,
    "common_selectors": {
        "new_page": 'text=/new page/i',
        "search": 'input[type="text"]',
        "page_title": '[contenteditable="true"]',
        "sidebar": 'nav, [role="navigation"]'
    },
    "notes": "Notion uses keyboard shortcuts extensively. Cmd+N for new page, Cmd+K for search."
}

WIKIPEDIA_CONTEXT = {
    "base_url": "https://en.wikipedia.org",
    "auth_required": False,
    "common_selectors": {
        "search_box": 'input[name="search"]',
        "search_button": 'button[type="submit"]',
        "article_link": 'a[href*="/wiki/"]',
        "article_title": 'h1#firstHeading',
        "suggestions": '.suggestions-dropdown'
    },
    "notes": "Wikipedia has stable selectors. Search opens suggestions dropdown (non-URL state)."
}

GOOGLE_CONTEXT = {
    "base_url": "https://google.com",
    "auth_required": False,
    "common_selectors": {
        "search_box": 'textarea[name="q"], input[name="q"]',
        "search_button": 'input[type="submit"][name="btnK"]',
        "result_link": 'a h3'
    }
}

YOUTUBE_CONTEXT = {
    "base_url": "https://youtube.com",
    "auth_required": False,
    "common_selectors": {
        "search_box": 'input#search, input[name="search_query"]',
        "search_button": 'button#search-icon-legacy, button[aria-label="Search"]',
        "video_link": 'a#video-title, a.yt-simple-endpoint',
        "video_thumbnail": 'ytd-thumbnail',
        "search_results": 'ytd-video-renderer',
        "trending_link": 'a[title="Trending"], a:has-text("Trending")',
        "subscriptions_link": 'a[title="Subscriptions"], a:has-text("Subscriptions")',
        "sidebar": 'ytd-guide-renderer, #guide'
    },
    "notes": "YouTube navigation tasks demonstrate sidebar menus, tabs, and page transitions."
}

GITHUB_CONTEXT = {
    "base_url": "https://github.com",
    "auth_required": False,  # Public features work without login
    "common_selectors": {
        "search_box": 'input[name="q"], input[placeholder*="Search"]',
        "search_button": 'button[type="submit"]',
        "repo_link": 'a[data-testid="repository-name"], a.v-align-middle',
        "filter_repos": 'a[href*="type=repositories"]',
        "repo_list": 'div[data-testid="results-list"]',
        "issues_tab": 'a:has-text("Issues"), a[data-tab-item="issues"]',
        "trending_link": 'a[href="/trending"]',
        "navigation": 'nav, header'
    },
    "keyboard_shortcuts": {
        "search": "/"
    },
    "notes": "GitHub navigation tasks capture tabs, filters, and page transitions (non-URL states)."
}