# trello-export

There are existing Trello CLIs, e.g.

      mheap/trello-cli: Command line client for Trello
      https://github.com/mheap/trello-cli

      Trello Command Line Interface (CLI) - Confluence
      https://bobswift.atlassian.net/wiki/spaces/TCLI/overview

      qcam/3llo: 3llo - Trello interactive CLI aplication
      https://github.com/qcam/3llo
      
However, currently they do not seem to be able to export Trello boards to JSON. In the web UI, I can go to 
```
Board menu > More > Print and Export > JSON
```
to download JSON of the board. 

We'd like to build an app that works as follows:

(1) Authenticate:
```
trello-export authenticate
```
(This could be via an API key stored in a file, whatever is easiest)

(2) List boards (the above apps can do that)
```
trello-export boardlist
```

(3) Export board as json
```
trello-export export --board=board_id
```
or
```
trello-export export --all
```

(4) It would be good to be able to export assests as well (such as attached images or files)
```
trello-export export --board=board_id --includeAttachments
```

What programming language should this use?
==========================================

Ideally this would be an extension to the existing tools above. Node/typescript/python would all be ok.
