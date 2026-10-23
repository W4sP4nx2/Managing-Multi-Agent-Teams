"""Run the no-cost simulation; 'live' describes terminal presentation only."""
from pathlib import Path
import time

from orchestrator import main, terminal_approval
from software_factory.workflow import FactoryOrchestrator


class DeterministicLiveDemo(FactoryOrchestrator):
    """Named teaching facade over the same tested approval and publication flow."""

    def __init__(self, workspace=Path("output/software-factory"), *,
                 publish_path=Path("index.html"), approval=terminal_approval, **kwargs):
        super().__init__(workspace, publish_path=publish_path, approval=approval, **kwargs)
        self.approval_required = True

    @property
    def total_simulated_cost(self):
        return self.costs.total_simulated_cost

    def simulate_thinking(self, agent_name: str, duration: float = 1.5):
        """Presentation delay only; never an actual model-thinking claim."""
        if not 0 <= duration <= 10:
            raise ValueError("Presentation delay must be between 0 and 10 seconds")
        self.emit(f"[{agent_name}] Simulated work indicator; no API call.")
        time.sleep(duration)

    def build_travel_website_demo(self):
        return self.run()


if __name__ == "__main__":
    raise SystemExit(main())
