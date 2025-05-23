# Prompt user with enumerate options and validates input
def enumchoices(text: str, options: dict[str]) -> any:

    # Format the multiple choice options as index: option \n index: option...
    keys, fullprompt = [], ""

    for index, option in enumerate(options.keys()):
        keys.append((index, option))
        fullprompt += f"{index}: {option}\n"
    
    keys = dict(keys)

    ans = input(f"{text}\n{fullprompt}\n")

    # Prompt the user until the input is valid
    while not ans.isdigit() or not (0 <= int(ans) < len(options)):
        ans = input(f"Please choose a valid option:\n{fullprompt}")

    return options[keys[int(ans)]]

# Prompts user for a single input and ensures that the input meets all requirements
def prompt(text: str, **validations: any) -> str:

    # Return false if any validation test specified fails
    def validate(ans: str): 
        for test, value in validations.items():
            match test:
                # Ensures the input is of the type specified
                case "type":
                    try:
                        value(ans)
                    except:
                        return False
                # Ensures input is of the length specified
                case "length":
                    if len(ans) not in value:
                        return False
                # Ensures the value is within the range specified
                case "value":
                    if int(ans) not in value:
                        return False
                # Pass the input through a custom function and return the output
                case "custom":
                    return value(ans)
                    
        return True
    
    ans = input(f"{text}\n")

    # Prompt the user until the input meets all validations
    while not validate(ans):
        ans = input(f"Please enter a valid input:\n")

    return ans

# ---------------------------------------------------------------------------------------------------------------------

class UIComponent:

    """
    
    This is the parent class of all UIComponents, taking an id and keyword arguments.
    Takes optional positional arguments components and keyword arguments properties.

    *components = UIComponent subclass
    
    """

    def __init__(self, *components: object, **properties: any) -> None:
        self.components = components
        self.props = properties
        self.props['id'] = self.props.get('id') # Sets the id property to None by default

    # Indexing is used to retrieve properties safely
    def __getitem__(self, key: str) -> any:
        if key not in self.props:
            print(f"UIComponent KeyError: Missing {key} property of {type(self).__name__} component.")
        return self.props.get(key)
    
    def run(self) -> tuple[str, any]:
        pass

# ---------------------------------------------------------------------------------------------------------------------

class MenuDivider(UIComponent):

    """

        Params:
            id: str
            *components: UIComponent
            pass_values: callable
    
        The MenuDivider UIComponent runs each component within it and passes a tuple containing the output of each
        component to the specified pass_values function. Returns a tuple in the format (id: str, outputs: any)
    
    """

    def run(self) -> dict[str: any]:

        # Construct a selections dictionary in the from of {prompt_id: selection...}
        selections = dict()
        for ui in self.components:
            ui_output = ui.run()
            print(ui_output)
            selections.update(ui_output)

        # Format the output as (id, selections_dict) if there is an id
        output = {self['id']: selections} if self['id'] else selections

        # Pass the output to the pass_values function if it exists and return it
        if self['pass_values']:
            self['pass_values'](output)

        return output

# ---------------------------------------------------------------------------------------------------------------------

class MultipleChoice(UIComponent):

    """

        Params:
            id: str
            prompt: str
            options: dict[str: UIComponent | any]
    
        The MultipleChoice UIComponent presents a multiple choice prompt to the user.
        Returns a tuple in the format (id: str, selection: any).
    
    """

    def run(self) -> dict[str: any]:
        selection = enumchoices(self['prompt'], self['options'])
        # Run the selection before returning if it is a UICompnent
        if issubclass(type(selection), UIComponent):
            selection = selection.run()
        output = {self['id']: selection} if self['id'] else selection
        if self['pass_values']:
            self['pass_values'](output)
        return output

# ---------------------------------------------------------------------------------------------------------------------

class UserInput(UIComponent):

    """

        Params:
            id: str = None
            prompt: str
            **properties: any
    
        The UserInput UIComponent prompts the user for input and validates the input based on the properties passed.
        Returns a tuple in the format (id: str, ans: any).
    
    """
    
    # Prompts the user for input, validating with properties, returns id and input
    def run(self) -> dict[str: any]:
        ans = prompt(self['prompt'], **self.props)
        return {self['id']: ans} if self['id'] else ans

# ---------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    pass