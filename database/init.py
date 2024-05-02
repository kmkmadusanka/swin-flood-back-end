import os
import mysql.connector
from mysql.connector import Error
from loguru import logger


def CreateDB():
  try:
    db = mysql.connector.connect(
      host = os.getenv("DB_HOST"),
      user = os.getenv("DB_USER"),
      password = os.getenv("DB_PASSWORD")
    )
  except Error as exception:
    logger.error(exception)
    return "Database conncection error!"

  if db.is_connected():
    cursor = db.cursor()
    cursor.execute("DROP DATABASE tip")
    cursor.execute("CREATE DATABASE tip")
    return "Database created"
  else:
    return "Database not created"
  

def CreateTables():
  db = mysql.connector.connect(
      host = os.getenv("DB_HOST"),
      user = os.getenv("DB_USER"),
      password = os.getenv("DB_PASSWORD"),
      database = os.getenv("DB_DATABASE")
    )
  cursor = db.cursor()

  cursor.execute("""CREATE TABLE IF NOT EXISTS users (
  id INT NOT NULL AUTO_INCREMENT,
  f_name VARCHAR(20),
  l_name VARCHAR(20),
  bday VARCHAR(20),
  edu_q TEXT,
  prof_q TEXT,
  email VARCHAR(50) UNIQUE,
  password VARCHAR(32),
  public_id VARCHAR(32) UNIQUE,
  user_type INT(1) DEFAULT 0 COMMENT '0-Casual, 1-Permanent, 2-Admin',
  status INT(1) DEFAULT 0 COMMENT '0-pending, 1-active, 2-deactivated',
  last_edit_on VARCHAR(10) DEFAULT(CURRENT_DATE),
  cv INT(1) DEFAULT 0,
  availability VARCHAR(15),
  PRIMARY KEY (id))""")

  cursor.execute("""CREATE TABLE IF NOT EXISTS vacancies (
  id INT NOT NULL AUTO_INCREMENT,
  public_id VARCHAR(32) UNIQUE,
  title VARCHAR(50),
  module INT(1) COMMENT 'modules table ref',
  base INT(1) DEFAULT 2 COMMENT '0-Full-time, 1-Part-time, 2-Casual',
  location VARCHAR(50),
  description TEXT,
  qualifications TEXT,
  salary VARCHAR(10) DEFAULT('Negotiable'),
  due VARCHAR(10),
  num_applicants INT(3) DEFAULT 0,
  published_by INT(2) COMMENT 'users table ref',
  publish_date VARCHAR(10) DEFAULT(CURRENT_DATE),
  last_edited_by INT(2) COMMENT 'users table ref',
  edit_date VARCHAR(10) DEFAULT(CURRENT_DATE),
  status INT(1) DEFAULT 1 COMMENT '1-live, 2-unpublished',
  PRIMARY KEY (id))""")

  cursor.execute("""CREATE TABLE IF NOT EXISTS modules (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(32) UNIQUE,
  PRIMARY KEY (id))""")

  cursor.execute("""CREATE TABLE IF NOT EXISTS applicants (
  id INT NOT NULL AUTO_INCREMENT,
  user_id INT(3),
  vacancy_id INT(3),
  date VARCHAR(10) DEFAULT(CURRENT_DATE),
  PRIMARY KEY (id),
  UNIQUE KEY (user_id, vacancy_id))""")

  cursor.close()
  db.close()
  return "Tables created"


def DropTables():
  db = mysql.connector.connect(
      host = os.getenv("DB_HOST"),
      user = os.getenv("DB_USER"),
      password = os.getenv("DB_PASSWORD"),
      database = os.getenv("DB_DATABASE")
    )
  cursor = db.cursor()
  cursor.execute("DROP TABLE users;")
  cursor.execute("DROP TABLE vacancies;")
  cursor.execute("DROP TABLE modules;")
  cursor.execute("DROP TABLE applicants;")
  db.commit()
  cursor.close()
  db.close()
  return "Tables dropped"


def TruncateTables():
  db = mysql.connector.connect(
      host = os.getenv("DB_HOST"),
      user = os.getenv("DB_USER"),
      password = os.getenv("DB_PASSWORD"),
      database = os.getenv("DB_DATABASE")
    )
  cursor = db.cursor()
  cursor.execute("TRUNCATE TABLE users;")
  cursor.execute("TRUNCATE TABLE vacancies;")
  cursor.execute("TRUNCATE TABLE applicants;")
  db.commit()
  cursor.close()
  db.close()
  return "Tables truncated"


