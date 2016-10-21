'''
Runs the web server for butterismycat.com
'''

import argparse
import os
import traceback

def main():
    '''
    Setup the things. Run the servers
    '''
    parser = argparse.ArgumentParser(description="ButterIsMyCat.com")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable the debug server")
    parser.add_argument("-p", "--port", action="store", type=int, help="Port to run on")

    args = parser.parse_args()

    try:
        import butterismycat.ui.web as grumbo
        grumbo.run(debug=args.debug, port=args.port)
    except BaseException as error:
        print("Exception: ", str(error))
        print("See", os.path.abspath(os.path.join(os.path.dirname(__file__), "bugreport.txt")),\
        "for extended error information")
        with open(os.path.join(os.path.dirname(__file__), "bugreport.txt"), 'w') as f:
            traceback.print_exc(file=f)
        exit(1)
    exit(0)

if __name__ == "__main__":
    main()
