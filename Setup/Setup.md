# Zbot Setup

For zbot specifications visit here

- Go to: [https://api.slack.com/apps](https://api.slack.com/apps)
	Here You can see a button to create a app

- Then after creating the **Zbot**, You will be redirected to the **Zbot** configurations page
	
	Here, you can be able to do all the operations to your zbot
	These are the features and settings to configure the **Zbot**
	In the settings section, The option **Basic Information** Let you see all the **Zbot** info (client id, Verification tokens, signing secrets)
	Copy the Signin Secret and Verification token and save it to `.env` file
	In the Features section, Go to **OAuth and Permissions**, Here under **Scopes**
	Add the required scopes for the bot,
	Give the scopes as mentioned below
		1. Chat:write
		2. im:write

	![enter image description here](hi)
	Under the Features section, Go to **Events Subscription** Turn it `on`
	Then, we can be able to use the slack events
	
	Once run the code in your machine or in the server, 
	
	
	There you can find an option called **Subscribe to bot events**, Here we should give the necessary scopes for the bot
	Give the required scopes as mentioned below:
	1. `message.im`
	
	Once run the code in your machine or in the server, add `slack\events` as the endpoint to your url
	Then Paste the link in the space provided	
	 Now, Slack will send a HTTP Post request to the provided link, The signin secret will verify the returned 200 HTTP Status was sent by you.
	 Then you can be able to **save the changes** and install the app into the workspace.
	 Its done.....
	 You've successfully installed and configured the Zbot into your workspace 


