

INSERT INTO lt_license VALUES (1, 'GNU AGPLv3', 'GNU Affero General Public License v3.0', ' GNU AFFERO GENERAL PUBLIC LICENSE Version 3, 19 November 2007 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/> Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed....', 'https://www.gnu.org/licenses/agpl-3.0.de.html', true, true, true, false, current_timestamp, current_timestamp),
                              (2, 'MIT License ', 'MIT License', 'MIT License Copyright (c) [year] [fullname] Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction,....', 'http://gamelab.mit.edu/eula/slower_eula_win.php', true, true, true, false, current_timestamp, current_timestamp),
                              (3, 'Beerware', 'THE BEER-WARE LICENSE', '"THE BEER-WARE LICENSE" (Revision 42): * <phk@FreeBSD.ORG> wrote this file. As long as you retain this notice you * can do whatever you want with this stuff. If we meet some day, and you think * this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp', 'https://people.freebsd.org/~phk/', true, true, true, false, current_timestamp, current_timestamp);
INSERT INTO lt_location VALUES (1, 8.060316, 50.432044, 4326, 'POINT', current_timestamp, current_timestamp, ST_GeomFromText('POINT(8.060316 50.432044)', 4326)),
                               (2, 8.06, 49.432, 4326, 'POINT', current_timestamp, current_timestamp, ST_GeomFromText('POINT(8.06 49.432)', 4326)),
                               (3, 1001875.42, 6274861.39, 3857, 'POINT', current_timestamp, current_timestamp, ST_GeomFromText('POINT(1001875.42 6274861.39)', 3857)),
                               (4, 9, 49, 4326, 'POINT', current_timestamp, current_timestamp, ST_GeomFromText('POINT(9 49)', 4326));
INSERT INTO lt_user VALUES (1, true, 'Hanna', 'Froh', 'school of waldorf', 'tree class', 'hanna@hat.se', 'the cutest flower in the pond', current_timestamp, current_timestamp),
                           (2, false, 'Elvis', 'Jackson', null, null, 'elvis@hea.vy', 'Likes no music', current_timestamp, current_timestamp),
                           (3, true, 'Will', 'ma', 'Paris school of arts', 'wodka drawing', 'blue@mad.gov', null, current_timestamp, current_timestamp),
                           (4, false, 'nerd', 'lily', null, null, 'red@hat.nw', null, current_timestamp, current_timestamp);
INSERT INTO lt_project VALUES (1, 'Vforwater', 1, current_timestamp, current_timestamp),
                              (2, 'polariq', 2, current_timestamp, current_timestamp),
                              (3, 'schnuffel', 2, current_timestamp, current_timestamp);
INSERT INTO lt_quality VALUES (1, 'bad', 1, current_timestamp, current_timestamp),
                              (2, 'not bad', 2, current_timestamp, current_timestamp),
                              (3, 'well', 2, current_timestamp, current_timestamp);
INSERT INTO lt_site VALUES (1, 'Mt Eddie', 3501.2, 78.74, null, 0.4, 'grasland', 'The place to be for getting samples', current_timestamp, current_timestamp),
                           (2, 'the cave', null, -222, 34, null, 0, 'you might need a torch', current_timestamp, current_timestamp),
                           (3, 'zuse-z3', 2, null, null, 0.01, 'treeland', 'sample temple', current_timestamp, current_timestamp);
INSERT INTO lt_soil VALUES (1, 'marl', null, null, null, null, current_timestamp, current_timestamp),
                           (2, 'gneiss', 'volcanic soil', null, null, null, current_timestamp, current_timestamp),
                           (3, 'sand', 'peat', null, null, null, current_timestamp, current_timestamp);
INSERT INTO lt_source_type VALUES (1, 'file path', current_timestamp, current_timestamp),
                                  (2, 'file url', current_timestamp, current_timestamp),
                                  (3, 'wms', current_timestamp, current_timestamp);
