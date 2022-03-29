# MySQL DB Creation script, to run on an instance of MYSQL (WAMP for example)
# username : isiblog | pwd : isiblog
# schema : dbisiblog
# table : comments

CREATE DATABASE IF NOT EXISTS dbisiblog;

# DROP TABLE dbisiblog.comments;
CREATE TABLE IF NOT EXISTS dbisiblog.comments (
	id INT PRIMARY KEY NOT NULL,
    auteur VARCHAR(50),
    titre VARCHAR(100),
    contenu TEXT,
    dateCreation VARCHAR(50));

TRUNCATE dbisiblog.comments;

# INSERT INTO dbisiblog.comments VALUES(0, '', ' quote', '', date_format(sysdate(), '%Y/%m/%d %T'));
INSERT INTO dbisiblog.comments VALUES(0, 'Nelson Mandela', 'Nelson Mandela quote', 'The greatest glory in living lies not in never falling, but in rising every time we fall.', date_format(sysdate(), '%Y/%m/%d %T'));
INSERT INTO dbisiblog.comments VALUES(1, 'Walt Disney', 'Walt Disney quote', 'The way to get started is to quit talking and begin doing.', date_format(sysdate(), '%Y/%m/%d %T'));
INSERT INTO dbisiblog.comments VALUES(2, 'Steve Jobs', 'Steve Jobs quote', 'Your time is limited, so don''t waste it living someone else''s life. Don''t be trapped by dogma – which is living with the results of other people''s thinking.', date_format(sysdate(), '%Y/%m/%d %T'));
INSERT INTO dbisiblog.comments VALUES(3, 'Eleanor Roosevelt', 'Eleanor Roosevelt quote', 'If life were predictable it would cease to be life, and be without flavor.', date_format(sysdate(), '%Y/%m/%d %T'));
INSERT INTO dbisiblog.comments VALUES(4, 'Oprah Winfrey', 'Oprah Winfrey quote', 'If you look at what you have in life, you''ll always have more. If you look at what you don''t have in life, you''ll never have enough.', date_format(sysdate(), '%Y/%m/%d %T'));
INSERT INTO dbisiblog.comments VALUES(5, 'James Cameron', 'James Cameron quote', 'If you set your goals ridiculously high and it''s a failure, you will fail above everyone else''s success.', date_format(sysdate(), '%Y/%m/%d %T'));
INSERT INTO dbisiblog.comments VALUES(6, 'John Lennon', 'John Lennon quote', 'Life is what happens when you''re busy making other plans.', date_format(sysdate(), '%Y/%m/%d %T'));

SELECT * FROM dbisiblog.comments;