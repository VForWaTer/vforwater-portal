## Procceses structure

### Introduction
As there is no documentation about the OGC processes available yet (15.03.2023) and also hardly any examples, we started
to define our own process structure (based on hello world of pygeoapi), but extended if needed.
If you know any documentation/description/definition about the OGC processes please let us know.

### VFW implementation
```js
metadata = {
    'version': '0.2.0',
    'id': 'hello-world',
    'title': {
        'en': 'Hello World',
        'fr': 'Bonjour le Monde'
    },
    'description': {
        'en': 'An example process that takes a name as input, and echoes '
              'it back as output. Intended to demonstrate a simple '
              'process with a single literal input.',
        'fr': 'Un exemple de processus qui prend un nom en entrée et le '
              'renvoie en sortie. Destiné à démontrer un processus '
              'simple avec une seule entrée littérale.',
    },
    'keywords': ['hello world', 'example', 'echo'],
    'links': [{
        'type': 'text/html',
        'rel': 'about',
        'title': 'information',
        'href': 'https://example.org/process',
        'hreflang': 'en-US'
    }],
    'inputs': {
        'name': {
            'title': 'Name',
            'description': 'The name of the person or entity that you wish to'
                           'be echoed back as an output',
            'schema': {
                'type': 'string'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None,
            'keywords': ['full name', 'personal']
        },
        'message': {
            'title': 'Message',
            'description': 'An optional message to echo as well',
            'schema': {
                'type': 'string'
            },
            'minOccurs': 0,
            'maxOccurs': 1,
            'metadata': None,
            'keywords': ['message']
        }
    },
    'outputs': {
        'echo': {
            'title': 'Hello, world',
            'description': 'A "hello world" echo with the name and (optional)'
                           ' message submitted for processing',
            'keywords': ['pickle', 'html']
            'schema': {
                'type': 'object',
                'contentMediaType': 'application/json'
            },
            'source': { 'URI' }
        },
        'error': {
            'type': 'string',
            'description': 'Error occurred during process',
            'schema': {
                'type': 'object',
                'contentMediaType': 'application/json'
            },
        }
    },
    'example': {
        'inputs': {
            'name': 'World',
            'message': 'An optional message.',
        }
    }
}
```

```python
def execute(self, data):

        mimetype = 'application/json'
        name = data.get('name')

        ###
        # your function
        ###

        # outputs = {
        #     'id': 'echo',
        #     'value': 'your result'
        # }

        outputs = {
            'echo': {
                'value': 'your result',
                'URI': 'path to your result'
            },
            'error': {
                'value': 'your error message',
                'code': 'error code',
                'message': 'error message'
            }
        }

        return mimetype, outputs

```
