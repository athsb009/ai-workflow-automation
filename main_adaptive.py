"""
Adaptive AI Workflow System - Version 2.0
This version can handle COMPLEX tasks with self-correction
"""
import config
from adaptive_planner import AdaptivePlanner
from adaptive_executor import AdaptiveExecutor
from utils import generate_markdown_report

def main():
    print("=" * 60)
    print("🚀 ADAPTIVE AI WORKFLOW SYSTEM v2.0")
    print("   Self-correcting | Vision-enabled | Multi-strategy")
    print("=" * 60)
    
    # 1. Setup
    planner = AdaptivePlanner(api_key=config.API_KEY)
    executor = AdaptiveExecutor()

    # 2. Define Task (You can change this!)
    task = "How do I search for 'python automation' repositories on GitHub?"
    app = "GitHub"
    context = config.GITHUB_CONTEXT
    
    
    try:
        # 3. Plan with adaptive AI
        plan = planner.plan_initial_workflow(task, app, context)
        
        print(f"\n📋 Generated {len(plan['steps'])} steps")
        print("\n" + "=" * 60 + "\n")
        
        # 4. Execute with self-healing
        timestamp = "adaptive_run_01"
        save_path = f"{config.OUTPUT_DIR}/{app.lower()}_{timestamp}"
        
        history = executor.run_adaptive_workflow(plan, save_path, planner, app)
        
        # 5. Report
        generate_markdown_report(task, history, save_path)
        
        # 6. Summary
        print("\n" + "=" * 60)
        successful_steps = sum(1 for h in history if h.get('success', False))
        print(f"✅ Completed: {successful_steps}/{len(history)} steps")
        print(f"📁 Results saved to: {save_path}/")
        print(f"📖 View guide: {save_path}/README.md")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ CRITICAL FAILURE: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n⏸️  Press Enter to close browser...")
        input()
        executor.close()

if __name__ == "__main__":
    main()

