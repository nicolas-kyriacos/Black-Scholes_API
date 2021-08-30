# Black-Scholes_API
API to calculate European call options

**How the program works**

The program contains two files, namely 'main.py' and 'UI.py'. The 'main.py' file contains an API which is used to calculate European call options using a Black-Scholes function.
The 'UI.py' file contains a user interface which takes in user input, makes a call request to the API which calculates the call option using the Black-Scholes 
function, and retrieves the output to the user.

**Additional functionality**

The program continously runs until the user decides to exit and handles user error in order to ensure that it runs smoothly.
Additionally, while the Black-Scholes formula directly requires the current price of a stock as an input, the UI works in such a way that the user can instead enter a ticker symbol of a stock
and it will search the web for the ticker's current stock price. However, if the user provides a ticker that doesn't actually exist, the UI will require them to enter the current price of the ticker that couldn't be found, which will then be used as an input in Black-Scholes

**How to get the program set up and running**

First, the user needs to open two command prompts and navigate to the directory that the program's files are stored in each command prompt. The program cannot run if the user is in the wrong directory.
Then, in the first command prompt, the user will type `python main.py` to start running the API. This creates a local URL for the API which the UI will use to access it. 
In the seconds command prompt, the user will type `python UI.py` to start running the user interface.
Note that the API needs to be run before the UI as the UI depends on it to function. 
Additionally, the UI assumes that the API is running on the local url://127.0.0.1:5000/. If API's local url is different on the user's computer for whatever reason, then the user needs to look for the
source code labeled `BASE = //127.0.0.1:5000/` and substitute the value of the `BASE` variable to their local URL.
