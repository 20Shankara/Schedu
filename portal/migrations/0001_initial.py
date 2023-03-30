# Generated by Django 4.1.6 on 2023-03-30 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Advisor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("advisor_first_name", models.CharField(max_length=255)),
                ("advisor_last_name", models.CharField(max_length=255)),
                ("advisor_email", models.EmailField(max_length=255)),
                (
                    "advisor_department",
                    models.CharField(
                        choices=[
                            (
                                "African-American and African Studies",
                                "African-American and African Studies",
                            ),
                            ("Accounting", "Accounting"),
                            ("Air Science", "Air Science"),
                            (
                                "Architecture and Landscape Architecture",
                                "Architecture and Landscape Architecture",
                            ),
                            ("Applied Mechanics", "Applied Mechanics"),
                            ("American Studies", "American Studies"),
                            ("Anthropology", "Anthropology"),
                            ("Applied Mathematics", "Applied Mathematics"),
                            ("Arabic", "Arabic"),
                            ("Arts Administration", "Arts Administration"),
                            (
                                "History of Art and Architecture",
                                "History of Art and Architecture",
                            ),
                            ("Architecture", "Architecture"),
                            ("Archaeology", "Archaeology"),
                            ("Architectural History", "Architectural History"),
                            ("History of Art", "History of Art"),
                            ("Arabic in Translation", "Arabic in Translation"),
                            ("Studio Art", "Studio Art"),
                            ("American Sign Language", "American Sign Language"),
                            ("Astronomy", "Astronomy"),
                            ("Biomedical Sciences", "Biomedical Sciences"),
                            ("Biochemistry", "Biochemistry"),
                            ("Biology", "Biology"),
                            ("Biophysics", "Biophysics"),
                            ("Biomedical Engineering", "Biomedical Engineering"),
                            ("Business", "Business"),
                            (
                                "College Art Scholars Seminar",
                                "College Art Scholars Seminar",
                            ),
                            ("Civil Engineering", "Civil Engineering"),
                            ("Cell Biology", "Cell Biology"),
                            ("Chemical Engineering", "Chemical Engineering"),
                            ("Chemistry", "Chemistry"),
                            ("Chinese", "Chinese"),
                            ("Chinese in Translation", "Chinese in Translation"),
                            ("Classics", "Classics"),
                            ("Cognitive Science", "Cognitive Science"),
                            ("College Advising Seminar", "College Advising Seminar"),
                            ("Commerce", "Commerce"),
                            ("Commerce-Non-Credit", "Commerce-Non-Credit"),
                            ("Computer Engineering", "Computer Engineering"),
                            ("Creole", "Creole"),
                            ("Computer Science", "Computer Science"),
                            ("Dance", "Dance"),
                            ("Democracy Initiative", "Democracy Initiative"),
                            ("Digital Humanities", "Digital Humanities"),
                            ("Drama", "Drama"),
                            ("Data Science", "Data Science"),
                            (
                                "East Asian Languages, Literatures, and Cultures",
                                "East Asian Languages, Literatures, and Cultures",
                            ),
                            ("East Asian Studies", "East Asian Studies"),
                            (
                                "Electrical and Computer Engineering",
                                "Electrical and Computer Engineering",
                            ),
                            ("Economics", "Economics"),
                            ("Education-Human Services", "Education-Human Services"),
                            (
                                "Education-Curriculum, Instruction, & Special Ed",
                                "Education-Curriculum, Instruction, & Special Ed",
                            ),
                            (
                                "Education-Leadership, Foundations, and Policy",
                                "Education-Leadership, Foundations, and Policy",
                            ),
                            ("Education-Non-Credit", "Education-Non-Credit"),
                            ("Engagement", "Engagement"),
                            ("Engaging the Liberal Arts", "Engaging the Liberal Arts"),
                            ("English-Creative Writing", "English-Creative Writing"),
                            ("English Literature", "English Literature"),
                            ("Engineering", "Engineering"),
                            ("Entrepreneurship", "Entrepreneurship"),
                            (
                                "English-Academic, Professional, & Creative Writing",
                                "English-Academic, Professional, & Creative Writing",
                            ),
                            (
                                "English as a Second Language",
                                "English as a Second Language",
                            ),
                            (
                                "Enviromental Thought and Practice",
                                "Enviromental Thought and Practice",
                            ),
                            ("European Studies", "European Studies"),
                            (
                                "Environmental Sciences-Atmospheric Sciences",
                                "Environmental Sciences-Atmospheric Sciences",
                            ),
                            (
                                "Environmental Sciences-Ecology",
                                "Environmental Sciences-Ecology",
                            ),
                            (
                                "Environmental Sciences-Geosciences",
                                "Environmental Sciences-Geosciences",
                            ),
                            (
                                "Environmental Sciences-Hydrology",
                                "Environmental Sciences-Hydrology",
                            ),
                            ("Environmental Sciences", "Environmental Sciences"),
                            ("French", "French"),
                            (
                                "Graduate Business Analytics Commerce",
                                "Graduate Business Analytics Commerce",
                            ),
                            ("Graduate Business", "Graduate Business"),
                            (
                                "Global Commerce in Culture and Society",
                                "Global Commerce in Culture and Society",
                            ),
                            ("Clinical Nurse Leader", "Clinical Nurse Leader"),
                            ("Graduate Commerce", "Graduate Commerce"),
                            (
                                "Global Development Studies",
                                "Global Development Studies",
                            ),
                            ("German", "German"),
                            ("German in Translation", "German in Translation"),
                            (
                                "Graduate Humanities and Social Sciences",
                                "Graduate Humanities and Social Sciences",
                            ),
                            ("Graduate Nursing", "Graduate Nursing"),
                            ("Greek", "Greek"),
                            ("Graduate Arts & Sciences", "Graduate Arts & Sciences"),
                            (
                                "Graduate Biological and Physical Sciences",
                                "Graduate Biological and Physical Sciences",
                            ),
                            (
                                "Global Studies-Global Studies",
                                "Global Studies-Global Studies",
                            ),
                            (
                                "Global Studies: Middle East and South Asia",
                                "Global Studies: Middle East and South Asia",
                            ),
                            (
                                "Global Studies-Security and Justice",
                                "Global Studies-Security and Justice",
                            ),
                            (
                                "Global Studies-Environments and Sustainability",
                                "Global Studies-Environments and Sustainability",
                            ),
                            ("Human Biology", "Human Biology"),
                            ("Hebrew", "Hebrew"),
                            (
                                "Health, Humanities & Ethics",
                                "Health, Humanities & Ethics",
                            ),
                            ("History-African History", "History-African History"),
                            (
                                "History-East Asian History",
                                "History-East Asian History",
                            ),
                            ("History-European History", "History-European History"),
                            (
                                "History-Latin American History",
                                "History-Latin American History",
                            ),
                            (
                                "History-Middle Eastern History",
                                "History-Middle Eastern History",
                            ),
                            ("Hindi", "Hindi"),
                            (
                                "History-South Asian History",
                                "History-South Asian History",
                            ),
                            ("History-General History", "History-General History"),
                            (
                                "History-United States History",
                                "History-United States History",
                            ),
                            ("Human Resources", "Human Resources"),
                            (
                                "College Science Scholars Seminar",
                                "College Science Scholars Seminar",
                            ),
                            ("Interdisciplinary Thesis", "Interdisciplinary Thesis"),
                            ("Interdisciplinary Studies", "Interdisciplinary Studies"),
                            (
                                "Interdisciplinary Studies-Business",
                                "Interdisciplinary Studies-Business",
                            ),
                            (
                                "Interdisciplinary Studies-Humanities",
                                "Interdisciplinary Studies-Humanities",
                            ),
                            (
                                "Interdisciplinary Studies-Code of Inquiry",
                                "Interdisciplinary Studies-Code of Inquiry",
                            ),
                            (
                                "Interdisciplinary Studies-Liberal Studies Seminar",
                                "Interdisciplinary Studies-Liberal Studies Seminar",
                            ),
                            (
                                "Interdisciplinary Studies-Social Sciences",
                                "Interdisciplinary Studies-Social Sciences",
                            ),
                            ("Informational Technology", "Informational Technology"),
                            ("Italian", "Italian"),
                            ("Italian in Translation", "Italian in Translation"),
                            ("Japanese", "Japanese"),
                            ("Japanese in Translation", "Japanese in Translation"),
                            ("Maya K'iche'", "Maya K'iche'"),
                            ("Kinesiology", "Kinesiology"),
                            (
                                "Kinesiology Lifetime Physical Activity",
                                "Kinesiology Lifetime Physical Activity",
                            ),
                            ("Korean", "Korean"),
                            ("Landscape Architecture", "Landscape Architecture"),
                            ("Liberal Arts Seminar", "Liberal Arts Seminar"),
                            ("Latin American Studies", "Latin American Studies"),
                            ("Latin", "Latin"),
                            ("Law", "Law"),
                            ("Linguistics", "Linguistics"),
                            ("General Linguistics", "General Linguistics"),
                            (
                                "Leadership Public Policy - Analysis",
                                "Leadership Public Policy - Analysis",
                            ),
                            (
                                "Leadership Public Policy - Leadership",
                                "Leadership Public Policy - Leadership",
                            ),
                            (
                                "Leadership Public Policy - Policy",
                                "Leadership Public Policy - Policy",
                            ),
                            (
                                "Leadership Public Policy - Substance",
                                "Leadership Public Policy - Substance",
                            ),
                            (
                                "Mechanical & Aerospace Engineering",
                                "Mechanical & Aerospace Engineering",
                            ),
                            ("Mathematics", "Mathematics"),
                            ("Media Studies", "Media Studies"),
                            ("Medicine", "Medicine"),
                            (
                                "Middle Eastern & South Asian Languages & Cultures",
                                "Middle Eastern & South Asian Languages & Cultures",
                            ),
                            ("Microbiology", "Microbiology"),
                            ("Military Science", "Military Science"),
                            (
                                "Materials Science and Engineering",
                                "Materials Science and Engineering",
                            ),
                            ("Medieval Studies", "Medieval Studies"),
                            ("Music-Marching Band", "Music-Marching Band"),
                            ("Music-Ensembles", "Music-Ensembles"),
                            (
                                "Music-Private Performance Instruction",
                                "Music-Private Performance Instruction",
                            ),
                            ("Music", "Music"),
                            ("Naval Science", "Naval Science"),
                            (
                                "Non-Credit Professional Review",
                                "Non-Credit Professional Review",
                            ),
                            ("Neuroscience", "Neuroscience"),
                            ("Nursing Core", "Nursing Core"),
                            ("Nursing Interprofessional", "Nursing Interprofessional"),
                            ("Nursing", "Nursing"),
                            ("Pathology", "Pathology"),
                            (
                                "Procurement and Contracts Management",
                                "Procurement and Contracts Management",
                            ),
                            ("Persian", "Persian"),
                            ("Persian in Translation", "Persian in Translation"),
                            ("Pharmacology", "Pharmacology"),
                            ("Philosophy", "Philosophy"),
                            ("Public Health Sciences", "Public Health Sciences"),
                            ("Physiology", "Physiology"),
                            ("Physics", "Physics"),
                            ("Planning Application", "Planning Application"),
                            (
                                "Politics-Departmental Seminar",
                                "Politics-Departmental Seminar",
                            ),
                            (
                                "Urban and Environmental Planning",
                                "Urban and Environmental Planning",
                            ),
                            (
                                "Politics-American Politics",
                                "Politics-American Politics",
                            ),
                            (
                                "Politics-Comparative Politics",
                                "Politics-Comparative Politics",
                            ),
                            (
                                "Politics-International Relations",
                                "Politics-International Relations",
                            ),
                            ("Politics-Political Theory", "Politics-Political Theory"),
                            ("Polish", "Polish"),
                            ("Portuguese", "Portuguese"),
                            ("Portuguese in Translation", "Portuguese in Translation"),
                            (
                                "Political Philosophy, Policy, and Law",
                                "Political Philosophy, Policy, and Law",
                            ),
                            (
                                "Professional Studies-Health Sciences Management",
                                "Professional Studies-Health Sciences Management",
                            ),
                            ("PS-Leadership Program", "PS-Leadership Program"),
                            (
                                "Professional Studies-Public Administration",
                                "Professional Studies-Public Administration",
                            ),
                            (
                                "Professional Studies-Project Management",
                                "Professional Studies-Project Management",
                            ),
                            (
                                "Professional Studies - Public Safety",
                                "Professional Studies - Public Safety",
                            ),
                            (
                                "Political and Social Thought",
                                "Political and Social Thought",
                            ),
                            ("Psychology", "Psychology"),
                            (
                                "Religion-African Religions",
                                "Religion-African Religions",
                            ),
                            ("Religion-Buddhism", "Religion-Buddhism"),
                            ("Religion-Christianity", "Religion-Christianity"),
                            ("Religion-General Religion", "Religion-General Religion"),
                            ("Religion-Hinduism", "Religion-Hinduism"),
                            ("Religion-Islam", "Religion-Islam"),
                            ("Religion-Judaism", "Religion-Judaism"),
                            ("Religion-Special Topic", "Religion-Special Topic"),
                            ("Russian", "Russian"),
                            ("Russian in Translation", "Russian in Translation"),
                            ("Sanskrit", "Sanskrit"),
                            ("Architecture School", "Architecture School"),
                            ("South Asian Studies", "South Asian Studies"),
                            (
                                "South Asian Literature in Translation",
                                "South Asian Literature in Translation",
                            ),
                            ("CYB SEC Analysis", "CYB SEC Analysis"),
                            ("Slavic", "Slavic"),
                            ("Slavic in Translation", "Slavic in Translation"),
                            ("Sociology", "Sociology"),
                            ("Spanish", "Spanish"),
                            ("Statistics", "Statistics"),
                            (
                                "Science, Technology, and Society",
                                "Science, Technology, and Society",
                            ),
                            ("Swahili", "Swahili"),
                            (
                                "Systems & Information Engineering",
                                "Systems & Information Engineering",
                            ),
                            ("Turkish", "Turkish"),
                            ("Urban Design", "Urban Design"),
                            ("University Studies", "University Studies"),
                            ("Urdu", "Urdu"),
                            ("University Seminar", "University Seminar"),
                            (
                                "Women, Gender, and Sexuality",
                                "Women, Gender, and Sexuality",
                            ),
                        ],
                        default="",
                        max_length=50,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Instructor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Meeting",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("days", models.CharField(max_length=255)),
                ("start_time", models.CharField(max_length=255)),
                ("end_time", models.CharField(max_length=255)),
                ("facility_descr", models.CharField(max_length=255)),
                ("room", models.CharField(max_length=255)),
                ("instructor", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("student_first_name", models.CharField(max_length=255)),
                ("student_last_name", models.CharField(max_length=255)),
                ("student_email", models.EmailField(max_length=255)),
                (
                    "year_in_school",
                    models.CharField(
                        choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4")],
                        default="",
                        max_length=2,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Class",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("crse_id", models.CharField(max_length=255)),
                ("class_section", models.CharField(max_length=255)),
                ("start_dt", models.CharField(max_length=255)),
                ("end_dt", models.CharField(max_length=255)),
                ("campus_descr", models.CharField(max_length=255)),
                ("class_nbr", models.CharField(max_length=255)),
                ("acad_career", models.CharField(max_length=255)),
                ("component", models.CharField(max_length=255)),
                ("subject", models.CharField(max_length=255)),
                ("subject_descr", models.CharField(max_length=255)),
                ("catalog_nbr", models.CharField(max_length=255)),
                ("acad_group", models.CharField(max_length=255)),
                ("instruction_mode_descr", models.CharField(max_length=255)),
                ("wait_tot", models.CharField(max_length=255)),
                ("wait_cap", models.CharField(max_length=255)),
                ("class_capacity", models.CharField(max_length=255)),
                ("enrollment_total", models.CharField(max_length=255)),
                ("enrollment_available", models.CharField(max_length=255)),
                ("descr", models.CharField(max_length=255)),
                ("units", models.CharField(max_length=255)),
                ("enrl_stat_descr", models.CharField(max_length=255)),
                ("topic", models.CharField(max_length=255)),
                ("section_type", models.CharField(max_length=255)),
                ("instructors", models.ManyToManyField(to="portal.instructor")),
            ],
        ),
    ]
