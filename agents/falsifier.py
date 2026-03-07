class FalsifierAgent(BaseAgent):
    def analyze(self, state):
        prompt = build_falsifier_prompt(state)
        return self.llm.generate(prompt)