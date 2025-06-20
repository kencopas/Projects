import json
import subprocess
from pathlib import Path

from dotenv import load_dotenv

from myutils.openai import EasyGPT
from myutils.logging import gotenv, gen_file_structure


def vibes(main_fp: str, python_path: str = gotenv('PYTHONPATH')) -> None:
    """Process a Python file, generate its structure, and interact with GPT.

    This is the ultimate vibe code. It takes a project structure, formats it
    into json for ai-readability, including each file's contents, runs the main.py
    file or specified entry point, captures the stdout and stderr, and sends all
    of that data to an AI Assistant made for project building/refinement.

    Args:
        main_fp (str): The filepath to the entrypoint python file of your project
        python_path (Optional[str]): Optionally specify the interpreter path

    Returns:
        None: Simply creates file-structure.json, input.md, and output.md
    """

    # Load environment variables
    load_dotenv()

    # Retrieve assistant id
    assistant_id = gotenv('ASSISTANT_ID')

    # Generate and format the file structure json data
    fs_data = gen_file_structure('file-structure.json', main_fp)
    fs = json.dumps(fs_data, indent=2, sort_keys=True)

    # Create EasyGPT instance
    gpt = EasyGPT(assistant_id)

    # Run the main python file and capture the output
    result = subprocess.run(
        [rf"{python_path.replace(r'\"', '')}\python.exe", main_fp],
        capture_output=True,
        text=True
    )

    # Construct message
    message = (
        f"File Structure:\n\n```json\n{fs}\n```\n\n"
        f"**STDOUT:**\n```\n{result.stdout.strip() or '[No output]'}\n```\n\n"
        f"**STDERR:**\n```\n{result.stderr.strip() or '[No output]'}\n```"
    )

    # Create a message, run, and retrieve the output
    gpt.create(message)
    response = gpt.retrieve()

    # Write the markdown response to input.md
    with open('input.md', 'w', encoding='utf-8') as f:
        f.write(message)

    # Write the markdown response to output.md
    with open('output.md', 'w', encoding='utf-8') as f:
        f.write(response)


if __name__ == '__main__':
    vibes(r"<Absolute path to main.py (or other entry point python file)>")
