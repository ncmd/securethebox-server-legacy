from app_controllers.academy.categories import Categories
from app_controllers.academy.category import Category
from app_controllers.academy.courses import Courses
from app_controllers.academy.course import Course
from app_controllers.academy.steps import Steps
from app_controllers.academy.step import Step
import json
def main():
    category = Category()
    category.setCategory(0,'web','Web','#3f51b5')
    categories = Categories()
    categories.addCategory(category.to_dict()) 
    course = Course()
    steps = Steps()
    step = Step()
    step.setStep('0','Overview','<h1>Overview</h1>')
    steps.addStep(step.to_dict())
    course.setCourse(
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
    courses.addCourse(course.to_dict())
    return categories.getCategories(),courses.getCourses()


    
