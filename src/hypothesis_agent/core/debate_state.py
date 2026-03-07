class DebateState:
    def __init__(self, query: str, context: list[str]):
        self.query = query
        self.context = context
        self.initial_hypothesis = None
        self.falsification_report = None
        self.refined_hypothesis = None
        self.simulation_results = None
        self.scores = {}