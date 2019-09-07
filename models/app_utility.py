from flask import jsonify


def success(result):
    if result == "":
        return jsonify({
            "message": "success"
        })
    else:
        return jsonify({
            "message": "success",
            "result": result
        })


def failure(message):
    return jsonify({
        "message": message
    })
