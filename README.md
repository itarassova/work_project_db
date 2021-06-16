
**Online Lookup of Hazards for Chemical Compounds**

Given an inherent danger associated with many chemical reagents (flammability, toxicity, carcinogenicity etc), it is imperative for any scientists to consider the potential risks and the manner in which they can be mitigated for their own safety and the safety of others in the laboratory. The generation of a locally accessible database containing in-house chemicals and associated hazards would facilitate the risk assessment procedure before the reaction set-up.

**Pre-requisites**

Python libraries:

* openpyxl
*	sqlite3
*	flask

**Tutorial**

* **Download the repo**

* **Run importer.py**

This script uses in-house chemicals inventory in Excel spreadsheet containing both compound names and CAS numbers (unique numerical identifier assigned to every chemical substance in the open scientific literature) as an input file to populate output SQL database with chemicals’ names, CAS numbers and associated hazards. (The source for chemical hazards for compounds is PubChem, the lookup is by compound CAS number and name).

Input file formatting:

Compound name|Compound CAS number
-------------|-------------------
(R)-Tol-BINAP|99646-28-3


* **Run hello_world.py**

This script is responsible for the lookup of compounds of interest by CAS number or name in the populated database with autofill prompts generating output risk assessment form with compounds’ names and associated hazards.
