import os
from pathlib import Path

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-5.1" 

# ---------------- OUTPUT ----------------
# All workflow outputs saved to project_root/dataset/
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = str(PROJECT_ROOT / "dataset")


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
        "view_options": 'button:has-text("Display"), button:has-text("View")',
        "new_issue_button": 'button[aria-label*="new issue"]',
        "issue_title_input": '[contenteditable="true"]',
        "create_issue_button": 'button:has-text("Create issue")'
    },
    "keyboard_shortcuts": {
        "new_issue": "c",
        "search": "/",
        "command_menu": "Meta+k"
    },
    "notes": "Linear create issue: Press 'c' key → opens dialog (non-URL modal) → Title input is [contenteditable], NOT <input>! → Click 'Create issue' button. Button is button[aria-label*='new issue'] (lowercase!)."
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
    "auth_required": False,
    "common_selectors": {
        "search_box": 'input[name="q"], input[placeholder*="Search"]',
        "search_button": 'button[type="submit"]',
        "repo_link": 'a[data-testid="repository-name"], a.v-align-middle',
        "filter_repos": 'a[href*="type=repositories"]',
        "repo_list": 'div[data-testid="results-list"]',
        "issues_tab": 'a:has-text("Issues"), a[data-tab-item="issues"]',
        "trending_link": 'a[href="/trending"]',
        "navigation": 'nav, header',
        "create_button": '[aria-label="Create something new"]',
        "new_repo_link": 'a:has-text("New repository")',
        "repo_name_input": 'input#repository_name',
        "repo_description": 'input#repository_description',
        "create_repo_button": 'button[type="submit"]'
    },
    "keyboard_shortcuts": {
        "search": "/"
    },
    "notes": "GitHub has create menus, repository forms, search, and navigation."
}