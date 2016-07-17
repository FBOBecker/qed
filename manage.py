from argparse import ArgumentParser


def test(_):
    print("testing... ok")


def check(_):
    from flake8.main import main
    from sys import argv

    argv.clear()
    argv.extend(("flake8", "qed", "--max-line-length=100"))

    try:
        main()
    except SystemExit:
        pass
    else:
        print("No errors found.")


def flask(args):
    from qed import create_app
    from qed.config import Debug

    app = create_app(Debug)

    try:
        args.flask_handle(args, app)
    except AttributeError:
        flask_parser.print_help()


def run(args, app):
    app.run(host=args.interface, port=args.port, debug=args.debug)


def shell(_, app):
    from IPython import embed
    from qed.models import Category, Character, ForumUser, Post, Thread, User  # noqa
    from qed.enums import Spec  # noqa
    from pony.orm import db_session, commit, rollback

    with app.app_context():
        with db_session:
            embed()


def db(args):
    from qed.models import db
    from qed.config import Debug

    from pony.orm import db_session

    from db import drop, fill

    engine, path = Debug.DB_ARGS
    db.bind(engine, "qed/" + path, create_db=True)
    db.generate_mapping(create_tables=True)

    if args.operation == "fill":
        with db_session:
            fill()
    elif args.operation == "drop":
        drop()


parser = ArgumentParser()
sub_parsers = parser.add_subparsers()

test_parser = sub_parsers.add_parser("test")
test_parser.set_defaults(handle=test)


check_parser = sub_parsers.add_parser("check")
check_parser.set_defaults(handle=check)


flask_parser = sub_parsers.add_parser("flask")
flask_parser.set_defaults(handle=flask)

sub_flask = flask_parser.add_subparsers()

run_parser = sub_flask.add_parser("run")
run_parser.set_defaults(flask_handle=run)

run_parser.add_argument("--interface", "-i", type=str, default="127.0.0.1")
run_parser.add_argument("--port", "-p", type=int, default=80)
run_parser.add_argument("--no-debug", "-n", action="store_false", dest="debug")

shell_parser = sub_flask.add_parser("shell")
shell_parser.set_defaults(flask_handle=shell)

db_parser = sub_parsers.add_parser("db")
db_parser.set_defaults(handle=db)
db_parser.add_argument("operation", choices=["fill", "drop"])


if __name__ == '__main__':
    arguments = parser.parse_args()
    try:
        arguments.handle(arguments)
    except AttributeError as e:
        if "handle" in str(e):
            parser.print_help()
        else:
            raise
