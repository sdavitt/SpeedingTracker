from flask import current_app as app, session


@app.context_processor
def game_stuff():
    if 'game' not in session:
        session['game'] = {
            'players': [],
        }
    return {'game': session['game']}