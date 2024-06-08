import logging

import psutil

from run.runner import Runner
from microscope_schema.schema import microscope


class Extractor:
    
    cfamily_extractor = ""
    go_extractor = ""
    java_extractor = ""
    javascript_extractor = ""
    properties_extractor = ""
    python_extractor = ""
    sql_extractor = ""
    swift_extractor = ""
    xml_extractor = ""

    def __init__(self):
        Extractor.cfamily_extractor = microscope.home / "language" / "cfamily" / "extractor" / "usr" / "bin" / "microscope-cfamily-src-extractor"
        Extractor.go_extractor = microscope.home / "language" / "go" / "extractor" / "microscope-go-src-extractor"
        Extractor.java_extractor = microscope.home / "language" / "java" / "extractor" / "microscope-java-src-extractor_deploy.jar"
        Extractor.javascript_extractor = microscope.home / "language" / "javascript" / "extractor" / "microscope-javascript-src-extractor"
        Extractor.properties_extractor = microscope.home / "language" / "properties" / "extractor" / "microscope-properties-src-extractor_deploy.jar"
        Extractor.python_extractor = microscope.home / "language" / "python" / "extractor" / "microscope-python-src-extractor"
        Extractor.sql_extractor = microscope.home / "language" / "sql" / "extractor" / "microscope-sql-src-extractor_deploy.jar"
        Extractor.swift_extractor = microscope.home / "language" / "swift" / "extractor" / "usr" / "bin" / "microscope-swift-src-extractor"
        Extractor.xml_extractor = microscope.home / "language" / "xml" / "extractor" / "microscope-xml-extractor_deploy.jar"


def cfamily_extractor_cmd(source_root, database, options):
    return [
        str(Extractor.cfamily_extractor),
        f"--compile-commands={source_root}",
        f"--output-db-path={database}"
    ]


def go_extractor_cmd(source_root, database, options):
    cmd = list()
    cmd += [str(Extractor.go_extractor)]
    if options:
        for (key, value) in options.items():
            if key == "extract-config":
                for tmp in value.split(","):
                    cmd += ["-ex", tmp]
            elif key == "go-build-flag":
                for tmp in value.split(","):
                    cmd += [tmp]
            else:
                logging.warning("unsupported config name: %s for Go extractor.", key)
    cmd += ["-o", str(database/"microscope_go_src.db")]
    cmd += [str(source_root)]
    return cmd


def java_extractor_cmd(source_root, database, options):
    cmd = list()
    cmd += jar_extractor_cmd(Extractor.java_extractor, source_root, database)
    if options:
        for (key, value) in options.items():
            if key == "white-list" or key == "whiteList":
                cmd += ["-w=", value]
            elif key == "cp":
                cmd += ["-cp=", value]
            elif key == "classpath":
                cmd += ["--classpath=", value]
            elif key == "incremental":
                if value == "true":
                    cmd += ["--incremental"]
                    cmd += ["--cache-dir=" + options.get("cache-dir", "null")]
                    cmd += ["--commit=" + options.get("commit", "null")]
                    cmd += ["--remote-cache-type=" + options.get("remote-cache-type", "null")]
                    cmd += ["--oss-bucket=" + options.get("oss-bucket", "null")]
                    cmd += ["--oss-config-file=" + options.get("oss-config-file", "null")]
                    cmd += ["--oss-path-prefix=" + options.get("oss-path-prefix", "null")]
                else:
                    logging.warning("java.incremental does not take effect, please use java.incremental=true")
            else:
                if key != "cache-dir" and key != "commit" and key != "remote-cache-type" and \
                        key != "oss-bucket" and key != "oss-config-file" and key != "oss-path-prefix":
                    logging.warning("unsupported config name:%s for java extractor.", key)
    if "incremental" not in options or options["incremental"] != "true":
        cmd += ["--parallel"]
    return cmd


def javascript_extractor_cmd(source_root, database, options):
    cmd = list()
    cmd += [str(Extractor.javascript_extractor), "extract"] + \
           ["--src", str(source_root)] + \
           ["--db", str(database/"microscope_javascript_src.db")]
    if options:
        for (key, value) in options.items():
            if key == "black-list" or key == "blacklist":
                cmd += ["--blacklist"]
                for tmp in value.split(','):
                    cmd += [tmp]
            elif key == "use-gitignore":
                if value == "true":
                    cmd += ["--use-gitignore"]
                else:
                    logging.warning("javascript.use-gitignore does not take effect, please use "
                                    "javascript.use-gitignore=true")
            elif key == "extract-dist":
                if value == "true":
                    cmd += ["--extract-dist"]
                else:
                    logging.warning("javascript.extract-dist does not take effect, please use "
                                    "javascript.extract-dist=true")
            elif key == "extract-deps":
                if value == "true":
                    cmd += ["--extract-deps"]
                else:
                    logging.warning("javascript.extract-deps does not take effect, please use "
                                    "javascript.extract-deps=true")
            elif key == "file-size-limit":
                cmd += ["--file-size-limit", value]
            else:
                logging.warning("unsupported config name:%s for javascript extractor.", key)
    return cmd


def properties_extractor_cmd(source_root, database, options):
    cmd = jar_extractor_cmd(Extractor.properties_extractor, source_root, database)
    return cmd


def python_extractor_cmd(source_root, database, options):
    cmd = list()
    cmd += [str(Extractor.python_extractor), "-s", str(source_root), "-d", str(database)]
    return cmd


def sql_extractor_cmd(source_root, database, options):
    cmd = list()
    cmd += jar_extractor_cmd(Extractor.sql_extractor, source_root, database)
    if "sql-dialect-type" in options:
        cmd += ["--sql-dialect-type", options["sql-dialect-type"]]
    return cmd


def swift_extractor(source_root, database, options):
    cmd = list()
    cmd += [str(Extractor.swift_extractor), str(source_root), str(database)]
    if options:
        for (key, value) in options.items():
            if key == "corpus":
                for tmp in value.split(","):
                    cmd += ["--corpus", tmp]
            else:
                logging.warning("unsupported config name:%s for Swift extractor.", key)
    return cmd


def xml_extractor_cmd(source_root, database, options):
    cmd = jar_extractor_cmd(Extractor.xml_extractor, source_root, database)
    return cmd


def jar_extractor_cmd(extractor_path, source_root, database):
    mem = psutil.virtual_memory()
    total_memory = mem.total
    total_memory_gb = round(total_memory / (1024 ** 3))
    logging.info("current memory is : %s GB", total_memory_gb)
    xmx = max(total_memory_gb - 1, 6)
    logging.info("final -Xmx is: %s GB", xmx)
    cmd = list()
    cmd += ["java", "-jar", "-Xmx" + str(xmx) + "g", str(extractor_path)]
    cmd += [str(source_root), str(database)]
    return cmd


def extractor_run(language, source_root, database, timeout, options):
    function_name = language + "_extractor_cmd"
    if function_name in globals():
        function = globals()[function_name]
        cmd = function(source_root, database, options)
        if cmd == -1:
            logging.error("option error")
            logging.error("Failed to obtain the %s extractor", language)
            return -1
        tmp = Runner(cmd, timeout)
        return tmp.subrun()
    else:
        logging.error("Not supported language: %s", language)
        return -1

