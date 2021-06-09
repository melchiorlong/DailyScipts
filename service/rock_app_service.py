from exception.rock_exception import ParameterError, UserNotAllowed
from controller.impl.GetTimezoneImpl import GetTimezoneImpl
from controller.impl.server.get_server_time_impl import GetServerTimeImpl
from flask import Flask, request, make_response
from util.config_reader import get_config


app = Flask(__name__)

user_blacklist = get_config().get('user_blacklist')

@app.route('/')
def index_page():
    return 'Rock实训 Flask Ver.'


@app.route('/time/server/get/', methods=['GET'])
def get_server_time():
    username = request.args.get('user')

    if username in user_blacklist:
        error = UserNotAllowed(400, username)
        return make_response(error.get_UserNotAllowed())

    get_server_time_impl = GetServerTimeImpl
    res = get_server_time_impl.get_time_now(self=get_server_time_impl)
    return make_response(res)


@app.route('/time/get', methods=['GET'])
def get_timezone():
    username = request.args.get('user')
    if username in user_blacklist:
        error = UserNotAllowed(400, username)
        return make_response(error.get_UserNotAllowed())
    time_zone = request.args.get('timezone')

    if not time_zone.isdigit():
        error = ParameterError(400)
        return make_response(error.get_ParameterError())
    if int(time_zone) < -12 or int(time_zone) > 12:
        error = ParameterError(400)
        return make_response(error.get_ParameterError())
    get_timezone_impl = GetTimezoneImpl
    res = get_timezone_impl.get_time_zone(self=get_timezone_impl, time_zone=time_zone)
    return make_response(res)


app.run()
