from flask import Flask,render_template,request,redirect
#from flask_sqlA
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app  = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    author = db.Column(db.String(20), nullable =False)
    date_posted = db.Column(db.DateTime , nullable = False , default = datetime.utcnow)

    def __repr__(self):
        return 'Blog post'+ str(self.id)

all_post  = [
    {
        'title':'AEIOU. I love u',
        'content':'This is the content of post 1. Lalalalalla',
        'author':'Pratyush'
    },
    {
        'title':"God can only save India's Ass",
        'content':'This is the content of post 2. Lalalalalla',
        'author':'Harsh'
    },
    {
        'title':"Economics @post Covid world",
        'content':'This is the content of post 3. Lalalalalla',
    }


]

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/home/<string:name>/posts/<int:id>')
def helloWorld(id,name):
    return "Fetched post number id "+str(id)+"  "+"for person "+str(name)

@app.route('/onlyget',methods=['GET','POST'])
def get_req():
    return "Nothing Special ...."

@app.route("/posts/delete/<int:id>")
def delete(id):
    print("Delete!!")
    post =BlogPost.query.get_or_404(id)
    print(post)
    db.session.delete(post)
    db.session.commit()
    return redirect("/posts")
    

@app.route('/posts',methods = ['GET','POST'])
def posts():
    print("------------in posts")
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        new_post = BlogPost(title=title , content=content, author =request.form['author'])
        db.session.add(new_post)
        db.session.commit()
        return redirect("/posts")
    else:
        all_post = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('post.html',posts = all_post)
if __name__ == "__main__":
    app.run(debug=True)


