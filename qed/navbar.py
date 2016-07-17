from dominate.tags import a, button, div, form, input_, li, nav, span, ul

from flask import url_for

from flask_login import current_user

from flask_nav.elements import Navbar as Navbar_, NavigationItem, View
from flask_nav.renderers import Renderer

from flask_wtf.csrf import generate_csrf


class Input(NavigationItem):
    def __init__(self, name, type_="text"):
        self.name = name
        self.type = type_


class NavForm(NavigationItem):
    def __init__(self, title, action, alert, *items):
        self.title = title
        self.action = action
        self.alert = alert
        self.items = items


class Navbar(Navbar_):
    def __init__(self, title, *items, forms=()):
        super().__init__(title, *items)
        self.forms = forms


NAVBAR_BTN = {
    "type": "button",
    "cls": "navbar-toggle collapsed",
    "data-toggle": "collapse",
    "data-target": "#navbar-collapse",
    "aria-expanded": "false"
}


class BootstrapRenderer(Renderer):
    @classmethod
    def visit(cls, node):
        if isinstance(node, type):
            mro = node.mro()
        else:
            mro = type(node).mro()
        for sub in mro:
            meth = getattr(cls, 'visit_' + sub.__name__.lower(), None)
            if meth is None:
                continue
            return meth(node)

        raise NotImplementedError('No visitation method visit_{}'.format(node.__class__.__name__))

    @classmethod
    def visit_navbar(cls, node):
        parent = nav(cls="navbar navbar-default")
        with parent:
            container = div(cls="container-fluid")
        with container:
            header = div(cls="navbar-header")
        with header:
            with button(**NAVBAR_BTN):
                span("Toggle navigation", cls="sr-only")
                span(cls="icon-bar")
                span(cls="icon-bar")
                span(cls="icon-bar")
            a(node.title, cls="navbar-brand", href=url_for("main.index"))

        with container:
            content = div(cls="collapse navbar-collapse", id="navbar-collapse")
        with content:
            list_ = ul(cls="nav navbar-nav")
        with list_:
            for item in node.items:
                cls.visit(item)
        with content:
            for item in node.forms:
                cls.visit(item)

        return parent

    @classmethod
    def visit_view(cls, node):
        if node.active:
            list_item = li(cls="active")
        else:
            list_item = li()
        with list_item:
            a(node.text, href=url_for(node.endpoint))
        return list_item

    @classmethod
    def visit_navform(cls, node):
        f = form(cls="navbar-form navbar-right", action=url_for(node.action), method="POST")
        with f:
            input_(type="hidden", name="csrf_token", value=generate_csrf(None, None))
            with div(cls="form-group"):
                for item in node.items:
                    cls.visit(item)
            button(node.title, cls="btn btn-" + node.alert, type="submit")
        return f

    @classmethod
    def visit_input(cls, node):
        i = input_(type=node.type, cls="form-control", name=node.name)
        return i


def nav_not_logged_in():
    return Navbar(
        "q.e.d.",
        View("Home", "main.index"),
        forms=[
            NavForm("Login", "user.login", "primary",
                    Input("nick_name"),
                    Input("password", "password"))
        ]
    )


def nav_not_active():
    return Navbar(
        "q.e.d.",
        View("Home", "main.index"),
        forms=[
            NavForm("Logout", "user.logout", "danger")
        ]
    )


def nav_user():
    return Navbar(
        "q.e.d.",
        View("Home", "main.index"),
        View("Forum", "forum.index"),
        View("Profile", "profile.index"),
        forms=[
            NavForm("Logout", "user.logout", "danger")
        ]
    )


def nav_admin():
    return Navbar(
        "q.e.d.",
        View("Home", "main.index"),
        View("Forum", "forum.index"),
        View("Profile", "profile.index"),
        forms=[
            NavForm("Logout", "user.logout", "danger")
        ]
    )


def nav_builder():
    if current_user.is_anonymous:
        return nav_not_logged_in()
    if not current_user.is_active:
        return nav_not_active()
    if current_user.is_admin:
        return nav_admin()
    return nav_user()
