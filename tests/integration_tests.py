import requests
import psycopg2

# connect using psycopg2 library to communicate to PostGreSQL database
connection = psycopg2.connect(user="cs162_user",
                                  password="cs162_password",
                                  host="localhost",
                                  port="5432",
                                  database="cs162")
cursor = connection.cursor()

# check for response
def test_add_response():
    response = requests.post('http://127.0.0.1:5000/add',data={'expression':'57+100'})
    assert response.status_code == 200

# check for added to database
def test_add_db():
    cursor.execute("SELECT * FROM Expression WHERE text='57+100' LIMIT 1")
    es = cursor.fetchall()
    assert es is not None
    assert es[0] is not None
    assert es[0][2] == 157

# check for error output (cannot divide by 0)
def test_add_error():
    response = requests.post('http://127.0.0.1:5000/add', data={'expression':'2/0'})
    assert response.status_code == 500

# test for last expression output in db
def test_last_exp():
    cursor.execute("SELECT * FROM Expression ORDER BY id DESC LIMIT 1")
    es = cursor.fetchall()
    assert es is not None
    assert es[0] is not None
    assert es[0][1] == '57+100'

# run tests
if __name__=="__main__":
    try:
        print("Testing...")
        test_add_response()
        test_add_db()
        test_add_error()
        test_last_exp()
        print("All passed.")
    except:
        print("Error testing.")
