class GeneratorAgent(BaseAgent):
    def generate(self, state):
        prompt = build_generator_prompt(state)
        return self.llm.generate(prompt)