class DebateCoordinator:
    def __init__(
        self,
        generator,
        falsifier,
        refiner,
        simulator,
        scorer,
        memory_manager,
        retriever
    ):
        self.generator = generator
        self.falsifier = falsifier
        self.refiner = refiner
        self.simulator = simulator
        self.scorer = scorer
        self.memory = memory_manager
        self.retriever = retriever

    def run(self, query: str):
        context = self.retriever.retrieve(query)
        state = DebateState(query, context)

        # Round 1
        state.initial_hypothesis = self.generator.generate(state)

        # Round 2
        state.falsification_report = self.falsifier.analyze(state)

        # Round 3
        state.refined_hypothesis = self.refiner.refine(state)

        # Simulation
        state.simulation_results = self.simulator.run(state)

        # Scoring
        state.scores = self.scorer.evaluate(state)

        # Store memory
        self.memory.store(state)

        return state