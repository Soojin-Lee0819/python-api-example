from flask import Flask, jsonify, request #common library to build servers
from flask_restful import Api, Resource #give additional resources to play with doc strings
from flasgger import Swagger

import book_review

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

class UppercaseText(Resource):
    def get(self):
        """
        This method responds to the GET request for this endpoint and returns the data in uppercase.
        ---
        tags:
        - Text Processing
        parameters:
            - name: text
              in: query
              type: string
              required: true
              description: The text to be converted to uppercase
        responses:
            200:
                description: A successful GET request
                content:
                    application/json:
                      schema:
                        type: object
                        properties:
                            text:
                                type: string
                                description: The text in uppercase
        """
        text = request.args.get('text')

        return {"text": text.upper()},200

class StringGenerator(Resource):
    def get(self):
        """
        This method responds to the GET request for this endpoint and generates a modified string based on provided parameters.
        ---
        tags:
        - String Processing
        parameters:
            - name: message
              in: query
              type: string
              required: true
              description: The message to be processed
            - name: duplication_factor
              in: query
              type: integer
              required: false
              default: 1
              description: The number of times the message should be duplicated
            - name: capitalization
              in: query
              type: string
              required: false
              enum: [UPPER, LOWER, None]
              description: Specify 'UPPER' for uppercase, 'LOWER' for lowercase, or leave empty for no capitalization change
        responses:
            200:
                description: A successful GET request
                content:
                    application/json:
                      schema:
                        type: object
                        properties:
                            result:
                                type: string
                                description: The processed message
        """
        args = request.args
        message = args['message']
        duplication_factor = int(args.get('duplication_factor',1))
        capitalization = args.get('capitalization',None)
     
        if capitalization == 'UPPER':
            message = message.upper()
        elif capitalization == 'LOWER':
            message = message.lower()

        generated_text = message * duplication_factor
        return {"generated_text": generated_text} , 200

api.add_resource(StringGenerator, "/generate")
api.add_resource(UppercaseText, "/uppercase")

if __name__ == "__main__":
    app.run(debug=True)