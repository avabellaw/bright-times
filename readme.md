# Bright Times - Milestone Project 4

Bright Times is a platform for exploring and keeping up-to-date on new and upcoming events. 

This projects demonstrates my ability to create a full-stack application with eccommerce funtionality. It uses the Django framework along with HTML5, CSS3, JavaScript and ofcourse Python. I also use SQL to manage the database.

[View the live project here]()

![]()

## Technologies used

### Lanuages used

* HTML5
* CSS3
* JavaScript
* Python

### Frameworks, Libraries & Programs Used

* JQuery datetimepicker
* boto3
    * To interact with AWS S3 bucket.
* django-allauth
    * User authentication, registration and management.
    * To send and manage emails.
* Stripe
    * To implement the card payment system. 
* djlint 
    * For django-html auto formatting.
* Django 5
    * Full python framework.
* Bootstrap 5
    * CSS framework
* autopep8 extension/package
    * Package to automatically format to PEP8 standards.
* Google Fonts
* Easy access to many fonts supplied from a CDN that is close to the user, increasing download speed.
* Font Awesome
    * Professional icons
* Git 
    * Used for version control.
* GitHub
    * Used to store commits.
* Heroku
    * Hosts the live project.
* Visual Studio Code
    * Used as the IDE for the project.
    * I set a shortcut for Visual Code to format HTML/CSS/JS (ctrl+shift+f).
        * This also worked for Python after installing autopep8.
* Paint.NET
    * Used to edit images for the project.
* Figma
    * Used to create the mockup of the website before developing.
* Lucid.app
    * Used to create an Entity Relationship Diagram to model the data.
* Word 
    * Used to present the project requirements in my own words, for project research, and brainstorming.
* Notepad and Notepad++
    * Used for quick notes from my mentor and for notes while developing.
    * Used for planning.
* Chrome - Inspect element
    * This was used to:
        * Style the website and test new ideas to be copied into the project.
        * Continuously test responsiveness by adjusting the screen size and by testing preset device dimensions.
        * Bug fix.
* Firefox, Microsoft Edge, Safari
    * Used to test compatibility on other browsers.
* [Responsinator](http://www.responsinator.com/) for testing on different screens.
* [Grammarly](https://app.grammarly.com/)
    * To help find and correct grammar and spelling mistakes.

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

### Data model

I decided to seperate the address from Venue to better organise the data. I considered a one-to-one relationship, however, a one-to-many relationship would enable a different venue under the same address to use the existing address record. Therefore, it allows for the future introduction of this feature. While aknowedging that this is a rare case, this would avoid duplicate address records.

The original idea was to use a user ID to set the Event's created by. If you wanted the venue manager, you just use the user ID. However, a user can also have a ticket and therefore I believe it makes it more clear if created_by is set to the venue manager who created the event.

Django doesn't support composite primary keys so the junction table VenueManager still has a primary key. I have set the meta so that the combination of User ID and Venue ID is unique. The primary key will be useful for indexing in future anyway.
This will allow me to filter by userID and VenueID and get a result as if using a composite ID.

#### Ticket

A ticket is a junction table between an event and a user.
It also contains the foreign key of a ticket order. Multiple tickets can be created under one order.

#### Ticket order

* Ticket order has it's primary key as a UUID. 
    * This makes guessing the checkout-success page url practically impossible. 
    * A UUID is unique as it's mathematically impossible to get the same one twice. Although techincally it is a non-zero chance.
* Order date.
    * Contains the date on creation. Useful information for the customer and for debugging.
* Quantity and price redundancy.
    * Although this information is redundant, it will help debugging in future.
    * This way, the quantity and price will never change regardless of the event or ticket instances.
    * The information can be easily matched with the information on Stripe's end too.


**Future adaptations**

* Change about field into a rich text field.
    * This will allow the user to add images and style their text.


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

PaymentIntent is created with a customer ID if user profile has one. If not, a new customer object is created.
The customer object contains the email for the receipt. The reciept will only be sent once Stripe is set to live mode.

The Stripe PaymentIntent is also created with a description of the ticket ordered and quantity. 

When the stripe payment is completed, the return url is the create_order view. This confirms the payment intent and ensures it's not already been created. It then creates the order and the tickets associated with it.

Quantity, price and total price are added to the TicketOrder model. This is redundant information but is useful for debugging in future.
If an order were to go wrong, you would have the quantity and price of the ticket at order creation.
The order total also adds an extra level of redundancy incase a calculation went wrong. It ensures that this information will match up with stripe records in one way or another. Order total is also useful for auditing data or creating reports.

# Bug fixes

* Cripsy forms returns error "too many values to unpack (expected 2)"
  * [https://stackoverflow.com/questions/37244808/valueerror-too-many-values-to-unpack-expected-2-in-django](Make choices a tuple of 2)

# Known bugs

* Quantity button on buy ticket page flickers when you go under 1 or over 10 (using the up/down arrows).
    * This is to allow the JavaScript validation to show the error message.
    * I originally had the min/max values set but this would mean the validation message wasn't triggered.
    * Besides, I believe the flickering back to a valid number enforces the validation further.

# Credits

## Images

* Location icon from [flaticon by Shastry](https://www.flaticon.com/free-icon/map_9120063?term=venue&page=1&position=79&origin=search&related_id=9120063)
* Calendar icon from [fontawesome](https://fontawesome.com/icons/calendar?f=classic&s=regular)
* Venue icon from [thenounproject by Vicons Design](https://thenounproject.com/icon/venue-79187/)
* Sun icon from [freepik by Muzammal Hussain](https://www.freepik.com/icon/sun_13443601#fromView=search&page=1&position=28&uuid=c73706b9-c633-4704-9131-5ffd741c6e21)
    * I created the favicon in paint.NET using this icon
* Logo I created in paint.NET

## Code

* Test a view from [docs.djangoproject](https://docs.djangoproject.com/en/5.0/intro/tutorial05/#test-a-view)
* How to use JQuery datetimepicker from [xdsoft.net](https://xdsoft.net/jqplugins/datetimepicker/) 
* Create a user profile when a user is created from [medium.com](https://medium.com/@abdullafajal/automating-user-profile-creation-with-default-data-using-django-signals-50abef9ce529)
* Implemented stripe payments using the [stripe documentation for checkouts](https://docs.stripe.com/checkout/quickstart?lang=python), [stripe documentation for payment intents](https://docs.stripe.com/api/payment_intents/create), and this guide from [testdriven.io](https://testdriven.io/blog/django-stripe-tutorial/)

## GitHub

* How to use GitHub roadmap from [GitHub docs](https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/customizing-the-roadmap-layout)