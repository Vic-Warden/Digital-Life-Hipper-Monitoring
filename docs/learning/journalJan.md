# Learning Journal

This file contains the learning journal with the learning stories of Jan.

## Learning stories

#111 As a student, I want to learn about clean web app implementations, so that I can use it to my advantage to come up with components/requirements for a web app.

* The first thing I did was look at my phones health "gezondheid" app. Here I could get a good impression of how Apple did their layouts to make them look super intuitive. Together with Darian and Indigo I looked into this and together we agreed on certain components/requirements. After checking the Apple Health app I started looking on google for basic login pages, web layouts, and again together with Darian and Indigo we decided on things that looked really great. We want to go for a simplistic look that is understandable for anyone no matter the age. This PDF file has since been comitted to the repository under `design/Components_Requirements`

#120 As a Student, I need a PowerPoint template for the Sprint Review, so I can clearly and professionally present the completed work to the Product Owner.

* As a Business IT & Management Student leaving a good impression on a client is important for further success. For this specific learning story I went ahead and looked up some templates online, and how to use the designer tool that is built-in to PowerPoint. In the year before I was in a project with an old friend of mine Miguel Schagen. In his PowerPoint's I would see that he inserted the Client's company logo in the bottom right, which is a really good idea to make it feel more personal. So, I also incorporated this into the PowerPoint template for this team. The powerpoint file has been comitted to the repository under `docs/assets`

#112 As a student, I want to learn how to easily merge common datasets together within PowerBI, so that I can correctly use the data of multiple Hipper devices.

* Apparently Power BI Desktop allows users to efficiently import and combine multiple data files stored in a local folder, such as .csv reports. By connecting to a folder as a data source, Power BI can automatically detect and list all files within it. Using a sample file as a template, it enables consistent transformations—like removing headers or changing column types—across all files. I researched this by looking up a few things online to do this automatically. I then tried it myself and it immediately worked without issue! The file of the tutorial can be found at: `frontend/powerbi/powerbi-importing-data.md`

#201 As a student, I want to learn and look into how Hipper analyzed their device data, so that we know how to document it ourselves.

* Since we as a team have been tasked to test the Hipper output data in comparison with other devices, we obviously need to do that by complying with a certain procedure. Because if we do not, then our test data could not be comparable to previous tests documented by Hipper therapeutics themselves. Here I took it on myself to investigate the Research report that our Product Owner Michel sent to us. With the help of ChatGPT I quickly analyzed what tests they were doing, and I also inspected all of the graphs they made.
What I learned is that for us to perform a similar test we need to also take two (or more) Hipper devices and get them to stick together as close as possible. After that it is time for a series of tests, such as walking, running etc. Any and all movements are acceptable. Finally after collecting data it is time to start comparing datasets of unique Hipper devices to eachother. Do the Hipper devices give nearly similar data according to the graphs that are present in the already existing Research report? That, we will find out in another User Story. The files linked to this user story can be found at: `docs/data/research`

#211 As a student, I want to learn how to make a basic login page, so that I can later incorporate that directly into the web app.

* Starting with this one I had contact with Indigo and Richard on how to go about doing this. I was already expecting to have to do something with figma. I barely have any experience with it, so I got pointed to something Indigo had already made. That gave me a good base and would let me explore figma a little. After starting the first thing I did was go back to an earlier user story I did which was about the components for our web app. Then too I looked at some login pages through Google image search. After deciding on a lay-out, I went to work in Figma. I looked up a mini tutorial on YouTube: `https://www.youtube.com/watch?v=7TF2ZmtkZz0` this quickly helped me with where to find certain things. That way I constructed the login page fairly quickly. 

#223 As a student, I want to learn more about docker, so that I can setup a script which will run the web app locally.

* Having already heard about docker many times throughout my IT life it always came across as a little scary. Especially for me as a BIMmer it always seemed like something only diehard developers would get in touch with. In my recent years I taught myself to have a mentality that I can learn anything as long as I truly set my mind to it. Then when first searching on google for some sample scripts, I noticed that for the things we needed as a group it really was not that scary after all.

* So, my first goal was to re-implement the docker script Indigo had already created for the mysql database. I talked to him about how we wanted to do this, because again, I have 0 docker experience. He explained to me that the `docker-compose.yml` file would need to be in the main folder structure. Then we could leave all of the specific files in their respective folders where they belong. So after some more research and prompting `ChatGPT`, I now know what he ment with that.
So using common sense I was able to switch over his SQL docker file to the main `docker-compose.yml`. After that implementing a simple nginx script to launch our web app turned out to not be difficult too. Again with some help from `ChatGPT` I had successfully done that. Of course I needed to adjust the file structures and where it had to search for certain things myself, but with my common sense it worked out perfectly.

#244 As a student, I want to know how to connect the database to the flask app, so that I can implement it into the docker script.

