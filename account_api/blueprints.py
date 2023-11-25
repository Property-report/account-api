from account_api import app
from account_api.views import general, user, payments


def register_blueprints(app):
    """
    Adds all blueprint objects into the app.
    """
    app.register_blueprint(general.general)
    app.register_blueprint(user.user)
    app.register_blueprint(payments.payment)

    # All done!
    app.logger.info("Blueprints registered")
