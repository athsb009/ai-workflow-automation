import hashlib
from playwright.sync_api import Page

# The JavaScript that draws the Red Boxes (Set-of-Marks)
SOM_JS = """
(function() {
    // 1. Cleanup existing marks
    document.querySelectorAll('.ai-mark').forEach(el => el.remove());
    document.querySelectorAll('[data-ai-id]').forEach(el => el.removeAttribute('data-ai-id'));
    
    // 2. Helper to traverse Shadow DOMs recursively
    function getAllInteractiveElements(root) {
        let elements = [];
        // Get all descendants
        let nodes = Array.from(root.querySelectorAll('*'));
        
        nodes.forEach(node => {
            // Check if node has a Shadow Root and traverse it
            if (node.shadowRoot) {
                elements.push(...getAllInteractiveElements(node.shadowRoot));
            }
            
            // Check if node matches our interactive criteria
            if (node.matches && node.matches('button, input, a, textarea, select, [role="button"], [role="menuitem"], [role="option"]')) {
                elements.push(node);
            }
        });
        return elements;
    }

    let elements = getAllInteractiveElements(document);
    let counter = 0;
    
    elements.forEach((el) => {
        let rect = el.getBoundingClientRect();
        
        // 3. Filter: Must be visible and not tiny (tracking pixels)
        let style = window.getComputedStyle(el);
        let isVisible = style.visibility !== 'hidden' && style.display !== 'none' && style.opacity !== '0';
        let isBigEnough = rect.width > 10 && rect.height > 10;
        
        if (isVisible && isBigEnough) {
            el.setAttribute('data-ai-id', counter);
            
            // Create the Visual Mark (Red Box)
            let tag = document.createElement('div');
            tag.className = 'ai-mark';
            tag.textContent = counter;
            
            // Style it to float on top of everything
            Object.assign(tag.style, {
                position: 'absolute',
                left: (rect.left + window.scrollX) + 'px',
                top: (rect.top + window.scrollY) + 'px',
                backgroundColor: '#ff0000',
                color: 'white',
                fontSize: '12px',
                fontWeight: 'bold',
                zIndex: '2147483647',
                padding: '2px 4px',
                borderRadius: '4px',
                pointerEvents: 'none',
                boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
            });
            
            document.body.appendChild(tag);
            counter++;
        }
    });
    return counter;
})();
"""

def get_page_hash(page: Page) -> str:
    """
    Creates a unique fingerprint of the current UI state.
    If a Modal opens, the text content changes -> Hash changes -> We take screenshot.
    """
    try:
        visible_text = page.evaluate("document.body.innerText")
        html_len = len(page.content())
        fingerprint = f"{page.url}-{len(visible_text)}-{html_len}"
        return hashlib.md5(fingerprint.encode()).hexdigest()
    except Exception:
        return "error-hash"

def inject_visual_marks(page: Page):
    """Runs the SOM javascript to paint Red Boxes on the UI"""
    try:
        return page.evaluate(SOM_JS)
    except Exception as e:
        print(f"⚠️ Perception Warning: Could not inject marks: {e}")
        return 0