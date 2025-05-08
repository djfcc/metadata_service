INSERT INTO company
(name)
VALUES('devcompany'),
	  ('testcompany');

INSERT INTO user
(name, email, company_id)
VALUES('devuser', 'devuser@fake.com', 1),
	  ('testuser', 'testuser@fake.com', 2);

INSERT INTO team
(name, company_id, description)
VALUES('devteam', 1, 'devteam description'),
	  ('testteam', 2, 'testteam description');

INSERT INTO team_members
(user_id, team_id)
VALUES(1, 1),
	  (2, 2);

INSERT INTO resource
(name, type, lifecycle_status, description, owner)
VALUES('devresource', 'devtype', 'active', 'devresource description', 1),
	  ('testresource', 'testtype', 'inactive', 'testresource description', 2);