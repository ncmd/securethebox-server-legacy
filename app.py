from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from subprocess import check_output, CalledProcessError, STDOUT

'''
/api/v1/...

Firebase
[GET]
/app/user/status/logged - Check if user is logged in
/app/user/status/logout
/app/user/status/login
[GET]
/app/challenges/list - list all challenges available
/app/challenge/1/checklist
/app/challenge/1/checklist/performance

Heroku Kubectl Client (securethebox-server)
[GET] 
/heroku/status/uptime - Get uptime status of Heroku Server (need this to deploy)
/heroku/status/resources - Get cpu/memory load

Google Kubernetes Engine 
[GET]
/kubernetes/status/clusters/uptime - Get all cluster uptime
/kubernetes/status/pods/uptime - Get all pod uptime
/kubernetes/status/resources - Get cpu/memory load
/kubernetes/status/zones - Get Regional clusters available
/kubernetes/status/dns - Get External-DNS status/records

Kubernetes commands
[POST] 
/kubernetes/challenge/1/deploy - Deploy challenge #1 pods (traefik, waf, app, splunk)
- args=username, recaptcha token, auth2 token, jwt
- should use a dynamic yml file when deploying
[GET] 
/kubernetes/challenge/1/status/pods - Check deployment status of pods/containers (every 5 seconds)
/kubernetes/challenge/1/status/dns - Check status of dns records created (dig)
/kubernetes/challenge/1/status/pods/ready - Confirm when they are ready (if ready, ready=true)
- args=username,jwt
[GET] 
/kubernetes/challenge/1/status/pods/links - Get urls of containers and present it to frontend
- args=username,jwt
[POST]
/kubernetes/challenge/1/restart - Restart pod (destroy and redeploy)
- args=username,servicename,jwt
[POST]
/kubernetes/challenge/1/destroy - Destroy challenge 1: deletes challenge 1 pods ; args=username ; exec
- Delete pods after 2 hours
- args=username,servicename,jwt

Firebase Metrics
[GET]
/users/metrics/loggedin - How many users are logged in
/users/metrics/joined/24hours - How many users joined today
/usses/metrics/challenges - How many users are doing a challenge
- Collection: users
- Document: metrics

Stripe client
[POST] 
/stripe/subscription/start - Subscribe user via email address + CC (Should also send invoice)
- args=emailaddress,jwt
[GET] 
/stripe/invoice - Get invoice for frontend (save to Firebase storage)
- args=emailaddress,jwt
[GET] 
/stripe/subscription/status - Check user subscription (save to Firebase firestore)
- args=emailaddress,jwt
Sendgrid client



'''

app = Flask(__name__)
api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        # command = ["/app/vendor/google-cloud-sdk/bin/kubectl", "get", "all"]
        command = ["/app/vendor/google-cloud-sdk/bin/kubectl", "apply", "-f","/app/kubernetes-deployments/services/nginx.yml"]
        try:
            output = check_output(command, stderr=STDOUT).decode()
            success = True 
            abort(404, message=str(output))
        except CalledProcessError as e:
            output = e.output.decode()
            success = False
            abort(404, message=str(output))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
