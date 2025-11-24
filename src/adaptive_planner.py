"""
Adaptive Planner - A self-correcting AI that can see and replan
This is Agent A 2.0 - it can look at screenshots and adjust the plan
"""
import json
import base64
from openai import OpenAI
from config import MODEL_NAME
from pathlib import Path

class AdaptivePlanner:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.conversation_history = []
    
    def plan_initial_workflow(self, task_query, app_name, app_context):
        """Creates the initial plan"""
        print(f"🧠 Adaptive Brain: Planning steps for '{task_query}'...")
        
        prompt = f"""
        You are an advanced AI Workflow Planner with self-correction abilities.
        
        Task: "{task_query}"
        App: {app_name}
        Context: {json.dumps(app_context)}

        Create a flexible, robust plan. Return JSON with this structure:
        {{
            "steps": [
                {{
                    "step_number": 1,
                    "action": "navigate|click|type|press_enter|wait|scroll|keyboard_shortcut",
                    "description": "Clear explanation of what this does",
                    "primary_selector": "Preferred selector",
                    "fallback_selectors": ["Alternative selector 1", "Alternative selector 2"],
                    "text_match": "Text to find (for text-based clicking)",
                    "url": "For navigate action",
                    "input_value": "For type action",
                    "keyboard_shortcut": "For keyboard actions (e.g. 'Meta+K')",
                    "verification_text": "Specific text that should appear after this step",
                    "verification_selector": "Element that should exist after this step",
                    "requires_screenshot": true
                }}
            ]
        }}
        
        CRITICAL REQUIREMENTS:
        1. ASSUME USER IS ALREADY LOGGED IN - Do NOT include login steps
           - Start directly with the task actions
           - Skip any authentication or sign-in steps
        
        2. For each step, specify BOTH:
           - verification_text: Exact text that confirms success (e.g., "Create a new repository")
           - verification_selector: An element selector that should exist (e.g., 'input#repository-name')
        
        3. Prefer TEXT-BASED selectors: button:has-text("Create") over [data-testid="..."]
        
        4. Break complex tasks into small, verifiable steps
        
        5. Add explicit 'wait' steps after actions that trigger page loads or modals
        """

        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        plan = json.loads(response.choices[0].message.content)
        self.conversation_history.append({
            "role": "assistant",
            "content": f"Initial plan created with {len(plan['steps'])} steps"
        })
        
        return plan
    
    def discover_selectors(self, screenshot_path, task_query):
        """
        NEW FEATURE: Analyze a screenshot and discover selectors for a task
        This lets AI figure out the UI without any context!
        """
        print(f"🔍 AI is analyzing the page to discover selectors...")
        
        with open(screenshot_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        
        prompt = f"""
        Task: "{task_query}"
        
        Look at this screenshot and identify the UI elements needed for this task.
        
        For example, if the task is "create a repository":
        - Find the button/link to start creating (e.g., "New", "Create", "+")
        - Find form fields (repository name, description, etc.)
        - Find the submit button
        
        Respond with JSON containing suggested selectors:
        {{
            "discovered_selectors": {{
                "primary_action_button": "selector for main action (e.g., 'New' button)",
                "form_fields": ["selector1", "selector2"],
                "submit_button": "selector for final submit"
            }},
            "workflow_hints": "Brief description of the workflow you see",
            "confidence": 0-100
        }}
        
        Use robust selectors like:
        - Text-based: button:has-text("Create"), a:has-text("New")
        - Aria-labels: [aria-label="Create something new"]
        - IDs: input#repository_name
        - Placeholders: [placeholder="Repository name"]
        """
        
        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}}
                        ]
                    }
                ],
                response_format={"type": "json_object"}
            )
            
            discovery = json.loads(response.choices[0].message.content)
            print(f"   ✅ Discovered {len(discovery.get('discovered_selectors', {}))} selector categories")
            print(f"   💡 Workflow: {discovery.get('workflow_hints', 'N/A')}")
            return discovery
            
        except Exception as e:
            print(f"   ⚠️  Discovery failed: {e}")
            return {"discovered_selectors": {}, "confidence": 0}
    
    def verify_and_adapt(self, step, screenshot_path, success, error_message=None):
        """
        Look at what happened and decide next action
        This is the KEY feature - the AI can SEE the result and adapt!
        """
        print(f"🔍 Verifying Step {step['step_number']}...")
        
        # Encode screenshot for vision
        with open(screenshot_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        
        if success:
            prompt = f"""
            Step {step['step_number']} completed: "{step['description']}"
            Action: {step['action']} on {step.get('primary_selector', 'N/A')}
            
            Look at the screenshot. Did this action succeed?
            Expected: {step.get('verification', 'State change')}
            
            Respond with JSON:
            {{
                "success": true/false,
                "observation": "What you see in the screenshot",
                "next_action": "continue" or "retry_with_alternative" or "skip",
                "alternative_selector": "If retry needed, suggest a better selector",
                "confidence": 0-100
            }}
            """
        else:
            prompt = f"""
            Step {step['step_number']} FAILED: "{step['description']}"
            Error: {error_message}
            Tried selector: {step.get('primary_selector', 'N/A')}
            
            Look at the screenshot. What went wrong?
            
            Suggest a fix. Respond with JSON:
            {{
                "success": false,
                "problem": "Why it failed",
                "alternative_approach": "click_text|keyboard_shortcut|different_selector|skip",
                "alternative_selector": "Better selector to try",
                "text_to_click": "If using text-based approach",
                "keyboard_shortcut": "If using keyboard",
                "should_skip": false,
                "reasoning": "Why this approach is better"
            }}
            """
        
        messages = [
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{img_base64}",
                        "detail": "high"
                    }
                }
            ]}
        ]
        
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        print(f"   AI says: {result.get('observation', result.get('problem', 'Analyzing...'))}")
        
        return result
    
    def suggest_next_steps(self, current_state, task_query, completed_steps):
        """
        Dynamic replanning - ask AI what to do next based on current state
        """
        print("🔄 Asking AI for next steps based on current progress...")
        
        prompt = f"""
        Original Task: {task_query}
        Completed Steps: {len(completed_steps)}
        
        Steps completed so far:
        {json.dumps([s['description'] for s in completed_steps], indent=2)}
        
        What should we do next to complete the task?
        Return 1-3 more steps in the same JSON format as before.
        """
        
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)