* In an earlier user story I had already started with setting up a script for docker so that our groups application would be entirely containerized. Seeing my background as a BIM student I had a lot to learn. So what I had done was convert the simple SQL docker script by indigo to our root folders `docker-compose` including the flask service. When everything ran at first I though I was done. Then I realized the database was not connecting, so I had to figure out what was going wrong and where. Since the entire script links to quite a few files in the repository this took some time to figure out. With some scripting help and explanation from `ChatGPT` and `Google Gemini`, I managed to even go the extra mile to remove the hardcoded database values from our python files. So now all of the database credentials and other variables are located in: `./src/back-end/database/.env`. Docker also reads from this env file to set everything up correctly. 

#252 As a student, I need to fix remaining issues for Docker to successfully launch the webapp, so that we can continue development.

* Today Richard notified me about Docker no longer working. I was surprised because of course the last time I tested everything was working fine. So I cloned the main repository and to my surprise it indeed was no longer working. I had seen that Victor added a new component to the lib which is called "anomaly_detection". Unfortunately he didn't implement it in a way so that the .py module was recognizable for docker. I already notified him about this. Anyway, through a bit of help from `ChatGPT` I was able to notice this quickly. Then I also found a minor mistake in the database `init.sql` file which was causing the mysql service to spit out an error and not boot correctly. I fixed that too. Docker works now. 

#276 As a student, I want to learn how to make sure the website automatically adopts changes, so that my team can develop without needing to reload the docker container.




## Journal

### 5/7/2025

Today I am going to look into the list of components needed for the Figma design with Indigo. I will also look into the system components that are needed for our project, once again with Indigo. After that I will sit together with Darian to make a start with the PowerBI visualisations.

Now that I have done the previous things I personally took on the task with the user story about system components. I created a work document which has already been committed into the main branch. This document consists out of the acceptance criteria which belongs to that user story: A list of expected components (e.g. dashboard, settings, authentication, user profile) is created & The overview is reviewed and approved by at least one developer.

When I look back on today it was a decent start and I hope to continue this pace for the coming days. Tomorrow I will look into a PowerBI user story myself and hopefully finish it that same day. I am also keeping track of my learning story parts but I will submit those at a later time because they require a learning question and are required to be submitted individually.

### 5/8/2025

Today I will start working on the data visualisation. I am planning on doing this with Darian to see what possible graphs could work out, even though we know we do not have much data to do visualisations with. I also created a user story (number 102) where I will make sure I look into a solid way of constantly fetching new csv data into my test graphs.

I started looking into the visualisations with Darian and we came up with a few decent ones that somewhat visually represent the data for a better reading experience. Whilst doing this we both also looked into a way of sharing the PowerBI file online. After a bit of back and forth we realised that the HvA no longer has the PowerBI premium/pro plan which is needed to be able to do this. It could form a potential project risk because we rely on PowerBI to represent our data in a web app. Darian and me both requested permission through some sort of panel, now we wait for a response. Later on we might end up having a call with the HvA about this if needed.

Looking back on today I was able to complete my user story about easily fetching new sensor data from the same folder. It's important that we can easily import multiple .csv files when we have several hipper devices producing data, especially for the development stage. The PowerBI difficulties with not being able to share a report online remains a problem that is to be continued.

### 5/11/2025

Today I mostly reviewed some user stories and learning stories. I also started with my own learning story and one of my user stories was merged. 

Tomorrow back at school I will look into the PowerBI situation again. I really hope to then be able to make use of the online version. If not I will contact one of my lecturers to discuss the problem. Darian already talked about an alternative route we could take, so that could be the last resort. 

### 5/15/2025

Today as a team we have the sprint review with our Product Owner Michel Oey (from Digital Life). We prepared well as a team and plan on presenting all of the work we have done the past week. When I say past week I mean that. It's been slightly hard to really work on it when being introduced to the entire new Git system, especially for me as a bimmer. Combine that with all of the holidays, a week off, sometimes no classrooms available. It adds up to an non optimal start to the project in my opinion. 

### 5/21/2025

Today in the daily standup we as a group discussed what still needed to be done. Since this week we have a mini sprint we are focused on making sure we have a standing dataset and that the PAM device functions like we expect it to. In the to-do list I decided to pick up and analyze the way Hipper Therapeutics tested the PAM devices. In another user story it is also up to us to performs these tests, since it will be crucial for us to know if each device reports the exact same data, or at least nearly identical. 

### 5/25/2025

In the weekend I made sure to finish up one learning story. The coming week I will be working on my first programming challenges. I know a fair amount now, so I'm curious what I will walk into. Likely I will have to work on the web application where I need to work on my JavaScript skills and/or HTML CSS. I hope to first implement the login part, or at least the design. The functionality will be another challenge 

### 6/1/2025

Today I finished my learning story about docker. This was actually way easier than I thought in hindsight. My goal now is to work on the front end. Working on web stuff is probably my least favorite thing, but I will do what makes the group move forward. 

### 6/6/2025

Today I have my second expert review with Raymond. I achieved a meets expectation, although he had some criticism on the way I formed my user story. He explained that it looked too much like a developer story. I agreed with him. Thanks to his clear explanation he set me up in a way where I should now be able to do everything correctly for the final expert review with Gerald. 