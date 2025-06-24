import json
import subprocess
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template
from bs4 import BeautifulSoup

from myutils.openai import EasyGPT
from myutils.logging import gotenv, gen_file_structure

app = Flask(__name__)
_vc = None


class VibeCoder:
    """Process a Python file, generate its structure, and interact with GPT.

    This is the ultimate vibe code. It takes a project structure, formats it
    into json for ai-readability, including each file's contents, runs the
    main.py file or specified entry point, captures the stdout and stderr, and
    sends all of that data to an AI Assistant made for project building.

    Args:
        project_path (str): The filepath to the desired project folder
        python_path (Optional[str]): Optionally specify the interpreter path

    Returns:
        None: Simply creates file-structure.json, input.md, and output.md
    """

    def __init__(self, prompt: str, project_path: str, python_path: str = 'python', *, new: bool = False):

        # Save attributes
        self.project_path = Path(project_path)
        if python_path != 'python':
            python_path = f'{python_path.replace(r'"', '')}/python.exe'
        self.python_path = python_path

        # Load environment variables
        load_dotenv()

        # Retrieve assistant id
        assistant_id = gotenv('ASSISTANT_ID')

        # Create EasyGPT Assistant
        self.gpt = EasyGPT(assistant_id)

        # Initialize the project
        if new:
            self.init_project(prompt)

    def send_message(self, message: str) -> dict:
        """Sends a message to the assistant, returns the json data in the response"""

        # Create a message, run, and retrieve the output
        self.gpt.create(message)
        response = self.gpt.retrieve()

        # Write the markdown response to output.md
        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.write(response)

        soup = BeautifulSoup(response, 'lxml')

        target_element = soup.find(id='file-structure')

        if target_element:
            return json.loads(target_element.text)

        return None

    def init_project(self, prompt: str):
        """Creates project folder and main.py file, sets first update to project"""
        print("init")

        # Create the project folder
        self.project_path.mkdir(parents=True, exist_ok=True)

        # Create the main.py file (only if it doesn't exist) and write a sample line
        main_file = self.project_path / "main.py"
        if not main_file.exists():
            main_file.write_text("# main.py\n\nif __name__ == '__main__':\n    print('Hello from main.py')")

        # Create an empty project file structure
        fs_data = gen_file_structure('file-structure.json', str(main_file))
        fs = json.dumps(fs_data, indent=2, sort_keys=True)

        # Construct the message with the prompt and empty file structure
        message = (
            f"Project Prompt:\n\n{prompt}\n\n"
            f"Current File Structure:\n\n```json\n{fs}\n```\n\n"
        )

        self.main_file = main_file

        # Send the message
        response = self.send_message(message)

        self.write_structure(response)

        # Create venv
        subprocess.run(
            [self.python_path, '-m', 'venv', 'venv'],
            cwd=self.project_path
        )

        # Update the python path to the venv python
        self.python_path = self.project_path / "venv" / "Scripts" / "python.exe"

        # Install dependencies
        subprocess.run(
            [self.python_path, '-m', 'pip', 'install', '-r', 'requirements.txt'],
            cwd=self.project_path
        )

    def write_structure(self, fs_data: dict):
        """Takes json data and writes the filepaths and file contents

        This method taks json data that contains directory entries ordered
        by directories and subdirectories that each contain an absolute
        filepath and filecontents if a file or subdirectories if a folder.

        Args:
            fs_data (dict): File Structure data as a dictionary

        Example:

            # Input

            VibeCoder.write_structure({
                "path": "C:/Users/myuser/myproject"
                "subpaths": [
                    {
                        "path": "C:/Users/myuser/myproject/main.py",
                        "contents": "print('Hello World!')"
                    }
                ]
            })

            # Output (New Project Structure)

            my_project/
            └── main.py # print('Hello World!')
        """

        # Initialize current node
        node = fs_data['subpaths']

        # Depth-First Search function for file structure traversal
        def dfs(node: list):

            # Iterate through subnodes
            for subnode in node:

                # Get subpath
                subpath = Path(subnode['path'])

                # If file, write contents
                if subnode.get('contents') and not subnode['contents'].startswith('[TRUNCATED]'):
                    subpath.write_text(subnode.get('contents'))
                # If directory, create folder
                elif subnode.get('subpaths'):
                    subpath = Path(subnode['path'])
                    subpath.mkdir(parents=True, exist_ok=True)
                    dfs(subnode['subpaths'])

        # Perform DFS on the current working directory
        dfs(node)

    def vibe(self, main_file: str = None) -> None:
        """One project structure update from the assistant"""
        print('vibing')

        if not main_file:
            main_file = str(self.main_file)

        # Generate and format the file structure json data
        fs_data = gen_file_structure('file-structure.json', main_file)
        fs = json.dumps(fs_data, indent=2, sort_keys=True)

        print(self.project_path)

        # Run the main python file and capture the output
        result = subprocess.run(
            [self.python_path, main_file],
            cwd=self.project_path,
            capture_output=True,
            text=True
        )

        # Construct message
        message = (
            f"File Structure:\n\n```json\n{fs}\n```\n\n"
            f"**STDOUT:**\n```\n{result.stdout.strip() or '[No output]'}\n```\n\n"
            f"**STDERR:**\n```\n{result.stderr.strip() or '[No output]'}\n```"
        )

        # Send the message to the Assistant, write the response to the project structure
        response = self.send_message(message)
        self.write_structure(response)


def getvc():
    global _vc
    if not _vc:
        _vc = VibeCoder(
            """Create a project that manages an ETL Process for a banking
            dataset. The project should use PySpark and MySQL to read data from json
            flat files, reformat the data for MySQL, and then load the data into a
            MySQL database. All configurations should be pulled from one file
            for modularity, and the project itself should be very modular. Also
            include a CLI that can interact with the database after the ETL
            process is finished. This should be done in python and should
            include. a requirements.txt file for ease of use.""",
            r"C:\\Users\\kenneth.copas\\OneDrive - PeopleShores PBC\\Desktop\\Projects\\OpenAI\\ETLProject"
        )
    return _vc


@app.route('/')
def home():

    print("Vibing...")

    vc = getvc()

    vc.vibe(r"C:\\Users\\kenneth.copas\\OneDrive - PeopleShores PBC\\Desktop\\Projects\\OpenAI\\ETLProject\\main.py")

    return render_template('index.html')


if __name__ == '__main__':

    app.run(debug=True)
