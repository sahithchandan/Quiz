# Operation Notes

### 20th May 2022: 
Hmmmm.. This code test is goin to be interesting and challenging at the same time as this project requires GraphQl skills which I don't have. 
I only once tried GraphQL but never implemented in a real time project. All my projects where either Django using REST framework or AWS serverless. 
Eager to take this as a challenge and see how far can I go coding :)

### 21th May 2022: 
I faced some challenges getting the project up and running mainly due to version not being pinned down. 

Had to downgrade the django version from 4.0.4 to 3.2.13 to resolve the following error:
`ImportError: cannot import name ‘force_text’ from ‘django.utils.encoding’` 

I had two options to choose from:
1. Go ahead and upgrade the entire project and resolve the error. But I assumed this would take more time. I wanted to concentrate on models and code structure more than resolving the issues 
2. Go ahead and downgrade the django version which is suitable with the other packages. In this way I could concentrate on the code base. 


Started building the project, base model structure etc. Gone through a lot of online tutorials and read a lot of GraphQL documentation.   


My first encounter with an issue was a strange behaviour with choice fields. The output returns as a string. I did some research and found some reference [here](https://github.com/graphql-python/graphene-django/issues/67).
I resolved this issue by including `convert_choices_to_enum = False` in object node.


### 22nd May 2022:
Tried to implement relay in order to implement pagination which worked fine. But relay generates it own unique ID 
which caused problems especially when trying to fetch a specific questionnaire using the actual ID instead of relay generated global ID.
Had to then fetch the global ID of the object and pass it in the GET serializer for the FE to use it using `graphene.Node.to_global_id('QuestionnaireNode', obj.id)`
