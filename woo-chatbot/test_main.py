#gotta pip install pytest to begin

from main import app
from fastapi.testclient import TestClient
client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message" : "API is running"
    }
    """
    Last assert statement above asserts the response status code and the json body
    only hardcode the response if you're sure the API 
    is supposed to return a constant response at the endpoint.. else see what we do 
    in the chat endpoint below"""

def test_chat():
    response = client.post("/chat", json={"prompt": "show me lipstick"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "products" in data
    assert isinstance(data["products"], list)
    #above line: “Make sure that data["products"] is a list.”
    '''if data["products"]:
        product = data["products"][0]
        for field in ("title", "price", "thumbnail", "url"):
            assert field in product'''
    """
    the lst if block above is only valid if the API is REQUIRED TO 
    always return a list of products with those values. But in this case, the 
    product list is optional, as API may return an empty list if product isn't available.
    """
#now we'll test to break the chat endpoint in this API
#do this by using the wrong request model
#or a different json key than defined in the ChatRequest model
#then we expect that the status code will be 404
def test_chat_to_break():
    response = client.post("/chat", json={"answer": "show me lipstick"})
    assert response.status_code == 422
    """Besides the 200 status code we expect to get when the endpoint exists and the 
    POST request is valid, we've also asserted that the status code =  404 
    when the requests format is wrong"""

"""pytest auto detects test files to run when you do: pytest -v only if your file starts
test. not test_main.py good ones: test.py, test_main.py, will run if you specify the name:
pytest -v filename.py but best to stick with the conventions here
"""
