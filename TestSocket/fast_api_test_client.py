import requests

#gettin stuff from the API
def main():
    response = requests.get(url="http://127.0.0.1:8000/test_data/get_generated_data")
    print(response.text)
main()