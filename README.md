Platform to deal with bookings within the live entertainment industry built in Python3(django),Css,Html,Javascript and SQLite.


How it works?

You have to create an account to submit the artists you are managing, those instances of the user class 
are going to be stored in your Artist model which is related to it, where you can set the name, description, photo  and price for the service.
Once they are created they will appear in the home page where artists from all the users are being shown. When you want to contract an artist you click on the 
previous information where only the name an image is placed, this will take you to an url where the whole information is presented with an option to make the deal. 
After clicking this button you are going to be at the Offer page, here you have to submit a form with your offer, then this offer will show up on the user side 
in the page bookings to accept or cancel this offer, if  accepted  it will be inserted in the correspondent calendar.
