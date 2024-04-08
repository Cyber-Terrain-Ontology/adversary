REM script to sparql-anything

rem make a copy of the input json, and rename it to my-input.json

copy .\data\input\%1.json .\data\input\my-input.json 

rem execute the sparql-anything script

java -jar .\sparql-anything-0.8.1.jar -q .\sparql-anything\stix\%1.sparql -o .\data\output\%1.ttl


rem  delete the my-input.json file.

del .\data\input\my-input.json