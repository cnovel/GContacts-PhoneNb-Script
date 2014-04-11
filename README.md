Formating script for GMail Contacts' phone numbers
========================
This script formats the phone numbers of your GMail Contacts, using the .csv file provided by Google. It adds international code before the numbers and format them so they all look the same. It currently supports French numbers and UK numbers.

How to use it
---------------
Download your Google .csv contact file. Open it with Notepad or your usual text-editor. Copy all the text in the file and paste it in a new file. Save this file, for example gContact.csv. **Warning**: A simple right-click "Copy file" won't work here since Google is using a Byte Order Mark at the beginning of its file and the script can't deal with it currently.

Once this is done, simply call the command : `python script.py gContact.csv output.csv`

The contact file with the formatted numbers is output.csv. The upload it via GMail Contacts, and you are ready to go!

Possible bugs
---------------------
Currently, the .csv written is using quotation marks, which may cause issues if you have quotation marks in your original file.