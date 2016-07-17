

def create_app(config):
    from flask import Flask

    from flask_login import LoginManager

    from flask_nav import Nav, register_renderer

    from markdown import markdown

    from pony.orm import db_session

    from .csrf import csrf
    from .models import db, Post, User, Character
    from .view import api_view, main_view, forum_view, user_view, profile_view
    from .navbar import nav_builder, BootstrapRenderer
    from .filters import parents

    app = Flask("qed")
    app.config.from_object(config)
    try:
        with open(".secret_key") as fin:
            app.secret_key = fin.read()
    except FileNotFoundError:
        with open(".secret_key", "w") as fout:
            app.secret_key = input("NO SECRET KEY FOUND, ENTER IT HERE: ")
            fout.write(app.secret_key)

    manager = LoginManager(app)
    nav = Nav(app)

    csrf.init_app(app)

    register_renderer(app, "bootstrap", BootstrapRenderer)

    nav.register_element("top", nav_builder)

    @manager.user_loader
    @db_session
    def user_loader(user_id):
        return User[int(user_id)]

    app.register_blueprint(main_view)
    app.register_blueprint(forum_view, url_prefix="/forum/")
    app.register_blueprint(user_view, url_prefix="/user/")
    app.register_blueprint(api_view, url_prefix="/api/")
    app.register_blueprint(profile_view, url_prefix="/profile/")

    db.bind(*config.DB_ARGS, create_db=True)
    db.generate_mapping(create_tables=True)

    app.jinja_env.filters["parents"] = parents
    app.jinja_env.filters["markdown"] = markdown
    app.jinja_env.globals["Post"] = Post
    app.jinja_env.globals["Character"] = Character

    return app
