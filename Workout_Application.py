import numpy as np
import pandas
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
import requests
from datetime import datetime
import joblib
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from kivymd.uix.scrollview import MDScrollView
from matplotlib.figure import Figure
from kivy.clock import Clock
import time

Window.size = (320, 650)

kv = """
ScreenManager:
    LoginScreen:
    SignUpScreen1:   
    SignUpScreen2: 
    Home:
    Workouts:
    Progress:
    Profile:
    MaleWorkouts:
    FemaleWorkouts:
    MaleAbsWorkouts:
    MaleLegWorkouts:
    MaleChestWorkouts:
    MaleShoulderWorkouts:
    MaleBackWorkouts:
    MaleThighWorkouts:
    MaleArmsWorkouts:
    MaleBicepsWorkouts:
    MaleNeckWorkouts:
    FemaleAbsWorkouts:
    FemaleLegWorkouts:
    FemaleChestWorkouts:
    FemaleShoulderWorkouts:
    FemaleBackWorkouts:
    FemaleThighWorkouts:
    FemaleArmsWorkouts:
    FemaleGlutesWorkouts:
    FemaleNeckWorkouts:
    UpdateHeightAndWeight:
    PasswordChange:


<LoginScreen>
    name:'login'
    MDCard:
        style: 'elevated'
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        md_bg_color: '#000000'
        radius: [0, 0, 0, 0]
        MDLabel:
            text: 'Welcome to your fitness journey'
            halign: 'center'
            color: 'white'
            pos_hint: {'center_x':0.5, 'center_y':0.85}
            font_size: '25dp'
            size_hint: 0.5, 0.5
            padding: '10dp'
    MDCard:
        style: 'outlined'
        pos_hint: {'center_x':0.5, 'center_y':0.25}
        md_bg_color: '#ffffff'
        size_hint: 1, 1
        radius: [100, 0, 0, 0]
        MDRelativeLayout:
            MDLabel:
                text: 'Login'
                color: '#000000'
                halign:'center'
                font_size: '25dp'
                pos_hint: {'center_x':0.5, 'center_y':0.9}
                size_hint_x:None
            MDTextField:
                mode: 'fill'
                pos_hint: {'center_x':0.5, 'center_y':0.75}
                size_hint_x:0.82
                id: username_input
                hint_text:'username'
                helper_text:'eg: ashvindhakal'
                icon_left: 'account-circle'
                icon_left_color: app.theme_cls.primary_palette
            MDTextField:
                mode: 'fill'
                pos_hint: {'center_x':0.5, 'center_y':0.62}
                size_hint_x:0.82
                id: password_input 
                hint_text:'password'
                password: True
                icon_left: 'lock-outline'    
            MDRaisedButton:
                text:'Login'
                color: 'white'
                font_size: '17dp'
                pos_hint: {'center_x':0.5, 'center_y':0.5}
                size_hint_x: None
                md_bg_color:'#000000'
                on_release: root.send_login_data()
            MDTextButton:
                text: "Don't have an account? Sign Up"
                pos_hint: {'center_x':0.5, 'center_y':0.3}
                color: '#000000'
                font_size: '14dp'
                on_press: root.manager.current = 'signup1'


<SignUpScreen1>
    name:'signup1'
    MDCard:
        style: 'elevated'
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        md_bg_color: '#000000'
        radius: [0, 0, 0, 0]
        MDLabel:
            text: 'Welcome to your fitness journey'
            halign: 'center'
            color: 'white'
            pos_hint: {'center_x':0.5, 'center_y':0.92}
            font_size: '25dp'
            size_hint: 0.5, 0.5
            padding: '10dp'
    MDCard:
        style: 'outlined'
        pos_hint: {'center_x':0.5, 'center_y':0.35}
        md_bg_color: '#ffffff'
        size_hint:1,1
        radius: [100,0,0,0]
        MDRelativeLayout:
            MDLabel:
                text: 'Sign Up'
                color: '#000000'
                halign:'center'
                font_size: '25dp'
                pos_hint: {'center_x':0.5, 'center_y':0.95}
            MDTextField:
                mode: 'fill'
                pos_hint: {'center_x':0.5, 'center_y':0.86}
                size_hint_x:0.82
                id: name
                hint_text:'Enter your Name'
                helper_text:'eg: Ashvin Dhakal'
                icon_left: 'account-circle'
                icon_left_color: app.theme_cls.primary_palette
            MDTextField:
                mode: 'fill'
                pos_hint: {'center_x':0.5, 'center_y':0.74}
                size_hint_x:0.82
                id: user_name1
                hint_text:'Make a username'
                helper_text:'eg: @ashvin567'
                icon_left: 'account-circle'
                icon_left_color: app.theme_cls.primary_palette
            MDTextField:
                mode: 'fill'
                pos_hint: {'center_x':0.5, 'center_y':0.62}
                size_hint_x:0.82
                id: email
                hint_text:'Enter Your Email'
                helper_text:'eg: xyz@gmail.com'
                icon_left: 'email-box'
                icon_left_color: app.theme_cls.primary_palette
            MDTextField:
                mode: 'fill'
                pos_hint: {'center_x':0.5, 'center_y':0.5}
                size_hint_x:0.82
                id: mobile_number
                hint_text:'Mobile Number'
                icon_left: 'cellphone-basic'
            MDTextField:
                mode: 'fill'
                pos_hint: {'center_x':0.5, 'center_y':0.39}
                size_hint_x:0.82 
                id: date_of_birth
                hint_text:'Enter your birth date'
                helper_text: 'YYYY-MM-DD'
                icon_left: 'calendar-month'
            MDRaisedButton:
                text:'Next'
                color: 'white'
                font_size: '17dp'
                pos_hint: {'center_x':0.5, 'center_y':0.28}
                size_hint_x: None
                md_bg_color:'#000000'
                on_release: root.save_signup_data()
            MDTextButton:
                text: 'Already have an account? Login'
                pos_hint: {'center_x':0.5, 'center_y':0.2}
                color: '#000000'
                font_size: '14dp'
                on_press: root.manager.current = 'signup2'


<SignUpScreen2>
    name:'signup2'
    MDCard:
        style: 'elevated'
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        md_bg_color: '#000000'
        radius: [0, 0, 0, 0]
        MDLabel:
            text: 'Welcome to your fitness journey'
            halign: 'center'
            color: 'white'
            pos_hint: {'center_x':0.5, 'center_y':0.92}
            font_size: '25dp'
            size_hint: 0.5, 0.5
            padding: '10dp'
    MDCard:
        style: 'outlined'
        pos_hint: {'center_x':0.5, 'center_y':0.35}
        md_bg_color: '#ffffff'
        size_hint:1,1
        radius: [100,0,0,0]
        MDRelativeLayout:
            MDLabel:
                text: 'Sign Up'
                color: '#000000'
                halign:'center'
                font_size: '25dp'
                pos_hint: {'center_x':0.5, 'center_y':0.95}
            MDTextField:
                mode: 'fill'
                pos_hint: {'center_x':0.5, 'center_y':0.86}
                size_hint_x:0.82
                id: gender
                hint_text:'Select Gender'
                icon_left: 'account-circle'
                icon_left_color: app.theme_cls.primary_palette
                on_focus: if self.focus: root.open_menu()
            MDTextField:
                mode: 'fill'
                pos_hint: {'center_x':0.5, 'center_y':0.74}
                size_hint_x:0.82
                id: height
                hint_text:'Height in ft'
                helper_text:'eg: 5.10'
                icon_left: 'human-male-height-variant'
                icon_left_color: app.theme_cls.primary_palette
            MDTextField:
                mode: 'fill'
                pos_hint: {'center_x':0.5, 'center_y':0.62}
                size_hint_x:0.82
                id: weight
                hint_text:'Weight in KG'
                helper_text:'eg: 69'
                icon_left: 'weight-kilogram'
                icon_left_color: app.theme_cls.primary_palette
            MDTextField:
                mode: 'fill'
                pos_hint: {'center_x':0.5, 'center_y':0.5}
                size_hint_x:0.82 
                id: new_password
                hint_text:'New Password'
                password: True
                icon_left: 'lock-outline' 
                on_text: root.check_passwords(self)
            MDTextField:
                mode: 'fill'
                pos_hint: {'center_x':0.5, 'center_y':0.39}
                size_hint_x:0.82
                id: confirm_password
                hint_text:'Confirm Password'
                password: True
                icon_left: 'lock-outline'
                helper_text: "password must be same as above"
                on_text: root.check_passwords(self) 
            MDRaisedButton:
                text:'Sign Up'
                color: 'white'
                font_size: '17dp'
                pos_hint: {'center_x':0.5, 'center_y':0.28}
                size_hint_x: None
                md_bg_color:'#000000'
                on_release: root.send_signup_data()
            MDTextButton:
                text: 'Already have an account? Login'
                pos_hint: {'center_x':0.5, 'center_y':0.2}
                color: '#000000'
                font_size: '14dp'
                on_press: root.manager.current = 'login'


<Home>
    name: 'home'
    MDScrollView:
        MDBoxLayout:
            orientation: 'vertical'
            spacing: '25dp'
            padding: '20dp'
            size_hint_y: None               # Necessary for scrolling
            height: self.minimum_height     # Adjust to content height
            MDCard: 
                style: 'outlined'
                pos_hint: {'center_x':0.5,'center_y':0.85}
                size_hint_x: 1
                size_hint_y: None
                height: '140dp'
                theme_bg_color: 'Custom'
                md_bg_color: "#ffffff"
            MDCard: 
                style: 'elevated'
                pos_hint: {'center_x':0.5,'center_y':0.85}
                size_hint_x: 1
                size_hint_y: None
                height: '60dp'
                theme_bg_color: 'Custom'
                md_bg_color: "#ffffff"
                MDRelativeLayout:
                    MDLabel:
                        text: "Today's Calories Burn :  " + root.caloriesBurn+ " cal"
                        pos_hint: {'center_y':0.5}
                        font_size: '18dp'
                        size_hint_y: None
                        padding: '10dp'
            MDCard: 
                style: 'elevated'
                pos_hint: {'center_x':0.5,'center_y':0.85}
                size_hint_x: 1
                size_hint_y: None
                height: '300dp'
                theme_bg_color: 'Custom'
                md_bg_color: "#ffffff"
                MDRelativeLayout:
                    MDBoxLayout:
                        id: calories_graph
                        size_hint_y: None
                        size_hint_x: None
                        width: "260dp"
                        height: "260dp"
                        pos_hint: {'center_x':0.5,'center_y':0.5}
            MDCard: 
                style: 'elevated'
                pos_hint: {'center_x':0.5,'center_y':0.85}
                size_hint_x: 1
                size_hint_y: None
                height: '300dp'
                theme_bg_color: 'Custom'
                md_bg_color: "#ffffff"
                MDRelativeLayout:
                    MDBoxLayout:
                        id: progress_graph
                        pos_hint: {'center_x':0.5,'center_y':0.5}
                        size_hint_y: None
                        size_hint_x: None
                        width: "260dp"
                        height: "260dp"
            MDCard: 
                style: 'outlined'
                pos_hint: {'center_x':0.5,'center_y':0.85}
                size_hint_x: 1
                size_hint_y: None
                height: '70dp'
                theme_bg_color: 'Custom'
                md_bg_color: "#ffffff"
    MDCard: 
        size_hint_x: 1
        size_hint_y: 0.11
        theme_bg_color: 'Custom'
        md_bg_color: '#aaabaa'
        radius: [20, 20, 0,0]
        MDRelativeLayout:
            MDIconButton:
                icon: 'home-account'
                pos_hint: {'center_x':0.14,'center_y':0.65} 
            MDIconButton:
                icon: 'dumbbell'
                pos_hint: {'center_x':0.35,'center_y':0.65}
                on_release: root.on_icon_release('workouts')
            MDIconButton:
                icon: 'chart-bar'
                pos_hint: {'center_x':0.6,'center_y':0.65}
                on_release: root.on_icon_release('progress')
            MDIconButton:
                icon: 'account-circle-outline'
                pos_hint: {'center_x':0.84,'center_y':0.65}
                on_release: root.on_icon_release('profile')
    MDCard:
        style: "elevated"
        pos_hint: {"center_x":.5, "center_y":0.9}
        theme_shadow_color: "Custom"
        size_hint_x: 1                              # Fit the width of the screen
        size_hint_y: 0.3
        # height: "200dp"
        # orientation: "vertical"
        shadow_color: '#9850a1'
        theme_bg_color: 'Custom'
        md_bg_color: "#000000"
        padding: '20dp','39dp','0dp','0dp'
        BoxLayout:
            orientation: 'vertical'
            spacing: '0dp'  # Ensures no space between labels
            padding: '10dp'
            spacing: '20dp'
            MDLabel:
                text: "Hello " +root.Name+ "!"
                halign: "justify"
                color: "white"
                font_size: '25dp'
                bold: True
            MDLabel:
                text: "Welcome to your fitness journey"
                halign: "left"
                color: "white"
                font_size: '22dp'
                bold: True
            MDLabel:
                text: "Be healthy and get desired shape for your body."
                halign: "justify"
                color: "white"
                font_size: '15dp'
                bold: True
    


<Workouts>
    name: 'workouts'
    MDCard: 
        size_hint_x: 1
        size_hint_y: 0.11
        theme_bg_color: 'Custom'
        md_bg_color: '#aaabaa'
        radius: [20, 20, 0,0]
        MDRelativeLayout:
            MDIconButton:
                icon: 'home-account'
                pos_hint: {'center_x':0.14,'center_y':0.65}
                on_release: root.on_icon_release('home')
            MDIconButton:
                icon: 'dumbbell'
                pos_hint: {'center_x':0.35,'center_y':0.65}
            MDIconButton:
                icon: 'chart-bar'
                pos_hint: {'center_x':0.6,'center_y':0.65}
                on_release: root.on_icon_release('progress')
            MDIconButton:
                icon: 'account-circle-outline'
                pos_hint: {'center_x':0.84,'center_y':0.65}
                on_release: root.on_icon_release('profile')

    MDCard:
        style: 'elevated'
        pos_hint: {'center_x':0.5, 'center_y':0.9}
        theme_bg_color: 'Custom'
        md_bg_color: '#ffffff'
        size_hint_x: 1
        size_hint_y: 0.3
        background: "Images/Leg.jpg"
        padding: '20dp'
        MDLabel:
            text:'Select Your Exercise Here'
            color:'#ffffff'
            bold: True
            pos_hint: {'center_y':0.1}
            font_size: '23dp'

    MDCard:
        style: 'filled'
        pos_hint: {'center_x':0.5, 'center_y':0.58}
        theme_bg_color: 'Custom'
        md_bg_color: '#131313'
        size_hint_x: 1
        size_hint_y: 0.3
        radius: [50,0,50,0]
        padding: '20dp'
        BoxLayout:
            orientation: 'vertical'
            MDLabel:
                text: 'Essentials to Know Before You Exercise'
                bold: True
                color: '#ffffff'
                pos_hint: {'center_x':0.5, 'center_y':0.8}
            MDLabel:
                text: '1) Make Sure Your are hydrated.'
                color: '#ffffff'
                pos_hint: {'center_x':0.5, 'center_y':0.7}
            MDLabel:
                text: '2) Spend at least 5–10 minutes warming up'
                color: '#ffffff'
                pos_hint: {'center_x':0.5, 'center_y':0.5}
            MDLabel:
                text: '3) Make Mind Strong and get started..'
                color: '#ffffff'
                pos_hint: {'center_x':0.5, 'center_y':0.3}

    MDCard:
        style: 'filled'
        pos_hint: {'center_x':0.25, 'center_y':0.27}
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        size_hint_x: 0.35
        size_hint_y: 0.28
        radius: [10,10,10,10]
        ripple_behavior: True  # Enables ripple effect to act like a button
        on_release: root.on_male_card_press("male_workouts")  # Call function when the card is pressed
        BoxLayout:
            orientation: 'vertical'
            padding: '10dp'
            FitImage:
                source: "Images/male_workout.jpg"
                radius: [10,10,10,10]
                size_hint_y: 0.6             # Adjust height proportionally to card
                pos_hint: {'center_x':0.5, 'center_y':0.65}
            MDBoxLayout:
                orientation: 'vertical'
                padding: [10, 10]
                size_hint_y: 0.3
                MDLabel: 
                    text: 'Male'
                    bold: True
                    color: '#ffffff'
                    font_style: 'H6'
                    pos_hint: {'center_x':0.5, 'center_y':0.2}

    MDCard:
        style: 'filled'
        pos_hint: {'center_x':0.75, 'center_y':0.27}
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        size_hint_x: 0.35
        size_hint_y: 0.28
        radius: [10,10,10,10]
        ripple_behavior: True  # Enables ripple effect to act like a button
        on_release: root.on_female_card_press("female_workouts")  # Call function when the card is pressed
        BoxLayout:
            orientation: 'vertical'
            padding: '10dp'
            FitImage: 
                source: "Images/female_workout.jpg"
                pos_hint: {'center_x':0.5, 'center_y': 0.65}
                size_hint_y: 0.6
                radius: [10,10,10,10]
            MDBoxLayout:
                orientation: 'vertical'
                padding: [10, 10]
                size_hint_y: 0.3
                MDLabel:
                    text: "Female"
                    font_style: 'H6'
                    bold: True
                    color: '#ffffff'
                    pos_hint: {'center_x': 0.5, 'center_y': 0.2}


<Progress>
    name: 'progress'
    MDScrollView:
        MDBoxLayout:
            orientation: 'vertical'
            spacing: '20dp'
            padding: '20dp'
            size_hint_y: None               # Necessary for scrolling
            height: self.minimum_height     # Adjust to content height
            MDCard: 
                style: 'elevated'
                pos_hint: {'center_x':0.5,'center_y':0.85}
                size_hint_x: 1
                size_hint_y: None
                height: '100dp'
                theme_bg_color: 'Custom'
                md_bg_color: "#000000"
                MDRelativeLayout:
                    MDLabel:
                        text: 'Bmi: '+root.bmi_string
                        bold: True
                        halign: 'center'        # Horizontal alignment within the layout
                        valign: 'center'        # Vertical alignment within the layout
                        pos_hint: {'center_x': 0.3, 'center_y': 0.8} 
                        color: '#ffffff'
                        font_size: '25dp'
                    MDLabel:
                        text: root.bmi_gyan
                        bold: True
                        halign: 'center'        # Horizontal alignment within the layout
                        valign: 'center'        # Vertical alignment within the layout
                        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
                        color: '#ffffff'
                        font_size: '19dp'
            MDCard: 
                style: 'elevated'
                pos_hint: {'center_x':0.5,'center_y':0.85}
                size_hint_x: 1
                size_hint_y: None
                height: '150dp'
                theme_bg_color: 'Custom'
                md_bg_color: "#000000" 
                MDRelativeLayout:
                    MDLabel:
                        text: 'Exercise Recommendation'
                        bold: True
                        halign: 'center'        # Horizontal alignment within the layout
                        valign: 'center'        # Vertical alignment within the layout
                        pos_hint: {'center_x': 0.49, 'center_y': 0.86} 
                        color: '#ffffff'
                        font_size: '20dp'
                    MDTextField:
                        hint_text: "Exercising Duration (in mins)"
                        mode: "round"
                        id: desired_exercise_duration
                        helper_text: "Massage"
                        size_hint_x: 0.8
                        pos_hint: {'center_x': 0.45, 'center_y': 0.58}
                    MDFillRoundFlatButton
                        text: "Show Exercise"
                        text_color: "#000000"
                        pos_hint: {'center_x': 0.3, 'center_y': 0.2}
                        size_hint_x: 0.2
                        md_bg_color:'#d2d2d6'
                        on_release: root.show_exercise()
            MDCard: 
                style: 'elevated'
                pos_hint: {'center_x':0.5,'center_y':0.85}
                size_hint_x: 1
                size_hint_y: None
                height: '150dp'
                theme_bg_color: 'Custom'
                md_bg_color: "#000000"
                MDRelativeLayout:
                    MDLabel:
                        text: 'Diet Recommendation'
                        bold: True
                        halign: 'center'        # Horizontal alignment within the layout
                        valign: 'center'        # Vertical alignment within the layout
                        pos_hint: {'center_x': 0.45, 'center_y': 0.86} 
                        color: '#ffffff'
                        font_size: '20dp'
                    MDTextField:
                        hint_text: "Choose Exercise"
                        mode: "round"
                        id: desired_exercise
                        helper_text: "Massage"
                        size_hint_x: 0.8
                        pos_hint: {'center_x': 0.45, 'center_y': 0.58} 
                        background_color: app.theme_cls.bg_normal
                        on_focus: if self.focus: root.open_menu()
                    MDFillRoundFlatButton
                        text: "Show Diet"
                        text_color: "#000000"
                        pos_hint: {'center_x': 0.3, 'center_y': 0.2}
                        size_hint_x: 0.2
                        md_bg_color:'#d2d2d6'
                        on_release: root.show_diet()
            MDCard: 
                style: 'elevated'
                pos_hint: {'center_x':0.5,'center_y':0.85}
                size_hint_x: 1
                size_hint_y: None
                height: '150dp'
                theme_bg_color: 'Custom'
                md_bg_color: "#000000"
            MDCard: 
                style: 'filled'
                pos_hint: {'center_x':0.5,'center_y':0.85}
                size_hint_x: 1
                size_hint_y: None
                height: '50dp'
                theme_bg_color: 'Custom'
                md_bg_color: "#ffffff"
    MDCard: 
        size_hint_x: 1
        size_hint_y: 0.11
        theme_bg_color: 'Custom'
        md_bg_color: '#aaabaa'
        radius: [20, 20, 0,0]
        MDRelativeLayout:
            MDIconButton:
                icon: 'home-account'
                pos_hint: {'center_x':0.14,'center_y':0.65}
                on_release: root.on_icon_release('home')
            MDIconButton:
                icon: 'dumbbell'
                pos_hint: {'center_x':0.35,'center_y':0.65}
                on_release:root.on_icon_release('workouts')
            MDIconButton:
                icon: 'chart-bar'
                pos_hint: {'center_x':0.6,'center_y':0.65}
            MDIconButton:
                icon: 'account-circle-outline'
                pos_hint: {'center_x':0.84,'center_y':0.65}
                on_release: root.on_icon_release('profile')
                

<Profile>
    name: 'profile'
    MDCard:
        style: 'elevated'
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        md_bg_color: '#000000'
        radius: [0, 0, 0, 0]
        MDLabel:
            text: 'Profile Overview'
            halign: 'center'
            color: 'white'
            pos_hint: {'center_x':0.5, 'center_y':0.92}
            font_size: '25dp'
            size_hint: 0.5, 0.5
            padding: '10dp'
    MDCard:
        style: 'elevated'
        pos_hint: {'center_x':0.5, 'center_y':0.3}
        md_bg_color: '#ffffff'
        size_hint:1,1
        radius: [0,100,0,0]
        MDRelativeLayout:
            MDLabel:
                id: name_label
                text: 'Name:  '+root.Name
                halign: 'left'
                bold: True
                pos_hint: {'center_x':0.6, 'center_y':0.93}
                size_hint_x:None
                width:'400'
                color: '#000000'
                font_size: '18dp'
            MDLabel:
                id: username_label
                text: 'Username:  '+root.username
                halign: 'left'
                bold: True
                pos_hint: {'center_x':0.6, 'center_y':0.88}
                size_hint_x:None
                width:'400'
                color: '#000000'
                font_size: '18dp'
            MDLabel:
                id: email_label
                text: 'Email:  '+root.email
                halign: 'left'
                bold: True
                pos_hint: {'center_x':0.6, 'center_y':0.83}
                size_hint_x:None
                width:'400'
                color: '#000000'
                font_size: '18dp'
            MDLabel:
                id: mobile_label
                text: 'Mobile No:  '+root.mobile
                halign: 'left'
                bold: True
                pos_hint: {'center_x':0.6, 'center_y':0.78}
                size_hint_x:None
                width:'400'
                color: '#000000'
                font_size: '18dp'
            MDLabel:
                id: mobile_label
                text: "Date Of Birth: "+root.date_of_birth
                halign: 'left'
                bold: True
                pos_hint: {'center_x':0.6, 'center_y':0.73}
                size_hint_x:None
                width:'400'
                color: '#000000'
                font_size: '18dp'
            MDLabel:
                id: gender_label
                text: 'Gender:  '+root.gender
                halign: 'left'
                bold: True
                pos_hint: {'center_x':0.6, 'center_y':0.68}
                size_hint_x:None
                width:'400'
                color: '#000000'
                font_size: '18dp'
            ScrollView:
                pos_hint: {'center_x':0.5, 'center_y':0.14}
                MDList:
                    OneLineIconListItem:
                        text: 'Change Password'
                        on_press: root.manager.current = 'passwordChange'
                        IconLeftWidget:
                            icon: 'lock-reset'
                    OneLineIconListItem:
                        text: 'Update Height/Weight'
                        on_press: root.manager.current = 'updateHeightAndWeight'
                        IconLeftWidget:
                            icon: 'file-upload'
                    OneLineIconListItem:
                        text: 'Favourites'
                        IconLeftWidget:
                            icon: 'star'
                    OneLineIconListItem:
                        text: 'Logout'
                        on_release: root.manager.current = 'login'
                        IconLeftWidget:
                            icon: 'logout'
    MDCard: 
        size_hint_x: 1
        size_hint_y: 0.11
        theme_bg_color: 'Custom'
        md_bg_color: '#aaabaa'
        radius: [20, 20, 0,0]
        MDRelativeLayout:
            MDIconButton:
                icon: 'home-account'
                pos_hint: {'center_x':0.14,'center_y':0.65}
                on_release: root.on_icon_release('home')
            MDIconButton:
                icon: 'dumbbell'
                pos_hint: {'center_x':0.35,'center_y':0.65}
                on_release: root.on_icon_release('workouts')
            MDIconButton:
                icon: 'chart-bar'
                pos_hint: {'center_x':0.6,'center_y':0.65}
                on_release: root.on_icon_release('progress')
            MDIconButton:
                icon: 'account-circle-outline'
                pos_hint: {'center_x':0.84,'center_y':0.65}


<MaleWorkouts>
    name: 'male_workouts'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        theme_bg_color: 'Custom'
        md_bg_color: '#ffffff'
        size_hint_x: 1
        size_hint_y: 1
        radius: [0,0,0,0]
        MDCard:
            style: 'filled'
            pos_hint: {'center_x':0.5, 'center_y':0.45}
            size_hint_x: 1
            size_hint_y: 0.9
            theme_bg_color: 'Custom'
            md_bg_color: '#ffffff'
            radius: [0,0,0,0]
            GridLayout: 
                cols: 3
                padding: '10dp'
                spacing: '10dp'
                adaptive_height : True
                MDCard:
                    style: 'elevated'
                    theme_bg_color: 'Custom'
                    md_bg_color: '#000000'
                    size_hint_y: 0.1
                    radius: [10,10,10,10]
                    ripple_behavior: True  # Enables ripple effect to act like a button
                    on_release: root.on_male_abs_card_press("male_abs_workouts")
                    BoxLayout:
                        orientation: 'vertical'
                        padding: '10dp'
                        FitImage: 
                            source: "Images/abs_male.jpg"
                            pos_hint: {'center_x':0.5, 'center_y': 0.65}
                            size_hint_y: 0.6
                            radius: [10,10,10,10]
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: [10, 10]
                            size_hint_y: 0.3
                            MDLabel:
                                text: "Abs"
                                font_size: '15dp'
                                bold: True
                                color: '#ffffff'
                                pos_hint: {'center_x': 0.5, 'center_y': 0.2}                               
                MDCard:
                    style: 'elevated'
                    theme_bg_color: 'Custom'
                    md_bg_color: '#000000'
                    size_hint_x: 0.9
                    size_hint_y: 0.1
                    radius: [10,10,10,10]
                    ripple_behavior: True  # Enables ripple effect to act like a button
                    on_release: root.on_male_leg_card_press("male_leg_workouts")
                    BoxLayout: 
                        orientation: 'vertical'
                        padding: '10dp'                       
                        FitImage: 
                            source: "Images/leg_male.jpg"
                            size_hint_y: 0.6
                            pos_hint: {'center_x':0.5,'center_y':0.65}
                            radius: [10,10,10,10]
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: [10, 10]
                            size_hint_y: 0.3
                            MDLabel:
                                text:'Leg'
                                color:'#ffffff'
                                bold: True
                                font_size: '15dp'
                                pos_hint: {'center_y':0.2}
                MDCard:
                    style: 'elevated'
                    theme_bg_color: 'Custom'
                    md_bg_color: '#000000'
                    size_hint_x: 0.9
                    size_hint_y: 0.1
                    radius: [10,10,10,10]
                    ripple_behavior: True  # Enables ripple effect to act like a button
                    on_release: root.on_male_chest_card_press("male_chest_workouts")
                    BoxLayout:
                        orientation: 'vertical'
                        padding: '10dp'
                        FitImage: 
                            source: "Images/chest_male.jpg"
                            pos_hint: {'center_x':0.5, 'center_y': 0.65}
                            size_hint_y: 0.6
                            radius: [10,10,10,10]
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: [10, 10]
                            size_hint_y: 0.3
                            MDLabel:
                                text: "Chest"
                                font_size: '15dp'
                                bold: True
                                color: '#ffffff'
                                pos_hint: {'center_x': 0.5, 'center_y': 0.2}
                MDCard:
                    style: 'elevated'
                    theme_bg_color: 'Custom'
                    md_bg_color: '#000000'
                    size_hint_x: 0.9
                    size_hint_y: 0.1
                    radius: [10,10,10,10]
                    ripple_behavior: True  # Enables ripple effect to act like a button
                    on_release: root.on_male_shoulder_card_press("male_shoulder_workouts")
                    BoxLayout:
                        orientation: 'vertical'
                        padding: '10dp'
                        FitImage: 
                            source: "Images/shoulder_male.jpg"
                            pos_hint: {'center_x':0.5, 'center_y': 0.65}
                            size_hint_y: 0.6
                            radius: [10,10,10,10]
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: [7,7]
                            size_hint_y: 0.3
                            MDLabel:
                                text: "Shoulder"
                                font_size: '15dp'
                                bold: True
                                color: '#ffffff'
                                pos_hint: {'center_x': 0.5, 'center_y': 0.2}                        
                MDCard:
                    style: 'elevated'
                    theme_bg_color: 'Custom'
                    md_bg_color: '#000000'
                    size_hint_x: 0.9
                    size_hint_y: 0.1
                    radius: [10,10,10,10]
                    ripple_behavior: True  # Enables ripple effect to act like a button
                    on_release: root.on_male_back_card_press("male_back_workouts")
                    BoxLayout:
                        orientation: 'vertical'
                        padding: '10dp'
                        FitImage: 
                            source: "Images/back_male.jpg"
                            pos_hint: {'center_x':0.5, 'center_y': 0.65}
                            size_hint_y: 0.6
                            radius: [10,10,10,10]
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: [10, 10]
                            size_hint_y: 0.3
                            MDLabel:
                                text: "Back"
                                font_size: '15dp'
                                bold: True
                                color: '#ffffff'
                                pos_hint: {'center_x': 0.5, 'center_y': 0.2}                        
                MDCard:
                    style: 'elevated'
                    theme_bg_color: 'Custom'
                    md_bg_color: '#000000'
                    size_hint_x: 0.9
                    size_hint_y: 0.1
                    radius: [10,10,10,10]
                    ripple_behavior: True  # Enables ripple effect to act like a button
                    on_release: root.on_male_thigh_card_press("male_thigh_workouts")
                    BoxLayout:
                        orientation: 'vertical'
                        padding: '10dp'
                        FitImage: 
                            source: "Images/thigh_male.jpg"
                            pos_hint: {'center_x':0.5, 'center_y': 0.65}
                            size_hint_y: 0.6
                            radius: [10,10,10,10]
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: [10, 10]
                            size_hint_y: 0.3
                            MDLabel:
                                text: "Thigh"
                                font_size: '15dp'
                                bold: True
                                color: '#ffffff'
                                pos_hint: {'center_x': 0.5, 'center_y': 0.2}                       
                MDCard:
                    style: 'elevated'
                    theme_bg_color: 'Custom'
                    md_bg_color: '#000000'
                    size_hint_x: 0.9
                    size_hint_y: 0.1
                    radius: [10,10,10,10]
                    ripple_behavior: True  # Enables ripple effect to act like a button
                    on_release: root.on_male_arms_card_press("male_arms_workouts")
                    BoxLayout:
                        orientation: 'vertical'
                        padding: '10dp'
                        FitImage: 
                            source: "Images/arms_male.jpg"
                            pos_hint: {'center_x':0.5, 'center_y': 0.65}
                            size_hint_y: 0.6
                            radius: [10,10,10,10]
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: [10, 10]
                            size_hint_y: 0.3
                            MDLabel:
                                text: "Arms"
                                font_size: '15dp'
                                bold: True
                                color: '#ffffff'
                                pos_hint: {'center_x': 0.5, 'center_y': 0.2}                       
                MDCard:
                    style: 'elevated'
                    theme_bg_color: 'Custom'
                    md_bg_color: '#000000'
                    size_hint_x: 0.9
                    size_hint_y: 0.1
                    radius: [10,10,10,10]
                    ripple_behavior: True  # Enables ripple effect to act like a button
                    on_release: root.on_male_biceps_card_press("male_biceps_workouts")
                    BoxLayout:
                        orientation: 'vertical'
                        padding: '10dp'
                        FitImage: 
                            source: "Images/biceps_male.jpg"
                            pos_hint: {'center_x':0.5, 'center_y': 0.65}
                            size_hint_y: 0.6
                            radius: [10,10,10,10]
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: [10, 10]
                            size_hint_y: 0.3
                            MDLabel:
                                text: "Biceps"
                                font_size: '15dp'
                                bold: True
                                color: '#ffffff'
                                pos_hint: {'center_x': 0.5, 'center_y': 0.2}                        
                MDCard:
                    style: 'elevated'
                    theme_bg_color: 'Custom'
                    md_bg_color: '#000000'
                    size_hint_x: 0.9
                    size_hint_y: 0.1
                    radius: [10,10,10,10]
                    ripple_behavior: True  # Enables ripple effect to act like a button
                    on_release: root.on_male_neck_card_press("male_neck_workouts")
                    BoxLayout:
                        orientation: 'vertical'
                        padding: '10dp'
                        FitImage: 
                            source: "Images/neck_male.jpg"
                            pos_hint: {'center_x':0.5, 'center_y': 0.65}
                            size_hint_y: 0.6
                            radius: [10,10,10,10]
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: [10, 10]
                            size_hint_y: 0.3
                            MDLabel:
                                text: "Neck"
                                font_size: '15dp'
                                bold: True
                                color: '#ffffff'
                                pos_hint: {'center_x': 0.5, 'center_y': 0.2}
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'workouts'
            MDLabel:
                text: 'Male Workouts'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp'

<FemaleWorkouts>
    name: 'female_workouts'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        theme_bg_color: 'Custom'
        md_bg_color: '#ffffff'
        size_hint_x: 1
        size_hint_y: 1
        radius: [0,0,0,0]
        MDCard:
            style: 'filled'
            pos_hint: {'center_x':0.5, 'center_y':0.45}
            size_hint_x: 1
            size_hint_y: 0.9
            theme_bg_color: 'Custom'
            md_bg_color: '#ffffff'
            radius: [0,0,0,0]
            GridLayout: 
                cols: 3
                padding: '10dp'
                spacing: '10dp'
                adaptive_height : True
                MDCard:
                    style: 'elevated'
                    theme_bg_color: 'Custom'
                    md_bg_color: '#000000'
                    size_hint_y: 0.1
                    radius: [10,10,10,10]
                    ripple_behavior: True  # Enables ripple effect to act like a button
                    on_release: root.on_female_abs_card_press("female_abs_workouts")
                    BoxLayout:
                        orientation: 'vertical'
                        padding: '10dp'
                        FitImage: 
                            source: "Images/abs_female.jpg"
                            pos_hint: {'center_x':0.5, 'center_y': 0.65}
                            size_hint_y: 0.6
                            radius: [10,10,10,10]
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: [10, 10]
                            size_hint_y: 0.3
                            MDLabel:
                                text: "Abs"
                                font_size: '15dp'
                                bold: True
                                color: '#ffffff'
                                pos_hint: {'center_x': 0.5, 'center_y': 0.2}                               
                MDCard:
                    style: 'elevated'
                    theme_bg_color: 'Custom'
                    md_bg_color: '#000000'
                    size_hint_x: 0.9
                    size_hint_y: 0.1
                    radius: [10,10,10,10]
                    ripple_behavior: True  # Enables ripple effect to act like a button
                    on_release: root.on_female_leg_card_press("female_leg_workouts")
                    BoxLayout: 
                        orientation: 'vertical'
                        padding: '10dp'
                        FitImage: 
                            source: "Images/leg_female.jpg"
                            size_hint_y: 0.6
                            pos_hint: {'center_x':0.5,'center_y':0.65}
                            radius: [10,10,10,10]
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: [10, 10]
                            size_hint_y: 0.3
                            MDLabel:
                                text:'Leg'
                                color:'#ffffff'
                                bold: True
                                font_size: '15dp'
                                pos_hint: {'center_y':0.2}
                MDCard:
                    style: 'elevated'
                    theme_bg_color: 'Custom'
                    md_bg_color: '#000000'
                    size_hint_x: 0.9
                    size_hint_y: 0.1
                    radius: [10,10,10,10]
                    ripple_behavior: True  # Enables ripple effect to act like a button
                    on_release: root.on_female_chest_card_press("female_chest_workouts")
                    BoxLayout:
                        orientation: 'vertical'
                        padding: '10dp'
                        FitImage: 
                            source: "Images/chest_female.jpg"
                            pos_hint: {'center_x':0.5, 'center_y': 0.65}
                            size_hint_y: 0.6
                            radius: [10,10,10,10]
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: [10, 10]
                            size_hint_y: 0.3
                            MDLabel:
                                text: "Chest"
                                font_size: '15dp'
                                bold: True
                                color: '#ffffff'
                                pos_hint: {'center_x': 0.5, 'center_y': 0.2}
                MDCard:
                    style: 'elevated'
                    theme_bg_color: 'Custom'
                    md_bg_color: '#000000'
                    size_hint_x: 0.9
                    size_hint_y: 0.1
                    radius: [10,10,10,10]
                    ripple_behavior: True  # Enables ripple effect to act like a button
                    on_release: root.on_female_shoulder_card_press("female_shoulder_workouts")
                    BoxLayout:
                        orientation: 'vertical'
                        padding: '10dp'
                        FitImage: 
                            source: "Images/shoulder_female.jpg"
                            pos_hint: {'center_x':0.5, 'center_y': 0.65}
                            size_hint_y: 0.6
                            radius: [10,10,10,10]
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: [7,7]
                            size_hint_y: 0.3
                            MDLabel:
                                text: "Shoulder"
                                font_size: '15dp'
                                bold: True
                                color: '#ffffff'
                                pos_hint: {'center_x': 0.5, 'center_y': 0.2}                        
                MDCard:
                    style: 'elevated'
                    theme_bg_color: 'Custom'
                    md_bg_color: '#000000'
                    size_hint_x: 0.9
                    size_hint_y: 0.1
                    radius: [10,10,10,10]
                    ripple_behavior: True  # Enables ripple effect to act like a button
                    on_release: root.on_female_back_card_press("female_back_workouts")
                    BoxLayout:
                        orientation: 'vertical'
                        padding: '10dp'
                        FitImage: 
                            source: "Images/back_female.jpg"
                            pos_hint: {'center_x':0.5, 'center_y': 0.65}
                            size_hint_y: 0.6
                            radius: [10,10,10,10]
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: [10, 10]
                            size_hint_y: 0.3
                            MDLabel:
                                text: "Back"
                                font_size: '15dp'
                                bold: True
                                color: '#ffffff'
                                pos_hint: {'center_x': 0.5, 'center_y': 0.2}                        
                MDCard:
                    style: 'elevated'
                    theme_bg_color: 'Custom'
                    md_bg_color: '#000000'
                    size_hint_x: 0.9
                    size_hint_y: 0.1
                    radius: [10,10,10,10]
                    ripple_behavior: True  # Enables ripple effect to act like a button
                    on_release: root.on_female_thigh_card_press("female_thigh_workouts")
                    BoxLayout:
                        orientation: 'vertical'
                        padding: '10dp'
                        FitImage: 
                            source: "Images/thigh_female.jpg"
                            pos_hint: {'center_x':0.5, 'center_y': 0.65}
                            size_hint_y: 0.6
                            radius: [10,10,10,10]
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: [10, 10]
                            size_hint_y: 0.3
                            MDLabel:
                                text: "Thigh"
                                font_size: '15dp'
                                bold: True
                                color: '#ffffff'
                                pos_hint: {'center_x': 0.5, 'center_y': 0.2}                       
                MDCard:
                    style: 'elevated'
                    theme_bg_color: 'Custom'
                    md_bg_color: '#000000'
                    size_hint_x: 0.9
                    size_hint_y: 0.1
                    radius: [10,10,10,10]
                    ripple_behavior: True  # Enables ripple effect to act like a button
                    on_release: root.on_female_arms_card_press("female_arms_workouts")
                    BoxLayout:
                        orientation: 'vertical'
                        padding: '10dp'
                        FitImage: 
                            source: "Images/arms_female.jpg"
                            pos_hint: {'center_x':0.5, 'center_y': 0.65}
                            size_hint_y: 0.6
                            radius: [10,10,10,10]
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: [10, 10]
                            size_hint_y: 0.3
                            MDLabel:
                                text: "Arms"
                                font_size: '15dp'
                                bold: True
                                color: '#ffffff'
                                pos_hint: {'center_x': 0.5, 'center_y': 0.2}                       
                MDCard:
                    style: 'elevated'
                    theme_bg_color: 'Custom'
                    md_bg_color: '#000000'
                    size_hint_x: 0.9
                    size_hint_y: 0.1
                    radius: [10,10,10,10]
                    ripple_behavior: True  # Enables ripple effect to act like a button
                    on_release: root.on_female_glutes_card_press("female_glutes_workouts")
                    BoxLayout:
                        orientation: 'vertical'
                        padding: '10dp'
                        FitImage: 
                            source: "Images/glutes_female.jpg"
                            pos_hint: {'center_x':0.5, 'center_y': 0.65}
                            size_hint_y: 0.6
                            radius: [10,10,10,10]
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: [10, 10]
                            size_hint_y: 0.3
                            MDLabel:
                                text: "Glutes"
                                font_size: '15dp'
                                bold: True
                                color: '#ffffff'
                                pos_hint: {'center_x': 0.5, 'center_y': 0.2}                        
                MDCard:
                    style: 'elevated'
                    theme_bg_color: 'Custom'
                    md_bg_color: '#000000'
                    size_hint_x: 0.9
                    size_hint_y: 0.1
                    radius: [10,10,10,10]
                    ripple_behavior: True  # Enables ripple effect to act like a button
                    on_release: root.on_female_neck_card_press("female_neck_workouts")
                    BoxLayout:
                        orientation: 'vertical'
                        padding: '10dp'
                        FitImage: 
                            source: "Images/neck_female.jpg"
                            pos_hint: {'center_x':0.5, 'center_y': 0.65}
                            size_hint_y: 0.6
                            radius: [10,10,10,10]
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: [10, 10]
                            size_hint_y: 0.3
                            MDLabel:
                                text: "Neck"
                                font_size: '15dp'
                                bold: True
                                color: '#ffffff'
                                pos_hint: {'center_x': 0.5, 'center_y': 0.2}
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'workouts'
            MDLabel:
                text: 'Female Workouts'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp'


<MaleAbsWorkouts>
    name: 'male_abs_workouts'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'male_workouts'
            MDLabel:
                text: 'Abs Workouts'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        size_hint_x: 1
        size_hint_y: 0.9
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#ffffff'
        spacing: '10dp'
        BoxLayout:
            orientation: 'vertical'
            VideoPlayer:
                id: male_abs_1
                source: "Videos/male_abs_1.avi"
                allow_stretch: True
                on_state: root.track_video_time(self, 'male_abs_1', self.state)
            VideoPlayer:
                id: male_abs_2
                source: "Videos/male_abs_2.avi"
                on_state: root.track_video_time(self, 'male_abs_2', self.state)
            VideoPlayer:
                id: male_abs_3
                source: "Videos/male_abs_3.avi"
                on_state: root.track_video_time(self, 'male_abs_3', self.state)


<MaleLegWorkouts>
    name: 'male_leg_workouts'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'male_workouts'
            MDLabel:
                text: 'Leg Workouts'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        size_hint_x: 1
        size_hint_y: 0.9
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#ffffff'
        spacing: '10dp'
        BoxLayout:
            orientation: 'vertical'
            VideoPlayer:
                id:male_leg_1
                source: "Videos/male_abs_1.avi"
                allow_stretch: True
                on_state: root.track_video_time(self, 'male_leg_1', self.state)
            VideoPlayer:
                id: male_leg_2
                source: "Videos/male_abs_2.avi"
                on_state: root.track_video_time(self, 'male_leg_2', self.state)
            VideoPlayer:
                id: male_leg_3
                source: "Videos/male_abs_3.avi"
                on_state: root.track_video_time(self, 'male_leg_3', self.state)


<MaleChestWorkouts>
    name: 'male_chest_workouts'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'male_workouts'
            MDLabel:
                text: 'Chest Workouts'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        size_hint_x: 1
        size_hint_y: 0.9
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#ffffff'
        spacing: '10dp'
        BoxLayout:
            orientation: 'vertical'
            VideoPlayer:
                id:male_chest_1
                source: "Videos/male_abs_1.avi"
                allow_stretch: True
                on_state: root.track_video_time(self, 'male_chest_1', self.state)
            VideoPlayer:
                id: male_chest_2
                source: "Videos/male_abs_2.avi"
                on_state: root.track_video_time(self, 'male_chest_2', self.state)
            VideoPlayer:
                id: male_chest_3
                source: "Videos/male_abs_3.avi"
                on_state: root.track_video_time(self, 'male_chest_3', self.state)


<MaleShoulderWorkouts>
    name: 'male_shoulder_workouts'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'male_workouts'
            MDLabel:
                text: 'Shoulder Workouts'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp' 
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        size_hint_x: 1
        size_hint_y: 0.9
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#ffffff'
        spacing: '10dp'
        BoxLayout:
            orientation: 'vertical'
            VideoPlayer:
                id:male_shoulder_1
                source: "Videos/male_abs_1.avi"
                allow_stretch: True
                on_state: root.track_video_time(self, 'male_shoulder_1', self.state)
            VideoPlayer:
                id: male_shoulder_2
                source: "Videos/male_abs_2.avi"
                on_state: root.track_video_time(self, 'male_shoulder_2', self.state)
            VideoPlayer:
                id: male_shoulder_3
                source: "Videos/male_abs_3.avi"
                on_state: root.track_video_time(self, 'male_shoulder_3', self.state)


<MaleBackWorkouts>
    name: 'male_back_workouts'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'male_workouts'
            MDLabel:
                text: 'Back Workouts'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        size_hint_x: 1
        size_hint_y: 0.9
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#ffffff'
        spacing: '10dp'
        BoxLayout:
            orientation: 'vertical'
            VideoPlayer:
                id:male_back_1
                source: "Videos/male_abs_1.avi"
                allow_stretch: True
                on_state: root.track_video_time(self, 'male_back_1', self.state)
            VideoPlayer:
                id: male_back_2
                source: "Videos/male_abs_2.avi"
                on_state: root.track_video_time(self, 'male_back_2', self.state)
            VideoPlayer:
                id: male_back_3
                source: "Videos/male_abs_3.avi"
                on_state: root.track_video_time(self, 'male_back_3', self.state)


<MaleThighWorkouts>
    name: 'male_thigh_workouts'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'male_workouts'
            MDLabel:
                text: 'Thigh Workouts'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        size_hint_x: 1
        size_hint_y: 0.9
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#ffffff'
        spacing: '10dp'
        BoxLayout:
            orientation: 'vertical'
            VideoPlayer:
                id:male_thigh_1
                source: "Videos/male_abs_1.avi"
                allow_stretch: True
                on_state: root.track_video_time(self, 'male_thigh_1', self.state)
            VideoPlayer:
                id: male_thigh_2
                source: "Videos/male_abs_2.avi"
                on_state: root.track_video_time(self, 'male_thigh_2', self.state)
            VideoPlayer:
                id: male_thigh_3
                source: "Videos/male_abs_3.avi"
                on_state: root.track_video_time(self, 'male_thigh_3', self.state)


<MaleArmsWorkouts>
    name: 'male_arms_workouts'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'male_workouts'
            MDLabel:
                text: 'Arms Workouts'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        size_hint_x: 1
        size_hint_y: 0.9
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#ffffff'
        spacing: '10dp'
        BoxLayout:
            orientation: 'vertical'
            VideoPlayer:
                id:male_arms_1
                source: "Videos/male_abs_1.avi"
                allow_stretch: True
                on_state: root.track_video_time(self, 'male_arms_1', self.state)
            VideoPlayer:
                id: male_arms_2
                source: "Videos/male_abs_2.avi"
                on_state: root.track_video_time(self, 'male_arms_2', self.state)
            VideoPlayer:
                id: male_arms_3
                source: "Videos/male_abs_3.avi"
                on_state: root.track_video_time(self, 'male_arms_3', self.state)


<MaleBicepsWorkouts>
    name: 'male_biceps_workouts'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'male_workouts'
            MDLabel:
                text: 'Biceps Workouts'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        size_hint_x: 1
        size_hint_y: 0.9
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#ffffff'
        spacing: '10dp'
        BoxLayout:
            orientation: 'vertical'
            VideoPlayer:
                id:male_biceps_1
                source: "Videos/male_abs_1.avi"
                allow_stretch: True
                on_state: root.track_video_time(self, 'male_biceps_1', self.state)
            VideoPlayer:
                id: male_biceps_2
                source: "Videos/male_abs_2.avi"
                on_state: root.track_video_time(self, 'male_biceps_2', self.state)
            VideoPlayer:
                id: male_biceps_3
                source: "Videos/male_abs_3.avi"
                on_state: root.track_video_time(self, 'male_biceps_3', self.state)


<MaleNeckWorkouts>
    name: 'male_neck_workouts'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'male_workouts'
            MDLabel:
                text: 'Neck Workouts'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        size_hint_x: 1
        size_hint_y: 0.9
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#ffffff'
        spacing: '10dp'
        BoxLayout:
            orientation: 'vertical'
            VideoPlayer:
                id:male_neck_1
                source: "Videos/male_abs_1.avi"
                allow_stretch: True
                on_state: root.track_video_time(self, 'male_neck_1', self.state)
            VideoPlayer:
                id: male_neck_2
                source: "Videos/male_abs_2.avi"
                on_state: root.track_video_time(self, 'male_neck_2', self.state)
            VideoPlayer:
                id: male_neck_3
                source: "Videos/male_abs_3.avi"
                on_state: root.track_video_time(self, 'male_neck_3', self.state)


<FemaleAbsWorkouts>
    name: 'female_abs_workouts'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'female_workouts'
            MDLabel:
                text: 'Abs Workouts'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        size_hint_x: 1
        size_hint_y: 0.9
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#ffffff'
        spacing: '10dp'
        BoxLayout:
            orientation: 'vertical'
            VideoPlayer:
                id: female_abs_1
                source: "Videos/female_abs_1.mp4"
                on_state: root.track_video_time(self, 'female_abs_1', self.state)
                allow_stretch: True
            VideoPlayer:
                id: female_abs_2
                on_state: root.track_video_time(self, 'female_abs_2', self.state)
                source: "Videos/female_abs_2.mp4"
            VideoPlayer:
                id: female_abs_3
                source: "Videos/female_abs_3.mp4"
                on_state: root.track_video_time(self, 'female_abs_3', self.state)


<FemaleLegWorkouts>
    name: 'female_leg_workouts'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'female_workouts'
            MDLabel:
                text: 'Leg Workouts'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        size_hint_x: 1
        size_hint_y: 0.9
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#ffffff'
        spacing: '10dp'
        BoxLayout:
            orientation: 'vertical'
            VideoPlayer:
                id: female_leg_1
                source: "Videos/female_abs_1.mp4"
                on_state: root.track_video_time(self, 'female_leg_1', self.state)
                allow_stretch: True
            VideoPlayer:
                id: female_leg_2
                on_state: root.track_video_time(self, 'female_leg_2', self.state)
                source: "Videos/female_abs_2.mp4"
            VideoPlayer:
                id: female_leg_3
                source: "Videos/female_abs_3.mp4"
                on_state: root.track_video_time(self, 'female_leg_3', self.state)


<FemaleChestWorkouts>
    name: 'female_chest_workouts'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'female_workouts'
            MDLabel:
                text: 'Chest Workouts'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        size_hint_x: 1
        size_hint_y: 0.9
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#ffffff'
        spacing: '10dp'
        BoxLayout:
            orientation: 'vertical'
            VideoPlayer:
                id: female_chest_1
                source: "Videos/female_abs_1.mp4"
                on_state: root.track_video_time(self, 'female_chest_1', self.state)
                allow_stretch: True
            VideoPlayer:
                id: female_chest_2
                on_state: root.track_video_time(self, 'female_chest_2', self.state)
                source: "Videos/female_abs_2.mp4"
            VideoPlayer:
                id: female_chest_3
                source: "Videos/female_abs_3.mp4"
                on_state: root.track_video_time(self, 'female_chest_3', self.state)


<FemaleShoulderWorkouts>
    name: 'female_shoulder_workouts'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'female_workouts'
            MDLabel:
                text: 'Shoulder Workouts'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        size_hint_x: 1
        size_hint_y: 0.9
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#ffffff'
        spacing: '10dp'
        BoxLayout:
            orientation: 'vertical'
            VideoPlayer:
                id: female_shoulder_1
                source: "Videos/female_abs_1.mp4"
                on_state: root.track_video_time(self, 'female_shoulder_1', self.state)
                allow_stretch: True
            VideoPlayer:
                id: female_shoulder_2
                on_state: root.track_video_time(self, 'female_shoulder_2', self.state)
                source: "Videos/female_abs_2.mp4"
            VideoPlayer:
                id: female_shoulder_3
                source: "Videos/female_abs_3.mp4"
                on_state: root.track_video_time(self, 'female_shoulder_3', self.state)


<FemaleBackWorkouts>
    name: 'female_back_workouts'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'female_workouts'
            MDLabel:
                text: 'Back Workouts'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        size_hint_x: 1
        size_hint_y: 0.9
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#ffffff'
        spacing: '10dp'
        BoxLayout:
            orientation: 'vertical'
            VideoPlayer:
                id: female_back_1
                source: "Videos/female_abs_1.mp4"
                on_state: root.track_video_time(self, 'female_back_1', self.state)
                allow_stretch: True
            VideoPlayer:
                id: female_back_2
                on_state: root.track_video_time(self, 'female_back_2', self.state)
                source: "Videos/female_abs_2.mp4"
            VideoPlayer:
                id: female_back_3
                source: "Videos/female_abs_3.mp4"
                on_state: root.track_video_time(self, 'female_back_3', self.state)


<FemaleThighWorkouts>
    name: 'female_thigh_workouts'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'female_workouts'
            MDLabel:
                text: 'Thigh Workouts'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        size_hint_x: 1
        size_hint_y: 0.9
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#ffffff'
        spacing: '10dp'
        BoxLayout:
            orientation: 'vertical'
            VideoPlayer:
                id: female_thigh_1
                source: "Videos/female_abs_1.mp4"
                on_state: root.track_video_time(self, 'female_thigh_1', self.state)
                allow_stretch: True
            VideoPlayer:
                id: female_thigh_2
                on_state: root.track_video_time(self, 'female_thigh_2', self.state)
                source: "Videos/female_abs_2.mp4"
            VideoPlayer:
                id: female_thigh_3
                source: "Videos/female_abs_3.mp4"
                on_state: root.track_video_time(self, 'female_thigh_3', self.state)

<FemaleArmsWorkouts>
    name: 'female_arms_workouts'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'female_workouts'
            MDLabel:
                text: 'Arms Workouts'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        size_hint_x: 1
        size_hint_y: 0.9
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#ffffff'
        spacing: '10dp'
        BoxLayout:
            orientation: 'vertical'
            VideoPlayer:
                id: female_arms_1
                source: "Videos/female_abs_1.mp4"
                on_state: root.track_video_time(self, 'female_arms_1', self.state)
                allow_stretch: True
            VideoPlayer:
                id: female_arms_2
                on_state: root.track_video_time(self, 'female_arms_2', self.state)
                source: "Videos/female_abs_2.mp4"
            VideoPlayer:
                id: female_arms_3
                source: "Videos/female_abs_3.mp4"
                on_state: root.track_video_time(self, 'female_arms_3', self.state)

<FemaleGlutesWorkouts>
    name: 'female_glutes_workouts'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'female_workouts'
            MDLabel:
                text: 'Glutes Workouts'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        size_hint_x: 1
        size_hint_y: 0.9
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#ffffff'
        spacing: '10dp'
        BoxLayout:
            orientation: 'vertical'
            VideoPlayer:
                id: female_glutes_1
                source: "Videos/female_abs_1.mp4"
                on_state: root.track_video_time(self, 'female_glutes_1', self.state)
                allow_stretch: True
            VideoPlayer:
                id: female_glutes_2
                on_state: root.track_video_time(self, 'female_glutes_2', self.state)
                source: "Videos/female_abs_2.mp4"
            VideoPlayer:
                id: female_glutes_3
                source: "Videos/female_abs_3.mp4"
                on_state: root.track_video_time(self, 'female_glutes_3', self.state)


<FemaleNeckWorkouts>
    name: 'female_neck_workouts'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'female_workouts'
            MDLabel:
                text: 'Neck Workouts'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        size_hint_x: 1
        size_hint_y: 0.9
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#ffffff'
        spacing: '10dp'
        BoxLayout:
            orientation: 'vertical'
            VideoPlayer:
                id: female_neck_1
                source: "Videos/female_abs_1.mp4"
                on_state: root.track_video_time(self, 'female_neck_1', self.state)
                allow_stretch: True
            VideoPlayer:
                id: female_neck_2
                on_state: root.track_video_time(self, 'female_neck_2', self.state)
                source: "Videos/female_abs_2.mp4"
            VideoPlayer:
                id: female_neck_3
                source: "Videos/female_abs_3.mp4"
                on_state: root.track_video_time(self, 'female_neck_3', self.state)
            

<UpdateHeightAndWeight>
    name: 'updateHeightAndWeight'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'profile'
            MDLabel:
                text: 'Update Height and Weight'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp'
    MDTextField:
        mode: 'fill'
        pos_hint: {'center_x':0.5, 'center_y':0.74}
        size_hint_x:0.82
        id: height
        hint_text:'Height in ft'
        helper_text:'eg: 5.10'
        icon_left: 'human-male-height-variant'
        icon_left_color: app.theme_cls.primary_palette
    MDTextField:
        mode: 'fill'
        pos_hint: {'center_x':0.5, 'center_y':0.62}
        size_hint_x:0.82
        id: weight
        hint_text:'Weight in KG'
        helper_text:'eg: 69'
        icon_left: 'weight-kilogram'
        icon_left_color: app.theme_cls.primary_palette
    MDRaisedButton:
        text:'Update'
        color: 'white'
        font_size: '17dp'
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        size_hint_x: None
        md_bg_color:'#000000'
        on_release: root.updateHeightAndWeight()


<PasswordChange>
    name: 'passwordChange'
    MDCard:
        style: 'filled'
        pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        size_hint_x: 1
        size_hint_y: 0.1
        radius: [0,0,0,0]
        theme_bg_color: 'Custom'
        md_bg_color: '#000000'
        padding: '10dp'
        MDRelativeLayout:
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {'center_y':0.5}
                theme_icon_color: "Custom"
                icon_color: "#ffffff"
                on_press: root.manager.current = 'profile'
            MDLabel:
                text: 'Change Password'
                halign: 'center'
                bold: True
                size_hint_x:1
                color: '#ffffff'
                font_size: '18dp'
    MDTextField:
        mode: 'fill'
        pos_hint: {'center_x':0.5, 'center_y':0.75}
        size_hint_x:0.82
        id: old_password
        hint_text:'Old Password'
        password: True
        icon_left: 'lock-outline' 
        on_text: root.check_passwords(self)
    MDTextField:
        mode: 'fill'
        pos_hint: {'center_x':0.5, 'center_y':0.63}
        size_hint_x:0.82
        id: new_password
        hint_text:'New Password'
        password: True
        icon_left: 'lock-outline' 
        on_text: root.check_passwords(self)
    MDTextField:
        mode: 'fill'
        pos_hint: {'center_x':0.5, 'center_y':0.51}
        size_hint_x:0.82
        id: confirm_password
        hint_text:'Confirm Password'
        password: True
        icon_left: 'lock-outline'
        helper_text: "password must be same as above"
        on_text: root.check_passwords(self) 
    MDRaisedButton:
        text:'Update'
        color: 'white'
        font_size: '17dp'
        pos_hint: {'center_x':0.5, 'center_y':0.38}
        size_hint_x: None
        md_bg_color:'#000000'
        on_release: root.updatePassword()
        
"""


