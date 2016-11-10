## Installation / Requirements
* python3, with dependencies listed in requirements.txt
* Add your API key to settings.py

## Commands
#### getplatemeta [-h] ref
* **ref:** (str) The plate reference for which you want meta-data

#### setsamplequeue [-h] queue-id ref [ref ...]
* **queue-id:** (int) The id of the destination queue
* **ref:** (str) The sample references you wish to queue

#### setprojectresultspath [-h] ref path
* **ref:** (str) The project reference
* **path:** (str) The results data path (unique part)

#### getqueues
* No arguments

