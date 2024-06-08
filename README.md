# Microscope: A Data-Centric Static Code Analysis System

## What is Microscope?
In the domain of large-scale software development, the demands for dynamic and multifaceted static code analysis exceed the capabilities of traditional tools. To bridge this gap, we present Microscope, a system that redefines static code analysis through the fusion of Domain Optimized System Design and Logic Oriented Computation Design.
Microscope reimagines code analysis as a data computation task, support scanning over 10 billion lines of code daily and more than 300 different tasks. It optimizes resource utilization, prioritizes data reusability, applies incremental code extraction, and introduces tasks types specially for Code Change, underscoring its domain-optimized design. The system's logic-oriented facet employs Datalog, convert source code into data facts. Through datalog, Microscope enables formulation of complex tasks as logical expressions, harnessing Datalog's declarative prowess.

## Supported Programming Languages for Analysis
As of now, Microscope supports data analysis for 9 programming languages. Among them, support for 5 languages (Java, TS/JS, XML, Go, Python) is very mature, while the remaining 4 languages (Cfamily, Swift, SQL, Properties) are in beta stage and have room for further improvement and perfection. The specific support status is shown in the table below:

| Language | Status | MICROSCOPE Model Node Count |
| --- | --- | --- |
| Java | Mature | 162 |
| XML | Mature | 12 |
| TS/JS | Mature | 392 |
| Go | Mature | 40 |
| Python | Mature | 93 |
| Cfamily | Beta | 53/397 |
| Swift | Beta | 248 |
| SQL | Beta | 750 |
| Properties | Beta | 9 |


## Directory Structure Description
- `cli`: The entry point for the command-line tool, providing a unified command-line interface, calling other modules to complete specific functions
- `examples`: Datalog-based query language examples
- `language`: Core data and data modeling (lib) for various languages. Regarding the degree of openness, please refer to the section "Some Notes on the Scope of Open Source", consists of datalog rules.


## Some Notes on the Scope of Open Source
As of now, it is **not possible** to build an executable program from the source code because not all modules have been made open-source in this release, and missing modules will be released over the next year. Nevertheless, to ensure a complete experience, we have released **complete installation packages** for download, please see the Release page.
Regarding the openness of languages, you can refer to the table below:

| Language | Data Modeling Open Source | Data Core Open Source | Maturity |
| --- | --- | --- | --- |
| Python | Y | Y | RELEASE |
| Java | Y | N | RELEASE |
| TS/JS | Y | N | RELEASE |
| Go | Y | N | RELEASE |
| XML | Y | N | RELEASE |
| Cfamily | Y | N | BETA |
| SQL | Y | N | BETA |
| Swift | Y | N | BETA |
| Properties | Y | N | BETA |
