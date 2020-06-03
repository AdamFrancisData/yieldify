import os
from flask import Flask, request, abort, jsonify
from sql_queries import brower_with_params, os_with_params, device_with_params
from models import setup_db, Log, db


def get_error_message(error, default_text):
    """

    Args:
        error: error object
        default_text: A string message to return upon error

    Returns:

    """
    try:
        # Returns message contained in an error
        return error.description["message"]
    except TypeError:
        # otherwise, return given default text
        return default_text


def create_app(test_config=None):
    '''
    create and configure the app
    '''
    app = Flask(__name__)
    setup_db(app)

    @app.route('/stats/browser', methods=['GET'])
    def get_browser_stats():
        """

        Returns: All browser items as a json response

        """
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)

        # Gets all results from db
        if start_date and end_date:
            results = db.session.execute(
                brower_with_params.format(f"AND date >= '{start_date}' AND date <= '{end_date}'"))
        else:
            results = db.session.execute(brower_with_params.format(' '))

        data = results.fetchall()
        # If nothing is returned then throw up an error
        if not data:
            abort(400)

        dict_data = dict(data)

        # Return successful response with a complete list of browsers
        return jsonify({
            'success': True,
            'start_date': start_date,
            'end_date': end_date,
            'result': dict_data
        })

    @app.route('/stats/os', methods=['GET'])
    def get_os_stats():
        """

        Returns: All Operating systems items as a json response

        """
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)

        # Gets all results from db
        if start_date and end_date:
            results = db.session.execute(
                os_with_params.format(f"AND date >= '{start_date}' AND date <= '{end_date}'"))
        else:
            results = db.session.execute(os_with_params.format(' '))

        # If nothing is returned then throw up an error
        data = results.fetchall()
        if not data:
            abort(400)

        dict_data = dict(data)

        # Return successful response with a complete list of browsers
        return jsonify({
            'success': True,
            'start_date': start_date,
            'end_date': end_date,
            'result': dict_data
        })

    @app.route('/stats/device', methods=['GET'])
    def get_device_stats():
        """

         Returns: All device items as a json response

         """
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)

        # Gets all results from db
        if start_date and end_date:
            results = db.session.execute(
                device_with_params.format(f"AND date >= '{start_date}' AND date <= '{end_date}'"))
        else:
            results = db.session.execute(device_with_params.format(' '))

        data = results.fetchall()
        # If nothing is returned then throw up an error
        if not data:
            abort(400)

        dict_data = dict(data)

        # Return successful response with a complete list of browsers
        return jsonify({
            'success': True,
            'start_date': start_date,
            'end_date': end_date,
            'result': dict_data
        })


    # Error handling:
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": get_error_message(error, "bad request")
        }), 400

    @app.errorhandler(404)
    def ressource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": get_error_message(error, "resource not found")
        }), 404
    #
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": get_error_message(error, "unprocessable")
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app
