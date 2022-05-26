# Quiz App

A simple quiz application where uses can create questionnaires with questions. The user can then share the questionnaire
to public after which they can look at the responses. 

### App flow
- Users register and logs in to the application. 
- User can then create, edit or delete questionnaires with questions. 
- User can choose questions to be either one of the following: Short answer, Paragraph, Checkboxes, Multiple choices or Dropdown.      
- User can create a public sharable link for the questionnaire. A unique link is generated each time when shared which is unique for every user.  
- Public can fetch the questionnaire via the shared link and provide answers to the questions. 
- Public can only submit the questionnaire once. 
- User can then view the answers for the shared questionnaire submitted by the public.


### Prerequisites

Before starting on this project you should have:
 - [homebrew](https://brew.sh/)
 - [Docker for Mac](https://download.docker.com/mac/stable/Docker.dmg)


### Installing

- Open up a terminal, navigate to the directory containing this README.md.
- Run the following commands in order
```
# load start the container
./dc start

# to generate migrations and apply them
./dc migrate

# to create superuser
./dc createsuperuser

# to start the local development server
./dc startapp
```
- Navigate to [http://0.0.0.0:8000] 
- You can log in as a Django superuser by going to [http://localhost:8080/admin] and using the app


### Tests

To run all tests
`./dc manage test`

To run a specific test case
`./dc manage test api.quiz.tests.test_questionnaire_responses_list.QuestionnaireResponseAnswersListGraphQLTest`


### Before committing your code, check for the following
 - flake8 linting
 - python tests


### Built With
 - Django 3.2.13
 - Django Rest Framework 3.13.1
 - Python 3.8
 - Postgres 14.3



### Operation Notes

#### 20th May 2022
Hmmmm.. This code test is going to be interesting and challenging at the same time as this project requires GraphQl skills which I don't have. 
I only once tried GraphQL but never implemented in a real time project. All my projects where either Django using REST framework or AWS serverless. 
Eager to take this as a challenge and see how far can I go coding :)

#### 21th May 2022
I faced some challenges getting the project up and running mainly due to version not being pinned down. 

Had to downgrade the django version from 4.0.4 to 3.2.13 to resolve the following error:
`ImportError: cannot import name ‘force_text’ from ‘django.utils.encoding’` 

I had two options to choose from:
1. Go ahead and upgrade the entire project and resolve the error. But I assumed this would take more time. I wanted to concentrate on models and code structure more than resolving the issues 
2. Go ahead and downgrade the django version which is suitable with the other packages. In this way I could concentrate on the code base. 


Started building the project, base model structure etc. Gone through a lot of online tutorials and read a lot of GraphQL documentation.   


My first encounter with an issue was a strange behaviour with choice fields. The output returns as a string. I did some research and found some reference [here](https://github.com/graphql-python/graphene-django/issues/67).
I resolved this issue by including `convert_choices_to_enum = False` in object node.


#### 22nd May 2022
Tried to implement relay in order to implement pagination which worked fine. But relay generates it own unique ID 
which caused problems especially when trying to fetch a specific questionnaire using the actual ID instead of relay generated global ID.
Had to then fetch the global ID of the object and pass it in the GET serializer for the FE to use it using `graphene.Node.to_global_id('QuestionnaireNode', obj.id)`


#### 23rd May 2022
Got hold of how to write api's and started concentrating on the logic more. Got most of the api's done. I creted a new `dc` file in the root folder. This single file replaces the need for having the scripts folder and easier to main all docker realted commands in a single place.


#### 24th May 2022
Started writing test cases for the api's. Found it fairly simple. Used GraphQLTestCase.


#### 24th May 2022
I realised there was no way a User can share other user's questionnaire if he liked it. Added create_by field to QuestionnaireResponses model  


### Future scope
- Can register users who are answering and assign the user to QuestionnaireResponses model
- Integrate email forward to share questionnaire via an email
- Save user progress
- User can create copies of questionnaire and edit and share it