def DummyData():
  db = mysql.connector.connect(
      host = os.getenv("DB_HOST"),
      user = os.getenv("DB_USER"),
      password = os.getenv("DB_PASSWORD"),
      database = os.getenv("DB_DATABASE")
    )
  cursor = db.cursor()

  cursor.execute("""INSERT IGNORE INTO users (f_name, email, password, public_id, user_type, status) VALUES 
  ('Dinuka', 'dinuka@corputip.me', '1146b6c258a28b28941c57851ee084a1', '94da13d942686d452842ac61adf3bad4', 1, 1),
  ('Kasun', 'kasun@corputip.me', '1146b6c258a28b28941c57851ee084a1', 'b453d1a0900d948bfa4df3437dc27eae', 1, 1),
  ('Nuwanga', 'nuwanga@corputip.me', '1146b6c258a28b28941c57851ee084a1', 'a65c350db098e3a187a8210295216354', 1, 1),
  ('Lizzie', 'lizzie@corputip.me', '1146b6c258a28b28941c57851ee084a1', '2f62964015b3db835a5d4dda15ef8245', 1, 1),
  ('Yash', 'yash@corputip.me', '1146b6c258a28b28941c57851ee084a1', '182ea55668cb81b2f0dd98bfbe3b26ea', 1, 1),
  ('Staff1', 'staff1@corputip.me', '1146b6c258a28b28941c57851ee084a1', 'ce29c11c6abede16028b9fd12642ffc7', 1, 1),
  ('User1', 'user1@corputip.me', '1146b6c258a28b28941c57851ee084a1', '385dfe8949163253ec44a73bf876ea56', 0, 1);
  """)

  cursor.execute("""INSERT IGNORE INTO modules (name) VALUES 
  ('Information Technology'),
  ('Bio Science'),
  ('Phsycology'),
  ('Nursing'),
  ('Engineering');
  """)

  cursor.execute("""INSERT IGNORE INTO vacancies (public_id, title, module, base, location, description, qualifications, published_by, last_edited_by, salary, due) VALUES 
  ('4c8a7cd5073ffe966c41e4ae7fef49d7', 'Lecturer in Nursing', 4, 1, 'Hawthorn, Victoria', 'This is an exciting opportunity for an enthusiastic and motivated Registered Nurse to join a dynamic, progressive team within the University of Tasmanias College of Health and Medicine. The College has a focus on boosting health research performance and evidence-based learning and teaching to educate a new generation of agile health professionals and researchers with capability in leadership and future-focused health care. With a strong background in nursing education this teaching intensive position will contribute to student success through the educational preparation of pre-registration and post graduate students of nursing. This position also involves health services research and/or innovation in learning and teaching that can improve the health of Tasmanians.  You will assist in developing a positive culture that enables high levels of collaboration and productivity to support the vision of the University to deliver place-based education and research with high impacts', 'Registration as a Nurse, Post graduate nursing qualifications at PhD, or Masters level, desirable, Evidence of research capabilities, Significant experience in nursing practice.', 5, 2, '$35/hr', '2023-06-30'),
  ('eee7a89a9f013f9cdd46a6e1233294b6', 'Data Science Lecturer', 1, 1, 'Adelaide', 'We currently have a fantastic opportunity to join our academic staff, within our operations Division on a half-time, temporary basis as a Data Scientist Lecturer. This role responsible for contributing to the Analysis and Modelling portfolio in the Network Planning team, developing, and implementing decision support tools to be used across Operations. We offer flexible working arrangement to enable team members to work in ways that meet their work/life commitments and support their wellbeing, ongoing training and professional development to support your growth and help you achieve your goals, 13-weeks paid parental leave that can be taken in a flexible way to suit unique family needs, corporate employee discounts including travel, health insurance funds and financial services.', 'Relevant tertiary degree in computer science, data science, data analytics, environmental science, agricultural science, or associated discipline, Minimum of 2 years of experience in a quantitative and/or data analytical role, Strong experience with quantitative modelling, Experience with Azure DevOps.', 2, 4, '$45/hr', '2023-06-30'),
  ('367ec69b31b85ceb4357646fa7f7a4d8', 'A/Professor or Professor in Bio Science', 2, 1, 'Adelaide', 'An exciting opportunity has become available for an experienced Lecturer to join our team as an Associate Professor/Professor in Biomechanics. This area has achieved significant growth in recent years offering students exciting programs of study including two Exercise and Sports Science Australia (ESSA) accredited degrees.<br>The successful applicant will have management, teaching and research strengths within the field of Biomechanics. We are looking for staff who will take a key role in the continuing design and development of the curricula for the Exercise and Sport Science degrees, contribute to the school&#39;s research program and be a leader in this field. The successful candidate will have a track record in teaching and education development and be committed to the delivery of high-quality outcomes for students.', 'Having a completed doctoral qualification in a discipline or topic relevant to Biomechanics and demonstrated school teaching experience. Having a strong research contribution to the field, with evidence of capacity to build and maintain research networks, and skills in mentoring and supporting early career academics and higher degree research candidates. Having skills in people management and staff support', 2, 2, '$33/hr', '2023-06-30'),
  ('fbabd2b87a03237ceb51c4207ead603e', 'Software Engineering Lecturer', 1, 1, 'Hawthorn, Victoria', 'We adapt both our global curriculum and local approach to the technical trends and hiring environment of the times and cities we work in, but today our primary educational approach centers around JavaScript. In general, our curriculum is scaffolded to follow the historical evolution of software engineering. We start by teaching the fundamentals of programming and web design through JavaScript, HTML, and CSS. About 25% of our course (normally unit 2 of 4) focuses on Rails MVC or similar framework, using that context to introduce databases, security, and another foundational knowledge. The rest of the course (units 3 and 4) focuses back on JavaScript. We cover API development in Node, then tackle one or more front-end MV* frameworks (Backbone, Angular, Ember, React). We also cover all sorts of other things that junior web developers need to know, like source control, team collaboration, and developer workflow. We give students the chance to spend focused time building at least 4 major projects, in addition to other smaller projects and labs. About 20% of overall class time is spent on dedicated project work. Need to teach 16 hours per fortnight for duration of the program (Tuesday/Thursday evenings or Monday/Wednesday evenings, and Saturdays)', 'Fluent in HTML and CSS, Full-stack JavaScript (strong JavaScript highly preferred), At least one JS MV* framework (Angular, Backbone, or React preferred), SQL databases (we generally use PosgreSQL), NoSQL (we generally cover MongoDB and Redis), At least one additional object-oriented language (Python preferred)', 1, 4, '$32/hr', '2023-06-30'),
  ('d409c54857eb2c623e1e6280233fb538', 'Cyber Security Lecturer', 1, 1, 'Hawthorn, Victoria', 'We adapt both our global curriculum and local approach to the technical trends and hiring environment of the times and cities we work in, but today our primary educational approach centers around Cyber Security. In general, our curriculum is scaffolded to follow the historical evolution of software engineering. We start by teaching the fundamentals of Cyber Security. The candidate will be required to have a thorough understanding of cyber security risk management, governance, policy and process in a federal or state government context.', 'Minimum 8 years professional experience in IT, with at least 3-5 years of experience in an Information Security, Risk Management, Audit or equivalent discipline, Knowledge of information security, including threat intelligence, incident response, risk management, and security architecture, Knowledge of security standards such as the PSPF, ISM, Essential 8, DSPF, ISO 27000 series, NIST CSF and 800 series, CIS, Knowledge of, or performance of IRAP and system certification and accreditation, Ability to manage multiple projects, prioritize tasks, and meet project deadlines, Strong interpersonal skills, with the ability to build relationships and collaborate with stakeholders across the organization.', 1, 4, '$32/hr', '2023-06-30'),
  ('016c727148d5c689d015125a8fc0133e', 'Lecturer (Level B or Level C) - School of Civil Engineering', 5, 1, 'Perth', 'The School of Architecture and Civil Engineering are seeking Lecturers at Level B or Level C to join their staff to deliver high quality teaching and research activity to the school and wider University. Reporting to the Head of School, we are seeking the expertise of Lecturers in Construction Management or relevant field. With a strong focus on smart and sustainable construction, we are looking for two new team members to join the Construction Management Discipline. The team collaborates with other disciplines within the School of Architecture and Civil Engineering and more broadly across the university to deliver excellence in teaching and research in the field of construction management. The discipline supports fast-growing undergraduate and postgraduate programs in construction management.', 'PhD in Construction Management or a relevant field such as Construction Engineering, Architectural design, Engineering Management, Demonstrated ability (Level C) or Ability (Level B) to lead and deliver course design, and to deliver student centred learning and teaching activities at an undergraduate and postgraduate level, including the capacity to incorporate new technologies and new approaches to teaching and learning, Demonstrated ability to teach digital construction and building services. And/or Demonstrated ability to teach financial management, construction law and contract administration, Demonstrated track record of research funding, high quality publications and conference presentations relative to opportunity.', 1, 2, '$44/hr', '2023-06-30'),
  ('fc2b9ad746d5453a1f363a889b6f9412', 'Lecturer for School of Engineering', 5, 1, 'Adelaide', 'Architecture section of Civil Engineering are seeking Lecturers at Level A to join their staff to deliver high quality teaching and research activity to the school and wider University. Reporting to the Head of School, we are seeking the expertise of Lecturers in Construction Management or relevant field. With a strong focus on smart and sustainable construction, we are looking for two new team members to join the Construction Management Discipline. The team collaborates with other disciplines within the School of Architecture and Civil Engineering and more broadly across the university to deliver excellence in teaching and research in the field of construction management. The discipline supports fast-growing undergraduate and postgraduate programs in construction management.', 'PhD in Construction Management or a relevant field such as Construction Engineering, Architectural design, Engineering Management, Demonstrated ability (Level C) or Ability (Level B) to lead and deliver course design, and to deliver student centred learning and teaching activities at an undergraduate and postgraduate level, including the capacity to incorporate new technologies and new approaches to teaching and learning, Demonstrated ability to teach digital construction and building services. And/or Demonstrated ability to teach financial management, construction law and contract administration, Demonstrated track record of research funding, high quality publications and conference presentations relative to opportunity.', 1, 2, '$54/hr', '2023-06-30'),
  ('433b6cd03365cbd034104076749ad97f', 'Information Security Demonstrator', 1, 1, 'Perth', 'We adapt both our global curriculum and local approach to the technical trends and hiring environment of the times and cities we work in, but today our primary educational approach centers around Cyber Security. In general, our curriculum is scaffolded to follow the historical evolution of software engineering. We start by teaching the fundamentals of Cyber Security. The candidate will be required to have a thorough understanding of cyber security risk management, governance, policy and process in a federal or state government context.', 'Minimum 8 years professional experience in IT, with at least 3-5 years of experience in an Information Security, Risk Management, Audit or equivalent discipline, Knowledge of information security, including threat intelligence, incident response, risk management, and security architecture, Knowledge of security standards such as the PSPF, ISM, Essential 8, DSPF, ISO 27000 series, NIST CSF and 800 series, CIS, Knowledge of, or performance of IRAP and system certification and accreditation, Ability to manage multiple projects, prioritize tasks, and meet project deadlines, Strong interpersonal skills, with the ability to build relationships and collaborate with stakeholders across the organization.', 1, 4, '$32/hr', '2023-06-30'),
  ('dd39b5b2619416c77e4ba8d0091112f2', 'Assistant Lecturer in Nursing', 4, 1, 'Perth', 'This is an exciting opportunity for an enthusiastic and motivated Registered Nurse to join a dynamic, progressive team within the University of Tasmania&#39;s College of Health and Medicine. The College has a focus on boosting health research performance and evidence-based learning and teaching to educate a new generation of agile health professionals and researchers with capability in leadership and future-focused health care. With a strong background in nursing education this teaching intensive position will contribute to student success through the educational preparation of pre-registration and post graduate students of nursing. This position also involves health services research and/or innovation in learning and teaching that can improve the health of Tasmanians.  You will assist in developing a positive culture that enables high levels of collaboration and productivity to support the vision of the University to deliver place-based education and research with high impacts', 'Registration as a Nurse, Post graduate nursing qualifications at PhD, or master&#39;s level, desirable, Evidence of research capabilities, Significant experience in nursing practice.', 5, 2, '$30/hr', '2023-06-30');
  """)

  db.commit()
  cursor.close()
  db.close()
  return "Dummy data inserted"
