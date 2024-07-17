class Agent:
    def __init__(self, name):
        self.name = name
        self.system_prompt = self.get_system_prompt(name)

    def get_system_prompt(self, name):
        with open(f'agents/prompts/{name}/system_prompt.txt', 'r') as f:
            system_prompt = f.read()
        return system_prompt
