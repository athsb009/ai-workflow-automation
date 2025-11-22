"""
Adaptive Executor - Self-healing browser automation
This is Agent B 2.0 - it tries multiple strategies and doesn't give up easily
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from perception import get_page_hash, inject_visual_marks

class AdaptiveExecutor:
    def __init__(self, user_data_dir="./user_data"):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            viewport={'width': 1280, 'height': 800},
            slow_mo=100,  
            ignore_https_errors=True
        )
        self.page = self.browser.pages[0]
        self.last_hash = ""
        self.retry_count = 0
        self.max_retries = 3
        self.current_app = None  
    
    def _wait_for_stable_page(self, timeout=2000):
        """
        Smart Wait: Waits for the network to settle (no active requests for 500ms).
        If the network is 'chatty' (e.g., live websockets), it timeouts gracefully.
        """
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout)
        except PlaywrightTimeout:
            pass 

    def _capture_debug_snapshot(self, step_number, output_path, status="check"):
        """
        Saves a screenshot with the AI's 'Set-of-Marks' (Red Boxes) visible.
        This tells you exactly what elements the AI detected.
        """
        try:
            element_count = inject_visual_marks(self.page)
        except Exception as e:
            print(f"      ⚠️ SoM Injection failed: {e}")
            element_count = 0
        
        filename = f"step_{step_number:02d}_{status}_debug.png"
        full_path = output_path / filename
        self.page.screenshot(path=full_path)
        
        print(f"      📸 Debug Snapshot: {filename} (Detected {element_count} elements)")
        
        
        self.page.evaluate("""
            document.querySelectorAll('.ai-mark').forEach(el => el.remove());
            document.querySelectorAll('[data-ai-id]').forEach(el => el.removeAttribute('data-ai-id'));
        """)
        
        return str(full_path)

    def run_adaptive_workflow(self, workflow, output_dir, planner=None, app=None):
        """
        Runs workflow with adaptive capabilities:
        - Tries multiple selectors
        - Captures Clean AND Debug screenshots
        - Uses AI vision to verify and self-correct
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True, parents=True)
        
        self.current_app = app
        
        history = []
        print("\n🎬 Adaptive Executor: Starting Workflow...\n")

        for step in workflow['steps']:
            print(f"👉 Step {step['step_number']}: {step['description']}")
            
            success = False
            error_msg = None
            
            for attempt in range(self.max_retries):
                try:
                    if attempt == 0:
                        if self._use_app_specific_handler(step):
                            success = True
                            break
                        self._perform_action(step)
                        success = True
                        break
                    else:
                        print(f"   🔄 Attempt {attempt + 1}/{self.max_retries}...")
                        if self._try_fallback_strategy(step, attempt):
                            success = True
                            break
                
                except Exception as e:
                    error_msg = str(e)
                    print(f"   ⚠️  Attempt {attempt + 1} failed: {error_msg[:100]}")
                    self.page.wait_for_timeout(1000)
            
      
            status_label = "success" if success else "failed"
            clean_filename = f"step_{step['step_number']:02d}_{status_label}.png"
            clean_path = output_path / clean_filename
            self.page.screenshot(path=clean_path)
            
            debug_path = self._capture_debug_snapshot(
                step['step_number'], 
                output_path, 
                status=status_label
            )
            
            current_hash = get_page_hash(self.page)
            
            if success:
                print(f"   ✅ Success! Screenshot: {clean_filename}")
                
                history.append({
                    "step": step,
                    "screenshot": str(clean_path),
                    "debug_screenshot": str(debug_path),
                    "success": True
                })
                
                self.last_hash = current_hash
                
            else:
                print(f"   ❌ Failed after {self.max_retries} attempts")
                
                history.append({
                    "step": step,
                    "screenshot": str(clean_path),
                    "debug_screenshot": str(debug_path),
                    "success": False,
                    "error": error_msg
                })
        
                if planner:
                   
                    verification = planner.verify_and_adapt(
                        step, clean_path, success=False, error_message=error_msg
                    )
                    
                    if not verification.get('should_skip', False):
                        print(f"   🤖 AI suggests: {verification.get('reasoning', 'trying alternative')}")
                        
                        if self._try_ai_suggestion(step, verification):
                            history[-1]['success'] = True
                            print(f"   ✅ AI suggestion worked!")
                            
                            self.page.screenshot(path=output_path / f"step_{step['step_number']:02d}_ai_fixed.png")
        
        return history
    
    def _use_app_specific_handler(self, step):
        if step['action'] == 'type' and 'search' in step['description'].lower():
            for shortcut in ['/', 'Meta+K', 'Control+K']:
                try:
                    self.page.keyboard.press(shortcut)
                    self.page.wait_for_timeout(500)
                    if self.page.locator('input:focus, textarea:focus').count() > 0:
                        self.page.keyboard.type(step['input_value'], delay=50)
                        return True
                except:
                    continue
        
        if step['action'] == 'click' and 'new' in step['description'].lower():
            try:
                self.page.keyboard.press('Meta+N')
                self._wait_for_stable_page()
                return True
            except:
                pass
        return False
    
    def _perform_action(self, step):
        """Execute action with event-driven waiting"""
        action = step['action']
        selector = step.get('primary_selector') or step.get('selector')
        timeout = 10000

        if action == 'navigate':
            try:
                self.page.goto(step['url'], wait_until='networkidle', timeout=timeout)
            except PlaywrightTimeout:
                self.page.goto(step['url'], wait_until='domcontentloaded', timeout=timeout)
            
        elif action == 'click':
            if step.get('text_match'):
                target = self.page.locator(f'text=/{step["text_match"]}/i')
            else:
                target = self.page.locator(selector)
            
            target.scroll_into_view_if_needed()
            target.click(timeout=timeout)
            self._wait_for_stable_page()
        
        elif action == 'type':
            loc = self.page.locator(selector)
            loc.wait_for(state="visible", timeout=timeout)
            loc.scroll_into_view_if_needed()
            
           
            try:
                loc.click(delay=50)
            except:
                pass
                
            loc.fill("") 
            loc.type(step['input_value'], delay=30) 
            self.page.wait_for_timeout(500) # Wait for autosuggest
        
        elif action == 'press_enter':
            if selector:
                self.page.press(selector, "Enter", timeout=timeout)
            else:
                self.page.keyboard.press("Enter")
            self._wait_for_stable_page()
        
        elif action == 'keyboard_shortcut':
            shortcut = step.get('keyboard_shortcut', 'Enter')
            self.page.keyboard.press(shortcut)
            self._wait_for_stable_page()
        
        elif action == 'scroll':
            self.page.evaluate("window.scrollBy({top: 500, behavior: 'smooth'})")
            self.page.wait_for_timeout(500)
        
        elif action == 'wait':
            self.page.wait_for_timeout(2000)
    
    def _try_fallback_strategy(self, step, attempt_num):
        # Strategy 1: Fallback selectors
        if attempt_num == 1 and step.get('fallback_selectors'):
            for fallback in step['fallback_selectors']:
                try:
                    print(f"      Trying fallback: {fallback[:50]}...")
                    if step['action'] == 'click':
                        self.page.click(fallback, timeout=5000)
                        self._wait_for_stable_page()
                    elif step['action'] == 'type':
                        self.page.fill(fallback, step['input_value'], timeout=5000)
                    return True
                except:
                    continue
        
        # Strategy 2: Visible input strategy
        if attempt_num == 2 and step['action'] == 'type':
            try:
                visible_input = self.page.locator('input:visible, textarea:visible').first
                visible_input.click(timeout=3000)
                visible_input.fill(step['input_value'], timeout=5000)
                return True
            except:
                # Try typing directly
                try:
                    self.page.keyboard.type(step['input_value'], delay=50)
                    return True
                except:
                    pass
        
        # Strategy 3: Text-based clicking
        if attempt_num == 2 and step['action'] == 'click':
            words = step['description'].lower().split()
            action_words = ['search', 'create', 'new', 'submit', 'save', 'add', 'open']
            for word in action_words:
                if word in words:
                    try:
                        self.page.click(f'text=/{word}/i', timeout=5000)
                        self._wait_for_stable_page()
                        return True
                    except:
                        continue
        return False
    
    def _try_ai_suggestion(self, step, verification):
        try:
            approach = verification.get('alternative_approach', '')
            
            if approach == 'click_text' and verification.get('text_to_click'):
                text = verification['text_to_click']
                self.page.click(f'text="{text}"', timeout=5000)
                self._wait_for_stable_page()
                return True
            
            elif approach == 'keyboard_shortcut' and verification.get('keyboard_shortcut'):
                self.page.keyboard.press(verification['keyboard_shortcut'])
                self._wait_for_stable_page()
                return True
            
            elif approach == 'different_selector' and verification.get('alternative_selector'):
                selector = verification['alternative_selector']
                if step['action'] == 'click':
                    self.page.click(selector, timeout=5000)
                elif step['action'] == 'type':
                    self.page.fill(selector, step['input_value'], timeout=5000)
                self._wait_for_stable_page()
                return True
        except Exception as e:
            print(f"      AI suggestion failed: {e}")
            return False
        return False
    
    def close(self):
        self.browser.close()
        self.playwright.stop()