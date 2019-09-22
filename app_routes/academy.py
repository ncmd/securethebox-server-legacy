import subprocess
from subprocess import check_output
import requests
import json
from flask_restful import reqparse,Resource

from initialize.academy import main

academy_parser = reqparse.RequestParser()
academy_parser.add_argument('courseId', help='{error_msg}')
academy_parser.add_argument('courseHandle', help='{error_msg}')

categories, courses = main()
print(courses,categories)

# Challenges API
class apiAcademyCourses(Resource):
    def get(self):
        try:
            return courses, 201 ,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET"} 
        except:
            return 404

class apiAcademyCourse(Resource):
    
    def get(self):
        args = academy_parser.parse_args()
        try:
            for i in courses:
                print(i["id"],args['courseId'])
                if i["id"] == args['courseId']:
                    return i, 201 ,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET"} 
        except:
            return 404

class apiAcademyCategories(Resource):
    def get(self):
        try:
            return categories, 201 , {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET"} 
        except:
            return 404