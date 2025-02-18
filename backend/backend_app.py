from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    global POSTS
    highest_id = 0
    for post in POSTS:
        if 'id' in post and post.get('id') > highest_id:
            highest_id = post.get('id')
    if request.method == 'POST':
        data = request.get_json()
        if not data or not data.get('title') or not data.get('content'):
            return jsonify({'error': 'Both title and content are required.'}), 400
        new_post = {
            "id": highest_id +1,
            "title": data['title'],
            "content": data['content']
        }
        POSTS.append(new_post)
    return jsonify(POSTS), 201

@app.route("/api/posts/<int:id>", methods=['DELETE'])
def delete_post(id):
    global POSTS
    post = next((p for p in POSTS if p['id'] == id), None)

    if post is None:
        return jsonify({'error': 'post not found'}), 404

    POSTS = [p for p in POSTS if p['id'] != id]
    return jsonify({'message': f'Post with id {id} has been deleted successfully.'}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    global POSTS
    data = request.get_json()
    post = next((p for p in POSTS if p['id'] == id), None)

    if post is None:
        return jsonify({'error': 'post not found'}), 404

    if data.get('title'):
        post['title'] = data['title']
    if data.get('content'):
        post['content'] = data['content']

    return jsonify(post)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