# noinspection PyBroadException
class LoginScreen(Screen):
    def send_login_data(self):
        app = MDApp.get_running_app()
        app.user_name['user_name'] = self.ids.username_input.text  # stores username in app dictionary

        # Data to send
        login_data = {
            "user_name": self.ids.username_input.text,
            "password": self.ids.password_input.text
        }
        try:
            # Send POST request to Flask server
            response = requests.post("http://127.0.0.1:5000/api/login_data", json=login_data)
            # Display response
            print("Server Response:", response.json())

            if response.status_code == 200 and response.json().get("success"):
                self.manager.current = 'home'
                print("Login successful. Navigating to home screen...")
            elif response.status_code == 400 and response.json().get("error"):
                print("Login failed:", response.json().get("error"))
                close_button = MDFlatButton(text='Close', on_release=self.close_dialog)
                self.dialog = MDDialog(title='Login Check', text='Username and Password are required',
                                       buttons=[close_button])
                self.dialog.open()
            else:
                print("Login failed:", response.json().get("error"))
                close_button = MDFlatButton(text='Close', on_release=self.close_dialog)
                self.dialog = MDDialog(title='Login Check', text='Invalid username or password',
                                       buttons=[close_button])
                self.dialog.open()

        except requests.exceptions.RequestException as e:
            print("Error:", e)

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def on_pre_leave(self):
        try:
            current_user = self.ids.username_input.text
            try:
                response = requests.get(f'http://127.0.0.1:5000/user_info/{current_user}')
                if response.status_code == 200:
                    user_data = response.json()
                    self.Name = user_data['name']
                    self.username = user_data['username']
                    self.email = user_data['email']
                    self.mobile = user_data['mobile']
                    timestamp = user_data['dateofbirth']
                    self.date_of_birth = timestamp.split('00:')[0]  # Extract only the date part
                    self.gender = user_data['gender']
                    self.height = user_data['height']
                    self.weight = user_data['weight']
                    print("Welcome", current_user)
                    self.title_name = self.Name.split(' ')[0]
                else:
                    print("Error fetching data:", response.status_code)
                    print("Error", current_user)

            except Exception as e:
                print(f"Request failed: {e}")

            app = MDApp.get_running_app()
            app.user_info['name'] = self.Name
            app.user_info['user_name'] = self.username
            app.user_info['email'] = self.email
            app.user_info['mobile'] = self.mobile
            app.user_info['date_of_birth'] = self.date_of_birth
            app.user_info['gender'] = self.gender
            app.user_info['height'] = self.height
            app.user_info['weight'] = self.weight
            app.only_name['title_name'] = self.title_name

            # Fetch calories data
            try:
                response = requests.get(f'http://127.0.0.1:5000/fetchCaloriesData/{current_user}')
                if response.status_code == 200:
                    user_calories_burn = response.json()
                    self.date = user_calories_burn.get('date', [])
                    self.calories_burn = user_calories_burn.get('caloriesburn', [])
                    app.fetched_calories['Date'] = self.date
                    app.fetched_calories['caloriesBurn'] = self.calories_burn
                else:
                    print(f"Error fetching calories data. Status code: {response.status_code}")
            except Exception as e:
                print(f"Failed to fetch calories data: {e}")
        except:
            self.manager.current = 'signup1'


