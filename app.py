from flask import Flask
from pylti.flask import lti
from flask import request as flask_request
from canvasapi import Canvas

VERSION = '0.0.1'
app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def home_page():
    print("Home page loaded.")
    return 'Welcome to Home page!'


def error(exception=None):
    """ render error page
    :param exception: optional exception
    :return: the error.html template rendered
    """
    return "Error in LTI connection. \n {}".format(str(exception))


#@app.route('/api/v1/courses/7959767/users', methods=['GET','POST'])
#def obtain():
#    userID = flask_request.args.to_dict()
#    print("OBTAIN:", userID)
#    return userID


@app.route('/lti/', methods=['GET', 'POST'])
@lti(request='initial', error=error, app=app)
def index(lti=lti):
    """ initial access page to the lti provider.  This page provides
    authorization for the user.
    :param lti: the `lti` object from `pylti`
    :return: index page for lti provider
    """

    # Access the payload to LTI post request
    print('LTI initial page loaded.')
    print(lti)
    print(type(lti))
    print(flask_request.method)
    params = flask_request.form.to_dict()
    #print("params: {}".format(params))

    # User's name
    #name = params['lis_person_name_full']
    #print(f'{name=}')

    # Custom parameters
    #print("custom_field_name_01: {}".format(params['custom_field_name_01']))
    #print("custom_field_name_02: {}".format(params['custom_field_name_02']))
    
    #Test
    #test = obtain()
    #print("TEST:", test)
    
    # Canvas API URL
    API_URL = "https://canvas.instructure.com"
    # Canvas API key
    API_KEY = "7~NTEm2g0cHTJWI7ApGGP9TY7rbemxTaRcSVIfs6Dt9hcUqzE1UWEFolnMmqRw2jZD"
    # Initialize a new Canvas object
    canvas = Canvas(API_URL, API_KEY)
    
    course = canvas.get_course(params['custom_course_id'])
    teacher = canvas.get_user(params['custom_canvas_user_id'])
    
    OUTPUT_TEXT = "Welcome to my Canvas LTI Assignment.<br>"
    OUTPUT_TEXT += "<b>Teacher:</b> {}.<br>".format(teacher.get_profile()['short_name'])
    OUTPUT_TEXT += "<b>Course:</b> {}.<br>".format(course.name)
    
    OUTPUT_TEXT += "<br><b>List of users in the course:</b><br>".format(params['context_title'])
    
    users = course.get_users(enrollment_type=['student'])
    for user in users:
        profile = user.get_profile()
        OUTPUT_TEXT += "<b>Name:</b> {}. ".format(profile['short_name'])
        OUTPUT_TEXT += "<b>Email:</b> {}<br>".format(profile['primary_email'])
        
    OUTPUT_TEXT += "<br><b>List of assignments per student:</b><br><br>"
    
    for user in users:
        profile = user.get_profile()
        OUTPUT_TEXT += "<b>+Name:</b> {}.<br>".format(profile['short_name'])
        
        submissions = user.get_assignments(course)
        submission_list = [sub for sub in submissions]
        for sub in submission_list:
            OUTPUT_TEXT += "<b>-Assignment:</b> {}. ".format(sub.name)
            OUTPUT_TEXT += "<b>Submitted:</b> {}.<br>".format("Yes" if sub.has_submitted_submissions else "No")
            
    return OUTPUT_TEXT
            
    #https://canvas.instructure.com/login/canvas
    #https://canvasapi.readthedocs.io/en/stable/examples.html#assignments
    #https://canvas.instructure.com/doc/api/courses.html
    #https://canvas.instructure.com/doc/api/users.html
    #https://canvas.instructure.com/doc/api/index.html
    #file:///C:/Users/ronal/Documents/Fall2023/CS480-CSEdu/Flask/LTI%20Flask%20documentation.pdf
    #https://snyk.io/advisor/python/canvasapi/functions/canvasapi.paginated_list.PaginatedList
    #https://canvasapi.readthedocs.io/en/stable/examples.html
    #https://canvasapi.readthedocs.io/en/stable/class-reference.html
    #https://community.canvaslms.com/t5/Canvas-Question-Forum/Passing-Parameters-to-LTI-Launch-URL/m-p/222652
    #return "Hello {}! I'm LTI tool called from Canvas." .format(params['lis_person_name_full'])

# main driver function
if __name__ == '__main__':
    app.run(debug=True)
        