from pathlib import Path

#File directory
ROOT_PATH = Path(__file__).parent
FILES_ROOT_PATH = ROOT_PATH / "general_files"
HANDLERS_PATH = ROOT_PATH / "handlers"
LOGS_PATH = ROOT_PATH / "logs"
DIET_MODULE_PATH = ROOT_PATH / "modules" / "diet_module"
FINANCES_MODULE_PATH = ROOT_PATH / "modules" / "finances_module"
FILES_FINANCES_MODULE_PATH = FINANCES_MODULE_PATH / "files"
GOOGLE_CALENDAR_MODULE_PATH = ROOT_PATH / "modules" / "google_calendar_module"
NOTION_MODULE_PATH = ROOT_PATH / "modules" / "notion_module"
STUDY_MODULE_PATH = ROOT_PATH / "modules" / "study_module"
FILES_STUDY_MODULE_PATH = STUDY_MODULE_PATH / "files"
TESTS_PATH = ROOT_PATH / "tests"