class SignUpScreen1(Screen):
    def save_signup_data(self):
        name = self.ids.name.text
        user_name = self.ids.user_name1.text
        email = self.ids.email.text
        mobile_number = self.ids.mobile_number.text
        date_of_birth = self.ids.date_of_birth.text

        # store data in app's dictionary
        app = MDApp.get_running_app()
        app.signup_data['name'] = name
        app.signup_data['user_name'] = user_name
        app.signup_data['email'] = email
        app.signup_data['mobile_number'] = mobile_number
        app.signup_data['date_of_birth'] = date_of_birth

        if not name or not user_name or not email or not mobile_number or not date_of_birth:
            close_button = MDFlatButton(text='Close', on_release=self.close_dialog)
            self.dialog = MDDialog(title='Sign Up Check', text='Please provide all information',
                                   buttons=[close_button])
            self.dialog.open()
        else:
            # navigate to next page
            self.manager.current = 'signup2'

    def close_dialog(self, obj):
        self.dialog.dismiss()


class SignUpScreen2(Screen):
    def on_enter(self):
        self.menu = None  # Prevent reinitialization
        # Prepare the dropdown menu items
        menu_items = [
            {"text": "Male", "on_release": lambda x="Male": self.set_gender(x)},
            {"text": "Female", "on_release": lambda x="Female": self.set_gender(x)},
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.gender,
            items=menu_items,
            width_mult=4
        )

    def open_menu(self):
        # Open the dropdown menu
        if self.menu:
            self.menu.open()

    def set_gender(self, gender):
        # Set the selected gender in the text field
        self.ids.gender.text = gender
        self.menu.dismiss()

    def send_signup_data(self):
        gender = self.ids.gender.text
        height = self.ids.height.text
        weight = self.ids.weight.text
        new_password = self.ids.new_password.text
        confirm_password = self.ids.confirm_password.text

        # store data in app's dictionary
        app = MDApp.get_running_app()
        app.signup_data['gender'] = gender
        app.signup_data['height'] = height
        app.signup_data['weight'] = weight
        app.signup_data['new_password'] = new_password
        app.signup_data['confirm_password'] = confirm_password

        try:
            response = requests.post("http://127.0.0.1:5000/api/signup_data", json=app.signup_data)
            print("Server Response:", response.json())
            close_button = MDFlatButton(text='Close', on_release=self.close_dialog)
            login_button = MDFlatButton(text='Login', on_release=self.login_btn)
            self.dialog = MDDialog(title='Sign Up Check', text='SignUp Successful, Go to Login Page',
                                   buttons=[close_button, login_button])
            self.dialog.open()

        except requests.exceptions.RequestException as e:
            close_button = MDFlatButton(text='Close', on_release=self.close_dialog)
            self.dialog = MDDialog(title='Sign Up Check', text='Please provide all information',
                                   buttons=[close_button])
            self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def login_btn(self, obj):
        self.manager.current = 'login'
        self.dialog.dismiss()

    def check_passwords(self, instance):
        new_password = self.ids.new_password.text
        confirm_password = self.ids.confirm_password
        if instance == confirm_password:
            if new_password != confirm_password.text:
                confirm_password.error = True
                confirm_password.helper_text = "password must be same as above"
            else:
                confirm_password.error = False
                confirm_password.helper_text = ""  # clear helper text


