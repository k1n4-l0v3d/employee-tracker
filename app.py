from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Настройки БД — измените под свои данные
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql+psycopg://postgres:password@localhost:5432/employee_tracker'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ─── Модели ───────────────────────────────────────────────

class StupidQuestion(db.Model):
    __tablename__ = 'stupid_questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    comment = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class BrokenFlashdrive(db.Model):
    __tablename__ = 'broken_flashdrives'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300))
    comment = db.Column(db.String(500))
    broken_at = db.Column(db.DateTime, default=datetime.utcnow)

class SeriesWatch(db.Model):
    __tablename__ = 'series_watches'
    id = db.Column(db.Integer, primary_key=True)
    series_name = db.Column(db.String(200), nullable=False)
    episode = db.Column(db.String(100))
    duration_minutes = db.Column(db.Integer)
    comment = db.Column(db.String(500))
    watched_at = db.Column(db.DateTime, default=datetime.utcnow)

# ─── Маршруты ─────────────────────────────────────────────

@app.route('/')
def index():
    total_questions = StupidQuestion.query.count()
    total_series = SeriesWatch.query.count()
    total_flashdrives = BrokenFlashdrive.query.count()
    total_minutes = db.session.query(
        db.func.sum(SeriesWatch.duration_minutes)
    ).scalar() or 0
    return render_template('index.html',
        total_questions=total_questions,
        total_series=total_series,
        total_flashdrives=total_flashdrives,
        total_minutes=total_minutes
    )

# ── Глупые вопросы ──

@app.route('/api/questions', methods=['GET'])
def get_questions():
    questions = StupidQuestion.query.order_by(
        StupidQuestion.created_at.desc()
    ).all()
    return jsonify([{
        'id': q.id,
        'text': q.text,
        'comment': q.comment,
        'created_at': q.created_at.strftime('%d.%m.%Y %H:%M')
    } for q in questions])

@app.route('/api/questions', methods=['POST'])
def add_question():
    data = request.json
    if not data.get('text'):
        return jsonify({'error': 'Текст вопроса обязателен'}), 400
    q = StupidQuestion(
        text=data['text'],
        comment=data.get('comment', '')
    )
    db.session.add(q)
    db.session.commit()
    return jsonify({'id': q.id, 'message': 'Вопрос добавлен'}), 201

@app.route('/api/questions/<int:qid>', methods=['DELETE'])
def delete_question(qid):
    q = StupidQuestion.query.get_or_404(qid)
    db.session.delete(q)
    db.session.commit()
    return jsonify({'message': 'Удалено'})

# ── Сериалы ──

@app.route('/api/series', methods=['GET'])
def get_series():
    series = SeriesWatch.query.order_by(
        SeriesWatch.watched_at.desc()
    ).all()
    return jsonify([{
        'id': s.id,
        'series_name': s.series_name,
        'episode': s.episode,
        'duration_minutes': s.duration_minutes,
        'comment': s.comment,
        'watched_at': s.watched_at.strftime('%d.%m.%Y %H:%M')
    } for s in series])

@app.route('/api/series', methods=['POST'])
def add_series():
    data = request.json
    if not data.get('series_name'):
        return jsonify({'error': 'Название сериала обязательно'}), 400
    s = SeriesWatch(
        series_name=data['series_name'],
        episode=data.get('episode', ''),
        duration_minutes=int(data.get('duration_minutes', 0)),
        comment=data.get('comment', '')
    )
    db.session.add(s)
    db.session.commit()
    return jsonify({'id': s.id, 'message': 'Запись добавлена'}), 201

@app.route('/api/series/<int:sid>', methods=['DELETE'])
def delete_series(sid):
    s = SeriesWatch.query.get_or_404(sid)
    db.session.delete(s)
    db.session.commit()
    return jsonify({'message': 'Удалено'})

# ── Флешки ──

@app.route('/api/flashdrives', methods=['GET'])
def get_flashdrives():
    items = BrokenFlashdrive.query.order_by(
        BrokenFlashdrive.broken_at.desc()
    ).all()
    return jsonify([{
        'id': f.id,
        'description': f.description,
        'comment': f.comment,
        'broken_at': f.broken_at.strftime('%d.%m.%Y %H:%M')
    } for f in items])

@app.route('/api/flashdrives', methods=['POST'])
def add_flashdrive():
    data = request.json
    f = BrokenFlashdrive(
        description=data.get('description', ''),
        comment=data.get('comment', '')
    )
    db.session.add(f)
    db.session.commit()
    return jsonify({'id': f.id, 'message': 'Зафиксировано'}), 201

@app.route('/api/flashdrives/<int:fid>', methods=['DELETE'])
def delete_flashdrive(fid):
    f = BrokenFlashdrive.query.get_or_404(fid)
    db.session.delete(f)
    db.session.commit()
    return jsonify({'message': 'Удалено'})

# ── Статистика ──

@app.route('/api/stats', methods=['GET'])
def get_stats():
    total_q = StupidQuestion.query.count()
    total_s = SeriesWatch.query.count()
    total_f = BrokenFlashdrive.query.count()
    total_min = db.session.query(
        db.func.sum(SeriesWatch.duration_minutes)
    ).scalar() or 0

    # Топ сериалов
    top_series = db.session.query(
        SeriesWatch.series_name,
        db.func.count(SeriesWatch.id).label('cnt'),
        db.func.sum(SeriesWatch.duration_minutes).label('mins')
    ).group_by(SeriesWatch.series_name)\
     .order_by(db.func.count(SeriesWatch.id).desc())\
     .limit(5).all()

    return jsonify({
        'total_questions': total_q,
        'total_series': total_s,
        'total_flashdrives': total_f,
        'total_minutes': total_min,
        'total_hours': round(total_min / 60, 1),
        'top_series': [
            {'name': r.series_name, 'count': r.cnt, 'minutes': r.mins or 0}
            for r in top_series
        ]
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
