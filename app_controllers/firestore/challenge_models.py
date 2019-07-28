import datetime
import pprint

class Challenge(object):
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.overview = ""
        self.date_published = datetime.datetime.now()
        self.last_update = datetime.datetime.now()
        self.change_history = {}
        self.difficulty = 0
        self.tags = []
        self.category = ""
        self.duration = 0
        self.grading_criteria = []
        self.apps = []
        self.topology = {}
        self.resources = {}
        self.questions = {}
        self.submissions = {}

    def print_challenge(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.to_dict())

    def edit_title(self,new_title):
        self.title = new_title
    
    def edit_description(self,new_description):
        self.description = new_description

    def edit_overview(self,new_overview):
        self.overview = new_overview

    def edit_difficulty(self,new_difficulty):
        self.difficulty = int(new_difficulty)

    def add_tags(self, new_tag):
        if new_tag not in self.tags:
            self.tags.append(new_tag)
    
    def edit_category(self, new_category):
        self.category = new_category

    def edit_duration(self, new_duration):
        self.duration = new_duration

    def add_grading_criteria(self, new_criteria):
        if new_criteria not in self.grading_criteria:
            self.grading_criteria.append(new_criteria)

    def remove_grading_criteria(self, target_criteria):
        if target_criteria in self.grading_criteria:
            self.grading_criteria.remove(target_criteria)
    
    def add_app(self, new_app):
        if new_app not in self.apps:
            self.apps.append(new_app)

    def remove_app(self, target_app):
        if target_app in self.apps:
            self.apps.remove(target_app)
    
    def edit_topology(self, new_topology):
        self.topology = new_topology
    
    def add_resource(self, app_name, app_description, app_url, shell_url):
        resources_size = len(self.resources)
        self.resources[resources_size] = {
                "name" : app_name,
                "description" : app_description,
                "app_url" : app_url, 
                "shell_url" : shell_url,
                "credentials" : {},
                "references" : {},
                "tips": {}
            }

    # REFERENCES
    def add_resource_reference(self, resource_index, reference_title, 
                               reference_url):
        prev_resource = self.resources
        references_size = len(prev_resource[resource_index]["references"])
        prev_resource[resource_index]["references"][references_size] = {
            reference_title : reference_url
        }
        self.resources = prev_resource

    def remove_resource_reference_by_index(self, target_resource_index):
        prev_resource = self.resources[target_resource_index]
        del prev_resource["references"][target_resource_index]
        self.resources = prev_resource

    def remove_resource_by_index(self, target_index):
        del self.resources[target_index]

    # CREDENTIALS
    def add_resource_credential(self, target_resource_index, cred_user, 
                                 cred_password):
        prev_resource = self.resources[target_resource_index]
        prev_resource["credentials"][0] = {
            "user" : cred_user,
            "password" : cred_password
        }
        self.resources[target_resource_index] = prev_resource

    def remove_resource_credential_by_index(self, target_resource_index):
        prev_resource = self.resources[target_resource_index]
        del prev_resource["credentials"][target_resource_index]
        self.resources = prev_resource

    # TIPS
    def add_resource_tip(self, target_resource_index, new_tip):
        prev_resource = self.resources[target_resource_index]
        tips_size = len(prev_resource["tips"])
        prev_resource["tips"][tips_size] = new_tip
        self.resources[target_resource_index] = prev_resource

    def remove_resource_tip_by_index(self, target_resource_index):
        prev_resource = self.resources[target_resource_index]
        del prev_resource["credentials"][target_resource_index]
        self.resources = prev_resource

    def add_question(self,question_type, question_details):
        questions_size = len(self.questions)
        self.questions[questions_size] = {
                "type" : question_type,
                "details" : question_details
            }

    def edit_question_by_index(self,target_index,question_type, 
                               question_details):
        self.questions[target_index] = {
                "type" : question_type,
                "details" : question_details
            }

    def remove_question_by_index(self, target_index):
        del self.questions[target_index]

    def to_dict(self):
        this_dict = {
            u'title':self.title,
            u'description':self.description,
            u'overview':self.overview,
            u'date_published':self.date_published,
            u'last_update':self.last_update,
            u'difficulty':self.difficulty,
            u'tags':self.tags,
            u'category':self.category,
            u'duration':self.duration,
            u'grading_criteria':self.grading_criteria,
            u'apps':self.apps,
            u'topology':self.topology,
            u'resources':self.resources,
            u'questions':self.questions,
            u'submissions':self.submissions,
        }

        return this_dict

    