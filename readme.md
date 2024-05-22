# Bright Times - Milestone Project 4

Bright Times is a platform for exploring and keeping up-to-date on new and upcoming events. 

This projects demonstrates my ability to create a full-stack application with eccommerce funtionality. It uses the Django framework along with HTML5, CSS3, JavaScript and ofcourse Python. I also use SQL to manage the database.

[View the live project here]()

![]()

## Frameworks, etc used

* JQuery datetimepicker

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

I decided to keep not seperate venue into a seperate app. This can be done in future but, at present, venue is simple enough to not require it. A venue is used to create an event.

A ticket is a simple model linking an event with a user. I have decided not to seperate this either.

## Surface plane

I wanted to use a bright colour. Either yellow/orange to represent the sun or a calm blue representing trust. 

[cvent - how to choose event website color:](https://www.cvent.com/en/blog/events/how-to-choose-event-website-color)
Yellow. Bright and sunny, yellow is the color of optimism.
Green. This is the color of growth and health.
Blue. The color of trust, blue conveys tranquility, serenity, and peace.

# Stripe payments

I followed the Stripe documentation and a guide by testdriven as [mentioned in the code credits](#Code).

I also used the walkthrough project for additional guidence.

# Credits

## Images

* Location icon from [flaticon by Shastry](https://www.flaticon.com/free-icon/map_9120063?term=venue&page=1&position=79&origin=search&related_id=9120063)
* Calendar icon from [fontawesome](https://fontawesome.com/icons/calendar?f=classic&s=regular)
* Venue icon from [thenounproject by Vicons Design](https://thenounproject.com/icon/venue-79187/)

## Code

* Test a view from [docs.djangoproject](https://docs.djangoproject.com/en/5.0/intro/tutorial05/#test-a-view)
* How to use JQuery datetimepicker from [xdsoft.net](https://xdsoft.net/jqplugins/datetimepicker/) 
* Create a user profile when a user is created from [medium.com](https://medium.com/@abdullafajal/automating-user-profile-creation-with-default-data-using-django-signals-50abef9ce529)
* Implemented stripe payments using the [stripe documentation for checkouts](https://docs.stripe.com/checkout/quickstart?lang=python), [stripe documentation for payment intents](https://docs.stripe.com/api/payment_intents/create), and this guide from [testdriven.io](https://testdriven.io/blog/django-stripe-tutorial/)

## GitHub

* How to use GitHub roadmap from [GitHub docs](https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/customizing-the-roadmap-layout)