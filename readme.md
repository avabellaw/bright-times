# Bright Times - Milestone Project 2

Bright Times is a platform for exploring and keeping up-to-date on new and upcoming events. 

This projects demonstrates my ability to create a full-stack application with eccommerce funtionality. It uses the Django framework along with HTML5, CSS3, JavaScript and ofcourse Python. I also use SQL to manage the database.

[View the live project here]()

![]()

## User Experience (UX)

### Project Goals

This will be a website where you can discover an event that fits you. 

The project will be designed using the 5 planes of UX design. I will ofcourse be taking a mobile-first approach. This is especially important for an events based website, as usersare more likely to be travelling while using it.

### Stragtegy Plane

The audience will be diverse as events can be targeted towards a wide range of people.

Bright Times will be an event directory where users can find events and pay for tickets.

**User goals:**
* Browse events
* View event details.
* Filter events by location.
* Buy tickets.
* Save events to view later.

**Site owner goals**
* Gain commision from ticket sales.
* Spread awareness of events.

### Research

[Research conducted for this project can be found here](docs/research/Research.md)

## Scope Plane

Features to include:
* Login functionality - provided by alluth.
* Ability to save card details and address
* Users will be able to view their tickets.
* Users will be able to browse events, they will also be able to browse by location.

Possible features to include:
* Notify users of upcoming events by email.
* Ability to subscribe to a reminder of an event.

Future features:
* Reacurring events.

### User stories

<!-- Turn this into a table -->
1	User	I want to see events 	Find one I like and buy a ticket
2	User	I want to see event details	Make an informed decision before buying a ticket
3	User 	I want to sign up for an account	To buy tickets
4	Staff member	I want confirmation of work at an event	Revisit event details and confirm im booked
5	Venue manager	I want to list my venue	I can book events
6	Venue manager	I want to list events for my venue	I can sell tickets
7	Venue manager	I want to see how many people are signed up	To know how many people are coming
8	Venue manager	I want to edit my venue and event details	To keep them up-to-date

## Structure plane

I will include the following pages:
* Homepage
* Events pages
* Profile page

Under the header, there will be hierarchical navigation.

### The data

I decided to seperate the address from Venue to better organise the data. I considered a one-to-one relationship, however, a one-to-many relationship would enable a different venue under the same address to use the existing address record. Therefore, it allows for the future introduction of this feature. While aknowedging that this is a rare case, this would avoid duplicate address records.

The original idea was to use a user ID to set the Event's created by. If you wanted the venue manager, you just use the user ID. However, a user can also have a ticket and therefore I believe it makes it more clear if created_by is set to the venue manager who created the event.

Django doesn't support composite primary keys so the junction table VenueManager still has a primary key. I have set the meta so that the combination of User ID and Venue ID is unique. The primary key will be useful for indexing in future anyway.
This will allow me to filter by userID and VenueID and get a result as if using a composite ID.

## Skeleton plane

## Surface plane

I wanted to use a bright colour. Either yellow/orange to represent the sun or a calm blue representing trust. 

[cvent - how to choose event website color:](https://www.cvent.com/en/blog/events/how-to-choose-event-website-color)
Yellow. Bright and sunny, yellow is the color of optimism.
Green. This is the color of growth and health.
Blue. The color of trust, blue conveys tranquility, serenity, and peace.