class Home(Screen):
    def on_icon_release(self, screen_name):
        # Set transition effect
        self.manager.transition = SlideTransition(duration=0.01)
        # Switch to the specified screen
        self.manager.current = screen_name

    Name = StringProperty("")
    caloriesBurn = StringProperty("")

    def on_enter(self):
        self.progress_graph()
        self.fetch_title_name()
        self.show_caloriesBurn()
        self.calories_graph()

    def progress_graph(self):
        # Create a graph
        x = [1, 2, 3, 4, 5]
        y = [2, 3, 5, 7, 11]
        fig_progress = Figure()
        ax_progress = fig_progress.add_subplot(111)
        ax_progress.plot(x, y, marker="o")
        ax_progress.set_title("Progress Graph")
        # ax_progress.set_xlabel("X-axis")
        # ax_progress.set_ylabel("Y-axis")

        # Remove the previous graph (if any)
        graph_box = self.ids.progress_graph
        for child in graph_box.children[:]:
            graph_box.remove_widget(child)

        # Embed graph into the app
        graph_widget = FigureCanvasKivyAgg(fig_progress)
        self.ids.progress_graph.add_widget(graph_widget)

    def calories_graph(self):
        # Dummy data for graph
        app = MDApp.get_running_app()
        calories_data = app.fetched_calories
        dataset = pandas.DataFrame(calories_data)
        print(dataset)
        duplicate_dropped_dataset = dataset.drop_duplicates(keep='first')
        summed_calories = duplicate_dropped_dataset.groupby('Date', as_index=False)['caloriesBurn'].sum()
        # Print the result
        print(summed_calories)

        # dates = ['01-11', '01-12', '01-13']
        # calories = [200, 250, 300]
        dates = summed_calories['Date']
        calories = summed_calories['caloriesBurn']

        figure_progress = Figure()
        calories_graph = figure_progress.add_subplot(111)
        calories_graph.plot(dates, calories, marker="o")
        calories_graph.set_title("Calories Burn Over Time")
        # calories_graph.set_xlabel("Dates")
        # calories_graph.set_ylabel("Calories Burned")

        # Remove any previous widgets in the `calories_graph` container
        calories_graph = self.ids.calories_graph
        for child in calories_graph.children[:]:
            calories_graph.remove_widget(child)

        # Embed the Matplotlib graph
        graph = FigureCanvasKivyAgg(figure_progress)
        self.ids.calories_graph.add_widget(graph)

    def fetch_title_name(self):
        app = MDApp.get_running_app()
        self.Name = app.only_name.get('title_name')

    def show_caloriesBurn(self):
        self.caloriesBurn = str(round(calories_burn, 2))


