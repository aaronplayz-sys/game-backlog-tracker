-- Platforms
INSERT INTO platforms (name, manufacturer) VALUES ('PC', 'Various');
INSERT INTO platforms (name, manufacturer) VALUES ('PlayStation 5', 'Sony');
INSERT INTO platforms (name, manufacturer) VALUES ('Xbox Series X', 'Microsoft');
INSERT INTO platforms (name, manufacturer) VALUES ('Nintendo Switch', 'Nintendo');

-- Games (platform_id matches insertion order above: PC=1, PS5=2, XSX=3, Switch=4)
INSERT INTO games (title, genre, platform_id, release_year) VALUES ('Cyberpunk 2077', 'RPG', 1, 2020);
INSERT INTO games (title, genre, platform_id, release_year) VALUES ('Elden Ring', 'Action RPG', 1, 2022);
INSERT INTO games (title, genre, platform_id, release_year) VALUES ('Baldurs Gate 3', 'RPG', 1, 2023);
INSERT INTO games (title, genre, platform_id, release_year) VALUES ('Half-Life Alyx', 'FPS', 1, 2020);
INSERT INTO games (title, genre, platform_id, release_year) VALUES ('God of War Ragnarok', 'Action Adventure', 2, 2022);
INSERT INTO games (title, genre, platform_id, release_year) VALUES ('Spider-Man 2', 'Action Adventure', 2, 2023);
INSERT INTO games (title, genre, platform_id, release_year) VALUES ('Final Fantasy XVI', 'Action RPG', 2, 2023);
INSERT INTO games (title, genre, platform_id, release_year) VALUES ('Demon Souls Remake', 'Action RPG', 2, 2020);
INSERT INTO games (title, genre, platform_id, release_year) VALUES ('Halo Infinite', 'FPS', 3, 2021);
INSERT INTO games (title, genre, platform_id, release_year) VALUES ('Forza Horizon 5', 'Racing', 3, 2021);
INSERT INTO games (title, genre, platform_id, release_year) VALUES ('The Legend of Zelda Tears of the Kingdom', 'Action Adventure', 4, 2023);
INSERT INTO games (title, genre, platform_id, release_year) VALUES ('Metroid Dread', 'Action', 4, 2021);
INSERT INTO games (title, genre, platform_id, release_year) VALUES ('Fire Emblem Engage', 'Strategy RPG', 4, 2023);

-- Backlog Entries
INSERT INTO backlog_entries (game_id, status, personal_rating, hours_played, notes) VALUES (1, 'Completed', 9, 85.5, 'Great story after the patches');
INSERT INTO backlog_entries (game_id, status, personal_rating, hours_played, notes) VALUES (2, 'Completed', 10, 120.0, 'Best Soulslike ever made');
INSERT INTO backlog_entries (game_id, status, personal_rating, hours_played, notes) VALUES (3, 'Playing', NULL, 40.0, 'On Act 2, taking my time');
INSERT INTO backlog_entries (game_id, status, personal_rating, hours_played, notes) VALUES (4, 'Backlog', NULL, 0.0, 'Need a VR headset first');
INSERT INTO backlog_entries (game_id, status, personal_rating, hours_played, notes) VALUES (5, 'Completed', 10, 55.0, 'Incredible end to Kratos arc');
INSERT INTO backlog_entries (game_id, status, personal_rating, hours_played, notes) VALUES (6, 'Completed', 9, 30.0, 'Fun but shorter than expected');
INSERT INTO backlog_entries (game_id, status, personal_rating, hours_played, notes) VALUES (7, 'Dropped', 6, 15.0, 'Not for me, too button mashy');
INSERT INTO backlog_entries (game_id, status, personal_rating, hours_played, notes) VALUES (8, 'Backlog', NULL, 0.0, 'Heard it is brutally hard');
INSERT INTO backlog_entries (game_id, status, personal_rating, hours_played, notes) VALUES (9, 'Completed', 8, 45.0, 'Campaign was short but fun');
INSERT INTO backlog_entries (game_id, status, personal_rating, hours_played, notes) VALUES (10, 'Playing', NULL, 20.0, 'Great chill driving game');
INSERT INTO backlog_entries (game_id, status, personal_rating, hours_played, notes) VALUES (11, 'Completed', 10, 95.0, 'Masterpiece, one of the best ever');
INSERT INTO backlog_entries (game_id, status, personal_rating, hours_played, notes) VALUES (12, 'Completed', 9, 12.0, 'Tight and polished metroidvania');
INSERT INTO backlog_entries (game_id, status, personal_rating, hours_played, notes) VALUES (13, 'Backlog', NULL, 0.0, 'Christmas gift, havent started yet');