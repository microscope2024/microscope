import logging
import tempfile
import time
from pathlib import Path

from run.runner import Runner
from microscope_schema.schema import microscope


def datalog_version_judge(path) -> str:
    result = "script"
    try:
        with open(path, "r") as f:
            tmp = f.readline()
            if "1.0" in tmp:
                result = "1.0"
    except Exception as e:
        logging.error(f"datalog version judge error: {str(e)}")
    return result


def get_datalog_compile(path):
    version = datalog_version_judge(path)
    datalog = ""
    if version == "1.0":
        datalog = microscope.datalog_1_0
    elif version == "script":
        datalog = microscope.datalog_script
    return datalog


def backend_execute(path, database, output, timeout, output_format, verbose):
    datalog = get_datalog_compile(path)
    version = datalog_version_judge(path)
    cmd = list()
    cmd += [str(datalog), str(path), "--run-souffle-directly", "--package-path"]
    cmd += [str(microscope.lib_1_0)]
    if database is not None:
        cmd += ["--souffle-fact-dir", database]
    cmd += ["--souffle-output-format", output_format, "--souffle-output-path", output]
    if verbose:
        cmd += ["--verbose"]
    tmp = Runner(cmd, timeout)
    return tmp.subrun()


def execute(path, database, output, timeout, output_format, verbose):
    datalog = get_datalog_compile(path)
    version = datalog_version_judge(path)
    cmd = list()
    if version == "script":
        with tempfile.NamedTemporaryFile(suffix='.gdl') as temp_file:
            cmd += [str(datalog), str(path), "-p", str(microscope.lib_1_0), "-o", temp_file.name]
            if verbose:
                cmd += ["--verbose"]
            tmp = Runner(cmd, timeout)
            start_time = time.time()
            return_code = tmp.subrun()
            if return_code != 0:
                logging.error("%s compile error, please check it yourself", str(path))
                return -1
            logging.info("datalog-script compile time: %.2fs", time.time() - start_time)
            return backend_execute(Path(temp_file.name), database, output, timeout, output_format, verbose)
    else:
        return backend_execute(path, database, output, timeout, output_format, verbose)
