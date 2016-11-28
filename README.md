## Installation / Requirements
* python3, with dependencies listed in requirements.txt
* Add your API key to settings.py

## Commands
#### getplatemeta [-h] ref
* **ref:** (str) The plate reference for which you want meta-data

#### getqueues
* No arguments

#### setsamplequeue [-h] queue-id ref [ref ...]
* **queue-id:** (int) The id of the destination queue
* **ref:** (str) The sample reference(s) you wish to queue

#### setprojectresultspath [-h] ref path
* **ref:** (str) The project reference
* **path:** (str) The results data path (unique part)

#### updatesamples
* **ref** (str) The sample reference(s) you wish to update
* **-c, --suspected-contamination** (bool) Suspected sample contamination
Note: when updating boolean values you must specify both the option and the value: e.g., -c False
