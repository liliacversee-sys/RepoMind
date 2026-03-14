graph [
  directed 1
  node [
    id 0
    label "repos/407340a2-4a71-4586-be31-8fe13b13c099/app.py"
    type "file"
  ]
  node [
    id 1
    label "load_spoofing_model"
    type "function"
  ]
  node [
    id 2
    label "preprocess_audio_for_model"
    type "function"
  ]
  node [
    id 3
    label "before_request"
    type "function"
  ]
  node [
    id 4
    label "index"
    type "function"
  ]
  node [
    id 5
    label "static_files"
    type "function"
  ]
  node [
    id 6
    label "partial_html_files"
    type "function"
  ]
  node [
    id 7
    label "favicon"
    type "function"
  ]
  node [
    id 8
    label "register_user"
    type "function"
  ]
  node [
    id 9
    label "login_user"
    type "function"
  ]
  node [
    id 10
    label "logout_user"
    type "function"
  ]
  node [
    id 11
    label "get_current_user"
    type "function"
  ]
  node [
    id 12
    label "analyze_voice_api"
    type "function"
  ]
  node [
    id 13
    label "get_analyses"
    type "function"
  ]
  node [
    id 14
    label "get_news"
    type "function"
  ]
  node [
    id 15
    label "import os"
    type "import"
  ]
  node [
    id 16
    label "import threading"
    type "import"
  ]
  node [
    id 17
    label "import requests"
    type "import"
  ]
  node [
    id 18
    label "from flask import Flask, request, jsonify, render_template, session, redirect, url_for, send_from_directory"
    type "import"
  ]
  node [
    id 19
    label "from pymongo import MongoClient"
    type "import"
  ]
  node [
    id 20
    label "import uuid"
    type "import"
  ]
  node [
    id 21
    label "import librosa"
    type "import"
  ]
  node [
    id 22
    label "import numpy as np"
    type "import"
  ]
  node [
    id 23
    label "import tensorflow as tf"
    type "import"
  ]
  node [
    id 24
    label "from tensorflow.keras.models import load_model"
    type "import"
  ]
  node [
    id 25
    label "from werkzeug.security import generate_password_hash, check_password_hash"
    type "import"
  ]
  node [
    id 26
    label "from datetime import datetime"
    type "import"
  ]
  node [
    id 27
    label "repos/407340a2-4a71-4586-be31-8fe13b13c099/static/script.js"
    type "file"
  ]
  edge [
    source 0
    target 1
    relation "defines"
  ]
  edge [
    source 0
    target 2
    relation "defines"
  ]
  edge [
    source 0
    target 3
    relation "defines"
  ]
  edge [
    source 0
    target 4
    relation "defines"
  ]
  edge [
    source 0
    target 5
    relation "defines"
  ]
  edge [
    source 0
    target 6
    relation "defines"
  ]
  edge [
    source 0
    target 7
    relation "defines"
  ]
  edge [
    source 0
    target 8
    relation "defines"
  ]
  edge [
    source 0
    target 9
    relation "defines"
  ]
  edge [
    source 0
    target 10
    relation "defines"
  ]
  edge [
    source 0
    target 11
    relation "defines"
  ]
  edge [
    source 0
    target 12
    relation "defines"
  ]
  edge [
    source 0
    target 13
    relation "defines"
  ]
  edge [
    source 0
    target 14
    relation "defines"
  ]
  edge [
    source 0
    target 15
    relation "imports"
  ]
  edge [
    source 0
    target 16
    relation "imports"
  ]
  edge [
    source 0
    target 17
    relation "imports"
  ]
  edge [
    source 0
    target 18
    relation "imports"
  ]
  edge [
    source 0
    target 19
    relation "imports"
  ]
  edge [
    source 0
    target 20
    relation "imports"
  ]
  edge [
    source 0
    target 21
    relation "imports"
  ]
  edge [
    source 0
    target 22
    relation "imports"
  ]
  edge [
    source 0
    target 23
    relation "imports"
  ]
  edge [
    source 0
    target 24
    relation "imports"
  ]
  edge [
    source 0
    target 25
    relation "imports"
  ]
  edge [
    source 0
    target 26
    relation "imports"
  ]
]
