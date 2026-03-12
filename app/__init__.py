from flask import Flask, session, redirect, request
import os


def create_app(debug: bool = False):
    # Check if debug environment variable was passed
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", False)
    if FLASK_DEBUG:
        debug = FLASK_DEBUG

    # Create the Flask application instance
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
        static_url_path="/",
    )

    # Set current_app context
    app.app_context().push()

    if debug:
        from app.config.dev import DevConfig

        app.config.from_object(DevConfig)
    else:
        from app.config.prod import ProdConfig

        app.config.from_object(ProdConfig)

    # Uncomment to enable logger
    # from app.utils.logger import setup_flask_logger
    # setup_flask_logger()

    # Initialize extensions
    from app.extensions import db, cors, matrixpi

    db.init_app(app)
    cors.init_app(app)
    matrixpi.init_app(app)

    db.create_all()

    from app.routes import api_bp, pages_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(pages_bp)

    # Inject translation helper and current language into every template
    from app.i18n import get_translation, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE

    @app.context_processor
    def inject_i18n():
        lang = session.get('language', DEFAULT_LANGUAGE)

        def t(key, **kwargs):
            return get_translation(lang, key, **kwargs)

        return {'t': t, 'current_lang': lang}

    # Route to switch the UI language, stored in the session
    @app.route('/set-language/<lang>')
    def set_language(lang):
        if lang in SUPPORTED_LANGUAGES:
            session['language'] = lang
        return redirect(request.referrer or '/')

    return app
