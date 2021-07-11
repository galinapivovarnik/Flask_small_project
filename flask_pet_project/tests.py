import functools
from flask import Blueprint, render_template, url_for, request, flash, redirect, session
from . import dbase

bp = Blueprint('tests', __name__)


def login_required(func):
    """Decorator for ability to create and pass the tests, if not logged in"""

    @functools.wraps(func)
    def wrap(*args, **kwargs):
        try:
            if session['user_id']:
                return func(*args, **kwargs)
            return redirect(url_for('auth.login'))
        except KeyError:
            print('Key Error')
            return redirect(url_for('auth.login'))
    return wrap


@bp.route('/creating_tests', methods=('GET', 'POST'))
@login_required
def create_tests():
    """Function for creating title of test and numbers of questions & answers"""

    db = dbase.get_db()
    if request.method == 'POST':
        test_title = request.form['test_title']
        test_q_count = request.form['test_q_count']
        test_a_count = request.form['test_a_count']

        # Set up the error variable for flash message:
        error = None
        if not test_title:
            error = 'Title is required.'
        elif not test_q_count:
            error = 'Count of questions is required.'
        elif test_q_count:
            try:
                int(test_q_count)
            except ValueError:
                error = 'Only integers are allowed.'

        if not test_a_count:
            error = 'Count of answers is required.'
        elif test_a_count:
            try:
                int(test_a_count)
            except ValueError:
                error = 'Only integers are allowed.'
        elif db.cursor().execute('SELECT test_name from tests WHERE test_name=?', (test_title,)).fetchone() is not None:
            error = f'Test with title "{test_title}" is already exist.'

        # Saving data to the DB:
        if error is None:
            db.cursor().execute('INSERT INTO tests(test_name, status, user_id, test_date) VALUES (?,?,?,?)',
                                (test_title, 'incomplete', session['user_id'], 'date'))
            db.commit()
            session['test_id'] = (db.cursor().execute('SELECT * FROM tests WHERE test_name = ?',
                                                      (test_title,)).fetchone())['test_id']
            session['test_q_count'] = test_q_count
            session['test_a_count'] = test_a_count
            return redirect(url_for('.create_tests_2'))
        flash(error)

    session['test_id'] = None
    db.cursor().execute('DELETE FROM tests WHERE status=?', ('incomplete',))
    db.commit()
    return render_template('test_settings.html')


@bp.route('/creating_tests/q_a', methods=('GET', 'POST'))
def create_tests_2():
    """Function for continue creating test. User have to write down the questions and answers for each,
    also user have to check all right answers."""

    q = int(session['test_q_count'])
    a = int(session['test_a_count'])
    if request.method == 'POST':
        db = dbase.get_db()

        # Set up the error variable for flash message:
        error = None
        for i in range(q):
            if not request.form[f'question{i+1}']:
                error = f'You didn\'t specify question {i+1}.'
        for it in range(a*q):
            if not request.form[f'answer{it+1}']:
                error = f'You didn\'t fill some answer field.'

        # Checking if at least one answer for every question block are marked as correct:
        for i in range(q):
            exc_count = 0
            for it in range(a):
                try:
                    request.form[f'check_correct_answer_{(it+1)+(a*i)}']
                except KeyError:
                    exc_count += 1
                    if exc_count == a:
                        error = f'At least one answer for the question should be checked as "correct".'
                        break

        # Saving data to the DB (tables: tests, questions, answers):
        if error is None:
            for i_1 in range(q):
                db.cursor().execute('INSERT INTO questions(question, test_id) VALUES (?, ?)',
                                    (request.form[f'question{i_1+1}'], session['test_id']))
                question_ids = db.cursor().execute('SELECT * FROM questions ORDER BY question_id '
                                                   'DESC LIMIT 1').fetchone()['question_id']
                for it_1 in range(a):
                    try:
                        if request.form[f'check_correct_answer_{(it_1 + 1) + (a * i_1)}']:
                            db.cursor().execute('INSERT INTO answers(answer, answer_mark, question_id) '
                                                'VALUES (?, ?, ?)',
                                                (request.form[f'answer{(it_1+1)+(a*i_1)}'], 1, question_ids))
                    except KeyError:
                        db.cursor().execute('INSERT INTO answers(answer, answer_mark, question_id) VALUES (?, ?, ?)',
                                            (request.form[f'answer{(it_1 + 1) + (a * i_1)}'], 0,
                                             question_ids))
            db.cursor().execute('UPDATE tests SET status=? WHERE test_id=?', ('saved', session['test_id']))
            db.cursor().execute('UPDATE tests SET test_date=date("now") WHERE test_id=?', (session['test_id'],))
            db.commit()

            return redirect(url_for('.all_tests'))
    return render_template('creating_tests.html', qu_count=q, an_count=a)


