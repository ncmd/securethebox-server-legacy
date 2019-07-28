class Challenge(object):
    def __init__(self, title, description, overview, date_published, 
                 last_update, difficulty, tags, category, duration, 
                 grading_criteria, apps, topology, resources, video_questions,
                 vocal_questions, coding_questions, typed_questions, 
                 ctf_questions, video_submission, vocal_submission, 
                 coding_submission, typed_submission, ctf_submission):
        self.title = title
        self.description = description
        self.overview = overview
        self.date_published = date_published
        self.last_update = last_update
        self.difficulty = difficulty
        self.tags = tags
        self.category = category
        self.duration = duration
        self.grading_criteria = grading_criteria
        self.apps = apps
        self.topology = topology
        self.resources = resources
        self.video_questions = video_questions
        self.vocal_questions = vocal_questions
        self.coding_questions = coding_questions
        self.typed_questions = typed_questions
        self.ctf_questions = ctf_questions
        self.video_submission = video_submission
        self.vocal_submission = vocal_submission
        self.coding_submission = coding_submission
        self.typed_submission = typed_submission
        self.ctf_submission = ctf_submission

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
            u'video_questions':self.video_questions,
            u'vocal_questions':self.vocal_questions,
            u'coding_questions':self.coding_questions,
            u'typed_questions':self.typed_questions,
            u'ctf_questions':self.ctf_questions,
            u'video_submission':self.video_submission,
            u'vocal_submission':self.vocal_submission,
            u'coding_submission':self.coding_submission,
            u'typed_submission':self.typed_submission,
            u'ctf_submission':self.ctf_submission,
        }

        return this_dict
"""
challenges -> id ->
    challenge_id
    challenge_title
    challenge_description
    challenge_overview
    challenge_published |
        - MM/DD/YYYY
    challenge_last_update |
        - MM/DD/YYYY
    challenge_difficulty |
        - Level 1 - 5
    challenge_tags: [] 
    challenge_category |
        - web applications
        - secrets management
        - git repository
        - ids/ips
        - tls/ssl, pki
        - operating system internals
        - code review
        - pentesting
        - infrastructure
        - cryptography
        - vpn
        - identity access management
        - incident response
        - forensics
        - business
        - leadership
    challenge_duration |
        - 10 minutes - 2 hours
    challenge_grading_criteria
        - must pass | 
            - coding
            - verbal
            - video
            - ctf
            - etc...
    challenge_enabled_apps
        - kali
        - gitlab
        - splunk
        - juice-shop
    challenge_scenario_topology
        - json format
    challenge_resources |
        url |
            - kali-username.us-west1-a.securethebox.com
        shell |
            - kali-shell-username.us-west1-a.securethebox.com
        credentials |
            - username
            - password
        references |
            - url1
        tips | 
            - tip1
    challenge_video_questions |
        - id
        - question_description
        - helper_attachments
        - helper_urls
        - helper_images
    challenge_vocal_questions
    challenge_coding_questions
    challenge_typed_questions
    challenge_ctf_questions
    challenge_video_submission
    challenge_vocal_submission
    challenge_coding_submission
    challenge_typed_submission
    challenge_ctf_submission


"""