INSERT INTO lt_unit VALUES (1, 'centigrade', 'deg. C', 'C', false, null, null, null),
                           (2, 'percent', 'pct', '%', false, null, null, null),
                           (3, 'milibar', 'mbar', 'mbar', false, null, null, null),
                           (4, 'meter', 'm', 'm', false, null, null, null),
                           (5, 'velocity', 'm/s', 'm/s', false, null, null, null),
                           (6, 'hour', 'hr', 'h', false, null, null, null);
INSERT INTO tbl_data_source VALUES (1, 1, 'tbl_data', null, null, null);
INSERT INTO tbl_variable VALUES (1, 'air temperature', 'T', 'T', 1, null, null),
                                (2, 'realtive humidity', 'rel. rH', 'rH', 2, null, null),
                                (3, 'air pressure', 'p', 'p', 3, null, null),
                                (4, 'precipitation', 'R', 'R', 4, null, null),
                                (5, 'terrain height', 'H.ü. NN', 'H', 4, null, null),
                                (6, 'water content', 'Theta', 'Th', 2, null, null),
                                (7, 'saturation', 'Sw', 'Sw', 2, null, null),
                                (8, 'wind direction', 'D', 'D', 1 , null, null),
                                (9, 'soil temperature', 'T', 'T', 1 , null, null),
                                (10, 'water temperature', 'T', 'T', 1 , null, null);
INSERT INTO tbl_sensor VALUES (1, 'Ddect', 'pauling', 'www.Dp.de'), (2, 'bob', 'blop', 'www.Dp.bb'),
                              (3, 'fjodr', 'fjeul', 'www.wan.se'), (4, 'speedo', 'Airhus', 'www.Ah.com');

INSERT INTO tbl_meta VALUES (1, null, null, null, null, '5min', 1, 2, null, null, null, 1, 1, 2, 3, null, 'Sap flow velocity measured', '2017-06-28 15:05:52', '2017-06-28 15:05:52'),
                            (2, null, null, null, null, '5min', 2, 3, 1, 2, 1, 2, 2, 2, 4, null, 'dnd - deep nose drilling', '2017-06-28 15:05:52', '2017-06-28 15:05:52'),
                            (3, null, null, null, null, '5min', 3, 4, 2, 1, 2, 1, 2, 3, 2, null, 'wiedavor', '2017-06-28 15:05:52', '2017-06-28 15:05:52'),
                            (4, null, null, null, null, '5min', 4, 1, 3, 1, 3, 3, 1, 4, 1, null, 'bigerva', '2017-06-28 15:05:52', '2017-06-28 15:05:52'),
                            (5, null, null, null, null, '5min', 1, 2, 4, 2, 1, 2, 1, 5, 1, null, 'nunima', '2017-06-28 15:05:52', '2017-06-28 15:05:52'),
                            (6, null, null, null, null, '5min', 2, 3, 1, 3, 2, 1, 2, 6, 2, null, 'hrxxxwl', '2017-06-28 15:05:52', '2017-06-28 15:05:52'),
                            (7, null, null, null, null, '5min', 3, 4, 2, 3, 3, 3, 3, 7, 3, null, 'diedeldiedüb', '2017-06-28 15:05:52', '2017-06-28 15:05:52'),
                            (8, null, null, null, null, '5min', 4, 1, 3, 2, 1, 2, 2, 8, 4, null, 'yxdocknf', '2017-06-28 15:05:52', '2017-06-28 15:05:52'),
                            (9, null, null, null, null, '15min', 4, 1, 3, 2, 1, 2, 2, 9, 3, null, 'txt here', '2017-06-28 15:05:52', '2017-06-28 15:05:52'),
                            (10, null, null, null, null, '5min', 4, 1, 3, 2, 1, 2, 2, 10, 2, null, 'fil smth in', '2017-06-28 15:05:52', '2017-06-28 15:05:52'),
                            (11, null, null, null, null, '15min', 4, 1, 3, 2, 1, 2, 2, 7, 1, null, 'need input', '2017-06-28 15:05:52', '2017-06-28 15:05:52');
