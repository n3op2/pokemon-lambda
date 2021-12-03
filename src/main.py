import json
import os

from src.utils.request import Request
from src.utils.fibonacci import get_fibonacci
from typing import Dict

# create an instance of request for calling pokemon api
pokemon_api = Request(os.environ.get('POKEMON_API'))

# omit porperties that we are not intrested
def format_pokemon(pokemon: Dict):
    # check if exception and return stringified exception
    if isinstance(pokemon, Exception): return str(pokemon)

    return {
        'name': pokemon['name'],
        'abilities': list(map(lambda el: el['ability']['name'], pokemon['abilities']))
    }

def lambda_handler(event: Dict, context: Dict):
    try:
        if not 'id' in event['pathParameters']:
            raise ValueError('missing \'pathParameters.id\' property')
        id = event['pathParameters']['id']

        pokemon = pokemon_api.get('/pokemon/' + id)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'fibonacci': get_fibonacci(id),
                'pokemon': format_pokemon(pokemon),
            })
        }
        
    # exception will result in status 500 along with message
    except BaseException as err:
        return {
            'statusCode': 500,
            'body': str(err),
        }
