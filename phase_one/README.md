# Summary
This is for the scraping apparatus 

master will be the controller

client will be for the individual scrapers

## Master API
- /exists/<ip>/<auth>
	+ Checks if the IP is already registered.
- /register/<ip>/<auth>
	+ Registers the IP - will write out to file on disk
- /receive/<ip>/<auth>
	+ Receives an allocated URL to scrape

	+ This is where the server will check how many we've done in the hour and for the day

- /status/<ip>/<auth> 
	+ This will be called, letting the server know that we're starting up our request

- /post/<auth>
	+ Posts back the results, will then save to disk
	+ We don't care what the IP is
- /end/<ip>/<auth>
	+ Sends to the server letting us know that we have finished as many as we can, either for the hour or for the day

## Client design
- Start up - logging will be very important here
- Check if we already exist in the database 
	+ Register if we don't exist
- Start receive loop
	+ Receive our URL
	+ Send back the status update
	+ Scrape it
	+ Send back results

	+ Repeat until we receive the finished command

- Exit and note in the log that we are done