class Workouts(Screen):
    def on_icon_release(self, screen_name):
        # Set transition effect
        self.manager.transition = SlideTransition(duration=0.01)
        # Switch to the specified screen
        self.manager.current = screen_name

    def on_male_card_press(self, screen_name):
        # Set transition effect
        self.manager.transition = SlideTransition(duration=0.01)
        # Switch to the specified screen
        self.manager.current = screen_name
        print("Male card Pressed")

    def on_female_card_press(self, screen_name):
        # Set transition effect
        self.manager.transition = SlideTransition(duration=0.01)
        # Switch to the specified screen
        self.manager.current = screen_name

        print("Female card Pressed")

    def on_enter(self, *args):
        app = MDApp.get_running_app()
        print(f"After All Exercise, Your Workout Time is {total_exercise_time:.2f} seconds.")
        print(f"Calories Burn : {calories_burn}")

        username = app.user_name['user_name']
        date_time = str(datetime.now())
        # print(date_time)
        dt_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")
        date = str(dt_obj.date())
        month_day = dt_obj.strftime("%m-%d")
        # print(date)
        app.calories_data['username'] = username
        app.calories_data['total_exercise_time'] = total_exercise_time
        app.calories_data['calories_burn'] = calories_burn
        app.calories_data['date'] = date