@bp.route('/all_tests', methods=('GET', 'POST'))
def all_tests():
    """Function for depicting all existed tests from db. User able to select test for passing
    and also able to delete tests which were created only by current user."""

    db = dbase.get_db()
    db.cursor().execute('DELETE FROM tests WHERE status=?', ('incomplete',))
    db.commit()
    tests_ = db.cursor().execute(
        'SELECT test_id, test_name, user_id, test_date FROM tests WHERE status=? ORDER BY test_id DESC',
        ('saved',)).fetchall()

    if request.method == 'POST':
        # POST-method is for deleting the tests by author
        # Firstly, checking if the ids don't repeat:
        id_for_check = []
        for i in tests_:
            id__ = [i['test_id']][0]
            print(f'Test_id: {id__}')
            if id__ in id_for_check:
                continue
            else:
                id_for_check.append(id__)

            # Deleting correspond test with it's questions and answers:
            try:
                requ_form = int(request.form[f"delete_test_{id__}"])
                print(f'requ_form: {requ_form}')
                if request.form[f'delete_test_{id__}']:
                    print(f'id for delete: {id__}')
                    db.cursor().execute('DELETE FROM tests WHERE test_id=?', (id__,))
                    qu_id_list_for_delete = db.cursor().execute('SELECT question_id FROM questions '
                                                                'WHERE test_id=?', (id__,)).fetchall()
                    for ids in qu_id_list_for_delete:
                        ids__ = [ids['question_id']][0]
                        print(f'ids__ = {ids__}')
                        db.cursor().execute('DELETE FROM answers WHERE question_id=?', (ids__,))
                    db.cursor().execute('DELETE FROM questions WHERE test_id=?', (id__,))
                    db.commit()
            except KeyError:
                pass

        return redirect(url_for('.all_tests'))

    names_ = {}
    for i in tests_:
        id_ = [i['user_id']][0]
        name = db.cursor().execute('SELECT id, username FROM user WHERE id=?', (id_,)).fetchone()['username']
        names_.update({id_: name})
    return render_template('all_tests.html', tests=tests_, names=names_)


@bp.route('/all_tests/<test_id>', methods=('GET', 'POST'))
@login_required
def test_var(test_id):
    """Function for passing selected test. If method == 'POST' - user will be redirected to result-page."""

    # Page for passing chosen test
    db = dbase.get_db()
    test_name_ = db.cursor().execute('SELECT * FROM tests WHERE test_id=?', (test_id,)).fetchone()['test_name']
    questions_ = db.cursor().execute('SELECT question FROM questions WHERE test_id=?', (test_id,)).fetchall()
    questions_id = db.cursor().execute('SELECT question_id FROM questions WHERE test_id=?', (test_id,)).fetchall()
    question_num = len([i for i in questions_])
    answers_ = []
    for id_ in questions_id:
        for ids in id_:
            answers_.append(db.cursor().execute('SELECT * FROM answers WHERE question_id=?', (ids,)).fetchall())

    q = question_num
    a = len(answers_[0])

    if request.method == 'POST':
        error = None
        for i in range(q):
            exc_count = 0
            for it in range(a):
                try:
                    request.form[f'check_correct_answer_{(it+1)+(a*i)}']
                except KeyError:
                    exc_count += 1
                    if exc_count == a:
                        error = f'At least one answer for the question should be checked.'
                        break
        if error is not None:
            flash(error)

        # Checking number of correct answers:
        if error is None:
            total_correct_answers = 0
            num_of_user_correct_answers = 0
            num_of_user_incorrect_answers = 0
            for i in range(q):
                for it in range(a):
                    if answers_[i][it]['answer_mark'] == 1:
                        total_correct_answers += 1
                    try:
                        if request.form[f'check_correct_answer_{it+1 + a*i}']:
                            if answers_[i][it]['answer_mark'] == 1:
                                num_of_user_correct_answers += 1
                            elif answers_[i][it]['answer_mark'] == 0:
                                num_of_user_incorrect_answers += 1
                    except KeyError:
                        pass

            session['correct_answer_interest'] = (num_of_user_correct_answers * 100) // total_correct_answers
            session['incorrect_user_answer_num'] = num_of_user_incorrect_answers
            return redirect(url_for('.test_results', test_id=test_id))
    return render_template('passing_a_test.html', title='Test yourself!', test_name_=test_name_,
                           question_num=question_num, questions=questions_, answer_num=a, answers=answers_)


@bp.route('/results/<test_id>')
def test_results(test_id):
    """This function select the result of just passed test by current user."""

    # Page for selecting the result of testing
    return render_template('test_results.html', interest=session['correct_answer_interest'],
                           incorrect_a=session['incorrect_user_answer_num'], test_id_=test_id)
