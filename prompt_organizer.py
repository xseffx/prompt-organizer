#!/usr/bin/env python3

import json
import os
import sys

DATA_FILE = "prompts.json"


def load_prompts():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_prompts(prompts):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(prompts, file, indent=2, ensure_ascii=False)


def add_prompt(title, category, prompt):
    prompts = load_prompts()

    prompts.append({
        "title": title,
        "category": category,
        "prompt": prompt
    })

    save_prompts(prompts)
    print(f"Added: {title}")


def list_prompts():
    prompts = load_prompts()

    if not prompts:
        print("No prompts saved yet.")
        return

    for index, item in enumerate(prompts, start=1):
        print(f"{index}. {item['title']} [{item['category']}]")


def search_prompts(keyword):
    prompts = load_prompts()
    keyword = keyword.lower()

    results = [
        item for item in prompts
        if keyword in item["title"].lower()
        or keyword in item["category"].lower()
        or keyword in item["prompt"].lower()
    ]

    if not results:
        print("No matching prompts found.")
        return

    for item in results:
        print(f"\nTitle: {item['title']}")
        print(f"Category: {item['category']}")
        print(f"Prompt: {item['prompt']}")


def show_prompt(index):
    prompts = load_prompts()

    if index < 1 or index > len(prompts):
        print("Invalid prompt number.")
        return

    item = prompts[index - 1]

    print(f"\nTitle: {item['title']}")
    print(f"Category: {item['category']}")
    print(f"Prompt:\n{item['prompt']}")


def print_help():
    print("""
Prompt Organizer

Commands:

  add <title> <category> <prompt>
      Save a new prompt.

  list
      Show all saved prompts.

  search <keyword>
      Search prompts.

  show <number>
      Display a specific prompt.

Examples:

  python prompt_organizer.py add "Coding Helper" coding "Explain this Python code"
  python prompt_organizer.py list
  python prompt_organizer.py search coding
  python prompt_organizer.py show 1
""")


def main():
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) < 5:
            print("Usage: add <title> <category> <prompt>")
            return

        title = sys.argv[2]
        category = sys.argv[3]
        prompt = " ".join(sys.argv[4:])

        add_prompt(title, category, prompt)

    elif command == "list":
        list_prompts()

    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: search <keyword>")
            return

        search_prompts(" ".join(sys.argv[2:]))

    elif command == "show":
        if len(sys.argv) != 3:
            print("Usage: show <number>")
            return

        try:
            index = int(sys.argv[2])
            show_prompt(index)
        except ValueError:
            print("The prompt number must be an integer.")

    elif command in ("help", "--help", "-h"):
        print_help()

    else:
        print(f"Unknown command: {command}")
        print_help()


if __name__ == "__main__":
    main()
