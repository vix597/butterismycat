# Butterismycat

To install command-line tools to manage
dependencies and to run Butterismycat.com server.

1.  Download and install Node from [https://nodejs.org/](https://nodejs.org/). Node includes the node package manager command, `npm`.

1.  Install Python 3.5 or newer from [https://www.python.org/](https://www.python.org/). You will need this to run the server and to install dependencies with pip.

1.  Install `bower`:

        npm install -g bower
        
1.  Change directory to your local repo and install dependencies with `pip`:

        pip install -r requirements.txt
        
1.  Next, change into the inner `plumbus` directory within the local repo and install dependencies with `bower`:

        cd butterismycat
        bower install
        
1.  To run, execute the following from the root of the local repo directory:

        cd ..
        python server.py

    Use `python server.py -h` for usage documenation
    Once running, open `http://localhost:5000` in your browser.