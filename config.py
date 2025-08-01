from pathlib import Path

#File directory
CURRENT_PATH = Path(__file__).parent
HANDLERS_PATH = CURRENT_PATH / "handlers"
LOGS_PATH = CURRENT_PATH / "logs"
DIET_MODULE_PATH = CURRENT_PATH / "modules" / "diet_module"
FINANCES_MODULE_PATH = CURRENT_PATH / "modules" / "finances_module"
GOOGLE_CALENDAR_MODULE_PATH = CURRENT_PATH / "modules" / "google_calendar_module"
NOTION_MODULE_PATH = CURRENT_PATH / "modules" / "notion_module"
STUDY_MODULE_PATH = CURRENT_PATH / "modules" / "notion_module"
TESTS_PATH = CURRENT_PATH / "tests"
FILES_FINANCES_MODULE_PATH = FINANCES_MODULE_PATH / "files"