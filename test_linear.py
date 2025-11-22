"""
Test Linear - Assignment Demo
Shows system can handle complex project management tasks
"""
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
        # Plan the task dynamically (not hardcoded!)
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
        
        # Summary
        successful = sum(1 for h in history if h.get('success', False))
        print(f"\n✅ Result: {successful}/{len(history)} steps completed")
        print(f"📁 Saved to: {save_path}/\n")
        
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
    Test suite for Linear - Shows generalization
    These tasks are examples, but the system should handle ANY task
    """
    
    # Example tasks to test (you can change these!)
    tasks = [
        ("How do I view all issues in Linear?", "view_all_issues"),
        ("How do I navigate to Projects in Linear?", "view_projects"),
        ("How do I view my assigned issues in Linear?", "view_my_issues"),
    ]
    
    print("\n" + "🚀 LINEAR TEST SUITE - Assignment Demo".center(60))
    print("Showing: System can generalize to tasks it hasn't seen\n")
    print("These workflows demonstrate non-URL state capture:")
    print("  • Filter dropdowns (no URL)")
    print("  • Search modal (keyboard shortcut)")
    print("  • Dynamic content updates\n")
    print("Note: Requires Linear login (first time only)")
    
    # Pick which test to run
    print("Available tests:")
    for i, (task, _) in enumerate(tasks, 1):
        print(f"  {i}. {task}")
    
    choice = input("\nSelect test (1-3) or 'all': ").strip()
    
    results = []
    
    if choice.lower() == 'all':
        for task, run_name in tasks:
            success, total = test_linear_task(task, run_name)
            results.append((task, success, total))
            input("\nPress Enter to continue to next test...")
    else:
        try:
            idx = int(choice) - 1
            task, run_name = tasks[idx]
            success, total = test_linear_task(task, run_name)
            results.append((task, success, total))
        except:
            print("Invalid choice")
            return
    
    # Final summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    for task, success, total in results:
        rate = f"{success}/{total}" if total > 0 else "N/A"
        print(f"\n✓ {task}")
        print(f"  Result: {rate} steps")

if __name__ == "__main__":
    main()

