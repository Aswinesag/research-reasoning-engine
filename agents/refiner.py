class RefinerAgent(BaseAgent):
    def refine(self, state):
        prompt = build_refiner_prompt(state)
        return self.llm.generate(prompt)