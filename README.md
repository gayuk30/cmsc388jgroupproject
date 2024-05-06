## Description of your final project idea:

Personal website for a fictional person named “Bob” that shows off the different companies and roles he’s worked. Also, people he has worked with in the past can leave reviews about him.


## Describe what functionality will only be available to logged-in users:

Only logged in users can add jobs "Bob" has worked and give reviews about him. (Must be logged-in to have access to the work and review forms)

## List and describe at least 4 forms:

- **Registration form**: Allows employers to register
- **Login form**: Allows returning users to login
- **Job form**: Employers can add jobs "Bob" has worked
- **Review form**: Employers can provide a reviews about "Bob"

## List and describe your routes/blueprints:

- **Blueprint 1: users**
  - `/register` - user creates account
  - `/login` - route for user to login to an already existing account
- **Blueprint 2: employer**
  - `/job` - directs to form for employer to add "Bob" work experience
  - `/reviews` - directs to form for employer to write review for "Bob"

## Describe what will be stored/retrieved from MongoDB:

- Accounts, Job Information, Review Information

## Describe what Python package or API you will use and how it will affect the user experience:

Google Maps API to show all the locations "Bob" has worked. This will affect user experience by giving our application a cool feature where users can view a map of the places "Bob" has been.