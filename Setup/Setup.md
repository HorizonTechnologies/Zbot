# Zbot Setup

For zbot specifications visit here
Go to: [https://api.slack.com/apps](https://api.slack.com/apps)
Here You can see a button to create a app
![](https://raw.githubusercontent.com/HorizonTechnologies/Zapp/master/Setup/apipage.PNG)
- Here Give the name the select the workspace

![](https://raw.githubusercontent.com/HorizonTechnologies/Zapp/master/Setup/create.PNG)

- Then after creating the **Zbot**, You will be redirected to the **Zbot** configurations page

![](https://raw.githubusercontent.com/HorizonTechnologies/Zapp/master/Setup/list.PNG)

- Here, you can be able to do all the operations to your zbot
These are the features and settings to configure the **Zbot**
- In the settings section, The option **Basic Information** Let you see all the **Zbot** info (client id, Verification tokens, signing secrets)
Copy the Signin Secret and Verification token and save it to `.env` file

![](https://raw.githubusercontent.com/HorizonTechnologies/Zapp/master/Setup/secrets.PNG)
- Under the Features section, Go to **Events Subscription** Turn it `on`
	Then, we can be able to use the slack events
![](https://raw.githubusercontent.com/HorizonTechnologies/Zapp/master/Setup/events.PNG)

There you can find an option called **Subscribe to bot events**, Here we should give the neccessary scopes for the bot
Give the required scopes as mentioned below:
`message.im`

![](https://raw.githubusercontent.com/HorizonTechnologies/Zapp/master/Setup/scope.PNG)

- Once run the code in your machine or in the server, add `slack\events` as       the endpoint to your url
Then Paste the link in the space provided
 **Make sure that the link you provided have a valid SSL Certification**
Now, Slack will send a HTTP Post request to the provided link, The signin secret will verify the returned 200 HTTP Status was sent by you.

Then you can be able to **save the changes** and install the app into the workspace.
	 
![](https://raw.githubusercontent.com/HorizonTechnologies/Zapp/master/Setup/eventson.PNG)

-  Go to **interactivity** under features section

Turn on the interactions and Provide the link with endpoints as `slack/message_actions`
	 
![](https://raw.githubusercontent.com/HorizonTechnologies/Zapp/master/Setup/actions.PNG)


Its done.....
You've successfully installed and configured the Zbot into your workspace 
**Setup the DB Credential in the .env file**