class CustomDropdown(ModalView):
    def __init__(self, items, callback, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.auto_dismiss = True

        # Dynamically set width based on longest text
        longest_text = max(items, key=len)
        estimated_width = dp(len(longest_text) * 10)
        self.width = min(estimated_width, Window.width * 0.9)
        self.height = dp(300)  # Fixed height with scrolling

        layout = MDBoxLayout(orientation="vertical")
        scroll = MDScrollView()
        menu_list = MDList()

        for exercise in items:
            list_item = OneLineListItem(text=exercise)
            list_item.bind(on_release=self.create_callback(exercise, callback))
            menu_list.add_widget(list_item)

        scroll.add_widget(menu_list)
        layout.add_widget(scroll)
        self.add_widget(layout)

    @staticmethod
    def create_callback(exercise, callback):
        """Returns a lambda that correctly captures the exercise value."""
        return lambda instance: callback(exercise)


class Progress(Screen):
    def on_icon_release(self, screen_name):
        # Set transition effect
        self.manager.transition = SlideTransition(duration=0.01)
        # Switch to the specified screen
        self.manager.current = screen_name

    bmi_string = StringProperty("0.00")
    bmi_gyan = StringProperty("")

    def on_enter(self):
        self.bmi_calculation()

        self.menu = None  # Prevent reinitialization

    def open_menu(self):
        # Prepare the dropdown menu items
        menu_items = [
            "Body Weight",
            "BodyWeight with Endurance",
            "Cardio",
            "Cardio with Functional",
            "Endurance Training",
            "Endurance with Strength",
            "Heavy BodyWeight",
            "Heavy Cardio Training",
            "Heavy Endurance Training",
            "High Intensity Cardio",
            "Sports Specific Training",
            "Circuit Training",
            "High Intensity Cardio With Circuit"
        ]

        self.menu = CustomDropdown(items=menu_items, callback=self.set_exercise)
        self.menu.open()

    def set_exercise(self, exercise):
        # Set the selected gender in the text field
        self.ids.desired_exercise.text = exercise
        self.menu.dismiss()

    def bmi_calculation(self):
        app = MDApp.get_running_app()
        height = app.user_info.get('height')
        weight = app.user_info.get('weight')
        height_in_meters = height * 0.3048
        bmi = round(weight / (height_in_meters ** 2.0), 2)
        bmi_float = float(bmi)
        self.bmi_string = str(bmi_float)

        if bmi_float < 18.50:
            self.bmi_gyan = "Oops! Your Are Underweight"
        elif 18.5 <= bmi_float < 25:
            self.bmi_gyan = "Congrats! You have normal weight"
        elif 25 <= bmi_float < 30:
            self.bmi_gyan = "Oops! You are Overweight."
        elif bmi_float >= 30:
            self.bmi_gyan = "Oh my god! Obesity!!"
        else:
            self.bmi_gyan = "Keep your body healthy!"

    def show_diet(self):
        desired_exercise = self.ids.desired_exercise.text

        close_button = MDFlatButton(text="Close", on_release=self.close_dialog)
        if not desired_exercise:
            self.dialog = MDDialog(title="Recommend Diet", text="Please Select a Exercise",
                                   buttons=[close_button])
            self.dialog.open()
            return

        print(desired_exercise)

        if desired_exercise == "Body Weight":
            diet = (
                "For Body Weight Workout, You need more Calories. Diet are Nuts, Dried fruits,  High-Fat dairy, Healthy Oats, "
                "Lean Meats, Whole-grain bread, Eggs")
        elif desired_exercise == "BodyWeight with Endurance":
            diet = ("For BodyWeight and Endurance, You should take Carbohydrates: Whole grains, bananas, "
                    "Proteins: Egg, Meat, Beans ")
        elif desired_exercise == "Cardio":
            diet = ("For Cardio, You should take Carbohydrates: Whole grains, bananas, "
                    "Proteins: Lean Meat, Beans, Yogurt ")
        elif desired_exercise == "Cardio with Functional":
            diet = ("For Cardio with Functional, You should take Carbohydrates: Brown Rice, Sweet Potatoes, "
                    "Protein: Chicken, Tofu, Fiber: Vegetables, Legumes")
        elif desired_exercise == "Endurance Training":
            diet = (
                "For Endurance Training, You should take, Carbohydrates: Whole Grains, Bananas, Protein: Cottage, Cheese, Eggs,"
                "Electrolytes: Sodium, Potassium, Coconut water, Sports drinks")
        elif desired_exercise == "Endurance with Strength":
            diet = (
                "For Endurance with Strength Training: Carbohydrates:  Oats, Quinoa, Sweet Potatoes, Whole Grains, Bananas"
                " Protein: Cottage Cheese, Eggs, Fish, Tofu, Fats: Nuts, Seeds, Avocado")
        elif desired_exercise == "Heavy BodyWeight":
            diet = ("For Heavy Body Weight, You should take heavy Calories, Carbohydrates: Whole grains, Sweet Potatoes"
                    "Protein: Chickens, Eggs, Beans, Dairy Product, Fats: Avocado, Nuts, Seeds")
        elif desired_exercise == "Heavy Cardio Training":
            diet = ("For Heavy Cardio Training, You should take heavy Calories, Carbohydrates: Whole grains, bananas, "
                    "Proteins: Lean Meat, Beans, Yogurt ")
        elif desired_exercise == "Heavy Endurance Training":
            diet = (
                "For Heavy Endurance Training, You should take more Calories or Energy, Carbohydrates: for glycogen store, "
                "Whole Grains, Bananas, Proteins: For recovery, Cottage Cheese, Eggs")
        elif desired_exercise == "High Intensity Cardio":
            diet = (
                "For High Intensity Cardio, You should take AntiOxidants: Berries, Spinach, Protein: Eggs, Whey Protein Shake,"
                "Carbohydrates: Fruits, Energy Bars")
        elif desired_exercise == "Sports Specific Training":
            diet = "For Sport Specific Training, You should take Micronutrients: For energy, magnesium, iron, nuts, Protein: Protein Shakes"
        elif desired_exercise == "Circuit Training":
            diet = (
                "For Circuit Training, You should take Fats: Avocado, nuts, Protein: For muscle repair, Whey protein, turkey,"
                "Carbohydrates: Oats, Fruits for quick and sustained Energy")
        elif desired_exercise == "High Intensity Cardio with Circuit":
            diet = (
                "For High Intensity Cardio with Circuit Training, You should take heavy diet, AntiOxidants: Berries, Spinach,"
                "Fats: Avocado, Nuts, Electrolytes: Coconut water, Bananas, Carbohydrates: Fruits, Energy Bars, Oats,"
                "Protein: Whey protein, turkey, Greek Yogurt")
        else:
            diet = "You can take a healthy diet, Such as: Almonds, Vegetables like: Spanish, Carrot, Fruits: Bananas, Apple"

        self.dialog = MDDialog(title="Recommend Diet", text=f"{diet}",
                               buttons=[close_button])
        self.dialog.open()

    def show_exercise(self):
        self.model = joblib.load("new_exercise_recommendation_model.pkl")

        app = MDApp.get_running_app()
        gender = app.user_info.get('gender')
        date_of_birth_str = app.user_info.get('date_of_birth').strip()
        bmi = float(self.bmi_string)

        if gender == "Male":
            encoded_gender = 1.0
        else:
            encoded_gender = 0.0

        date_of_birth = datetime.strptime(date_of_birth_str, "%a, %d %b %Y")
        current_date = datetime.now()
        age = current_date.year - date_of_birth.year
        if (current_date.month, current_date.day) < (date_of_birth.month, date_of_birth.day):
            age -= 1

        desired_exercise_duration = self.ids.desired_exercise_duration.text

        close_button = MDFlatButton(text="Close", on_release=self.close_dialog)
        if not desired_exercise_duration:
            self.dialog = MDDialog(title="Recommend Exercise", text="Please Provide All Information",
                                   buttons=[close_button])
            self.dialog.open()
            return

        input_text = f"{bmi}, {desired_exercise_duration}"
        input_array = np.array([float(x) for x in input_text.split(',')]).reshape(1, -1)
        prediction = self.model.predict(input_array)
        predicted_value = prediction[0] if hasattr(prediction, "__getitem__") else prediction
        print(predicted_value)

        if predicted_value == 0:
            exercise_type = "You may do a Body Weight Exercise, Examples: Push-ups, planks, burpees, mountain climbers."
        elif predicted_value == 1:
            exercise_type = "You may do a Body Weight with Endurance Training, Examples: Push-ups, planks, Long-distance running, cycling."
        elif predicted_value == 2:
            exercise_type = "You may do a Cardio, Examples: Running, cycling, swimming, brisk walking, jumping rope, rowing. "
        elif predicted_value == 3:
            exercise_type = "You may do a Cardio with Functional Training, Examples: Planks, DeadLifts, Running, Cycling ."
        elif predicted_value == 4:
            exercise_type = "You may do a Endurance Training, Examples: Long-distance running, swimming, cycling."
        elif predicted_value == 5:
            exercise_type = "You may do a Endurance with Strength Training, Examples: Long-distance running, cycling, push-ups, squats, pull-ups"
        elif predicted_value == 6:
            exercise_type = "You may do a Heavy Body Weight, Examples: Push-ups, planks, squats and focus on diet also"
        elif predicted_value == 7:
            exercise_type = "You may do a Heavy Cardio Workouts, Examples: Long Running, Long Cycling, Squats, Jumping Rope"
        elif predicted_value == 8:
            exercise_type = "You may do a Heavy Endurance Training, Examples: Long Distance Running, Push-ups"
        elif predicted_value == 9:
            exercise_type = "You may do a High Intensity Cardio, Examples: Sprint intervals, burpees, KettleBell swings, Running"
        elif predicted_value == 10:
            exercise_type = "You may do a Sports Training, Examples: Agility drills for soccer, plyometric jumps for basketball."
        elif predicted_value == 11:
            exercise_type = "You may do a Circuit Training, Examples: A mix of push-ups, squats, jumping jacks, and sit-ups in quick succession."
        elif predicted_value == 12:
            exercise_type = (
                "You may do a High Intensity Cardio Circuit Training, Examples: Heavy Sprint intervals, burpees, KettleBell swings, "
                "Long Distance Running, Cycling, push-ups, squats, jumping jacks")
        else:
            exercise_type = "You may do a Light yoga, walking, foam rolling, Push-ups, Pull-ups"

        self.dialog = MDDialog(title="Recommend Exercise", text=f"{exercise_type}", buttons=[close_button])
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()


class Profile(Screen):
    def on_icon_release(self, screen_name):
        # Set transition effect
        self.manager.transition = SlideTransition(duration=0.01)
        # Switch to the specified screen
        self.manager.current = screen_name

    Name = StringProperty("")
    username = StringProperty("")
    email = StringProperty("")
    mobile = StringProperty("")
    date_of_birth = StringProperty("")
    gender = StringProperty("")

    def on_enter(self):
        self.fetch_user_data()

    def fetch_user_data(self):
        app = MDApp.get_running_app()
        print(app.user_info)
        self.Name = app.user_info.get('name', "")
        self.username = app.user_info.get('user_name', "")
        self.email = app.user_info.get('email', "")
        self.mobile = app.user_info.get('mobile', "")
        self.date_of_birth = app.user_info.get('date_of_birth', "")
        self.gender = app.user_info.get('gender', "")


class MaleWorkouts(Screen):
    def on_male_abs_card_press(self, screen_name):
        print("Male abs card pressed.")
        self.manager.current = screen_name

    def on_male_leg_card_press(self, screen_name):
        print("Male leg card pressed.")
        self.manager.current = screen_name

    def on_male_chest_card_press(self, screen_name):
        print("Male chest card pressed.")
        self.manager.current = screen_name

    def on_male_shoulder_card_press(self, screen_name):
        print("Male shoulder card pressed.")
        self.manager.current = screen_name

    def on_male_back_card_press(self, screen_name):
        print("Male back card pressed.")
        self.manager.current = screen_name

    def on_male_thigh_card_press(self, screen_name):
        print("Male thigh card pressed.")
        self.manager.current = screen_name

    def on_male_arms_card_press(self, screen_name):
        print("Male arms card pressed.")
        self.manager.current = screen_name

    def on_male_biceps_card_press(self, screen_name):
        print("Male biceps card pressed.")
        self.manager.current = screen_name

    def on_male_neck_card_press(self, screen_name):
        print("Male neck card pressed.")
        self.manager.current = screen_name

    def on_leave(self, *args):
        app = MDApp.get_running_app()

        date_time = str(datetime.now())
        # print(date_time)
        dt_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")
        date = str(dt_obj.date())
        month_day = dt_obj.strftime("%m-%d")
        app.fetched_calories['Date'].append(month_day)
        app.fetched_calories['caloriesBurn'].append(calories_burn)


class FemaleWorkouts(Screen):
    def on_female_abs_card_press(self, screen_name):
        print("Female abs card pressed.")
        self.manager.current = screen_name

    def on_female_leg_card_press(self, screen_name):
        print("Female leg card pressed.")
        self.manager.current = screen_name

    def on_female_chest_card_press(self, screen_name):
        print("Female chest card pressed.")
        self.manager.current = screen_name

    def on_female_shoulder_card_press(self, screen_name):
        print("Female shoulder card pressed.")
        self.manager.current = screen_name

    def on_female_back_card_press(self, screen_name):
        print("Female back card pressed.")
        self.manager.current = screen_name

    def on_female_thigh_card_press(self, screen_name):
        print("Female thigh card pressed.")
        self.manager.current = screen_name

    def on_female_arms_card_press(self, screen_name):
        print("Female arms card pressed.")
        self.manager.current = screen_name

    def on_female_glutes_card_press(self, screen_name):
        print("Female glutes card pressed.")
        self.manager.current = screen_name

    def on_female_neck_card_press(self, screen_name):
        print("Female neck card pressed.")
        self.manager.current = screen_name

    def on_leave(self, *args):
        app = MDApp.get_running_app()

        date_time = str(datetime.now())
        # print(date_time)
        dt_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")
        date = str(dt_obj.date())
        month_day = dt_obj.strftime("%m-%d")
        app.fetched_calories['Date'].append(month_day)
        app.fetched_calories['caloriesBurn'].append(calories_burn)


total_exercise_time = 0  # Tracks total exercise time for the workout
calories_burn = 0
MET = {
    'abs': 4.0,
    'leg': 5.5,
    'chest': 6.0,
    'shoulder': 4.5,
    'back': 6.0,
    'thigh': 5.0,
    'arms': 4.0,
    'biceps': 4.0,
    'neck': 2.5
}


# noinspection PyBroadException
class MaleAbsWorkouts(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_play_data = {}  # Tracks play time per video
        self.abs_workout_time = 0

    def track_video_time(self, video_player, video_id, state):
        import time
        global total_exercise_time
        if state == 'play':
            # Record the start time of the video
            self.video_play_data[video_id] = {
                'start_time': time.time(),
                'total_time': self.video_play_data.get(video_id, {}).get('total_time', 0)
            }
        elif state == 'pause' or state == 'stop':
            # Calculate the time the video was played
            if video_id in self.video_play_data and 'start_time' in self.video_play_data[video_id]:
                elapsed_time = time.time() - self.video_play_data[video_id]['start_time']
                self.video_play_data[video_id]['total_time'] += elapsed_time
                self.video_play_data[video_id].pop('start_time', None)

                self.abs_workout_time = self.abs_workout_time + elapsed_time
                # Add to the total exercise time
                total_exercise_time += elapsed_time

                print(f"Video {video_id} played for {elapsed_time:.2f} seconds. "
                      f"Total: {self.video_play_data[video_id]['total_time']:.2f} seconds.")
                print(f"Abs Workout Time: {self.abs_workout_time:.2f}")
                print(f"Total exercise time: {total_exercise_time:.2f} seconds.")

        global calories_burn
        global MET
        app = MDApp.get_running_app()
        weight = app.user_info['weight']
        total_exercise_duration_in_hours = self.abs_workout_time / 3600
        self.calories_burn_abs = MET.get('abs') * weight * total_exercise_duration_in_hours

    def on_leave(self, *args):
        try:
            global calories_burn
            calories_burn = calories_burn + self.calories_burn_abs
            print(f"Calories burn from abs: {self.calories_burn_abs}")
            print(f"Total Calories burn: {calories_burn}")

        except:
            self.manager.current = 'male_workouts'


# noinspection PyBroadException
class MaleLegWorkouts(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_play_data = {}  # Tracks play time per video
        self.leg_workout_time = 0

    def track_video_time(self, video_player, video_id, state):
        import time
        global total_exercise_time
        if state == 'play':
            # Record the start time of the video
            self.video_play_data[video_id] = {
                'start_time': time.time(),
                'total_time': self.video_play_data.get(video_id, {}).get('total_time', 0)
            }
        elif state == 'pause' or state == 'stop':
            # Calculate the time the video was played
            if video_id in self.video_play_data and 'start_time' in self.video_play_data[video_id]:
                elapsed_time = time.time() - self.video_play_data[video_id]['start_time']
                self.video_play_data[video_id]['total_time'] += elapsed_time
                self.video_play_data[video_id].pop('start_time', None)

                self.leg_workout_time += elapsed_time
                # Add to the total exercise time
                total_exercise_time += elapsed_time

                print(f"Video {video_id} played for {elapsed_time:.2f} seconds. "
                      f"Total: {self.video_play_data[video_id]['total_time']:.2f} seconds.")
                print(f"Total Leg Workout Time: {self.leg_workout_time:.2f}")
                print(f"Total exercise time: {total_exercise_time:.2f} seconds.")

        global calories_burn
        global MET
        app = MDApp.get_running_app()
        weight = app.user_info['weight']
        total_exercise_duration_in_hours = self.leg_workout_time / 3600
        self.calories_burn_leg = MET.get('leg') * weight * total_exercise_duration_in_hours

    def on_leave(self, *args):
        try:
            global calories_burn
            calories_burn = calories_burn + self.calories_burn_leg
            print(f"calories_burn for leg: {self.calories_burn_leg}")
            print(f"Total Calories Burn: {calories_burn}")
        except:
            self.manager.current = 'male_workouts'


# noinspection PyBroadException
class MaleChestWorkouts(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_play_data = {}  # Tracks play time per video
        self.chest_workout_time = 0

    def track_video_time(self, video_player, video_id, state):
        import time
        global total_exercise_time
        if state == 'play':
            # Record the start time of the video
            self.video_play_data[video_id] = {
                'start_time': time.time(),
                'total_time': self.video_play_data.get(video_id, {}).get('total_time', 0)
            }
        elif state == 'pause' or state == 'stop':
            # Calculate the time the video was played
            if video_id in self.video_play_data and 'start_time' in self.video_play_data[video_id]:
                elapsed_time = time.time() - self.video_play_data[video_id]['start_time']
                self.video_play_data[video_id]['total_time'] += elapsed_time
                self.video_play_data[video_id].pop('start_time', None)

                self.chest_workout_time += elapsed_time
                # Add to the total exercise time
                total_exercise_time += elapsed_time

                print(f"Video {video_id} played for {elapsed_time:.2f} seconds. "
                      f"Total: {self.video_play_data[video_id]['total_time']:.2f} seconds.")
                print(f"Total Leg Workout Time: {self.chest_workout_time:.2f}")
                print(f"Total exercise time: {total_exercise_time:.2f} seconds.")

        global calories_burn
        global MET
        app = MDApp.get_running_app()
        weight = app.user_info['weight']
        total_exercise_duration_in_hours = self.chest_workout_time / 3600
        self.calories_burn_chest = MET.get('leg') * weight * total_exercise_duration_in_hours

    def on_leave(self, *args):
        try:
            global calories_burn
            calories_burn = calories_burn + self.calories_burn_chest
            print(f"calories_burn for leg: {self.calories_burn_chest}")
            print(f"Total Calories Burn: {calories_burn}")
        except:
            self.manager.current = 'male_workouts'


# noinspection PyBroadException
class MaleShoulderWorkouts(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_play_data = {}  # Tracks play time per video
        self.shoulder_workout_time = 0

    def track_video_time(self, video_player, video_id, state):
        import time
        global total_exercise_time
        if state == 'play':
            # Record the start time of the video
            self.video_play_data[video_id] = {
                'start_time': time.time(),
                'total_time': self.video_play_data.get(video_id, {}).get('total_time', 0)
            }
        elif state == 'pause' or state == 'stop':
            # Calculate the time the video was played
            if video_id in self.video_play_data and 'start_time' in self.video_play_data[video_id]:
                elapsed_time = time.time() - self.video_play_data[video_id]['start_time']
                self.video_play_data[video_id]['total_time'] += elapsed_time
                self.video_play_data[video_id].pop('start_time', None)

                self.shoulder_workout_time += elapsed_time
                # Add to the total exercise time
                total_exercise_time += elapsed_time

                print(f"Video {video_id} played for {elapsed_time:.2f} seconds. "
                      f"Total: {self.video_play_data[video_id]['total_time']:.2f} seconds.")
                print(f"Total Leg Workout Time: {self.shoulder_workout_time:.2f}")
                print(f"Total exercise time: {total_exercise_time:.2f} seconds.")

        global calories_burn
        global MET
        app = MDApp.get_running_app()
        weight = app.user_info['weight']
        total_exercise_duration_in_hours = self.shoulder_workout_time / 3600
        self.calories_burn_shoulder = MET.get('leg') * weight * total_exercise_duration_in_hours

    def on_leave(self, *args):
        try:
            global calories_burn
            calories_burn = calories_burn + self.calories_burn_shoulder
            print(f"calories_burn for leg: {self.calories_burn_shoulder}")
            print(f"Total Calories Burn: {calories_burn}")
        except:
            self.manager.current = 'male_workouts'


# noinspection PyBroadException
class MaleBackWorkouts(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_play_data = {}  # Tracks play time per video
        self.back_workout_time = 0

    def track_video_time(self, video_player, video_id, state):
        import time
        global total_exercise_time
        if state == 'play':
            # Record the start time of the video
            self.video_play_data[video_id] = {
                'start_time': time.time(),
                'total_time': self.video_play_data.get(video_id, {}).get('total_time', 0)
            }
        elif state == 'pause' or state == 'stop':
            # Calculate the time the video was played
            if video_id in self.video_play_data and 'start_time' in self.video_play_data[video_id]:
                elapsed_time = time.time() - self.video_play_data[video_id]['start_time']
                self.video_play_data[video_id]['total_time'] += elapsed_time
                self.video_play_data[video_id].pop('start_time', None)

                self.back_workout_time += elapsed_time
                # Add to the total exercise time
                total_exercise_time += elapsed_time

                print(f"Video {video_id} played for {elapsed_time:.2f} seconds. "
                      f"Total: {self.video_play_data[video_id]['total_time']:.2f} seconds.")
                print(f"Total Leg Workout Time: {self.back_workout_time:.2f}")
                print(f"Total exercise time: {total_exercise_time:.2f} seconds.")

        global calories_burn
        global MET
        app = MDApp.get_running_app()
        weight = app.user_info['weight']
        total_exercise_duration_in_hours = self.back_workout_time / 3600
        self.calories_burn_back = MET.get('leg') * weight * total_exercise_duration_in_hours

    def on_leave(self, *args):
        try:
            global calories_burn
            calories_burn = calories_burn + self.calories_burn_back
            print(f"calories_burn for leg: {self.calories_burn_back}")
            print(f"Total Calories Burn: {calories_burn}")
        except:
            self.manager.current = 'male_workouts'


# noinspection PyBroadException
class MaleThighWorkouts(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_play_data = {}  # Tracks play time per video
        self.thigh_workout_time = 0

    def track_video_time(self, video_player, video_id, state):
        import time
        global total_exercise_time
        if state == 'play':
            # Record the start time of the video
            self.video_play_data[video_id] = {
                'start_time': time.time(),
                'total_time': self.video_play_data.get(video_id, {}).get('total_time', 0)
            }
        elif state == 'pause' or state == 'stop':
            # Calculate the time the video was played
            if video_id in self.video_play_data and 'start_time' in self.video_play_data[video_id]:
                elapsed_time = time.time() - self.video_play_data[video_id]['start_time']
                self.video_play_data[video_id]['total_time'] += elapsed_time
                self.video_play_data[video_id].pop('start_time', None)

                self.thigh_workout_time += elapsed_time
                # Add to the total exercise time
                total_exercise_time += elapsed_time

                print(f"Video {video_id} played for {elapsed_time:.2f} seconds. "
                      f"Total: {self.video_play_data[video_id]['total_time']:.2f} seconds.")
                print(f"Total Leg Workout Time: {self.thigh_workout_time:.2f}")
                print(f"Total exercise time: {total_exercise_time:.2f} seconds.")

        global calories_burn
        global MET
        app = MDApp.get_running_app()
        weight = app.user_info['weight']
        total_exercise_duration_in_hours = self.thigh_workout_time / 3600
        self.calories_burn_thigh = MET.get('leg') * weight * total_exercise_duration_in_hours

    def on_leave(self, *args):
        try:
            global calories_burn
            calories_burn = calories_burn + self.calories_burn_thigh
            print(f"calories_burn for leg: {self.calories_burn_thigh}")
            print(f"Total Calories Burn: {calories_burn}")
        except:
            self.manager.current = 'male_workouts'


# noinspection PyBroadException
class MaleArmsWorkouts(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_play_data = {}  # Tracks play time per video
        self.arms_workout_time = 0

    def track_video_time(self, video_player, video_id, state):
        import time
        global total_exercise_time
        if state == 'play':
            # Record the start time of the video
            self.video_play_data[video_id] = {
                'start_time': time.time(),
                'total_time': self.video_play_data.get(video_id, {}).get('total_time', 0)
            }
        elif state == 'pause' or state == 'stop':
            # Calculate the time the video was played
            if video_id in self.video_play_data and 'start_time' in self.video_play_data[video_id]:
                elapsed_time = time.time() - self.video_play_data[video_id]['start_time']
                self.video_play_data[video_id]['total_time'] += elapsed_time
                self.video_play_data[video_id].pop('start_time', None)

                self.arms_workout_time += elapsed_time
                # Add to the total exercise time
                total_exercise_time += elapsed_time

                print(f"Video {video_id} played for {elapsed_time:.2f} seconds. "
                      f"Total: {self.video_play_data[video_id]['total_time']:.2f} seconds.")
                print(f"Total Leg Workout Time: {self.arms_workout_time:.2f}")
                print(f"Total exercise time: {total_exercise_time:.2f} seconds.")

        global calories_burn
        global MET
        app = MDApp.get_running_app()
        weight = app.user_info['weight']
        total_exercise_duration_in_hours = self.arms_workout_time / 3600
        self.calories_burn_arms = MET.get('leg') * weight * total_exercise_duration_in_hours

    def on_leave(self, *args):
        try:
            global calories_burn
            calories_burn = calories_burn + self.calories_burn_arms
            print(f"calories_burn for leg: {self.calories_burn_arms}")
            print(f"Total Calories Burn: {calories_burn}")
        except:
            self.manager.current = 'male_workouts'


# noinspection PyBroadException
class MaleBicepsWorkouts(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_play_data = {}  # Tracks play time per video
        self.biceps_workout_time = 0

    def track_video_time(self, video_player, video_id, state):
        import time
        global total_exercise_time
        if state == 'play':
            # Record the start time of the video
            self.video_play_data[video_id] = {
                'start_time': time.time(),
                'total_time': self.video_play_data.get(video_id, {}).get('total_time', 0)
            }
        elif state == 'pause' or state == 'stop':
            # Calculate the time the video was played
            if video_id in self.video_play_data and 'start_time' in self.video_play_data[video_id]:
                elapsed_time = time.time() - self.video_play_data[video_id]['start_time']
                self.video_play_data[video_id]['total_time'] += elapsed_time
                self.video_play_data[video_id].pop('start_time', None)

                self.biceps_workout_time += elapsed_time
                # Add to the total exercise time
                total_exercise_time += elapsed_time

                print(f"Video {video_id} played for {elapsed_time:.2f} seconds. "
                      f"Total: {self.video_play_data[video_id]['total_time']:.2f} seconds.")
                print(f"Total Leg Workout Time: {self.biceps_workout_time:.2f}")
                print(f"Total exercise time: {total_exercise_time:.2f} seconds.")

        global calories_burn
        global MET
        app = MDApp.get_running_app()
        weight = app.user_info['weight']
        total_exercise_duration_in_hours = self.biceps_workout_time / 3600
        self.calories_burn_biceps = MET.get('leg') * weight * total_exercise_duration_in_hours

    def on_leave(self, *args):
        try:
            global calories_burn
            calories_burn = calories_burn + self.calories_burn_biceps
            print(f"calories_burn for leg: {self.calories_burn_biceps}")
            print(f"Total Calories Burn: {calories_burn}")
        except:
            self.manager.current = 'male_workouts'


# noinspection PyBroadException
class MaleNeckWorkouts(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_play_data = {}  # Tracks play time per video
        self.neck_workout_time = 0

    def track_video_time(self, video_player, video_id, state):
        import time
        global total_exercise_time
        if state == 'play':
            # Record the start time of the video
            self.video_play_data[video_id] = {
                'start_time': time.time(),
                'total_time': self.video_play_data.get(video_id, {}).get('total_time', 0)
            }
        elif state == 'pause' or state == 'stop':
            # Calculate the time the video was played
            if video_id in self.video_play_data and 'start_time' in self.video_play_data[video_id]:
                elapsed_time = time.time() - self.video_play_data[video_id]['start_time']
                self.video_play_data[video_id]['total_time'] += elapsed_time
                self.video_play_data[video_id].pop('start_time', None)

                self.neck_workout_time += elapsed_time
                # Add to the total exercise time
                total_exercise_time += elapsed_time

                print(f"Video {video_id} played for {elapsed_time:.2f} seconds. "
                      f"Total: {self.video_play_data[video_id]['total_time']:.2f} seconds.")
                print(f"Total Leg Workout Time: {self.neck_workout_time:.2f}")
                print(f"Total exercise time: {total_exercise_time:.2f} seconds.")

        global calories_burn
        global MET
        app = MDApp.get_running_app()
        weight = app.user_info['weight']
        total_exercise_duration_in_hours = self.neck_workout_time / 3600
        self.calories_burn_neck = MET.get('leg') * weight * total_exercise_duration_in_hours

    def on_leave(self, *args):
        try:
            global calories_burn
            calories_burn = calories_burn + self.calories_burn_neck
            print(f"calories_burn for leg: {self.calories_burn_neck}")
            print(f"Total Calories Burn: {calories_burn}")
        except:
            self.manager.current = 'male_workouts'


# noinspection PyBroadException
class FemaleAbsWorkouts(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_play_data = {}  # Tracks play time per video
        self.female_abs_workout_time = 0

    def track_video_time(self, video_player, video_id, state):
        import time
        global total_exercise_time
        if state == 'play':
            # Record the start time of the video
            self.video_play_data[video_id] = {
                'start_time': time.time(),
                'total_time': self.video_play_data.get(video_id, {}).get('total_time', 0)
            }
        elif state == 'pause' or state == 'stop':
            # Calculate the time the video was played
            if video_id in self.video_play_data and 'start_time' in self.video_play_data[video_id]:
                elapsed_time = time.time() - self.video_play_data[video_id]['start_time']
                self.video_play_data[video_id]['total_time'] += elapsed_time
                self.video_play_data[video_id].pop('start_time', None)

                self.female_abs_workout_time += elapsed_time
                # Add to the total exercise time
                total_exercise_time += elapsed_time

                print(f"Video {video_id} played for {elapsed_time:.2f} seconds. "
                      f"Total: {self.video_play_data[video_id]['total_time']:.2f} seconds.")
                print(f"Total Abs Workout Time: {self.female_abs_workout_time:.2f}")
                print(f"Total exercise time: {total_exercise_time:.2f} seconds.")

        global calories_burn
        global MET
        app = MDApp.get_running_app()
        weight = app.user_info['weight']
        total_exercise_duration_in_hours = self.female_abs_workout_time / 3600
        self.calories_burn_female_abs = MET.get('leg') * weight * total_exercise_duration_in_hours

    def on_leave(self, *args):
        try:
            global calories_burn
            calories_burn = calories_burn + self.calories_burn_female_abs
            print(f"calories_burn for Abs: {self.calories_burn_female_abs}")
            print(f"Total Calories Burn: {calories_burn}")
        except:
            self.manager.current = 'female_workouts'


# noinspection PyBroadException
class FemaleLegWorkouts(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_play_data = {}  # Tracks play time per video
        self.female_leg_workout_time = 0

    def track_video_time(self, video_player, video_id, state):
        import time
        global total_exercise_time
        if state == 'play':
            # Record the start time of the video
            self.video_play_data[video_id] = {
                'start_time': time.time(),
                'total_time': self.video_play_data.get(video_id, {}).get('total_time', 0)
            }
        elif state == 'pause' or state == 'stop':
            # Calculate the time the video was played
            if video_id in self.video_play_data and 'start_time' in self.video_play_data[video_id]:
                elapsed_time = time.time() - self.video_play_data[video_id]['start_time']
                self.video_play_data[video_id]['total_time'] += elapsed_time
                self.video_play_data[video_id].pop('start_time', None)

                self.female_leg_workout_time += elapsed_time
                # Add to the total exercise time
                total_exercise_time += elapsed_time

                print(f"Video {video_id} played for {elapsed_time:.2f} seconds. "
                      f"Total: {self.video_play_data[video_id]['total_time']:.2f} seconds.")
                print(f"Total Leg Workout Time: {self.female_leg_workout_time:.2f}")
                print(f"Total exercise time: {total_exercise_time:.2f} seconds.")

        global calories_burn
        global MET
        app = MDApp.get_running_app()
        weight = app.user_info['weight']
        total_exercise_duration_in_hours = self.female_leg_workout_time / 3600
        self.calories_burn_female_leg = MET.get('leg') * weight * total_exercise_duration_in_hours

    def on_leave(self, *args):
        try:
            global calories_burn
            calories_burn = calories_burn + self.calories_burn_female_leg
            print(f"calories_burn for leg: {self.calories_burn_female_leg}")
            print(f"Total Calories Burn: {calories_burn}")
        except:
            self.manager.current = 'female_workouts'


# noinspection PyBroadException
class FemaleChestWorkouts(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_play_data = {}  # Tracks play time per video
        self.female_chest_workout_time = 0

    def track_video_time(self, video_player, video_id, state):
        import time
        global total_exercise_time
        if state == 'play':
            # Record the start time of the video
            self.video_play_data[video_id] = {
                'start_time': time.time(),
                'total_time': self.video_play_data.get(video_id, {}).get('total_time', 0)
            }
        elif state == 'pause' or state == 'stop':
            # Calculate the time the video was played
            if video_id in self.video_play_data and 'start_time' in self.video_play_data[video_id]:
                elapsed_time = time.time() - self.video_play_data[video_id]['start_time']
                self.video_play_data[video_id]['total_time'] += elapsed_time
                self.video_play_data[video_id].pop('start_time', None)

                self.female_chest_workout_time += elapsed_time
                # Add to the total exercise time
                total_exercise_time += elapsed_time

                print(f"Video {video_id} played for {elapsed_time:.2f} seconds. "
                      f"Total: {self.video_play_data[video_id]['total_time']:.2f} seconds.")
                print(f"Total Chest Workout Time: {self.female_chest_workout_time:.2f}")
                print(f"Total exercise time: {total_exercise_time:.2f} seconds.")

        global calories_burn
        global MET
        app = MDApp.get_running_app()
        weight = app.user_info['weight']
        total_exercise_duration_in_hours = self.female_chest_workout_time / 3600
        self.calories_burn_female_chest = MET.get('leg') * weight * total_exercise_duration_in_hours

    def on_leave(self, *args):
        try:
            global calories_burn
            calories_burn = calories_burn + self.calories_burn_female_chest
            print(f"calories_burn for Chest: {self.calories_burn_female_chest}")
            print(f"Total Calories Burn: {calories_burn}")
        except:
            self.manager.current = 'female_workouts'


# noinspection PyBroadException
class FemaleShoulderWorkouts(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_play_data = {}  # Tracks play time per video
        self.female_shoulder_workout_time = 0

    def track_video_time(self, video_player, video_id, state):
        import time
        global total_exercise_time
        if state == 'play':
            # Record the start time of the video
            self.video_play_data[video_id] = {
                'start_time': time.time(),
                'total_time': self.video_play_data.get(video_id, {}).get('total_time', 0)
            }
        elif state == 'pause' or state == 'stop':
            # Calculate the time the video was played
            if video_id in self.video_play_data and 'start_time' in self.video_play_data[video_id]:
                elapsed_time = time.time() - self.video_play_data[video_id]['start_time']
                self.video_play_data[video_id]['total_time'] += elapsed_time
                self.video_play_data[video_id].pop('start_time', None)

                self.female_shoulder_workout_time += elapsed_time
                # Add to the total exercise time
                total_exercise_time += elapsed_time

                print(f"Video {video_id} played for {elapsed_time:.2f} seconds. "
                      f"Total: {self.video_play_data[video_id]['total_time']:.2f} seconds.")
                print(f"Total Shoulder Workout Time: {self.female_shoulder_workout_time:.2f}")
                print(f"Total exercise time: {total_exercise_time:.2f} seconds.")

        global calories_burn
        global MET
        app = MDApp.get_running_app()
        weight = app.user_info['weight']
        total_exercise_duration_in_hours = self.female_shoulder_workout_time / 3600
        self.calories_burn_female_shoulder = MET.get('leg') * weight * total_exercise_duration_in_hours

    def on_leave(self, *args):
        try:
            global calories_burn
            calories_burn = calories_burn + self.calories_burn_female_shoulder
            print(f"calories_burn for Shoulder: {self.calories_burn_female_shoulder}")
            print(f"Total Calories Burn: {calories_burn}")
        except:
            self.manager.current = 'female_workouts'


# noinspection PyBroadException
class FemaleBackWorkouts(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_play_data = {}  # Tracks play time per video
        self.female_back_workout_time = 0

    def track_video_time(self, video_player, video_id, state):
        import time
        global total_exercise_time
        if state == 'play':
            # Record the start time of the video
            self.video_play_data[video_id] = {
                'start_time': time.time(),
                'total_time': self.video_play_data.get(video_id, {}).get('total_time', 0)
            }
        elif state == 'pause' or state == 'stop':
            # Calculate the time the video was played
            if video_id in self.video_play_data and 'start_time' in self.video_play_data[video_id]:
                elapsed_time = time.time() - self.video_play_data[video_id]['start_time']
                self.video_play_data[video_id]['total_time'] += elapsed_time
                self.video_play_data[video_id].pop('start_time', None)

                self.female_back_workout_time += elapsed_time
                # Add to the total exercise time
                total_exercise_time += elapsed_time

                print(f"Video {video_id} played for {elapsed_time:.2f} seconds. "
                      f"Total: {self.video_play_data[video_id]['total_time']:.2f} seconds.")
                print(f"Total Back Workout Time: {self.female_back_workout_time:.2f}")
                print(f"Total exercise time: {total_exercise_time:.2f} seconds.")

        global calories_burn
        global MET
        app = MDApp.get_running_app()
        weight = app.user_info['weight']
        total_exercise_duration_in_hours = self.female_back_workout_time / 3600
        self.calories_burn_female_back = MET.get('leg') * weight * total_exercise_duration_in_hours

    def on_leave(self, *args):
        try:
            global calories_burn
            calories_burn = calories_burn + self.calories_burn_female_back
            print(f"calories_burn for Back: {self.calories_burn_female_back}")
            print(f"Total Calories Burn: {calories_burn}")
        except:
            self.manager.current = 'female_workouts'


class FemaleThighWorkouts(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_play_data = {}  # Tracks play time per video
        self.female_thigh_workout_time = 0

    def track_video_time(self, video_player, video_id, state):
        import time
        global total_exercise_time
        if state == 'play':
            # Record the start time of the video
            self.video_play_data[video_id] = {
                'start_time': time.time(),
                'total_time': self.video_play_data.get(video_id, {}).get('total_time', 0)
            }
        elif state == 'pause' or state == 'stop':
            # Calculate the time the video was played
            if video_id in self.video_play_data and 'start_time' in self.video_play_data[video_id]:
                elapsed_time = time.time() - self.video_play_data[video_id]['start_time']
                self.video_play_data[video_id]['total_time'] += elapsed_time
                self.video_play_data[video_id].pop('start_time', None)

                self.female_thigh_workout_time += elapsed_time
                # Add to the total exercise time
                total_exercise_time += elapsed_time

                print(f"Video {video_id} played for {elapsed_time:.2f} seconds. "
                      f"Total: {self.video_play_data[video_id]['total_time']:.2f} seconds.")
                print(f"Total Thigh Workout Time: {self.female_thigh_workout_time:.2f}")
                print(f"Total exercise time: {total_exercise_time:.2f} seconds.")

        global calories_burn
        global MET
        app = MDApp.get_running_app()
        weight = app.user_info['weight']
        total_exercise_duration_in_hours = self.female_thigh_workout_time / 3600
        self.calories_burn_female_thigh = MET.get('leg') * weight * total_exercise_duration_in_hours

    def on_leave(self, *args):
        try:
            global calories_burn
            calories_burn = calories_burn + self.calories_burn_female_thigh
            print(f"calories_burn for Thigh: {self.calories_burn_female_thigh}")
            print(f"Total Calories Burn: {calories_burn}")
        except:
            self.manager.current = 'female_workouts'


class FemaleArmsWorkouts(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_play_data = {}  # Tracks play time per video
        self.female_arms_workout_time = 0

    def track_video_time(self, video_player, video_id, state):
        import time
        global total_exercise_time
        if state == 'play':
            # Record the start time of the video
            self.video_play_data[video_id] = {
                'start_time': time.time(),
                'total_time': self.video_play_data.get(video_id, {}).get('total_time', 0)
            }
        elif state == 'pause' or state == 'stop':
            # Calculate the time the video was played
            if video_id in self.video_play_data and 'start_time' in self.video_play_data[video_id]:
                elapsed_time = time.time() - self.video_play_data[video_id]['start_time']
                self.video_play_data[video_id]['total_time'] += elapsed_time
                self.video_play_data[video_id].pop('start_time', None)

                self.female_arms_workout_time += elapsed_time
                # Add to the total exercise time
                total_exercise_time += elapsed_time

                print(f"Video {video_id} played for {elapsed_time:.2f} seconds. "
                      f"Total: {self.video_play_data[video_id]['total_time']:.2f} seconds.")
                print(f"Total Arms Workout Time: {self.female_arms_workout_time:.2f}")
                print(f"Total exercise time: {total_exercise_time:.2f} seconds.")

        global calories_burn
        global MET
        app = MDApp.get_running_app()
        weight = app.user_info['weight']
        total_exercise_duration_in_hours = self.female_arms_workout_time / 3600
        self.calories_burn_female_arms = MET.get('leg') * weight * total_exercise_duration_in_hours

    def on_leave(self, *args):
        try:
            global calories_burn
            calories_burn = calories_burn + self.calories_burn_female_arms
            print(f"calories_burn for Arms: {self.calories_burn_female_arms}")
            print(f"Total Calories Burn: {calories_burn}")
        except:
            self.manager.current = 'female_workouts'


class FemaleGlutesWorkouts(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_play_data = {}  # Tracks play time per video
        self.female_glutes_workout_time = 0

    def track_video_time(self, video_player, video_id, state):
        import time
        global total_exercise_time
        if state == 'play':
            # Record the start time of the video
            self.video_play_data[video_id] = {
                'start_time': time.time(),
                'total_time': self.video_play_data.get(video_id, {}).get('total_time', 0)
            }
        elif state == 'pause' or state == 'stop':
            # Calculate the time the video was played
            if video_id in self.video_play_data and 'start_time' in self.video_play_data[video_id]:
                elapsed_time = time.time() - self.video_play_data[video_id]['start_time']
                self.video_play_data[video_id]['total_time'] += elapsed_time
                self.video_play_data[video_id].pop('start_time', None)

                self.female_glutes_workout_time += elapsed_time
                # Add to the total exercise time
                total_exercise_time += elapsed_time

                print(f"Video {video_id} played for {elapsed_time:.2f} seconds. "
                      f"Total: {self.video_play_data[video_id]['total_time']:.2f} seconds.")
                print(f"Total Glutes Workout Time: {self.female_glutes_workout_time:.2f}")
                print(f"Total exercise time: {total_exercise_time:.2f} seconds.")

        global calories_burn
        global MET
        app = MDApp.get_running_app()
        weight = app.user_info['weight']
        total_exercise_duration_in_hours = self.female_glutes_workout_time / 3600
        self.calories_burn_female_glutes = MET.get('leg') * weight * total_exercise_duration_in_hours

    def on_leave(self, *args):
        try:
            global calories_burn
            calories_burn = calories_burn + self.calories_burn_female_glutes
            print(f"calories_burn for Glutes: {self.calories_burn_female_glutes}")
            print(f"Total Calories Burn: {calories_burn}")
        except:
            self.manager.current = 'female_workouts'


class FemaleNeckWorkouts(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_play_data = {}  # Tracks play time per video
        self.female_neck_workout_time = 0

    def track_video_time(self, video_player, video_id, state):
        import time
        global total_exercise_time
        if state == 'play':
            # Record the start time of the video
            self.video_play_data[video_id] = {
                'start_time': time.time(),
                'total_time': self.video_play_data.get(video_id, {}).get('total_time', 0)
            }
        elif state == 'pause' or state == 'stop':
            # Calculate the time the video was played
            if video_id in self.video_play_data and 'start_time' in self.video_play_data[video_id]:
                elapsed_time = time.time() - self.video_play_data[video_id]['start_time']
                self.video_play_data[video_id]['total_time'] += elapsed_time
                self.video_play_data[video_id].pop('start_time', None)

                self.female_neck_workout_time += elapsed_time
                # Add to the total exercise time
                total_exercise_time += elapsed_time

                print(f"Video {video_id} played for {elapsed_time:.2f} seconds. "
                      f"Total: {self.video_play_data[video_id]['total_time']:.2f} seconds.")
                print(f"Total Neck Workout Time: {self.female_neck_workout_time:.2f}")
                print(f"Total exercise time: {total_exercise_time:.2f} seconds.")

        global calories_burn
        global MET
        app = MDApp.get_running_app()
        weight = app.user_info['weight']
        total_exercise_duration_in_hours = self.female_neck_workout_time / 3600
        self.calories_burn_female_neck = MET.get('leg') * weight * total_exercise_duration_in_hours

    def on_leave(self, *args):
        try:
            global calories_burn
            calories_burn = calories_burn + self.calories_burn_female_neck
            print(f"calories_burn for Neck: {self.calories_burn_female_neck}")
            print(f"Total Calories Burn: {calories_burn}")
        except:
            self.manager.current = 'female_workouts'


class UpdateHeightAndWeight(Screen):
    def updateHeightAndWeight(self):
        app = MDApp.get_running_app()
        username = app.user_name.get('user_name')
        height = self.ids.height.text
        weight = self.ids.weight.text
        print(username)
        if not height or not weight:
            close_button = MDFlatButton(text='Close', on_release=self.close_dialog)
            self.dialog = MDDialog(title='Update Check', text='Please Provide Both details',
                                   buttons=[close_button])
            self.dialog.open()
            return

        try:
            # Send the data to the Flask backend
            # url = "http://127.0.0.1:5000/update"
            payload = {"username": username, "height": height, "weight": weight}
            response = requests.post("http://127.0.0.1:5000/update", json=payload)

            close_button = MDFlatButton(text='Close', on_release=self.close_dialog)
            if response.status_code == 200:
                self.dialog = MDDialog(title='Update Check', text='Update Successful',
                                       buttons=[close_button])
                self.dialog.open()
                print("Height and weight updated successfully!")
                app.user_info['height'] = float(height)
                app.user_info['weight'] = float(weight)
            else:
                self.dialog = MDDialog(title='Update Check', text='Update UnSuccessful',
                                       buttons=[close_button])
                self.dialog.open()
                print(f"Error: {response.json().get('error')}")

        except Exception as e:
            close_button = MDFlatButton(text='Close', on_release=self.close_dialog)
            self.dialog = MDDialog(title='Update Check', text='An Error Occurred',
                                   buttons=[close_button])
            self.dialog.open()
            print(f"An error occurred: {e}")

    def close_dialog(self, obj):
        self.dialog.dismiss()


class PasswordChange(Screen):
    def updatePassword(self):
        app = MDApp.get_running_app()
        username = app.user_name.get('user_name')
        old_password = self.ids.old_password.text
        new_password = self.ids.new_password.text
        confirm_password = self.ids.confirm_password.text

        close_button = MDFlatButton(text='Close', on_release=self.close_dialog)

        if not old_password or not new_password or not confirm_password:
            self.dialog = MDDialog(title='Update Check', text='Please Provide All details',
                                   buttons=[close_button])
            self.dialog.open()
            return

        try:
            datas = {'username': username, 'password': old_password, 'confirm_password': confirm_password}
            response = requests.post("http://127.0.0.1:5000/updatePassword", json=datas)

            if response.status_code == 201:
                self.dialog = MDDialog(title='Update Check', text='Password Updated Successfully',
                                       buttons=[close_button])
                self.dialog.open()

            else:
                self.dialog = MDDialog(title='Update Check', text='Password did not matched',
                                       buttons=[close_button])
                self.dialog.open()

        except Exception as e:
            close_button = MDFlatButton(text='Close', on_release=self.close_dialog)
            self.dialog = MDDialog(title='Update Check', text='An Error Occurred',
                                   buttons=[close_button])
            self.dialog.open()
            print(f"An error occurred: {e}")

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def check_passwords(self, instance):
        new_password = self.ids.new_password.text
        confirm_password = self.ids.confirm_password
        if instance == confirm_password:
            if new_password != confirm_password.text:
                confirm_password.error = True
                confirm_password.helper_text = "password must be same as above"
            else:
                confirm_password.error = False
                confirm_password.helper_text = ""  # clear helper text


sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(SignUpScreen1(name='signup1'))
sm.add_widget(SignUpScreen2(name='signup2'))
sm.add_widget(Home(name='home'))
sm.add_widget(Workouts(name='workouts'))
sm.add_widget(Progress(name='progress'))
sm.add_widget(Profile(name='profile'))
sm.add_widget(MaleWorkouts(name='male_workouts'))
sm.add_widget(FemaleWorkouts(name='female_workouts'))
sm.add_widget(MaleAbsWorkouts(name='male_abs_workouts'))
sm.add_widget(MaleLegWorkouts(name='male_leg_workouts'))
sm.add_widget(MaleChestWorkouts(name='male_chest_workouts'))
sm.add_widget(MaleShoulderWorkouts(name='male_shoulder_workouts'))
sm.add_widget(MaleBackWorkouts(name='male_back_workouts'))
sm.add_widget(MaleThighWorkouts(name='male_thigh_workouts'))
sm.add_widget(MaleArmsWorkouts(name='male_arms_workouts'))
sm.add_widget(MaleBicepsWorkouts(name='male_biceps_workouts'))
sm.add_widget(MaleNeckWorkouts(name='male_neck_workouts'))
sm.add_widget(FemaleAbsWorkouts(name='female_abs_workouts'))
sm.add_widget(FemaleLegWorkouts(name='female_leg_workouts'))
sm.add_widget(FemaleChestWorkouts(name='female_chest_workouts'))
sm.add_widget(FemaleShoulderWorkouts(name='female_shoulder_workouts'))
sm.add_widget(FemaleBackWorkouts(name='female_back_workouts'))
sm.add_widget(FemaleThighWorkouts(name='female_thigh_workouts'))
sm.add_widget(FemaleArmsWorkouts(name='female_arms_workouts'))
sm.add_widget(FemaleGlutesWorkouts(name='female_glutes_workouts'))
sm.add_widget(FemaleNeckWorkouts(name='female_neck_workouts'))
sm.add_widget(UpdateHeightAndWeight(name='updateHeightAndWeight'))
sm.add_widget(PasswordChange(name='passwordChange'))


class WorkoutApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        date_time = str(datetime.now())
        # print(date_time)
        dt_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S.%f")
        date = str(dt_obj.date())
        month_day = dt_obj.strftime("%m-%d")

        self.signup_data = {}  # Store signup data across screens
        self.user_name = {}  # Store username while login
        self.user_info = {}  # Store user information who is logged in
        self.only_name = {}  # Store only name of User, eg: Hari, Shyam
        self.calories_data = {}  # Store user's calories burn record
        self.fetched_calories = {'Date': [month_day],
                                 'caloriesBurn': [0]}  # Store User's Calories data fetched from database

    def build(self):
        self.theme_cls.primary_palette = "Brown"
        screen = Builder.load_string(kv)
        return screen

    def set_active_button(self, button_name):
        self.active_button = button_name
        self.root.current = button_name  # Navigate to the clicked screen

    def on_stop(self):
        # from datetime import date
        try:
            # Convert date to a string
            # if isinstance(self.calories_data["date"], date):
            #     self.calories_data["date"] = self.calories_data["date"].isoformat()

            response = requests.post("http://127.0.0.1:5000/api/insertCaloriesData", json=self.calories_data,
                                     timeout=10)
            print("Server Response:", response.json())
            print("Calories Record Successfully Inserted")

        except requests.exceptions.RequestException as e:
            print("Error Occurred: ", e)


if __name__ == "__main__":
    WorkoutApp().run()
