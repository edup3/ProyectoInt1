
## Libraries that must be installed before running the program:

django

whitenoise

openai

pillow

matplotlib

python-dotenv

twilio

### Command to install libraries:

` pip install -r "requirements.txt" `

## Command to run the program:

` py manage.py runserver `

For the chatbot to work you will need an Open AI api key

You can provide this key by creating a file called openAI.env on the root dir of the project, at the same level as the manage.py file.

```
#openAI.env
openAI_api_key =

```

You will also need a twilio accSid and auth token if you want to call emergency services, you can provide this by creating a file calles twilio.env on the root dir of the project.

```
#twilio.env
accSid =
authToken =

```
