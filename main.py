#!/usr/bin/env python
import os
import jinja2
import webapp2

from models import Message

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

class ShraniHandler(BaseHandler):
    def get(self):
        sporocila = Message.query().fetch()

        izpis = {"sporocila": sporocila}

        return self.render_template("shrani.html", izpis)

    def post(self):
        ime = self.request.get("ime")
        priimek = self.request.get("priimek")
        email = self.request.get("email")
        sporocilo = self.request.get("sporocilo")

        if "<script>" in sporocilo:
            return self.write("Nice try!")

        # shrani sporocilo v bazo.
        spr = Message(ime=ime, priimek=priimek, email=email, sporocilo=sporocilo)
        spr.put()

        return self.redirect_to("shrani-stran")

class GuestBookHandler(BaseHandler):
    def get(self):
        return self.render_template("guest.html")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/save', ShraniHandler, name="shrani-stran"),
    webapp2.Route('/guestbook', GuestBookHandler),
], debug=True)
