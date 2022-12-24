from flask import jsonify
from errors import ApiException
from views import UserView, AdvertisementView
from flask_api import app


@app.errorhandler(ApiException)
def error_handler(error: ApiException):
    response = jsonify({
        'status': 'error',
        'message': error.message
    })
    response.status_code = error.status_code
    return response


app.add_url_rule('/users/<int:user_id>', view_func=UserView.as_view('users'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/users/', view_func=UserView.as_view('users_create'), methods=['POST'])
app.add_url_rule('/adv/', view_func=AdvertisementView.as_view('adv_create'), methods=['POST'])
app.add_url_rule('/adv/<int:advertisement_id>', view_func=AdvertisementView.as_view('adv'), methods=['GET', 'PATCH', 'DELETE'])

if __name__ == '__main__':
    app.run()
