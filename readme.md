# Instalation guide for Ubuntu

1. Install python 3.7.2 on Ubuntu
	
	1. Install prerequisites
		```
		sudo apt-get install build-essential checkinstall
		
		sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev \
		 libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
		```
	
	2. Download python 3.7
	
		```
		cd /usr/src
		sudo wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
		```
	 
	3. Extract the downloaded package
	 
		```
		sudo tar xzf Python-3.7.2.tgz
		```
		
	4. Compile python source
		```
		cd Python-3.7.2
		sudo ./configure --enable-optimizations
		sudo make altinstall
		```
		
	5. Check python version and make it default
		```
		python3.7 -V
		
		# and choose puthon 3.7 in order to make the python3 to point to it
		sudo update-alternatives --config python3
		```
		
	5. Install pip
		```
		curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
		python3 get-pip.py
		```

 2. Edit the files inside bucket folder as you like
	 - configs.yml
		 - treads: 10
		`how much workers you want to run in parallel`
		 - mails_per_second: -1
		 `limit the quantity of workers that can start each second`
		 - subject: "Hello World" 
		 `the message subject`
	 - mail.html `the mail html body content`
	 - mail_servers.txt
		 - Each line `host:username:password:port`
		 - Optional limit `host:username:password:port:limit`
	 - proxies.txt
		 - Each line `ip:port`
	 - recipients.txt 
		 - Each line `email`
	 - senders.txt	
		 - Each line `email:name`
	 - attachment folder	
		 - Each file present here will be attached to the message
	 
 3. Copy the script `folder-name` to the server
 
	 1. Get  [winscp](https://winscp.net/eng/docs/task_upload) and upload the `folder-name` to the server.
	 2. Follow the website instructions `drag and drop the folder-name to your server home folder`
		 
 4. Run it!
 
	 1. Install requirements
		 ```
		 cd folder-name
		 pip install -r requirements.txt
		 ```
	 2. Run the script
		 ```
			 cd src
			 python3 program.py
		 ``` 