from src.main import lambda_handler

if __name__ == '__main__':
    event = {
        'pathParameters': { 'id': '200' },
    }

    print(lambda_handler(event, {}))
