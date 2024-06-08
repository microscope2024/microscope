import logging
from pathlib import Path


class microscope:
    home = ""
    datalog_1_0 = ""
    datalog_script = ""
    language = ""
    lib = ""
    lib_1_0 = ""
    lib_script = ""
    version = ""

    def __init__(self, microscope_home):
        microscope.home = Path(microscope_home).expanduser().resolve()
        microscope.datalog_1_0 = microscope.home/"datalog-1.0"/"usr"/"bin"/"datalog"
        microscope.datalog_script = microscope.home/"datalog-script"/"usr"/"bin"/"datalog"
        microscope.language = microscope.home/"language"
        microscope.lib = microscope.home/"lib"
        microscope.lib_1_0 = microscope.home/"lib-1.0"
        microscope.lib_script = microscope.home/"lib-script"
        version_path = microscope.home/"version.txt"
        if version_path.exists():
            try:
                with open(version_path, "r") as f:
                    content = f.read()
                    microscope.version = content
            except PermissionError as pe:
                microscope.version = "no version file found!"
                logging.warning(f"can not open version.txt: {str(pe)}")
            except Exception as e:
                microscope.version = "no version file found!"
                logging.warning(f"can not get version: {str(e)}")
        else:
            microscope.version = "no version file found!"
            logging.warning("no version file found!")
