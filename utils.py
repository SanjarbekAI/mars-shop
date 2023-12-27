import requests

async def next_product(products, index):
    try:
        return products[index + 1]
    except IndexError:
        return False


async def previous_product(products, index):
    try:
        if index == 0:
            return False
        return products[index - 1]
    except IndexError:
        return False

def login_def(login, password):
    url = 'https://api.marsit.uz/api/v1/auth/signin'
    payload = {
        "student": {
            "external_id": login,
            "code": f"{password}",
            "role": "student"
        }
    }
    response = requests.post(url=url, json=payload)
    if response.status_code == 200:
        return f"{response.json()['user']['first_name']} {response.json()['user']['last_name']}"
    return False