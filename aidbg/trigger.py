# aidbg/trigger.py

from pathlib import Path

from aidbg.context.collector import extract_error_location, get_code_snippet
from aidbg.context.project_tree import get_project_tree
from aidbg.context.environment import get_environment_info
from aidbg.context.dependencies import get_dependencies

from aidbg.prompt import SYSTEM_PROMPT, build_user_prompt
from aidbg.config import load_config

from aidbg.llm.groq import GroqClient
from aidbg.llm.openai import OpenAIClient
from aidbg.llm.ollama import OllamaClient

from aidbg.logic.complexity import classify_error
from aidbg.logic.token_budget import get_token_budget


def detect_crash(output: str, project_root: Path):
    if "Traceback (most recent call last)" not in output:
        print("✖ Program failed (no traceback found)")
        return

    print("✖ Crash detected\n")

    print("--- Traceback ---")
    print(output.strip())

    file_path, line_no = extract_error_location(output)

    snippet = ""
    if file_path and line_no:
        print("\n--- Code Snippet ---")
        snippet = get_code_snippet(file_path, line_no)
        print(snippet)

    tree = get_project_tree(project_root)
    env = get_environment_info()
    deps = get_dependencies(project_root)

    level = classify_error(output)
    token_budget = get_token_budget(level)

    try:
        cfg = load_config(project_root)
        provider = cfg.get("provider")

        if provider == "groq":
            client = GroqClient(
                api_key=cfg["api_key"],
                model=cfg.get("model", "llama-3.1-8b-instant"),
            )

        elif provider == "openai":
            client = OpenAIClient(
                api_key=cfg["api_key"],
                model=cfg.get("model", "gpt-4o-mini"),
            )

        elif provider == "ollama":
            client = OllamaClient(
                model=cfg.get("model", "llama3"),
            )

        else:
            raise RuntimeError(f"Unsupported LLM provider: {provider}")

        user_prompt = build_user_prompt(
            output,
            snippet,
            tree,
            env,
            deps,
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
