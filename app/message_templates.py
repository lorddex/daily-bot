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


def build_daily_report_message(messages):
    blocks = []
    list_elements = []
    date = None
    for m in messages:
        t_date = m.created.strftime("*%a %d/%m/%Y*")
        if date is None or date != t_date:
            if date != t_date:
                blocks.append(
                    {
                        'type': 'rich_text',
                        'elements': [
                            {
                                'type': 'rich_text_list',
                                'elements': list_elements,
                                'style': 'bullet',
                                'indent': 0,
                            },
                        ],
                    })
                list_elements = []
            date = t_date
            blocks.append(
                build_section_plain_text(date)
            )
        list_elements.append(
            {
                'type': 'rich_text_section',
                'elements': m.message,
            }
        )
    blocks.append(
        {
            'type': 'rich_text',
            'elements': [
                {
                    'type': 'rich_text_list',
                    'elements': list_elements,
                    'style': 'bullet',
                    'indent': 0,
                },
            ],
        })
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