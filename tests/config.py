from pathlib import Path

TESTS_DIR = Path(__file__).parent
INPUT_FILES_DIR = TESTS_DIR / "input_files"
CONFIGS_DIR = INPUT_FILES_DIR / "configs"
PLAIN_CONFIGS_DIR = CONFIGS_DIR / "plain"
OVERRIDES_CONFIGS_DIR = CONFIGS_DIR / "overrides"

CONFIG_ONE = CONFIGS_DIR / "one.yaml"
