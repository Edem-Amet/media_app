from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)



# ==========================
# ROOT TEST
# ==========================

def test_root():

    res = client.get("/")

    print(res.json())

    assert res.status_code == 200

    assert res.json()["message"] == "Welcome to my Fast API"



# ==========================
# USER TESTS
# ==========================

def test_create_user():

    res = client.post(
        "/create_user",
        json={
            "email": "kweku@gmail.com",
            "password": "koko123"
        }
    )


    print(res.json())


    assert res.status_code == 201

    assert res.json()["email"] == "koko@gmail.com"



def test_duplicate_user():

    user = {
        "email": "duplicate@gmail.com",
        "password": "password123"
    }


    # First creation

    res1 = client.post(
        "/create_user",
        json=user
    )


    # Second creation

    res2 = client.post(
        "/create_user",
        json=user
    )


    print(res2.json())


    assert res1.status_code == 201

    assert res2.status_code == 400




# ==========================
# AUTH TESTS
# ==========================

def test_login():


    # Create user

    client.post(
        "/create_user",
        json={
            "email": "login@gmail.com",
            "password": "password123"
        }
    )


    # Login

    response = client.post(
        "/login",
        data={
            "username": "login@gmail.com",
            "password": "password123"
        }
    )


    print(response.json())


    assert response.status_code == 200

    assert "access_token" in response.json()

    assert response.json()["token_type"] == "bearer"




def test_wrong_login():


    response = client.post(
        "/login",
        data={
            "username": "wrong@gmail.com",
            "password": "wrongpassword"
        }
    )


    print(response.json())


    assert response.status_code == 403




# ==========================
# TOKEN HELPER
# ==========================

def get_token():


    # Create user

    client.post(
        "/create_user",
        json={
            "email": "postuser@gmail.com",
            "password": "password123"
        }
    )


    # Login

    response = client.post(
        "/login",
        data={
            "username": "postuser@gmail.com",
            "password": "password123"
        }
    )


    return response.json()["access_token"]





# ==========================
# POST TESTS
# ==========================

def test_create_post():


    token = get_token()


    response = client.post(
        "/posts",
        json={
            "title": "FastAPI Testing",
            "content": "Learning pytest",
            "published": True
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


    print(response.json())


    assert response.status_code == 201




def test_get_posts():


    response = client.get("/posts")


    print(response.json())


    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )




def test_get_single_post():


    response = client.get(
        "/posts/1"
    )


    print(response.json())


    assert response.status_code == 200




def test_update_post():


    token = get_token()


    response = client.put(
        "/posts/1",
        json={
            "title": "Updated Title",
            "content": "Updated Content",
            "published": True
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


    print(response.json())


    assert response.status_code == 200




def test_delete_post():


    token = get_token()


    response = client.delete(
        "/posts/1",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


    print(response.json())


    assert response.status_code == 204