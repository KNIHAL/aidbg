# aidbg/trigger.py

from pathlib import Path

from aidbg.context.project_tree import get_project_tree
from aidbg.context.environment import get_environment_info
from aidbg.context.dependencies import get_dependencies

from aidbg.prompt import SYSTEM_PROMPT, build_user_prompt
from aidbg.config import load_config

from aidbg.llm.groq import GroqClient
from aidbg.llm.openai import OpenAIClient
from aidbg.llm.ollama import OllamaClient

from aidbg.logic.token_budget import get_token_budget


def handle_crash(output: str, project_root: Path, adapter):
    if not adapter.detect_crash(output):
        print("✖ Program failed (no recognizable crash)")
        return

    print("✖ Crash detected\n")
    print("--- Traceback / Error ---")
    print(output.strip())

    file_path, line_no = adapter.extract_location(output)

    snippet = ""
    if file_path and line_no:
        print("\n--- Code Snippet ---")
        snippet = adapter.get_snippet(file_path, line_no)
        print(snippet)

    tree = get_project_tree(project_root)
    env = get_environment_info()
    deps = get_dependencies(project_root)

    level = adapter.classify_error(output)
    token_budget = get_token_budget(level)

    try:
        cfg = load_config(project_root)
        provider = cfg.get("provider")

        if provider == "groq":
            client = GroqClient(
                api_key=cfg["api_key"],
                model=cfg.get("model"),
            )

        elif provider == "openai":
            client = OpenAIClient(
                api_key=cfg["api_key"],
                model=cfg.get("model"),
            )

        elif provider == "ollama":
            client = OllamaClient(
                model=cfg.get("model"),
            )

        else:
            raise RuntimeError(f"Unsupported LLM provider: {provider}")

        user_prompt = build_user_prompt(
            language=adapter.__class__.__name__.replace("Adapter", ""),
            traceback=output,
            snippet=snippet,
            tree=tree,
            env=env,
            deps=deps,
        )

        response = client.complete(
            SYSTEM_PROMPT + f"\n\nMAX TOKEN BUDGET: {token_budget}",
            user_prompt,
        )

        print("\n--- AI Debugger ---")
        print(response)

    except Exception as e:
        print("\n--- AI Debugger ---")
        print("⚠️ AI debugging failed")
        print(str(e))
