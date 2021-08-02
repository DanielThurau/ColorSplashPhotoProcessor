import json


from src import app

def test_lambda_handler(mocker):

    ret = app.lambda_handler({}, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
