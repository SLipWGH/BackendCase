insert into users_table (id, username, prefered_language)
values
(gen_random_uuid(),'Пользователь 1', 'Русский'),
(gen_random_uuid(), 'Пользователь 2', 'Русский'),
(gen_random_uuid(), 'User 1', 'English'),
(gen_random_uuid(), 'User 2', 'English'),
(gen_random_uuid(), 'NewUser', 'English'),
(gen_random_uuid(), 'ОхотникЗаДостижениями132','Русский'),
(gen_random_uuid(), 'LazyGuy451','English'),
(gen_random_uuid(), 'HighwayKing371', 'English');

--Заполнение достижений
insert into achievements_table (name, value, description)
values
('Добро пожаловать!', 10, '{"Русский":"Вы зарегистрировались в системе", "English": "You have registered in the system"}'),
('Тут есть достижения?', 20, '{"Русский":"Вы посмотрели свою статистику", "English": "You have looked at your statistics"}'),
('Соскучились?)', 20, '{"Русский":"Вы заходили 3 дня подряд", "English": "You have logged in 3 days in a row"}'),
('Вперед, к вершинам!', 10, '{"Русский":"Вы посмотрели статистику других участников", "English": "You have viewed the statistics of other participants"}'),
('Around the world', 10, '{"Русский":"Вы сменили свой язык в настройках", "English": "You have changed your language in the settings"}'),
('Первые шаги!', 20, '{"Русский":"Вы заработали 5 достижений", "English": "You have earned 5 achievements_table"}'),
('100!', 20, '{"Русский":"Вы заработали 100 очков", "English": "You have earned 100 points"}'),
('Топ-10', 30, '{"Русский":"Вы оказались в топ-10 участников по очкам", "English": "You are in the top 10 participants by points"}'),
('Топ-3', 50, '{"Русский":"Вы оказались в топ-3 участникво по очкам", "English": "You are in the top 10 participants by points"}'),
('Топ-1', 100, '{"Русский":"Вы стали лучшим участником в ситеме", "English": "You have become the best participant in the system"}'),
('Secret...', 60, '{"Русский":"Секрет...", "English": "Secret..."}');
--Присвоение достижений пользователям
insert into users_achievements_table (user_id, achievement_name, date)
select users_table.id, achievements_table.name, '2020-04-01'
from users_table, achievements_table
where achievements_table.name in ('Добро пожаловать!', 'Тут есть достижения?', 'Соскучились?)');

insert into users_achievements_table (user_id, achievement_name, date)
select users_table.id, achievements_table.name, '2020-04-10'
from users_table, achievements_table
where achievements_table.name in ('Вперед, к вершинам!')
and users_table.username in ('User 1', 'User 2', 'HighwayKing371');

insert into users_achievements_table (user_id, achievement_name, date)
select users_table.id, achievements_table.name, '2023-05-09'
from users_table, achievements_table
where users_table.username = 'HighwayKing371'
and achievements_table.name = 'Around the world';

insert into users_achievements_table (user_id, achievement_name, date)
select users_table.id, achievements_table.name, '2023-05-10'
from users_table, achievements_table
where users_table.username = 'HighwayKing371'
and achievements_table.name = 'Первые шаги!';

insert into users_achievements_table (user_id, achievement_name, date)
select users_table.id, achievements_table.name, '2023-05-11'
from users_table, achievements_table
where users_table.username = 'HighwayKing371'
and achievements_table.name = '100!';

insert into users_achievements_table (user_id, achievement_name, date)
select users_table.id, achievements_table.name, '2023-05-12'
from users_table, achievements_table
where users_table.username = 'HighwayKing371'
and achievements_table.name = 'Топ-10';

insert into users_achievements_table (user_id, achievement_name, date)
select users_table.id, achievements_table.name, '2023-05-13'
from users_table, achievements_table
where users_table.username = 'HighwayKing371'
and achievements_table.name = 'Топ-3';

insert into users_achievements_table (user_id, achievement_name, date)
select users_table.id, achievements_table.name, '2023-05-14'
from users_table, achievements_table
where users_table.username = 'HighwayKing371'
and achievements_table.name = 'Топ-1';

insert into users_achievements_table (user_id, achievement_name, date)
select users_table.id, achievements_table.name, '2023-05-15'
from users_table, achievements_table
where users_table.username = 'HighwayKing371'
and achievements_table.name = 'Secret...';