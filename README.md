# trello-export

There are existing Trello CLIs, e.g.

- mheap/trello-cli: Command line client for Trello https://github.com/mheap/trello-cli
- Trello Command Line Interface (CLI) - Confluence https://bobswift.atlassian.net/wiki/spaces/TCLI/overview
- qcam/3llo: 3llo - Trello interactive CLI aplication https://github.com/qcam/3llo
      
However, currently they do not seem to be able to export Trello boards to JSON. In the web UI, you can go to 
```
Board menu > More > Print and Export > JSON
```
to download JSON of the board. 

# Installation
```
pip install py-trello
git clone https://github.com/edtechhub/trello-export.git
cd trello-export
```
# Setup
Add the api_key in config.json. Can be found from https://trello.com/1/appKey/generate
```
./trello-export.py --help
./trello-export.py --authenticate
./trello-export.py --token TOKEN
```
# Usage

List boards (the above apps can do that)
```
trello-export --list
```

Export board as json
```
trello-export --board=board_id
```
or
```
trello-export --all
```

Note: You will get up to 1000 actions ('card history').

# Credits

This tool was developed by https://github.com/a1diablo with input from https://github.com/bjohas.
