from flask import render_template
from . import main

# Error handlers defined here within the @main namespace are only used by the
# main blueprint. To use them application wide error handlers should use the
# global @app_errorhandler decorator.

@main.app_errorhandler(404)
def page_not_found(error):
    # return render_template('404.html'), 404
    return '404'

@main.app_errorhandler(500)
def internal_server_error(error):
    # return render_template('500.html'), 500
    return '500'
