#  ~ *Swap Books - Share the fun*

![logo](https://i.imgur.com/zg49V5K.png)

# Introduction

## The Project
Tradit will address the common scenario where individuals accumulate books they no longer need. Often, after reading a book, one might prefer not to keep it unless they are building a personal library. Tradit will offer a platform to exchange, or give away these books, creating an opportunity to connect with others interested in these titles.

## The Context
This project serves as my Portfolio Project, marking the conclusion of my Foundation at ALX - Holberton School. I had the option of working either in a team or doing it solo. While I desired to undertake this project collaboratively and reap the benefits of teamwork, I ultimately chose to work alone due to my availability constraints during these days. I didn't want to be a burden to anyone.

## The Team
I am a passionate coder who enjoys bringing a creative touch to projects. Here's a bit about me:

[Jules Ntizimira](https://twitter.com/NtizimiraJ) - Book lover and entrepreneur, currently working solo on this project. I bring a unique perspective to coding, fueled by a passion for both literature and entrepreneurship.

Follow me on Twitter for more tech related awesomeness!

## Blog posts
After the development phase, we each wrote a blog post to reflect on the PuppR journey.

* Marc's article: [PuppR: It’s Like Tinder For Dogs](https://medium.com/@mcavigli/puppr-its-like-tinder-for-dogs-c498bf4bdd9b)
* Drew's article: [PuppR: The social app for dog people](https://medium.com/@andrew.maring/puppr-the-social-app-for-dog-people-dcdb1c496f29)
* Laura's article: [PuppR: Learnings from building a dating site for dogs](https://medium.com/@laura.derohan/learnings-from-building-a-dating-site-for-dogs-70f4d649f2b3)

# Tutorial

## Take a tour of the deployed version at puppr.best
-> [**PuppR**](https://puppr.best/)

Here is a little preview of our main feature, the swiping through other dogs' profiles:

![swiping](./public/icons/browse_no_text.png)

Here is a simple flow for the user experience on PuppR:

![user-flow](https://i.imgur.com/hRxU79B.jpg)

## Run PuppR with Vue-CLI
Installing the programs necessary to view this project is pretty simple!

We'll be using [`npm`](https://www.npmjs.com/get-npm) to install Vue and Vue-CLI. First clone this repo, then navigate to the root and [install Vue](https://vuejs.org/v2/guide/installation.html) by executing this command:
`puppr$ npm install vue`

Once that has finished, [install Vue-CLI](https://cli.vuejs.org/guide/installation.html) with this command:
`puppr$ npm install -g @vue/cli`

In case there are any missing dependencies, please execute `puppr$ npm install` to get them. If there's an error, it should return the specific command you need to enter.

Once this is all done you're ready to run **PuppR**! Still in the root of this directory, simply execute `puppr$ npm run serve` and give it a few seconds to get started. Once it's up, you can open your web browser and enter `localhost:8080`. This will allow you to try out **PuppR**!

When you are finished simply go back to your terminal and hit `ctrl + c` to quit the program.

## Known bugs
* Some transitions are not as fluid as expected, and due to API calls lag can be a bit off.
* Issue when viewing on mobile. Many of the assets become squished vertically.

# Architecture

## Overview
web app consists of Python and MySQL on the backend, Flask as the framework interface, and HTML/CSS and Javascript for frontend functionalities. Nginx manage the server side and served by gunicorn application server. 


![infra](https://i.imgur.com/fSbo6ho.jpg)

## Vue.js
For this project, we decided to focus on learning a new front-end framework. Following the advice of mentors and professionals, we chose to learn and use Vue.js.

Every different section of the app is a Vue component, and all the components can be found in the directory [src/components/](./src/components/). The main component "App" is defined in [App.vue](./src/App.vue), and is the entry point of the app.

All the components are linked together thanks to a VueRouter instance, defined in [index.js](./routes/index.js). Each component is linked to a route, which path is appended automatically at the end of our URL.

The [main.js](./src/main.js) file contains the instanciation of the Vue for the entire app, as well as the config options, database session and authentication session.

Another interesting point about Vue.js is that it allowed us to use a store, defined in [store.js](./src/store.js). This store is a front-end store that keep strack of the state of components and data throughout the app. This is were the data from our database requests is stored and updated before going back in the database. This store also allows to not pass props from each component to all its children components, and to access data from anywhere without having to use and event bus.

### List of components

These components make up what a user experiences when they check out **Tradit**. Each component contains the code for a specific page of the app. These components can be located in [webdynamic/templates](./webdynamic/templates).

| Component | Description |
|-----------|-------------|
| [index](./webdynamic/Landing.vue) | The landing page a user sees when they navigate to **Tradit**. |
| [Login](./webdynamic/templates/login.html)   | The login page. There's a link to go to the Signup page if a user hasn't signed up. |
| [Community](./webdynamic/templates/users.html) | Page where users can see the other users. |
| [chat room](./webdynamic/templates/room.html) | The chat room page where users can have a secure conversation  |
| [Signup](./webdynamic/templates/register.html) | Signup page for users who do not have an account. It asks for a name, username, email, address, and a profile photo upload |
| [dashboad](./webdynamic/templates/book.html) | The main page of **Tradit** where users can go through available books in wishlist and offer list. you can even search  |
| [about](./webdynamic/templates/book.html) | about page where you can visit and get additional informations about the pratform |

## Firebase
We decided to go with Firebase for our backend/database as it provides all the functionality we need to develop this project such as authentication, database storage, and cloud storage. As a non-relational database, it made calling any required information simple.

Firebase was incredibly helpful while we were testing as it allowed us to look through each user's collection of information. This was helpful while we were implementing the logic for user likes and matches.

### Firestore
Since our app requires frequent and numerous database calls, Firestore provides a reliable and responsive solution to achieve a seamless experience. Practically all user information, such as display name, dog info, and even their like/match lists are kept in the Firestore. This lets us quickly populate each vue with relevant information.

For instance, when a user logs in they'll be taken to the main [Swiping](./src/components/Swiping.vue) component where another user's image, dog name, age, and location will be dispalyed. They can choose to 'like' or 'pass' the dog, which will immediately populate with another dog's information. Firebase's quick database calls populate this information and help keep this functionality snappy.

Images are kept in the Firestore as a link to where they're held in cloud storage. 
### Authentication
As our app connects people and their dogs, authentication is a necessity. Firebase provides a straightforward and easy-to-implement solution so we can focus on designing an accessible app. Users simply sign up with an existing email address and a password of their choice. Firebase Authentication does the heavy lifting to make sure users are authentic.
### Cloud Firestore
The obvious choice for storing users' dog photos. It provides straightforward implementation for users to upload their photo and a relatively quick way to call and display these images for users to sift through.

# Acknowledgments

* Holberton School staff - For the help, advice and resources they provided us with during this project and during all our curriculum.

* Cohort 8 and all Holberton students - For your friendship, invaluable support, and insight not only for this project, but over the last year.

* Our dogs (or friends' dogs) - For the inspiration, courage and love they brought us when we were working hard and tired.

* Romain Bonhomme - For his incredible Vue.js knowledge and overall front-end good practices.

* Valentin Roudge - For his help and advice in Node.js and architecture best practices.

* YOU - For reading this documentation and testing out **PuppR**. We hope you enjoyed the ride!

# Related projects

* [AirBnB Clone](https://github.com/lroudge/AirBnB_clone_v4): a simple web app made in Python, Flask, and JQuery.

* [Simple Shell](https://github.com/scurry222/simple_shell): a command line interpreter that replicates the sh program.

# License

MIT License
