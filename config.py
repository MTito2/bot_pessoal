from pathlib import Path

ROOT_PATH = Path(__file__).parent
HANDLERS_PATH = ROOT_PATH / "handlers"
LOGS_PATH = ROOT_PATH / "logs"
DIET_MODULE_PATH = ROOT_PATH / "modules" / "diet_module"
FINANCES_MODULE_PATH = ROOT_PATH / "modules" / "finances_module"
AGENDA_MODULE_PATH = ROOT_PATH / "modules" / "agenda_module"
NOTION_MODULE_PATH = ROOT_PATH / "modules" / "notion_module"
STUDY_MODULE_PATH = ROOT_PATH / "modules" / "study_module"
BOOKS_MODULE_PATH = ROOT_PATH / "modules" / "books_module"
TESTS_PATH = ROOT_PATH / "tests"
WORKOUT_MODULE_PATH = ROOT_PATH / "modules" / "workout_module"
RUN_SUB_MODULE_PATH = WORKOUT_MODULE_PATH / "run_sub-module"

FILES_ROOT_PATH = ROOT_PATH / "general_files"
FILES_FINANCES_MODULE_PATH = FINANCES_MODULE_PATH / "files"
FILES_STUDY_MODULE_PATH = STUDY_MODULE_PATH / "files"
FILES_RUN_SUB_MODULE_PATH = RUN_SUB_MODULE_PATH / "files"
FILES_AGENDA_MODULE_PATH = AGENDA_MODULE_PATH / "files"
FILES_BOOKS_MODULE = BOOKS_MODULE_PATH / "files"
FILES_TESTS = TESTS_PATH / "files"


