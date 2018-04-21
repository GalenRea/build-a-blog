from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'thisappissecret'


class Diary(db.Model):
    '''
    Stores blog entries
    '''

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(4000))
   


    def __init__(self, title, body):
        self.title = title
        self.body = body
       

    def is_valid(self):
        '''
        all blanks must be filled in for a valid blog post
        '''
        if self.title and self.body:
            return True
        else:
            return False



@app.route("/")
def index():
    return redirect("/blog")

@app.route('/blog') 
def display_entries():
    entry_id = request.args.get('id')
    
    if (entry_id): 
        entry = Diary.query.get(entry_id)
        return render_template('single_entry.html', title ="Blog Post", entry=entry)

        #blog_title = request.form['Blog']
        #new_blog = Blog(blog_title, blog_body)
        #db.session.add(new_blog)
        #db.session.commit()
    #return render_template('index.html', title=title, body=body) 

    sort = request.args.get('sort')
    if (sort=="newest"):
        all_entries = Diary.query.order_by(Diary.created.desc()).all()
    else:
        all_entries = Diary.query.all()
    return render_template('all_entries.html', title = "All Entries", all_entries=all_entries)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    '''
    GET: Requests info from the server to display on the browser
    POST: gets info from the user on browser to save to the server
    '''
    
    if request.method == 'POST':
        new_entry_title = request.form['title']
        new_entry_body = request.form['body'] 
        new_entry = Diary(new_entry_title, new_entry_body)
    
        if new_entry.is_valid():
            db.session.add(new_entry)
            db.session.commit()
            url = "/blog?id=" + str(new_entry.id)
            return redirect(url)
        else:
            flash("Please fill in all required fields")
            return redirect('/new_entry')
            #title="Create new blog entry",
            #new_entry_title=new_entry_title
            #new_entry_body=new_entry_body

    else: #GET request
        return render_template('new_entry_form.html', title="Create new blog entry")

if __name__ == '__main__':
    app.run()



 