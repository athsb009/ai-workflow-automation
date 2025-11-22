"""
Test YouTube - Assignment Demo
Shows system can handle video platform workflows
Reliable, no auth required, demonstrates non-URL states
"""
import config
from adaptive_planner import AdaptivePlanner
from adaptive_executor import AdaptiveExecutor
from utils import generate_markdown_report

def test_youtube_task(task_description, run_name):
    """Run a single YouTube task"""
    print("\n" + "="*60)
    print(f"🎯 YOUTUBE TEST: {task_description}")
    print("="*60 + "\n")
    
    planner = AdaptivePlanner(api_key=config.API_KEY)
    executor = AdaptiveExecutor()
    
    try:
        # Plan the task dynamically (not hardcoded!)
        plan = planner.plan_initial_workflow(
            task_query=task_description,
            app_name="YouTube",
            app_context=config.YOUTUBE_CONTEXT
        )
        
        print(f"\n📋 AI Generated {len(plan['steps'])} steps\n")
        
        # Execute with self-correction
        save_path = f"{config.OUTPUT_DIR}/youtube_{run_name}"
        history = executor.run_adaptive_workflow(plan, save_path, planner, "YouTube")
        
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
    Test suite for YouTube - Shows generalization
    These tasks are examples, but the system should handle ANY task
    """
    
    # Example tasks to test (you can change these!)
    tasks = [
        ("How do I search for 'Python tutorials' on YouTube?", "search_python"),
        ("How do I navigate to the Trending page on YouTube?", "view_trending"),
        ("How do I view my YouTube subscriptions page?", "view_subscriptions"),
    ]
    
    print("\n" + "🚀 YOUTUBE TEST SUITE - Assignment Demo".center(60))
    print("Showing: System can generalize to tasks it hasn't seen\n")
    
    # Pick which test to run
    print("Available tests:")
    for i, (task, _) in enumerate(tasks, 1):
        print(f"  {i}. {task}")
    
    choice = input("\nSelect test (1-3) or 'all': ").strip()
    
    results = []
    
    if choice.lower() == 'all':
        for task, run_name in tasks:
            success, total = test_youtube_task(task, run_name)
            results.append((task, success, total))
            if task != tasks[-1][0]:  # Not the last one
                input("\nPress Enter to continue to next test...")
    else:
        try:
            idx = int(choice) - 1
            task, run_name = tasks[idx]
            success, total = test_youtube_task(task, run_name)
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

