# nuhome-files
An add-on which allows to upload one or multiple files into a accessible folder on the homematic-ccu

# Uploading files
To Upload a file, simply drag and drop it into the gray square, and wait until they're done.

![upload](/img/upload.gif "upload")

# Deleting files
Deleting files is simple. Just click the "X"

![delete](/img/delete.gif "delete")

# Accessing files via URL
At the bottom of the page you'll find a list of all uploaded files. 
They all contain their absolute link to the file, so you can simply copy the url.
It will generally look like this:

http://[IP-of-CCU]/addons/nuhome-files/data/[Escaped_Filename.xxx]

# Upload restriction
You need to be logged in to the Homeamtic in order to uplaod files, but not to access them. (SID-Check)
