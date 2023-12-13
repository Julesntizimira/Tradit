# Tradit - Empowering Book Enthusiasts through Shared Reading

![Tradit Logo](https://i.imgur.com/zg49V5K.png)

## Introduction

### The Project

Tradit addresses the common scenario where individuals accumulate books they no longer need. This platform offers a space to exchange or give away books, fostering connections among individuals with shared literary interests.

### The Context

This project serves as my Portfolio Project, marking the conclusion of my Foundation at ALX - Holberton School. Despite the option to work in a team, I chose to work solo due to availability constraints. I aimed to create a seamless experience for book enthusiasts while showcasing my coding skills.

### The Team

I am Jules Ntizimira, a passionate coder with a unique perspective fueled by a love for literature and entrepreneurship. Follow me on [Twitter](https://twitter.com/NtizimiraJ) for more tech-related updates.

## User Stories

As a book enthusiast:
- I want to discover a platform for exchanging books
- So that I can exchange my read books for new ones without incurring additional costs

**Acceptance Criteria:**
- Users can create a profile
- Browse diverse books
- Search for specific books by title, author, or genre
- View detailed book information and user reviews
- Propose book exchanges and receive notifications
- Access a secure communication channel for finalizing exchanges

## Blog Posts

After the development phase, I wrote a reflective blog post on the Tradit journey.

Read the blog post: [Tradit: Swap Books — Share the Joy](https://medium.com/@ntizimijules5/swap-books-share-the-joy-229b658b00fb)

## Tutorial

Take a tour of the deployed version at [Tradit](https://julesntizimira.github.io/Tradit/).

Explore the main feature, the dashboard:

![Tradit Dashboard](landingImages/Screenshot 2023-12-08 at 00.21.53.png)

User chatroom flow on Tradit:

![User Chatroom Flow](https://i.imgur.com/hRxU79B.jpg)

## Known Bugs

- The app is slow due to pictures being saved on the server
- Not responsive views

## Architecture

### Overview

The web app comprises Python and MySQL on the backend, with Flask as the framework interface. HTML/CSS and JavaScript handle frontend functionalities. Nginx manages the server side, served by the Gunicorn application server. An additional app for API runs on different ports. For certain functionalities, the main app accesses the server directly, while others use the API.

### List of Components

These components define the user experience in Tradit, with each component housing code for a specific app page. Components can be located in [webdynamic/templates](./webdynamic/templates).

| Component     | Description                                      |
| ------------- | ------------------------------------------------ |
| [Index](./webdynamic/Landing.vue)   | Landing page for users on Tradit                 |
| [Login](./webdynamic/templates/login.html)   | Login page with a link to the Signup page         |
| [Community](./webdynamic/templates/users.html) | Page displaying other users                     |
| [Chat Room](./webdynamic/templates/room.html) | Secure chat room for users                       |
| [Signup](./webdynamic/templates/register.html) | Signup page requiring user information           |
| [Dashboard](./webdynamic/templates/book.html) | Main page where users explore available books    |
| [About](./webdynamic/templates/book.html) | Information page about the platform              |
| [Register Book](./webdynamic/templates/registerb.html) | Page for users to register a new book    |

## Authentication

I had to learn Flask-Login to implement login management functionalities. The login manager handles user login, taking advantage of its other features, such as using the current user.

## Socket Chat Rooms

Tradit provides real-time live chat between users, facilitating communication. If a user likes a book, they can chat with the owner.

# Acknowledgments

- ALX staff: For the help, advice, and resources throughout the project and curriculum.
- Cohort 13 and all ALX students: For friendship, support, and insights over the last year.
- YOU: For reading this documentation and testing out Tradit. We hope you enjoyed the ride!

# Related Projects

- [AirBnB Clone](https://github.com/Julesntizimira/AirBnB_clone_v4): A web app in Python, Flask, and JQuery.
- [Simple Shell](https://github.com/Julesntizimira/simple_shell): A command line interpreter replicating the sh program.
