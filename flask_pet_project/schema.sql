CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tests (
    test_id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_name TEXT UNIQUE NOT NULL,
    status TEXT INTEGER NOT NULL,
    user_id TEXT INTEGER NOT NULL,
    test_date TEXT,
    FOREIGN KEY (user_id) REFERENCES user (id)
);


CREATE TABLE IF NOT EXISTS questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    test_id INTEGER NOT NULL,
    FOREIGN KEY (test_id) REFERENCES tests (test_id)
);

CREATE TABLE IF NOT EXISTS answers (
    answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    answer TEXT NOT NULL,
    answer_mark INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    FOREIGN KEY (question_id) REFERENCES tests (answer_id)
);
