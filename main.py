import logging
from pathlib import Path

from src.polygon.loaders import ConfigLoader
from src.polygon.models.simulation import SimulationConfig
from src.polygon.core import Simulation

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    base_dir = Path(__file__).parent
    config_path = base_dir / "examples" / "dough_branch.json"
    schema_path = base_dir / "src" / "polygon" / "schemas" / "simulation.schema.json"

    loader = ConfigLoader()
    raw_config = loader.load(str(config_path), str(schema_path))
    config = SimulationConfig.model_validate(raw_config)

    sim = Simulation(config)
    sim.run()

if __name__ == "__main__":
    main()