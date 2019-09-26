from app_controllers.academy.categories import Categories
from app_controllers.academy.category import Category
from app_controllers.academy.courses import Courses
from app_controllers.academy.course import Course
from app_controllers.academy.steps import Steps
from app_controllers.academy.step import Step

category1 = Category()
category2 = Category()
category3 = Category()
category4 = Category()
category1.setCategory(0, 'web', 'Web', '#3f51b5')
category2.setCategory(1, 'aws', 'AWS', '#3f51b5')
category3.setCategory(2, 'gcp', 'GCP', '#3f51b5')
category4.setCategory(3, 'cicd', 'CI-CD', '#3f51b5')
categories = Categories()
categories.addCategory(category1.to_dict())
categories.addCategory(category2.to_dict())
categories.addCategory(category3.to_dict())
categories.addCategory(category4.to_dict())

course1 = Course()
steps = Steps()
step1 = Step()
step1.setStep('0', 'Overview', '<h1>Overview</h1>')
step2 = Step()
step2.setStep('1', 'Overview', '<h1>2</h1>')
steps.addStep(step1.to_dict())
steps.addStep(step2.to_dict())
course1.setCourse(
    '15459251a6d6b397565',
    'Challenge 1',
    'challenge-1',
    'Defense Scenario',
    'web',
    121,
    11,
    0,
    steps.getSteps())
courses = Courses()
courses.addCourse(course1.to_dict())

def addCourse(course_payload):
    # print("COURSE PAYLOAD",course_payload['steps'])
    course2 = Course()
    steps = Steps()
    
    for x in course_payload["steps"]:
        print(x)
        step = Step()
        step.setStep(x["id"], x["title"], x["content"])
        steps.addStep(step.to_dict())
    
    course2.setCourse(
        course_payload["id"],
        course_payload["title"],
        course_payload["slug"],
        course_payload["description"],
        course_payload["category"],
        course_payload["length"],
        course_payload["totalSteps"],
        course_payload["activeStep"],
        steps.getSteps())
    courses.addCourse(course2.to_dict())


def main():

    return categories.getCategories(), courses.getCourses()
