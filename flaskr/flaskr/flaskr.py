import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import json
from flask import jsonify


import flaskr.query_list as qs

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, '/Users/venkat299/work/MPB_18_19/mpb_18-19.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)




def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


# def init_db():
#     db = get_db()
#     with app.open_resource('schema.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()

# @app.cli.command('initdb')
# def initdb_command():
#     """Initializes the database."""
#     init_db()
#     print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute(qs.get_sanc())
    # cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

def get_as_json(cursor):
    rows = [x for x in cursor]
    cols = [x[0] for x in cursor.description]
    ls = []
    for row in rows:
        item = {}
        for prop, val in zip(cols, row):
            item[prop] = val
        ls.append(item)
    return json.dumps(ls)

@app.route('/filter', methods=['POST'])
def show_entries_filter():
    qfilter = request.form['filter']
    print('filter=', qfilter,";")
    db = get_db()
    db1 = get_db()
    db2 = get_db()
    entries = []
    footer = []
    dscd_json =[]
    unit_json=[]
    try:
        cur_dscd = db1.execute('select desig||"_"||grade||"_"||dscd as name, dscd as value from desg')
        dscd_json = get_as_json(cur_dscd)
        # print(dscd_json)

        cur_unit = db2.execute('select name||"_"||type||"_"||code as name, code as value from unit')
        unit_json = get_as_json(cur_unit)
        # print(unit_json)

        # cur = db.execute(qs.get_sanc_filter(filter=qfilter))
        cur = db.execute(qs.get_sanc_filter(filter=qfilter))
        # cur = db.execute('select title, text from entries order by id desc')
        # entries = cur.fetchall()
        rows = [x for x in cur]
        cols = [x[0] for x in cur.description]
        ls = []
        for row in rows:
            item = {}
            for prop, val in zip(cols, row):
                if val is None and prop != "remark":
                    val=0
                item[prop] = val
            ls.append(item)
        # Create a string representation of your array of ls.
        lsJSON = json.dumps(ls)

        cur = db.execute(qs.get_sanc_filter_footer(filter=qfilter))
        # cur = db.execute('select title, text from entries order by id desc')
        footer = cur.fetchall()

    except sqlite3.OperationalError as e:
        raise e
        # return render_template('show_entries.html', entries=[], qfilter=qfilter, dscd_json=[], unit_json=[],  footer=footer, error=e )

    return render_template('show_entries.html', entries=lsJSON, qfilter=qfilter, dscd_json=dscd_json, unit_json=unit_json, footer=footer )

@app.route('/update_sanction', methods=['POST'])
def update_entry():
    if not session.get('logged_in'):
        abort(401)
    
    response = {"success":True}
    db = get_db()
    # db.execute('insert into entries (title, text) values (?, ?)',
    #              [request.form['title'], request.form['text']])
    db.execute('delete from sanc where dscd=? and unit=?',[request.form['dscd'], request.form['unit']])
    db.execute('insert into sanc (req, san, remark, dscd, unit) values (?,?,?,?,?)',
                 [request.form['req'], request.form['san'], request.form['remark'], request.form['dscd'], request.form['unit']])
    db.commit()
    # flash('New entry was successfully posted')
    print(request.form['dscd'], request.form['unit'],request.form['req'], request.form['san'])
    return jsonify(response)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

# @app.route('/')
# def index():
#     return 'Index Page'

# @app.route('/projects/')
# def projects():
#     return 'The project page'

# @app.route('/about')
# def about():
#     return 'The about page'