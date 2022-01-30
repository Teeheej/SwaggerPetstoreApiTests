## Automated API tests for Swagger Petstore 
####(user operation endpoints)
***

### How to run tests
Since the project is not packaged for distribution, one of the ways to run it is in virtual environment (venv)

#### Windows
1. download the source code (git clone / manually with zip archive)
2. navigate to the project directory in powershell / command prompt
3. create venv in the project directory: `python -m venv env`
   1. virtualenv library is required: `py -m pip install --user virtualenv`
4. activate project venv: `.\env\Scripts\activate`
   1. use `where python` to check the venv (interpreter should be in the project directory)
5. install project dependencies: `pip install -r requirements.txt`
6. run tests:
   * `py -m pytest` – for all tests
   * `py -m pytest tests/user/test_negative_cases.py` – for a module
   * `py -m pytest tests/user/test_negative_cases.py::test_login_with_no_credentials` – for one test
   * `py -m pytest -k "negative_cases"` – filter tests by keyword expression

###Unix (tested on MacOS)
The steps are the same as for Windows, the only differences are:
* venv activation is `source env/bin/activate`
* check Python interpreter location: `which python`

<br />

#####Some additional notes
* `GET /user/{username}` sometimes returns 404 even if users exists
  * added reruns in the tests that rely on the endpoint
* `GET /user/login` and `/user/logout` endpoints don't seem to response with stubs
* `DELETE /user/{username}` works without authorization
* Sometimes `test_delete_user` receives 404 in all retries, 
but consecutive cleanup fixture function successfully deletes the test user
