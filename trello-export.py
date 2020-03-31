import os
from trello import TrelloClient
import requests
import json
import argparse

TRELLO_JSON_URL = 'https://trello.com/1/boards/{}?key={}&token={}&fields=all&actions=all&action_fields=all&actions_limit=1000&cards=all&card_fields=all&card_attachments=true&lists=all&list_fields=all&members=all&member_fields=all&checklists=all&checklist_fields=all&organization=false'

parser = argparse.ArgumentParser(description='Trello command line utility')
parser.add_argument('-l', '--authenticate', action='store_true', default=False)
parser.add_argument('-t', '--token', action='store', type=str)
parser.add_argument('-a', '--all', action='store_true', default=False)
parser.add_argument('-b', '--board', action='store', type=str)
parser.add_argument('--list', action='store_true', default=False)


class Auth:
    @classmethod
    def authenticate(cls):
        config = json.load(open('./config.json'))
        api_key = config.get('api_key')
        auth_url = 'https://trello.com/1/authorize?expiration=30days&name=TrelloExport&scope=read,write&response_type=token&key={}'.format(
            api_key)
        print('Please visit the url: \n\n{}\nand run \n\ntrello-export --token <token>'.format(auth_url))

    @classmethod
    def set_token(cls, token):
        config = json.load(open('./config.json'))
        config['token'] = token
        with open('config.json', 'w') as f:
            json.dump(config, f)
        print('Token set successfully')


class TrelloExport:
    def __init__(self):
        config = json.load(open('./config.json'))
        self.api_key = config.get('api_key')
        self.token = config.get('token')
        self.client = TrelloClient(
            api_key=self.api_key,
            token=self.token
        )

    def to_json(self):
        all_boards = self.client.list_boards()
        for board in all_boards:
            self.board_to_json(board.id)

    def board_to_json(self, board_id):
        board_resp = requests.get(TRELLO_JSON_URL.format(
            board_id, self.api_key, self.token))
        actions = board_resp.json()['actions']
        print('actions size: ', len(actions))
        if len(actions) > 1000:
            print('More than 1000 actions. Truncating to recent 1000.')
        with open('{}.json'.format(board_id), 'w') as f:
            json.dump(board_resp.json(), f)

    def list_boards(self):
        for board in self.client.list_boards():
            print('{}: {}'.format(board.id, board.name))


if __name__ == "__main__":
    arguments = parser.parse_args()
    if arguments.authenticate:
        print('Authenticate request')
        Auth.authenticate()

    elif arguments.token:
        print('Setting token in config')
        Auth.set_token(arguments.token)

    else:
        trello_export = TrelloExport()
        if arguments.all:
            trello_export.to_json()

        elif arguments.board:
            trello_export.board_to_json(arguments.board)

        elif arguments.list:
            trello_export.list_boards()
