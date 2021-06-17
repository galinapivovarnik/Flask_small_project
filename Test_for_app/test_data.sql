INSERT INTO user (username, password)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');


INSERT INTO tests (test_name, status, user_id, test_date)
VALUES
  ('test_name_1', 'saved', (SELECT id FROM user WHERE username='test' LIMIT 1), date("now")),
  ('test_name_2', 'saved', (SELECT id FROM user WHERE username='test' LIMIT 1), date("now")),
  ('test_name_3', 'saved', (SELECT id FROM user WHERE username='test' LIMIT 1), date("now")),
  ('test_name_4', 'saved', (SELECT id FROM user WHERE username='test' LIMIT 1), date("now")),
  ('test_name_5', 'saved', (SELECT id FROM user WHERE username='other' LIMIT 1), date("now")),
  ('test_name_6', 'saved', (SELECT id FROM user WHERE username='other' LIMIT 1), date("now")),
  ('test_name_7', 'saved', (SELECT id FROM user WHERE username='other' LIMIT 1), date("now")),
  ('test_name_8', 'saved', (SELECT id FROM user WHERE username='other' LIMIT 1), date("now"));


INSERT INTO questions (question, test_id)
VALUES
  ('What is the weather like outside 1.1?', (SELECT test_id FROM tests WHERE test_name='test_name_1' LIMIT 1)),
  ('What is the weather like outside 1.2?', (SELECT test_id FROM tests WHERE test_name='test_name_1' LIMIT 1)),
  ('What is the weather like outside 2.1?', (SELECT test_id FROM tests WHERE test_name='test_name_2' LIMIT 1)),
  ('What is the weather like outside 2.2?', (SELECT test_id FROM tests WHERE test_name='test_name_2' LIMIT 1)),
  ('What is the weather like outside 3.1?', (SELECT test_id FROM tests WHERE test_name='test_name_3' LIMIT 1)),
  ('What is the weather like outside 3.2?', (SELECT test_id FROM tests WHERE test_name='test_name_3' LIMIT 1)),
  ('What is the weather like outside 4.1?', (SELECT test_id FROM tests WHERE test_name='test_name_4' LIMIT 1)),
  ('What is the weather like outside 4.2?', (SELECT test_id FROM tests WHERE test_name='test_name_4' LIMIT 1)),
  ('What is the weather like outside 5.1?', (SELECT test_id FROM tests WHERE test_name='test_name_5' LIMIT 1)),
  ('What is the weather like outside 5.2?', (SELECT test_id FROM tests WHERE test_name='test_name_5' LIMIT 1)),
  ('What is the weather like outside 6.1?', (SELECT test_id FROM tests WHERE test_name='test_name_6' LIMIT 1)),
  ('What is the weather like outside 6.2?', (SELECT test_id FROM tests WHERE test_name='test_name_6' LIMIT 1)),
  ('What is the weather like outside 7.1?', (SELECT test_id FROM tests WHERE test_name='test_name_7' LIMIT 1)),
  ('What is the weather like outside 7.2?', (SELECT test_id FROM tests WHERE test_name='test_name_7' LIMIT 1)),
  ('What is the weather like outside 8.1?', (SELECT test_id FROM tests WHERE test_name='test_name_8' LIMIT 1)),
  ('What is the weather like outside 8.2?', (SELECT test_id FROM tests WHERE test_name='test_name_8' LIMIT 1));


INSERT INTO answers (answer, answer_mark, question_id)
VALUES
('Sunny', 1, (SELECT question_id FROM questions WHERE question='What is the weather like outside 1.1?' LIMIT 1)),
  ('Rainy', 0, (SELECT question_id FROM questions WHERE question='What is the weather like outside 1.1?' LIMIT 1)),
('Sunny', 1, (SELECT question_id FROM questions WHERE question='What is the weather like outside 1.2?' LIMIT 1)),
  ('Rainy', 0, (SELECT question_id FROM questions WHERE question='What is the weather like outside 1.2?' LIMIT 1)),
('Sunny', 1, (SELECT question_id FROM questions WHERE question='What is the weather like outside 2.1?' LIMIT 1)),
  ('Rainy', 0, (SELECT question_id FROM questions WHERE question='What is the weather like outside 2.1?' LIMIT 1)),
('Sunny', 1, (SELECT question_id FROM questions WHERE question='What is the weather like outside 2.2?' LIMIT 1)),
  ('Rainy', 0, (SELECT question_id FROM questions WHERE question='What is the weather like outside 2.2?' LIMIT 1)),
('Sunny', 1, (SELECT question_id FROM questions WHERE question='What is the weather like outside 3.1?' LIMIT 1)),
  ('Rainy', 0, (SELECT question_id FROM questions WHERE question='What is the weather like outside 3.1?' LIMIT 1)),
('Sunny', 1, (SELECT question_id FROM questions WHERE question='What is the weather like outside 3.2?' LIMIT 1)),
  ('Rainy', 0, (SELECT question_id FROM questions WHERE question='What is the weather like outside 3.2?' LIMIT 1)),
('Sunny', 1, (SELECT question_id FROM questions WHERE question='What is the weather like outside 4.1?' LIMIT 1)),
  ('Rainy', 0, (SELECT question_id FROM questions WHERE question='What is the weather like outside 4.1?' LIMIT 1)),
('Sunny', 1, (SELECT question_id FROM questions WHERE question='What is the weather like outside 4.2?' LIMIT 1)),
  ('Rainy', 0, (SELECT question_id FROM questions WHERE question='What is the weather like outside 4.2?' LIMIT 1)),
('Sunny', 1, (SELECT question_id FROM questions WHERE question='What is the weather like outside 5.1?' LIMIT 1)),
  ('Rainy', 0, (SELECT question_id FROM questions WHERE question='What is the weather like outside 5.1?' LIMIT 1)),
('Sunny', 1, (SELECT question_id FROM questions WHERE question='What is the weather like outside 5.2?' LIMIT 1)),
  ('Rainy', 0, (SELECT question_id FROM questions WHERE question='What is the weather like outside 5.2?' LIMIT 1)),
('Sunny', 1, (SELECT question_id FROM questions WHERE question='What is the weather like outside 6.1?' LIMIT 1)),
  ('Rainy', 0, (SELECT question_id FROM questions WHERE question='What is the weather like outside 6.1?' LIMIT 1)),
('Sunny', 1, (SELECT question_id FROM questions WHERE question='What is the weather like outside 6.2?' LIMIT 1)),
  ('Rainy', 0, (SELECT question_id FROM questions WHERE question='What is the weather like outside 6.2?' LIMIT 1)),
('Sunny', 1, (SELECT question_id FROM questions WHERE question='What is the weather like outside 7.1?' LIMIT 1)),
  ('Rainy', 0, (SELECT question_id FROM questions WHERE question='What is the weather like outside 7.1?' LIMIT 1)),
('Sunny', 1, (SELECT question_id FROM questions WHERE question='What is the weather like outside 7.2?' LIMIT 1)),
  ('Rainy', 0, (SELECT question_id FROM questions WHERE question='What is the weather like outside 7.2?' LIMIT 1)),
('Sunny', 1, (SELECT question_id FROM questions WHERE question='What is the weather like outside 8.1?' LIMIT 1)),
  ('Rainy', 0, (SELECT question_id FROM questions WHERE question='What is the weather like outside 8.1?' LIMIT 1)),
('Sunny', 1, (SELECT question_id FROM questions WHERE question='What is the weather like outside 8.2?' LIMIT 1)),
  ('Rainy', 0, (SELECT question_id FROM questions WHERE question='What is the weather like outside 8.2?' LIMIT 1));
