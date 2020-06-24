#  Daily-Bot
#  Copyright (C) 2020  Francesco Apollonio
#
#  This file is part of Daily-Bot.
#  Daily-Bot is free software:
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.


def build_link(link, text):
    return {
        'type': 'link',
        'url': link,
        'text': text,
    }


def build_text(message):
    return {
            "type": "text",
            "text": message,
        }


def build_bloc_section_plain_text(message):
    return {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": message,
                        "emoji": True
                    }
                }
            ]
        }


def build_section_plain_text(text):
    return {
        "type": "section",
        "fields": [
            {
                "type": "plain_text",
                "text": text,
                "emoji": True
            }
        ]
    }


def build_rich_text_rich_text_list(list_elements):
    return {
        'type': 'rich_text',
        'elements': [
            {
                'type': 'rich_text_list',
                'elements': list_elements,
                'style': 'bullet',
                'indent': 0,
            },
        ],
    }


def build_daily_report_message(messages):
    blocks = []
    list_elements = []
    date = None
    for m in messages:
        t_date = m['message'].created.strftime("%a %d/%m/%Y")
        if date is None or date != t_date:
            if date != t_date:
                blocks.append(build_rich_text_rich_text_list(list_elements))
                list_elements = []
            date = t_date
            blocks.append(
                build_section_plain_text(date)
            )
        list_elements.append(
            {
                'type': 'rich_text_section',
                'elements': m['elements'],
            }
        )
    blocks.append(build_rich_text_rich_text_list(list_elements))
    response_message = {
        'blocks': blocks
    }
    return response_message


# not currently used
def build_attachment_buttons():
    return {
        'attachments': [
            {
                'fallback': 'Would you like to remove the stored messages?',
                'title': 'Would you like to remove the stored messages?',
                'callback_id': 'daily_0000_remove_messages',
                'color': '#3AA3E3',
                'attachment_type': 'default',
                'actions': [
                    {
                        'name': 'delete',
                        'text': 'Yes, delete them!',
                        'type': 'button',
                        'value': 'delete'
                    },
                    {
                        'name': 'no',
                        'text': 'No',
                        'type': 'button',
                        'value': 'no'
                    }
                ]
            }
        ],
    }