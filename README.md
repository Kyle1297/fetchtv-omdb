# fetchtv-omdb

A simple web form for looking up movies and television shows from an external API where the responses from the API are stored in a database to be used as results for future searches.

## Installation and set-up

Assuming you have Python 3 installed, setup your virtual environment and cloned this repository:

1. Change into the top-most directory, 'fetchtv-omdb'
2. Run 'pip3 install -r requirements.txt'
3. Then, run 'python manage.py runserver'
4. Interact with the application at 'localhost:8000'

## Walkthrough

1. On the index page('/'), there is a simple form with two fields. Both 'Type' and 'Query' fields are required. Once filled, click 'Submit'. A POST request is then transmitted, which triggers a redirect to '/search/'.
2. At '/search/', you will see the same form (containing your inputs) with corresponding results displayed in a table from the OMDB database. Note, there is first a local lookup in our SQLite database. If the number of entries returned from this lookup is less than a set limit (i.e. MINIMUM_ENTRIES in the settings.py file), then an API call is made to the OMDb database to retrieve additional results.
3. Any errors that occur in this process will be displayed. You can easily try another search on the same page.

### Admin

Feel free to browse the '/admin/' site and log in with the following credientials:
- username: admin
- password: admin

Here, you will click on the 'Videos' option and preview all the videos currently stored in the local database. 

A couple of features you may note:
- You cannot ADD new videos, only edit or delete pre-existing ones (as per instructions)
- You can either filter by searching in the textfield or filter by 'Type' on the right

### Management script

Finally, there is a Django management script that can be run periodically to keep local records up-to-date. 

Note, until OMDB updates their API and allows a list of IMDb IDs to be searched at once, this process will be quite inefficient and slow. So, please use it infrequently and conservatively to minimise the number of API calls.

To run it, simply use 'python manage.py update_omdb'.

## Final notes

If you have any questions, please get it touch. I am more than happy to discuss.

** Environment variables have been included in this repository as this project is not designated for production.