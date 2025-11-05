from flask import Flask

app = Flask(__name__)

'''
def main():

   # print(f"*** Entered main, application name = {__name__}")
   app.run(host="0.0.0.0")

   
if __name__ == "__main__":
   main()   
else:
   pass
   # print(f"*** application name = {__name__}")
'''


print(f"*** Entered main, application name = {__name__}")

from app import routes
