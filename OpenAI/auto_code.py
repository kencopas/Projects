from openai_test import EasyGPT
import os

# Takes a response in markdown format and extracts python and bash commands from it
def extract(response: str) -> tuple:

    mode = "markdown"
    python, bash = [], []
    arrays = {"python": python, "bash": bash, "sh": bash}

    lines = response.splitlines()
    for line in lines:
        if mode != "markdown":
            arrays[mode].append(line)

        if line.startswith(r'```'):
            if mode == "markdown":
                mode = line[3:]
            else:
                mode = "markdown"
    
    return ('\n'.join(python), '\n'.join(bash))

# Overwrites a file wiht new content
def overwrite(filepath: str, content: str):
    with open(filepath, "w", encoding="utf-8") as f:
        f.seek(0)
        f.truncate()
        f.write(content)

# Runs a file, writes the output to another file, returns the output
def run(filepath: str):
    
    index = filepath.find(".")
    ext = filepath[index:]
    output_file = f"{filepath[:index]}_output.txt"

    commands = {".py": "python", ".sh": "bash", ".bat": ""}

    try:
        os.system(f"> {output_file}")
        os.system(f"{commands[ext]} {filepath} >> {output_file}")
        with open(output_file, "r") as f:
            output = f.read()
        return output
    except Exception as e:
        print(e)


# This class creates an easy way to perform Agentic-AI operations
class EasyAgent:

    def __init__(self):
        pass

    # Produces a markdown response, extracts python and bash code, writes and runs both
    def develop(self, filepath: str, project: str):

        # Create a virtual environement
        os.system("python -m venv devenv")
        os.system(r".\devenv\Scripts\activate.bat")

        # Markdown Bro
        mdbro = EasyGPT("You are a helpful assistant. You explain how to use python to complete a project, and how to use cmd commands to install the necessary dependencies. You responses should be in markdown format.")
        
        # Give Markdown Bro the prompt
        response = mdbro.send(project)
        
        # Write the response to an md file
        overwrite("output.md", response)

        # Extract the python and bash from the response
        python, cmd = extract(response)

        # Write the python and bash code to the corresponding files
        overwrite("cmd.bat", cmd)
        overwrite(filepath, python)

        # Run the files, save the outputs
        cmdout = run("cmd.bat")
        pyout = run(filepath)

    def conversation(self, bot_one: tuple, bot_two: tuple):

        name_one, premise_one = bot_one
        name_two, premise_two = bot_two

        one = EasyGPT(f"You are someone who {premise_one}, and you are debating someone that {premise_two}. The debate is turn-based, each person gets three sentence responses at a time")
        two = EasyGPT(f"You are someone who {premise_two}, and you are debating someone that {premise_one}. The debate is turn-based, each person gets three sentence responses at a time")

        cur_response =  one.send("You may start the debate.")

        for _ in range(10):

            with open("output.txt", "r+") as output_file:

                print(f"{name_one}: \n\n{cur_response}\n\n")
                cur_response = two.send(f"{output_file.read()}{cur_response}")
                output_file.write(f"{name_two}: \n\n{cur_response}\n\n")

            with open("output.txt", "r+") as output_file:

                print(f"{name_two}: \n\n{cur_response}\n\n")
                cur_response = one.send(f"{output_file.read()}{cur_response}")
                output_file.write(f"{name_one}: \n\n{cur_response}\n\n")

if __name__ == "__main__":

    my_agent = EasyAgent()
    # a = ("name", "premise")
    # b = ("name", "premise")
    my_agent.develop("project.py", "How would I create a project that acts as a custom GUI for a postgres database?")