from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

SWAGGER_URL="/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL="/static/masterblog.json" # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API' # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET','POST'])
def get_posts():
    highest_id = 0
    for post in POSTS:
        if 'id' in post and post.get('id') > highest_id:
            highest_id = post.get('id')

    if request.method == 'GET':
        sort_field = request.args.get('sort')
        sort_direction = request.args.get('direction')
        print(sort_field, sort_direction)

        if sort_field not in [None, 'title', 'content']:
            return jsonify({'error': 'Invalid sort field. Must be "title" or "content".'}), 400

        if sort_direction not in [None, 'asc', 'desc']:
            return jsonify({'error': 'Invalid sort direction. Must be "asc" or "desc".'}), 400

        sorted_posts = POSTS

        if sort_field:
            reverse = True if sort_direction == 'desc' else False
            sorted_posts = sorted(POSTS, key=lambda p: p[sort_field].lower(), reverse=reverse)

        return jsonify(sorted_posts), 200

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
    data = request.get_json()
    post = next((p for p in POSTS if p['id'] == id), None)

    if post is None:
        return jsonify({'error': 'post not found'}), 404

    if data.get('title'):
        post['title'] = data['title']
    if data.get('content'):
        post['content'] = data['content']

    return jsonify(post)


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    global POSTS
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    filtered_posts = [p for p in POSTS if
                    (title_query and title_query in p['title'].lower()) or
                    (content_query and content_query in p['content'].lower())]

    print(filtered_posts)
    return jsonify(filtered_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
