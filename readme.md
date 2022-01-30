## Automated API tests for Swagger Petstore 
#### (user operation endpoints)
***

### How to run tests
Since the project is not packaged for distribution, one of the ways to run it is via virtual environment (venv)

#### Windows
1. Download the source code (git clone / manually with zip archive)
2. Navigate to the project directory in powershell / command prompt
3. Create venv in the project directory: `python -m venv env`
   1. virtualenv library is required: `py -m pip install --user virtualenv`
4. Activate project venv: `.\env\Scripts\activate`
   1. use `where python` to check the venv (interpreter should be in the project directory)
5. Install project dependencies: `pip install -r requirements.txt`
6. Run tests:
   * `py -m pytest` – for all tests
   * `py -m pytest tests/user/test_negative_cases.py` – for a module
   * `py -m pytest tests/user/test_negative_cases.py::test_login_with_no_credentials` – for one test
   * `py -m pytest -k "negative_cases"` – filter tests by keyword expression
7. `deactivate` the venv

#### Unix (tested on MacOS)
The steps and commands are the same as for Windows, the only differences are:
* Venv activation is `source env/bin/activate`
* Check Python interpreter location: `which python`

> More on [python venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
and [pytest usage](https://docs.pytest.org/en/latest/how-to/usage.html)

***
### Additional info and notes

* Test basis for automated tests is [petstore swagger specification](https://petstore.swagger.io/)
  * 4 out of 6 negative tests cases fail; however, expected conditions in those cases are backed by test basis
  * 1 negative test case `create_user_with_empty_request_body` is not explicitly backed by test basis,
  but inferred from tester's expirience (of course, it is a subject to change)
* `GET /user/{username}` sometimes returns 404 even if users exists
  * added reruns in the tests that rely on the endpoint
* `GET /user/login` and `/user/logout` endpoints seem to response with stubs
  * `username` and `password` as explicit query-parameters for `/login` endpoint is not
  the best idea secure-wise :)
* `DELETE /user/{username}` works without authorization
* Sometimes `test_delete_user` receives 404 in all retries, 
but consecutive cleanup fixture function successfully deletes the test user
