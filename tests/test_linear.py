"""
Test Linear - Assignment Demo
Shows system can handle project management workflows
Requires authentication, demonstrates non-URL states (modals, dropdowns)
"""
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import config
from adaptive_planner import AdaptivePlanner
from adaptive_executor import AdaptiveExecutor
from utils import generate_markdown_report

def test_linear_task(task_description, run_name):
    """Run a single Linear task"""
    print("\n" + "="*60)
    print(f"🎯 LINEAR TEST: {task_description}")
    print("="*60 + "\n")
    
    planner = AdaptivePlanner(api_key=config.API_KEY)
    executor = AdaptiveExecutor()
    
    try:
        # Plan the task dynamically
        plan = planner.plan_initial_workflow(
            task_query=task_description,
            app_name="Linear",
            app_context=config.LINEAR_CONTEXT
        )
        
        print(f"\n📋 AI Generated {len(plan['steps'])} steps\n")
        
        # Execute with self-correction
        save_path = f"{config.OUTPUT_DIR}/linear_{run_name}"
        history = executor.run_adaptive_workflow(plan, save_path, planner, "Linear")
        
        # Generate report
        generate_markdown_report(task_description, history, save_path)
        
        successful = sum(1 for h in history if h.get('success', False))
        return successful, len(history)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 0, 0
    finally:
        executor.close()

def main():
    """
    Test suite for Linear - Shows complex workflow handling
    Demonstrates: modals, keyboard shortcuts, contenteditable inputs
    """
    
    # Linear workflows
    tasks = [
        ("How do I create a new issue in Linear?", "create_issue"),
        ("How do I navigate to Projects in Linear?", "view_projects"),
        ("How do I view my assigned issues in Linear?", "view_my_issues"),
    ]
    
    print("\n" + "🚀 LINEAR TEST SUITE - Assignment Demo".center(60))
    print("Showing: System can handle authenticated apps with complex UIs\n")
    print("Features demonstrated:")
    print("  • Modal dialogs (non-URL state)")
    print("  • Keyboard shortcuts (press 'c' to create)")
    print("  • Contenteditable inputs (rich text)")
    print("  • Filter dropdowns")
    print("\n⚠️  Note: Requires Linear login (first time only)\n")
    
    # Pick which test to run
    print("Available tests:")
    for i, (task, _) in enumerate(tasks, 1):
        note = " (complex - uses modal & keyboard)" if i == 1 else ""
        print(f"  {i}. {task}{note}")
    
    choice = input("\nSelect test (1-3) or 'all': ").strip()
    
    results = []
    
    if choice.lower() == 'all':
        for task, run_name in tasks:
            success, total = test_linear_task(task, run_name)
            results.append((task, success, total))
            if task != tasks[-1][0]:
                input("\nPress Enter to continue to next test...")
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(tasks):
                task, run_name = tasks[idx]
                success, total = test_linear_task(task, run_name)
                results.append((task, success, total))
            else:
                print("Invalid selection!")
                return
        except ValueError:
            print("Invalid input!")
            return
    
    # Final summary
    if results:
        print("Done")

if __name__ == "__main__":
    main()

