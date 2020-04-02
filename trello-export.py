import os
from trello import TrelloClient
import requests
import json
import argparse
import datetime

TRELLO_JSON_URL = 'https://trello.com/1/boards/{}?key={}&token={}&fields=all&actions=all&action_fields=all&actions_limit={}&cards={}&card_fields=all&card_attachments=true&lists=all&list_fields=all&members=all&member_fields=all&checklists=all&checklist_fields=all&organization=false'

parser = argparse.ArgumentParser(description='Trello command line utility')
parser.add_argument('-A', '--authenticate', action='store_true', default=False)
parser.add_argument('-t', '--token', action='store', type=str)
parser.add_argument('-a', '--all', action='store_true', default=False)
parser.add_argument('-b', '--board', action='store', type=str)
parser.add_argument('-B', '--boards', action='store_true', default=False)
parser.add_argument('-f', '--filter', action='store', type=str)
parser.add_argument('-u', '--user', action='store', type=str)


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

    def save_json_to_file(self, content, file_name):
        with open(file_name, 'w') as f:
            json.dump(content, f)

    def to_json(self):
        all_boards = self.client.list_boards()
        resp = []
        for board in all_boards:
            resp.append(self.board_to_json(board.id))
        return resp

    def board_to_json(self, board_id, actions=1000, cards='all'):
        board_resp = requests.get(TRELLO_JSON_URL.format(
            board_id, self.api_key, self.token, actions, cards))
        actions_retrieved = board_resp.json()['actions']
        if len(actions_retrieved) > 1000:
            print('More than 1000 actions. Truncating to recent 1000.')

        response = board_resp.json()
        return response

    def list_boards(self):
        for board in self.client.list_boards():
            print('{}: {}'.format(board.id, board.name))

    def get_filters_from_file(self, filter_file):
        with open(filter_file) as f:
            content = f.readlines()
        filters = [(c.split(' ')[0].strip(), ' '.join(c.split(' ')[1:]).strip())
                   for c in content]
        return filters

    def get_cards(self, board_id, trello_list=None, user=None):
        board = self.board_to_json(board_id, actions=0, cards='visible')
        all_cards = board.get('cards')
        if trello_list:
            found = False
            for found_list in filter(
                    lambda item: item.get('name') == trello_list, board.get('lists')):
                found = True
                all_cards = list(filter(
                    lambda item: item.get('idList') == found_list.get('id'), all_cards))
            if not found:
                all_cards = []

        if user:
            found = False
            for found_user in filter(lambda item: item.get(
                    'username') == user, board.get('members')):
                found = True
                all_cards = list(filter(lambda item: found_user.get(
                    'id') in item.get('idMembers'), all_cards))
            if not found:
                all_cards = []

        return all_cards


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
        output = None
        output_file = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        if arguments.all:
            output = trello_export.to_json()
            output_file = "all_{}.json".format(output_file)

        elif arguments.board:
            output = trello_export.board_to_json(arguments.board)
            output_file = "{}_{}.json".format(arguments.board, output_file)

        elif arguments.boards:
            trello_export.list_boards()

        elif arguments.filter:
            filters = trello_export.get_filters_from_file(arguments.filter)
            output = []
            for (board_id, list_name) in filters:
                output += trello_export.get_cards(
                    board_id, list_name, arguments.user)
            output_file = "{}_{}.json".format(arguments.filter, output_file)

        if output:
            trello_export.save_json_to_file(output, output_file)
