#!/usr/local/bin/python
import os
from concurrent.futures import ThreadPoolExecutor
import uuid
import pathlib

import pysparql_anything as sa

path = "C:\\repositories\\glashimer\\data\\input\\2023\\34xxx"
output_dir = "C:\\repositories\\glashimer\\data\\output\\2023\\34xxx"
temp_dir = "C:\\repositories\\glashimer\\.temp"
dir_list = os.listdir(path)


engine = sa.SparqlAnything()

def run_sparql_anything(location: str, output: str, query: str, format="ttl"):
    location = pathlib.PureWindowsPath(os.path.relpath(location)).as_posix()
    # location = os.path.relpath(location)
    print("- Running SPARQL Anything against file: " + location)
    # Create temporary file in '.temp/' containing replaced '$SA_INPUT_PATH' with input file location
    _file_contents = None
    with open(query, 'r') as _file:
        _file_contents = _file.read()
        
    _file_contents = _file_contents.replace("__PATH__", location)

    _temp_file_path = os.path.join(temp_dir, str(uuid.uuid4())+".sparql")
    try:
        with open(_temp_file_path, "w") as _file:
            _file.write(_file_contents)
        engine.run(
            q=_temp_file_path,
            f=format,
            o=output,
        )
    finally:
        os.remove(_temp_file_path)

    print("    [$]")
    return output



print("- Running files")
results = None

arguments = []
for _file_set in os.walk(path):
    (root, dirs, files) = _file_set
    for _file in files:
        _path = os.path.join(root, _file)
        _output_file = _file.rsplit('.')[0] + ".ttl"
        _output_path = os.path.join(output_dir,_output_file)
        _args = {
            "location":_path,
            "output": _output_path,
            "query": "C:\\repositories\\glashimer\\sparql-anything\\cve\\cve-json-2-rdf.sparql"
        }
        arguments.append(_args)

print(arguments)
with ThreadPoolExecutor(max_workers=2) as executor:
    for args in arguments:
        executor.submit(run_sparql_anything, **args)
    executor.shutdown(wait=True)



    

# engine = sa.SparqlAnything()
# engine.run(
#     q = "./sparql-anything/cve/cve-json-2-rdf.sparql",
#     f = "ttl",
#     o = "CVE-2023-51812.ttl",
#     l = "./data/input/2023/51xxx",
#  #   v = [location=dir_list]
# )

# for file in dir_list:
#    print(file)
