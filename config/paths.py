import pathlib

CONFIG = pathlib.Path(__file__).parent
PROJECT = CONFIG.parent
DATA_DIR = PROJECT / "data"
SINGLE_PARTICLE_FILE = DATA_DIR / "01_raw" / "S_random_1.xyz"
PARTICLES_FILE = DATA_DIR / "01_raw" / "S_random_8000.xyz"
TRANSPORT_FILE = DATA_DIR / "01_raw" / "S_random_8000.trans"
FEATURES_CACHE = DATA_DIR / "02_features" / "particle"
