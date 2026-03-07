class HypothesisScorer:
    def __init__(self, novelty, consistency, plausibility):
        self.novelty = novelty
        self.consistency = consistency
        self.plausibility = plausibility

    def evaluate(self, state):
        return {
            "novelty": self.novelty.compute(state),
            "consistency": self.consistency.compute(state),
            "plausibility": self.plausibility.compute(state),
            "final_score": self._aggregate(...)
        }