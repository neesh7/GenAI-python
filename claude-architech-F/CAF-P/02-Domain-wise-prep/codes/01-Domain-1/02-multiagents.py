from claude_agent import Agent, Task

coordinator = Agent(
    model="claude-sonnet-4-20250514",
    tools=[
        Task,              # Required for spawning subagents
        summarize_results, # Coordinator-level synthesis
        format_report,     # Final output formatting
    ]
)

# Subagent with scoped tool access (4 tools each)
market_researcher = Agent(
    model="claude-sonnet-4-20250514",
    tools=[web_search, read_doc, extract_data, format_citation],
)

tech_analyst = Agent(
    model="claude-sonnet-4-20250514",
    tools=[read_code, grep_patterns, analyze_deps, format_report],
)

# Coordinator delegates with EXPLICIT context per subtask
coordinator.run("""
Research AI infrastructure market. Delegate:
1. Market research → market_researcher
2. Technology analysis → tech_analyst
Pass each subagent ONLY the context relevant to their task.
""")