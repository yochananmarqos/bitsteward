#!/usr/bin/python


from gi.repository import Gtk, Adw, GLib
import gi
import subprocess
import json
import os
import requests
import time

from widgets.vault_types.secure_note import SecureNote
from widgets.vault_types.login import Login
from widgets.vault_types.credit_card import CreditCard
from widgets.vault_types.id import Id


from dotenv import load_dotenv

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
load_dotenv()


class AppWindow(Adw.ApplicationWindow):

    nombre = 0
    pages = []
    totp_code = ""
    bw_server_pid = ""

    hostname = "localhost"
    port = "8055"


    def __init__(self, app):

        super(AppWindow, self).__init__(application=app)

        self.connect("destroy", self.on_destroy)

        self.jsonOutput = self.load_json_data()

        self.init_ui()

    def init_ui(self):
        self.set_title('Bitsteward')
        self.set_default_size(800, 550)  # default app size
        self.set_size_request(300, 200)  # minimum app size
        # add devel stripes to the headerbar
        self.get_style_context().add_class('devel')

        # Main window
        window = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Headerbar
        self.header_bar = Gtk.HeaderBar()
        window.append(self.header_bar)

        # Leaflet
        self.leaflet_main = Adw.Leaflet(
            halign=Gtk.Align.FILL,
            valign=Gtk.Align.FILL
        )
        self.leaflet_main.set_can_unfold(True)
        self.leaflet_main.set_can_navigate_back(True)
        window.append(self.leaflet_main)  # add the content to the main window

        ### SideBar ###
        # Stack
        stack_sidebar = Gtk.Stack()
        stack_sidebar.set_hexpand(True)
        stack_sidebar.set_vexpand(True)

        # Sidebar
        self.sidebar = Gtk.StackSidebar()
        self.sidebar.set_stack(stack_sidebar)
        self.sidebar.set_vexpand(True)
        self.sidebar.set_size_request(200, 0)

        self.leaflet_main.append(self.sidebar)
        self.leaflet_main.append(stack_sidebar)

        # add elements to the stack
        for page in self.jsonOutput:

            # type 1 = login
            # type 2 = standalone secure note
            # type 3 = credit card
            # type 4 = ID
            scrollView = Gtk.ScrolledWindow()
            scrollView.set_policy(
                Gtk.PolicyType.NEVER,
                Gtk.PolicyType.AUTOMATIC
            )
            scrollView.set_kinetic_scrolling(True)

            # clamp
            adwbin = Adw.Bin()
            self.box_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.clamp = Adw.Clamp()
            self.box_content.append(self.clamp)

            scrollView.set_child(self.box_content)

            adwbin.set_child(scrollView)

            if (page["type"] == 1):
                content = Login.init_ui(self, page)

            if (page["type"] == 2):
                content = SecureNote.init_ui(self, page)

            if (page["type"] == 3):
                content = CreditCard.init_ui(self, page)

            if (page["type"] == 4):
                content = Id.init_ui(self, page)

            self.clamp.set_child(content)

            # Sidebar items/names
            name = page["id"]
            title = page["name"]

            if (len(title) > 30):
                title = title[0:27] + "..."

            stack_sidebar.add_titled(adwbin, name, title)


        stack_sidebar.connect("notify::visible-child", self.on_stack_switch)

        # display the content
        self.set_content(window)



        # load the JSON data from the BW Server
    def load_json_data(self):
        bw_location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.bw_server_pid = subprocess.Popen([bw_location + "/bw", "serve", "--port", self.port, "--session", os.getenv("BW_SESSION")])
        

        while True:
            try:
                response = requests.get(f"http://{self.hostname}:{self.port}/status")

                if response.status_code == 200:

                    requests.post(f"http://{self.hostname}:{self.port}/sync")
                    cmdOutput = requests.get(f"http://{self.hostname}:{self.port}/list/object/items")

                    jsonOutput = json.loads(cmdOutput.content)
                    return jsonOutput["data"]["data"]
            except:
                time.sleep(0.1)



    def on_destroy(self, widget, data=None):
        self.bw_server_pid.terminate



    # button to go back in folded view
    def on_back_btn_clicked(self, param):
        self.header_bar.remove(self.back_button)
        self.leaflet_main.set_visible_child(self.sidebar)



    # handle the clicks to vault items
    def on_stack_switch(self, stack, param_spec):
        self.leaflet_main.set_visible_child(stack)

        if (self.leaflet_main.get_folded() == True):
            self.back_button = Gtk.Button(label="Back")
            self.header_bar.pack_start(self.back_button)
            self.back_button.connect("clicked", self.on_back_btn_clicked)



def on_activate(app):
    win = AppWindow(app)
    win.present()


app = Adw.Application(application_id='net.adaoh.Bitsteward')
app.connect('activate', on_activate)
app.run(None)
