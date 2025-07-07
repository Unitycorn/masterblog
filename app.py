from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def get_all_blog_posts():
    with open('data.json', 'r') as handle:
        blog_posts = json.load(handle)
    return blog_posts


def save_to_file(data):
    with open('data.json', 'w') as handle:
        json.dump(data, handle)


def fetch_post_by_id(blog_id):
    blog_posts = get_all_blog_posts()
    for post in blog_posts:
        if post['id'] == blog_id:
            return post
    return None


@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    blog_posts = get_all_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    blog_posts = get_all_blog_posts()
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']
        new_blog_id = 0
        for blog in blog_posts:
            if blog['id'] >= new_blog_id:
                new_blog_id = blog['id'] + 1
        blog_posts.append({'id': new_blog_id, 'author': author, 'title': title, 'content': content})
        save_to_file(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = get_all_blog_posts()
    for blog in blog_posts:
        if blog['id'] == post_id:
            blog_posts.remove(blog)
            break
    save_to_file(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    blog_posts = get_all_blog_posts()
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        pass
        # Update the post in the JSON file
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']
        for index, blog in enumerate(blog_posts):
            if blog['id'] == post['id']:
                blog_posts[index] = {'id': post['id'], 'author': author, 'title': title, 'content': content}
        save_to_file(blog_posts)
        # Redirect back to index
        return redirect(url_for('index'))
    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
