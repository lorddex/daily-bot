def build_link(link, text):
    return {
        'type': 'link',
        'url': link,
        'text': text,
    }


def build_simple_text(message):
    return {
            "type": "text",
            "text": message,
        }


def build_section_with_text(message):
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


def build_daily_report_message(messages):
    message_list = []
    for m in messages:
        message_list.append(
            {
                'type': 'rich_text_section',
                'elements': m.message,
            }
        )
    response_message = {
        'blocks': [
            {
                'type': 'rich_text',
                'elements': [
                    {
                        'type': 'rich_text_list',
                        'elements': message_list,
                        'style': 'bullet',
                        'indent': 0,
                    },
                ],
            },
        ]
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