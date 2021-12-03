# Pokemon and Fibonacci lambda function
A python implementation of AWS API Gateway proxy to the lambda function. Attempted to use [serverless framework](https://www.serverless.com/) but it was not a very friendly as AWS SAM when it comes to python run times and a lot of JS dependencies e.g. node/serverless, etc so switched back to AWS SAM. This lambda function returns a pokemon and a Fibonacci number. If there is a server error expect status to be 500, otherwise it should return 200 even if no pokemon found or fibonacci could not be found.

### Local Setup
```sh
# 1. make sure you have got pipenv installed if - run the below command
pip install pipenv
# 2. to install required packages
pipenv install
# 3. setup aws-sam-cli if you already don't have -> https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html
brew tap aws/tap
brew install aws-sam-cli
# 4. start stack locally
sam local start-api
# should see something like:
Mounting PokemonFibFunction at http://127.0.0.1:3000/pokemon-fib/{id} [GET]
# test command
$ curl -i -X GET http://localhost:3000/pokemon-fib/20
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 97
Server: Werkzeug/1.0.1 Python/3.8.12
Date: Fri, 03 Dec 2021 19:31:24 GMT
$ {"fibonacci": 6765, "pokemon": {"name": "raticate", "abilities": ["run-away", "guts", "hustle"]}
```

### Utils
##### There are two primary utils
- `src/utils/Fibonacci - for find a number of Fibonacci sequence
- `src/utils/requests` - this is a `requests` wrapper for better error handling, the idea was to create a `pokemon_api` but since we are using basic operations decided to leave it as a wrapper as it can be used for calling other API services

### Unit tests
Unit tests do lack coverage as I was having a little difficult time switching from the `jest` mindset to `pytest or `unittests`. Especially mocking up classes and functions/modules. Thisdefinitelyitelly would need to be improved. In order to run unit tests please run the below command
```sh
# make sure you have installed dependencies `pipenv install`
pythond3.7 -m pytest tests/ -vv

# example output
collected 9 items                                                                                                      

tests/test_main.py::test_lambda_handler_success PASSED                                                           [ 11%]
tests/test_main.py::test_lambda_handler_pokemon_not_found PASSED                                                 [ 22%]
tests/test_main.py::test_lambda_handler_pokemon_and_fibonaci_throws PASSED                                       [ 33%]
tests/test_main.py::test_lambda_handler_invalid_payload PASSED                                                   [ 44%]
tests/test_utils.py::test_get_fibonacci PASSED                                                                   [ 55%]
tests/test_utils.py::test_requests_wrapper_constructor PASSED                                                    [ 66%]
tests/test_utils.py::test_requests_wrapper_custom_headers PASSED                                                 [ 77%]
tests/test_utils.py::test_requests_get_method PASSED                                                             [ 88%]
tests/test_utils.py::test_requests_http_errors PASSED                                                            [100%]

================================================== 9 passed in 0.22s ===================================================
```

### Endpoints
* `/pokemon-fib/{id}` - GET - Take an id parameter which is also a fibonacci sequence index and return pokemon along with fibonacci. Response examples below:
```json
/* success */
{
    "fibonacci": 1,
    "pokemon": {
        "name": "ivysaur", 
        "abilities": ["overgrow", "chlorophyll"]
    }
}
/* id is not a number */
{
    "fibonacci": 0,
    "pokemon": "404 Client Error: Not Found for url: https://pokeapi.co/api/v2/pokemon/ab"
}
/* if no pokemon for id */
{
    "fibonacci": 17937362957614421485739794629281840208175624583257624165255681705328503542086633274122020296761574501458809301757594224667177036805013875010136580659797337792159160128372409395301179947004818874853960353968895662597604808775540855458,
    "pokemon": "404 Client Error: Not Found for url: https://pokeapi.co/api/v2/pokemon/1113"
}
```

## TODO
- [ ] - environment variables for test/prod/local
- [ ] - expand unit tests coverage
- [ ] - refactor `format_pokemon()` function
- [ ] - figure out a way of persisting cache so during cold starts it won't reset
- [ ] - error class so each unknown exception can be clearly defined
- [ ] - *build and deployment scripts
