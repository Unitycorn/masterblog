from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

with open('data.json', 'r') as handle:
    blog_posts = json.load(handle)


@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']
        new_blog_id = 0
        for blog in blog_posts:
            if blog['id'] >= new_blog_id:
                new_blog_id = blog['id'] + 1
        blog_posts.append({'id': new_blog_id, 'author': author, 'title': title, 'content': content})
        with open('data.json', 'w') as handle:
            json.dump(blog_posts, handle, indent=4)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    for blog in blog_posts:
        if blog['id'] == post_id:
            blog_posts.remove(blog)
            break
    with open('data.json', 'w') as handle:
        json.dump(blog_posts, handle, indent=4)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
