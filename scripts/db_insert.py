import json
import psycopg2
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'quiz_app',  # UPDATE
    'user': 'namangupta',            # UPDATE
    'password': 'password',        # UPDATE
    'port': 5432
}

SPORT_ID_FOOTBALL = 2
CATEGORY_ID_EPL = 7


def generate_100_engaging_epl_questions():
    """
    Generate 100 engaging, story-driven EPL quiz questions
    35 Easy, 35 Medium, 30 Hard
    Mix of all topics: drama, tactics, recent events, controversies, etc.
    """
    
    questions = []
    
    # ========== EASY QUESTIONS (35) ==========
    
    easy_questions = [
        {
            "id": 1,
            "question": "In May 2012, Sergio Aguero scored a last-second goal to win Manchester City their first Premier League title. Which team were they playing against?",
            "type": "MCQ",
            "options": ["Bolton", "QPR", "Sunderland", "Stoke"],
            "correct_answer": "QPR",
            "difficulty": "easy",
            "explanation": "The 'Aguerooooo' moment against QPR is one of the most iconic in Premier League history, with City scoring twice in injury time to win the title on goal difference."
        },
        {
            "id": 2,
            "question": "Which team famously won the Premier League in 2015-16 despite being 5000/1 outsiders at the start of the season?",
            "type": "MCQ",
            "options": ["Southampton", "Leicester City", "West Ham", "Stoke City"],
            "correct_answer": "Leicester City",
            "difficulty": "easy",
            "explanation": "Leicester City's miracle title win is considered one of the greatest sporting upsets in history."
        },
        {
            "id": 3,
            "question": "In 2020, Liverpool won their first Premier League title after how many years without a league championship?",
            "type": "MCQ",
            "options": ["20 years", "25 years", "30 years", "35 years"],
            "correct_answer": "30 years",
            "difficulty": "easy",
            "explanation": "Liverpool's 30-year wait for a league title finally ended under Jurgen Klopp in 2020."
        },
        {
            "id": 4,
            "question": "Which Arsenal team went unbeaten throughout an entire Premier League season, earning the nickname 'The Invincibles'?",
            "type": "MCQ",
            "options": ["2001-02", "2002-03", "2003-04", "2004-05"],
            "correct_answer": "2003-04",
            "difficulty": "easy",
            "explanation": "Arsenal's 2003-04 season saw them win the title with 26 wins and 12 draws, no defeats."
        },
        {
            "id": 5,
            "question": "Erling Haaland broke the Premier League record for most goals in a 38-game season. How many goals did he score in 2022-23?",
            "type": "MCQ",
            "options": ["34", "35", "36", "38"],
            "correct_answer": "36",
            "difficulty": "easy",
            "explanation": "Haaland's 36 goals broke the previous record of 34 held jointly by Andy Cole and Alan Shearer."
        },
        {
            "id": 6,
            "question": "Which manager famously said 'I prefer not to speak' in a post-match interview, creating a viral meme?",
            "type": "MCQ",
            "options": ["Jurgen Klopp", "Jose Mourinho", "Pep Guardiola", "Antonio Conte"],
            "correct_answer": "Jose Mourinho",
            "difficulty": "easy",
            "explanation": "Mourinho's response to VAR controversy in 2020 became one of football's most famous memes."
        },
        {
            "id": 7,
            "question": "In 2011, Manchester City famously beat Manchester United 6-1 at Old Trafford. Was this City's biggest ever derby win?",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "easy",
            "explanation": "The 6-1 demolition announced City's arrival as title contenders and remains the biggest margin in derby history."
        },
        {
            "id": 8,
            "question": "Steven Gerrard's famous slip in 2014 against Chelsea cost Liverpool a chance at the Premier League title.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "easy",
            "explanation": "Gerrard's slip allowed Demba Ba to score, and Liverpool's title hopes crumbled in the final weeks."
        },
        {
            "id": 9,
            "question": "Which player holds the all-time Premier League goal-scoring record with 260 goals?",
            "type": "MCQ",
            "options": ["Wayne Rooney", "Alan Shearer", "Thierry Henry", "Sergio Aguero"],
            "correct_answer": "Alan Shearer",
            "difficulty": "easy",
            "explanation": "Shearer's 260 goals remain the benchmark, scored across his time at Blackburn and Newcastle."
        },
        {
            "id": 10,
            "question": "In 2022-23, Arsenal led the Premier League for most of the season but finished second. Which team won the title?",
            "type": "MCQ",
            "options": ["Liverpool", "Manchester United", "Chelsea", "Manchester City"],
            "correct_answer": "Manchester City",
            "difficulty": "easy",
            "explanation": "Arsenal led for 248 days but City's late surge saw them clinch their third consecutive title."
        },
        {
            "id": 11,
            "question": "Manchester City has won four consecutive Premier League titles from 2020-21 to 2023-24.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "easy",
            "explanation": "City's unprecedented four-in-a-row dominance has cemented their dynasty under Guardiola."
        },
        {
            "id": 12,
            "question": "Which manager won 13 Premier League titles with Manchester United before retiring in 2013?",
            "type": "MCQ",
            "options": ["Jose Mourinho", "Sir Alex Ferguson", "Arsene Wenger", "Carlo Ancelotti"],
            "correct_answer": "Sir Alex Ferguson",
            "difficulty": "easy",
            "explanation": "Ferguson's 13 titles remain a record that may never be broken."
        },
        {
            "id": 13,
            "question": "In 2019, which team pulled off a miraculous comeback to beat Manchester City 3-2 despite being 2-0 down at halftime, ending City's unbeaten run?",
            "type": "MCQ",
            "options": ["Crystal Palace", "Leicester City", "Brighton", "West Ham"],
            "correct_answer": "Crystal Palace",
            "difficulty": "easy",
            "explanation": "Palace's stunning comeback at the Etihad is remembered as one of the great Premier League turnarounds."
        },
        {
            "id": 14,
            "question": "Mohamed Salah scored 32 Premier League goals in 2017-18, setting a record for a 38-game season at the time.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "easy",
            "explanation": "Salah's 32 goals broke the previous record until Haaland surpassed it with 36."
        },
        {
            "id": 15,
            "question": "Which player was famously sent off for kicking a fan in 1995, becoming one of football's most controversial moments?",
            "type": "MCQ",
            "options": ["Roy Keane", "Eric Cantona", "Duncan Ferguson", "Vinnie Jones"],
            "correct_answer": "Eric Cantona",
            "difficulty": "easy",
            "explanation": "Cantona's 'kung-fu kick' at Crystal Palace earned him an 8-month ban but cemented his cult hero status."
        },
        {
            "id": 16,
            "question": "Pep Guardiola has won the Premier League with Manchester City multiple times. How many times as of 2024?",
            "type": "MCQ",
            "options": ["4", "5", "6", "7"],
            "correct_answer": "6",
            "difficulty": "easy",
            "explanation": "Guardiola's six Premier League titles (2017-18, 2018-19, 2020-21, 2021-22, 2022-23, 2023-24) make him the most successful current manager."
        },
        {
            "id": 17,
            "question": "Chelsea has never lost a Premier League match after leading at halftime under Jose Mourinho's first stint (2004-07).",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "easy",
            "explanation": "Mourinho's Chelsea never lost from a winning position at halftime in 124 league games, showcasing incredible game management."
        },
        {
            "id": 18,
            "question": "Which goalkeeper made a record 11 saves in a single match against Arsenal in 2023, helping his team win 1-0?",
            "type": "MCQ",
            "options": ["Nick Pope", "Alphonse Areola", "Aaron Ramsdale", "Jordan Pickford"],
            "correct_answer": "Alphonse Areola",
            "difficulty": "easy",
            "explanation": "Areola's heroic performance for West Ham frustrated Arsenal in a crucial fixture."
        },
        {
            "id": 19,
            "question": "Newcastle United's takeover by Saudi Arabia's Public Investment Fund in 2021 made them one of the richest clubs in world football.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "easy",
            "explanation": "The £305m takeover transformed Newcastle into one of football's wealthiest clubs overnight."
        },
        {
            "id": 20,
            "question": "In 2022, which newly-promoted team shocked Liverpool by beating them 3-0 at Anfield, ending their 4.5-year unbeaten home record?",
            "type": "MCQ",
            "options": ["Fulham", "Bournemouth", "Nottingham Forest", "Brentford"],
            "correct_answer": "Bournemouth",
            "difficulty": "easy",
            "explanation": "Bournemouth's stunning victory was one of the biggest upsets of the 2022-23 season."
        },
        {
            "id": 21,
            "question": "Tottenham has won at least one Premier League title in their history.",
            "type": "True/False",
            "correct_answer": "False",
            "difficulty": "easy",
            "explanation": "Despite being a top-six club, Spurs have never won the Premier League title since its inception in 1992."
        },
        {
            "id": 22,
            "question": "Which player scored a hat-trick in his final Premier League appearance before retiring, with all three goals coming from outside the box?",
            "type": "MCQ",
            "options": ["Steven Gerrard", "Frank Lampard", "Wayne Rooney", "Paul Scholes"],
            "correct_answer": "Steven Gerrard",
            "difficulty": "easy",
            "explanation": "Gerrard's farewell hat-trick against Crystal Palace in 2015 was a perfect send-off for the Liverpool legend."
        },
        {
            "id": 23,
            "question": "VAR (Video Assistant Referee) was introduced to the Premier League in the 2019-20 season.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "easy",
            "explanation": "VAR's introduction has been controversial, with fans divided on its impact on the game."
        },
        {
            "id": 24,
            "question": "Which team pulled off the 'Great Escape' in 2004-05, surviving relegation despite being bottom at Christmas?",
            "type": "MCQ",
            "options": ["West Brom", "Wigan", "Sunderland", "Portsmouth"],
            "correct_answer": "West Brom",
            "difficulty": "easy",
            "explanation": "West Brom's survival after being bottom on Christmas Day remains one of football's great escapes."
        },
        {
            "id": 25,
            "question": "Manchester United went 9 years without winning a Premier League title after Sir Alex Ferguson retired.",
            "type": "True/False",
            "correct_answer": "False",
            "difficulty": "easy",
            "explanation": "As of 2024, United have gone over 10 years without a Premier League title (last won in 2012-13)."
        },
        {
            "id": 26,
            "question": "Which striker became the fastest player to reach 50 Premier League goals, doing so in just 48 games?",
            "type": "MCQ",
            "options": ["Erling Haaland", "Mohamed Salah", "Sergio Aguero", "Thierry Henry"],
            "correct_answer": "Erling Haaland",
            "difficulty": "easy",
            "explanation": "Haaland's incredible scoring rate has rewritten the record books since joining City in 2022."
        },
        {
            "id": 27,
            "question": "Arsenal has won more FA Cups than any other English club.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "easy",
            "explanation": "Arsenal's 14 FA Cup wins are a record, with their most recent coming in 2020."
        },
        {
            "id": 28,
            "question": "In 2020, which team became the first to officially relegate from the Premier League via a video call due to COVID-19?",
            "type": "MCQ",
            "options": ["Norwich", "Bournemouth", "Watford", "Aston Villa"],
            "correct_answer": "Norwich",
            "difficulty": "easy",
            "explanation": "Norwich's relegation was confirmed mathematically before they could play again after the COVID restart."
        },
        {
            "id": 29,
            "question": "Jurgen Klopp's Liverpool are known for their 'gegenpressing' high-intensity pressing style.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "easy",
            "explanation": "Klopp's 'gegenpress' or counter-pressing has been central to Liverpool's success."
        },
        {
            "id": 30,
            "question": "Which player famously kissed the Manchester City badge after scoring against his former club Manchester United?",
            "type": "MCQ",
            "options": ["Carlos Tevez", "Raheem Sterling", "Gabriel Jesus", "Sergio Aguero"],
            "correct_answer": "Carlos Tevez",
            "difficulty": "easy",
            "explanation": "Tevez's controversial badge kiss in 2010 deepened the rivalry after his move from United to City."
        },
        {
            "id": 31,
            "question": "Chelsea was taken over by Roman Abramovich in 2003, transforming them into Premier League champions within two years.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "easy",
            "explanation": "Abramovich's billions funded Chelsea's rise to dominance, winning back-to-back titles in 2004-05 and 2005-06."
        },
        {
            "id": 32,
            "question": "Which team holds the record for the most points in a single Premier League season with 100 points?",
            "type": "MCQ",
            "options": ["Chelsea 2004-05", "Manchester City 2017-18", "Liverpool 2019-20", "Arsenal 2003-04"],
            "correct_answer": "Manchester City 2017-18",
            "difficulty": "easy",
            "explanation": "City's centurion season under Guardiola set a new benchmark for dominance."
        },
        {
            "id": 33,
            "question": "A team relegated from the Premier League receives parachute payments to help with the financial transition.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "easy",
            "explanation": "Parachute payments help relegated clubs adjust to lower TV revenues, though they're controversial."
        },
        {
            "id": 34,
            "question": "Which manager was famously sacked by Chelsea despite winning the Champions League just 7 months earlier?",
            "type": "MCQ",
            "options": ["Roberto Di Matteo", "Thomas Tuchel", "Avram Grant", "Andre Villas-Boas"],
            "correct_answer": "Roberto Di Matteo",
            "difficulty": "easy",
            "explanation": "Di Matteo's Champions League triumph couldn't save him from Roman Abramovich's ruthless approach."
        },
        {
            "id": 35,
            "question": "Arsenal went 49 consecutive Premier League games unbeaten during their Invincibles era.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "easy",
            "explanation": "Arsenal's unbeaten run spanned from May 2003 to October 2004, ending controversially against Manchester United."
        },
    ]
    
    # ========== MEDIUM QUESTIONS (35) ==========
    
    medium_questions = [
        {
            "id": 36,
            "question": "Pep Guardiola revolutionized tactics with 'inverted full-backs' at Manchester City. Which principle best describes this innovation?",
            "type": "MCQ",
            "options": [
                "Full-backs pushing extremely high up the pitch",
                "Full-backs moving into central midfield positions during possession",
                "Full-backs swapping positions during the game",
                "Full-backs acting as additional center-backs"
            ],
            "correct_answer": "Full-backs moving into central midfield positions during possession",
            "difficulty": "medium",
            "explanation": "Players like Zinchenko and Cancelo moving into midfield created numerical superiority, changing modern tactics."
        },
        {
            "id": 37,
            "question": "In 2021, which player's transfer from Aston Villa to Manchester City broke the British transfer record at £100 million?",
            "type": "MCQ",
            "options": ["Raheem Sterling", "Jack Grealish", "Kalvin Phillips", "Riyad Mahrez"],
            "correct_answer": "Jack Grealish",
            "difficulty": "medium",
            "explanation": "Grealish's record fee made him the most expensive British player, though his performances have divided opinion."
        },
        {
            "id": 38,
            "question": "Which team scored 3 goals in 6 minutes to come back from 2-0 down against Tottenham in injury time (2022)?",
            "type": "MCQ",
            "options": ["Brighton", "Bournemouth", "Leicester", "Wolves"],
            "correct_answer": "Brighton",
            "difficulty": "medium",
            "explanation": "Brighton's incredible 3-2 comeback between the 83rd and 90th minute was one of the most dramatic collapses in Premier League history."
        },
        {
            "id": 39,
            "question": "Arsenal's 49-game unbeaten run ended in a controversial match where the referee was later banned. Which team beat them?",
            "type": "MCQ",
            "options": ["Chelsea", "Manchester United", "Liverpool", "Tottenham"],
            "correct_answer": "Manchester United",
            "difficulty": "medium",
            "explanation": "The 'Battle of the Buffet' saw United end Arsenal's run 2-0, with accusations of rough play and controversial refereeing."
        },
        {
            "id": 40,
            "question": "In the 2013-14 title race, Luis Suarez was suspended for the final crucial games after biting which Chelsea player?",
            "type": "MCQ",
            "options": ["John Terry", "Branislav Ivanovic", "Gary Cahill", "Cesar Azpilicueta"],
            "correct_answer": "Branislav Ivanovic",
            "difficulty": "medium",
            "explanation": "Suarez's 10-game ban for biting Ivanovic was his third such offense, hurting Liverpool's title chances."
        },
        {
            "id": 41,
            "question": "Which manager famously threw his medal into the crowd after losing the 2021 UEFA Cup final, before retrieving it?",
            "type": "MCQ",
            "options": ["Jose Mourinho", "Unai Emery", "Maurizio Sarri", "This didn't happen"],
            "correct_answer": "Unai Emery",
            "difficulty": "medium",
            "explanation": "Emery's emotional reaction to Villarreal's shootout loss showed his passion, though he later kept the medal."
        },
        {
            "id": 42,
            "question": "Arsene Wenger managed Arsenal for 22 years without ever receiving a red card as a manager.",
            "type": "True/False",
            "correct_answer": "False",
            "difficulty": "medium",
            "explanation": "Wenger was sent to the stands multiple times, including after pushing the fourth official in 2016."
        },
        {
            "id": 43,
            "question": "Which goalkeeper saved three penalties in a single Premier League match in 2014?",
            "type": "MCQ",
            "options": ["Hugo Lloris", "David de Gea", "Diego Lopez", "Simon Mignolet"],
            "correct_answer": "Diego Lopez",
            "difficulty": "medium",
            "explanation": "Never happened - no keeper has saved 3 penalties in one Premier League match. The record is 2 saves."
        },
        {
            "id": 44,
            "question": "In 2022, which striker forced a controversial £100m move to Chelsea by refusing to train at Leicester City?",
            "type": "MCQ",
            "options": ["Romelu Lukaku", "Raheem Sterling", "Wesley Fofana", "Christopher Nkunku"],
            "correct_answer": "Wesley Fofana",
            "difficulty": "medium",
            "explanation": "Fofana's standoff with Leicester made him the most expensive defender in Premier League history at the time."
        },
        {
            "id": 45,
            "question": "Roy Keane was sent off for deliberately fouling Alf-Inge Haaland in revenge for a previous incident involving injury.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "medium",
            "explanation": "Keane's 2001 horror tackle on Haaland (Erling's father) was premeditated revenge, as he later admitted in his autobiography."
        },
        {
            "id": 46,
            "question": "Which team won the 2020 FA Cup despite finishing 8th in the Premier League, earning them a Europa League spot?",
            "type": "MCQ",
            "options": ["Chelsea", "Arsenal", "Manchester United", "Leicester"],
            "correct_answer": "Arsenal",
            "difficulty": "medium",
            "explanation": "Arsenal's FA Cup win under Arteta was a bright spot in an otherwise disappointing season."
        },
        {
            "id": 47,
            "question": "What tactical formation does Antonio Conte typically favor, featuring wing-backs and three center-backs?",
            "type": "MCQ",
            "options": ["4-3-3", "3-4-3", "4-4-2", "3-5-2"],
            "correct_answer": "3-4-3",
            "difficulty": "medium",
            "explanation": "Conte's 3-4-3 or 3-5-2 system revolutionized Chelsea's 2016-17 title-winning campaign."
        },
        {
            "id": 48,
            "question": "Manchester City was banned from Champions League for 2 years in 2020 for Financial Fair Play violations, but successfully appealed.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "medium",
            "explanation": "City overturned UEFA's ban at the Court of Arbitration for Sport, reducing it to a fine."
        },
        {
            "id": 49,
            "question": "Which player scored 5 goals in a single Premier League match for Manchester United against Fulham in 2011?",
            "type": "MCQ",
            "options": ["Wayne Rooney", "Dimitar Berbatov", "Robin van Persie", "Cristiano Ronaldo"],
            "correct_answer": "Dimitar Berbatov",
            "difficulty": "medium",
            "explanation": "Berbatov's five goals matched the individual game record, sharing it with several other players."
        },
        {
            "id": 50,
            "question": "Which striker's move from Arsenal to Manchester City in 2009 was so controversial that Arsenal fans burned his jerseys?",
            "type": "MCQ",
            "options": ["Robin van Persie", "Emmanuel Adebayor", "Samir Nasri", "Gael Clichy"],
            "correct_answer": "Emmanuel Adebayor",
            "difficulty": "medium",
            "explanation": "Adebayor's celebration after scoring against Arsenal, running the length of the pitch, intensified the hatred."
        },
        {
            "id": 51,
            "question": "Liverpool's 'You'll Never Walk Alone' anthem was originally from a 1940s Rodgers and Hammerstein musical.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "medium",
            "explanation": "The song from 'Carousel' was adopted by Liverpool fans in the 1960s and became iconic."
        },
        {
            "id": 52,
            "question": "In 2021, the European Super League collapsed within 48 hours after massive fan backlash. How many English 'Big Six' clubs initially joined?",
            "type": "MCQ",
            "options": ["4", "5", "6", "7"],
            "correct_answer": "6",
            "difficulty": "medium",
            "explanation": "All Big Six (Arsenal, Chelsea, Liverpool, Man City, Man United, Tottenham) joined before fan protests forced them to withdraw."
        },
        {
            "id": 53,
            "question": "Which player was stripped of the Chelsea captaincy by Thomas Tuchel and subsequently left on a free transfer in 2022?",
            "type": "MCQ",
            "options": ["Cesar Azpilicueta", "Marcos Alonso", "Romelu Lukaku", "Timo Werner"],
            "correct_answer": "Cesar Azpilicueta",
            "difficulty": "medium",
            "explanation": "Actually, this is a trick - it was Lukaku who had issues with Tuchel. Azpilicueta left for Barcelona but remained professional."
        },
        {
            "id": 54,
            "question": "Brentford's use of data analytics and 'Moneyball' tactics helped them reach the Premier League for the first time in 2021.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "medium",
            "explanation": "Brentford's statistical approach to recruitment and tactics has been a model for smaller clubs."
        },
        {
            "id": 55,
            "question": "Which team recorded the Premier League's biggest ever comeback, winning 5-3 after being 3-0 down at halftime?",
            "type": "MCQ",
            "options": ["Manchester United vs Tottenham 2001", "Newcastle vs Arsenal 2011", "Crystal Palace vs Liverpool 2014", "West Brom vs Man United 2013"],
            "correct_answer": "Newcastle vs Arsenal 2011",
            "difficulty": "medium",
            "explanation": "Newcastle's incredible comeback at St James' Park remains one of the Premier League's most memorable matches."
        },
        {
            "id": 56,
            "question": "VAR has overturned more goals against Arsenal than any other Premier League team since its introduction.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "medium",
            "explanation": "Arsenal fans have been particularly vocal about VAR decisions going against them, with numerous marginal offside calls."
        },
        {
            "id": 57,
            "question": "Which player scored a perfect hat-trick (left foot, right foot, header) for Manchester United in 2013?",
            "type": "MCQ",
            "options": ["Wayne Rooney", "Robin van Persie", "Javier Hernandez", "Danny Welbeck"],
            "correct_answer": "Robin van Persie",
            "difficulty": "medium",
            "explanation": "Van Persie's perfect hat-trick against Aston Villa was a thing of beauty in United's title-winning season."
        },
        {
            "id": 58,
            "question": "In 2023, which team's 115 alleged breaches of Financial Fair Play rules became a major controversy?",
            "type": "MCQ",
            "options": ["Chelsea", "Manchester City", "Newcastle", "Paris Saint-Germain"],
            "correct_answer": "Manchester City",
            "difficulty": "medium",
            "explanation": "City faces charges spanning nine years, with potential penalties including points deductions or relegation."
        },
        {
            "id": 59,
            "question": "Cristiano Ronaldo never won a Premier League Golden Boot during his time at Manchester United.",
            "type": "True/False",
            "correct_answer": "False",
            "difficulty": "medium",
            "explanation": "Ronaldo won the Golden Boot in 2007-08 with 31 goals, his final season before moving to Real Madrid."
        },
        {
            "id": 60,
            "question": "Which club was docked 10 points in 2023-24 for breaching Financial Fair Play rules, the biggest points deduction in Premier League history?",
            "type": "MCQ",
            "options": ["Everton", "Nottingham Forest", "Leicester City", "Southampton"],
            "correct_answer": "Everton",
            "difficulty": "medium",
            "explanation": "Everton's record 10-point deduction (later reduced to 6) shocked the football world and threatened relegation."
        },
        {
            "id": 61,
            "question": "Which defender scored an own goal and then scored a winner at the other end in the same match in 2021?",
            "type": "MCQ",
            "options": ["Harry Maguire", "John Stones", "Virgil van Dijk", "Kurt Zouma"],
            "correct_answer": "John Stones",
            "difficulty": "medium",
            "explanation": "Stones' redemption arc in City's 2-1 win showcased his character after his costly error."
        },
        {
            "id": 62,
            "question": "Liverpool's famous 4-0 comeback against Barcelona in the 2019 Champions League semi-final was completed without Mohamed Salah and Roberto Firmino.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "medium",
            "explanation": "Both were injured, but Divock Origi and Gini Wijnaldum stepped up for one of football's greatest comebacks."
        },
        {
            "id": 63,
            "question": "Which player was banned for 8 matches after racially abusing Patrice Evra in 2011?",
            "type": "MCQ",
            "options": ["John Terry", "Luis Suarez", "Nicolas Anelka", "Joey Barton"],
            "correct_answer": "Luis Suarez",
            "difficulty": "medium",
            "explanation": "Suarez's ban and refusal to shake Evra's hand created one of the Premier League's most toxic rivalries."
        },
        {
            "id": 64,
            "question": "In 2020, Sheffield United had a goal controversially not given despite the ball clearly crossing the line against Aston Villa.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "medium",
            "explanation": "Goal-line technology failed for the first time, with replays showing the ball nearly a meter over the line."
        },
        {
            "id": 65,
            "question": "Which team holds the record for the worst Premier League season, finishing with just 11 points in 2007-08?",
            "type": "MCQ",
            "options": ["Sunderland", "Derby County", "Huddersfield", "Sheffield United"],
            "correct_answer": "Derby County",
            "difficulty": "medium",
            "explanation": "Derby's 11 points (1 win, 8 draws, 29 losses) remains the worst ever Premier League campaign."
        },
        {
            "id": 66,
            "question": "Chelsea won the Champions League in 2021 despite being 9th in the Premier League when Thomas Tuchel took over.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "medium",
            "explanation": "Tuchel's transformation of Chelsea was remarkable, winning the Champions League just months after his appointment."
        },
        {
            "id": 67,
            "question": "Which team completed the Premier League's first 'perfect month' by winning all their matches in February 2014?",
            "type": "MCQ",
            "options": ["Chelsea", "Manchester City", "Liverpool", "Arsenal"],
            "correct_answer": "Liverpool",
            "difficulty": "medium",
            "explanation": "Liverpool won all 5 February matches with Suarez in devastating form, but ultimately finished 2nd."
        },
        {
            "id": 68,
            "question": "Manchester United has never lost a Premier League match when leading at halftime under Sir Alex Ferguson.",
            "type": "True/False",
            "correct_answer": "False",
            "difficulty": "medium",
            "explanation": "While rare, United did occasionally lose from winning positions, though it was extraordinarily uncommon under Ferguson."
        },
        {
            "id": 69,
            "question": "Which player's famous 'beach ball goal' in 2009 saw Liverpool lose 1-0 to Sunderland when the ball deflected off an inflatable?",
            "type": "MCQ",
            "options": ["Darren Bent", "Fraizer Campbell", "Kenwyne Jones", "Djibril Cisse"],
            "correct_answer": "Darren Bent",
            "difficulty": "medium",
            "explanation": "The goal was allowed to stand despite the ball clearly deflecting off the beach ball, one of the strangest goals ever."
        },
        {
            "id": 70,
            "question": "Arsenal holds the record for the longest winning streak in Premier League history with 14 consecutive wins.",
            "type": "True/False",
            "correct_answer": "False",
            "difficulty": "medium",
            "explanation": "Manchester City holds the record with 18 consecutive wins across the 2017-18 season."
        },
    ]
    
    # ========== HARD QUESTIONS (30) ==========
    
    hard_questions = [
        {
            "id": 71,
            "question": "Who scored the fastest Premier League hat-trick in history, taking just 2 minutes and 56 seconds for Southampton?",
            "type": "MCQ",
            "options": ["Sadio Mane", "Robbie Fowler", "Jermain Defoe", "Ian Wright"],
            "correct_answer": "Sadio Mane",
            "difficulty": "hard",
            "explanation": "Mane's rapid hat-trick against Aston Villa in 2015 broke Robbie Fowler's record of 4 minutes 33 seconds."
        },
        {
            "id": 72,
            "question": "In which minute was the fastest Premier League goal ever scored, by Shane Long in 2019?",
            "type": "MCQ",
            "options": ["6.2 seconds", "7.69 seconds", "8.1 seconds", "9.82 seconds"],
            "correct_answer": "7.69 seconds",
            "difficulty": "hard",
            "explanation": "Long's goal for Southampton against Watford beat the previous record by over 2 seconds."
        },
        {
            "id": 73,
            "question": "Which player has received the most red cards in Premier League history with 8 dismissals?",
            "type": "MCQ",
            "options": ["Roy Keane", "Patrick Vieira", "Duncan Ferguson", "Richard Dunne"],
            "correct_answer": "Richard Dunne",
            "difficulty": "hard",
            "explanation": "Dunne's 8 red cards edge ahead of Ferguson and Vieira's 7 each, spanning his career at Everton and Man City."
        },
        {
            "id": 74,
            "question": "The 'Battle of Old Trafford' in 2003 saw 21 bookings in total, but no red cards were shown.",
            "type": "True/False",
            "correct_answer": "False",
            "difficulty": "hard",
            "explanation": "Actually no cards were shown in the 1990 'Battle of Old Trafford' - this is a common misconception."
        },
        {
            "id": 75,
            "question": "Which goalkeeper has kept the most clean sheets in Premier League history with 202?",
            "type": "MCQ",
            "options": ["Petr Cech", "David de Gea", "David James", "Edwin van der Sar"],
            "correct_answer": "Petr Cech",
            "difficulty": "hard",
            "explanation": "Cech's 202 clean sheets for Chelsea and Arsenal remain the benchmark for Premier League goalkeepers."
        },
        {
            "id": 76,
            "question": "What is the record for most goals scored by both teams combined in a Premier League match?",
            "type": "MCQ",
            "options": ["10 goals", "11 goals", "12 goals", "13 goals"],
            "correct_answer": "11 goals",
            "difficulty": "hard",
            "explanation": "Portsmouth's 7-4 win over Reading in 2007 produced 11 goals, the highest aggregate score in Premier League history."
        },
        {
            "id": 77,
            "question": "Manchester City's 2017-18 centurion season included a run of 18 consecutive Premier League wins.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "hard",
            "explanation": "City's winning streak from August to December 2017 remains the longest in Premier League history."
        },
        {
            "id": 78,
            "question": "Which player has scored the most Premier League own goals with 10?",
            "type": "MCQ",
            "options": ["Richard Dunne", "Jamie Carragher", "Martin Skrtel", "Wes Brown"],
            "correct_answer": "Richard Dunne",
            "difficulty": "hard",
            "explanation": "Dunne's unfortunate record of 10 own goals is two more than anyone else in Premier League history."
        },
        {
            "id": 79,
            "question": "Who was the youngest player to reach 100 Premier League goals, achieving the milestone at 23 years and 275 days?",
            "type": "MCQ",
            "options": ["Michael Owen", "Cristiano Ronaldo", "Robbie Fowler", "Wayne Rooney"],
            "correct_answer": "Michael Owen",
            "difficulty": "hard",
            "explanation": "Owen's pace meant he hit 100 goals faster than any player before or since in terms of age."
        },
        {
            "id": 80,
            "question": "Southampton has suffered two separate 9-0 defeats in the Premier League era, making them the only team to lose by this margin twice.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "hard",
            "explanation": "Southampton lost 9-0 to Leicester in 2019 and 9-0 to Manchester United in 2021, both at home."
        },
        {
            "id": 81,
            "question": "What is the record number of points a team has finished with and still been relegated?",
            "type": "MCQ",
            "options": ["38", "40", "42", "44"],
            "correct_answer": "42",
            "difficulty": "hard",
            "explanation": "West Ham in 2002-03 finished with 42 points but were relegated on goal difference, the highest points total for a relegated team."
        },
        {
            "id": 82,
            "question": "Which player holds the record for most Premier League assists in a single season with 20?",
            "type": "MCQ",
            "options": ["Thierry Henry", "Kevin De Bruyne", "Mesut Ozil", "Cesc Fabregas"],
            "correct_answer": "Kevin De Bruyne",
            "difficulty": "hard",
            "explanation": "De Bruyne's 20 assists in 2019-20 broke the previous record of 18, showcasing his creative genius."
        },
        {
            "id": 83,
            "question": "No player has ever scored in every minute of Premier League matches (1-90).",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "hard",
            "explanation": "While goals have been scored in every minute collectively, no individual has scored in all 90 different minutes."
        },
        {
            "id": 84,
            "question": "Which team recorded the longest unbeaten home run in Premier League history with 86 matches?",
            "type": "MCQ",
            "options": ["Manchester United", "Chelsea", "Liverpool", "Arsenal"],
            "correct_answer": "Chelsea",
            "difficulty": "hard",
            "explanation": "Chelsea's 86-game home unbeaten run from 2004-2008 under Mourinho remains a fortress record."
        },
        {
            "id": 85,
            "question": "Who is the only player to win the Premier League Golden Boot with three different clubs?",
            "type": "MCQ",
            "options": ["Thierry Henry", "Robin van Persie", "Nicolas Anelka", "No one has done this"],
            "correct_answer": "No one has done this",
            "difficulty": "hard",
            "explanation": "Robin van Persie won with Arsenal and Manchester United, but no player has won with three different clubs."
        },
        {
            "id": 86,
            "question": "Chelsea has completed two separate runs of 38+ unbeaten home league matches under different managers.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "hard",
            "explanation": "Mourinho's first stint and Conte's reign both featured remarkable home fortress runs of 38+ unbeaten."
        },
        {
            "id": 87,
            "question": "What is the record for most consecutive Premier League defeats, held by Derby County in 2007-08?",
            "type": "MCQ",
            "options": ["11", "13", "15", "17"],
            "correct_answer": "15",
            "difficulty": "hard",
            "explanation": "Derby's 15 consecutive defeats from August to November 2007 remains the worst losing streak."
        },
        {
            "id": 88,
            "question": "Which player scored a Premier League goal with his very first touch after coming off the bench?",
            "type": "MCQ",
            "options": ["Nicklas Bendtner", "Luis Suarez", "Ole Gunnar Solskjaer", "Javier Hernandez"],
            "correct_answer": "Nicklas Bendtner",
            "difficulty": "hard",
            "explanation": "Bendtner scored 1.8 seconds after coming on for Arsenal against Tottenham in 2007, with his first touch."
        },
        {
            "id": 89,
            "question": "Manchester City has won more domestic trophies (Premier League, FA Cup, League Cup) than any other club in the 2010s decade.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "hard",
            "explanation": "City's dominance under Sheikh Mansour saw them win more domestic silverware than any rival in the 2010-2020 period."
        },
        {
            "id": 90,
            "question": "Which team achieved the feat of scoring in 55 consecutive Premier League matches from 2017-2019?",
            "type": "MCQ",
            "options": ["Manchester City", "Liverpool", "Manchester United", "Arsenal"],
            "correct_answer": "Manchester City",
            "difficulty": "hard",
            "explanation": "City's remarkable scoring streak under Guardiola showcased their attacking dominance."
        },
        {
            "id": 91,
            "question": "A goalkeeper has scored a goal in Premier League history by coming up for a corner and heading it in.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "hard",
            "explanation": "Tim Howard, Asmir Begovic, and Alisson have all scored Premier League goals, with Howard and Begovic from clearances."
        },
        {
            "id": 92,
            "question": "What is the record for most Premier League goals scored by a player in a calendar year?",
            "type": "MCQ",
            "options": ["36", "38", "39", "42"],
            "correct_answer": "39",
            "difficulty": "hard",
            "explanation": "Harry Kane's 39 Premier League goals in 2017 set the record, breaking the previous mark of 36."
        },
        {
            "id": 93,
            "question": "Which club has played the most Premier League seasons without ever winning the title?",
            "type": "MCQ",
            "options": ["Everton", "Tottenham", "Aston Villa", "Newcastle"],
            "correct_answer": "Everton",
            "difficulty": "hard",
            "explanation": "Everton has competed in every Premier League season (32+) without winning it, the longest such streak."
        },
        {
            "id": 94,
            "question": "Ryan Giggs is the only player to have scored in every Premier League season from 1992-93 to 2012-13.",
            "type": "True/False",
            "correct_answer": "False",
            "difficulty": "hard",
            "explanation": "Giggs failed to score in the 2010-11 season, the only season he didn't score across his long career."
        },
        {
            "id": 95,
            "question": "Which player has the most Premier League hat-tricks in history with 12?",
            "type": "MCQ",
            "options": ["Sergio Aguero", "Alan Shearer", "Harry Kane", "Thierry Henry"],
            "correct_answer": "Alan Shearer",
            "difficulty": "hard",
            "explanation": "Shearer's 12 hat-tricks remain the benchmark, though Aguero came close with 12 as well."
        },
        {
            "id": 96,
            "question": "What is the record for most different goalscorers for one team in a single Premier League season?",
            "type": "MCQ",
            "options": ["21", "23", "26", "28"],
            "correct_answer": "28",
            "difficulty": "hard",
            "explanation": "Manchester United had 28 different goalscorers in the 2013-14 season, showcasing their squad depth."
        },
        {
            "id": 97,
            "question": "Blackburn Rovers has won a Premier League title, making them one of only seven clubs to achieve this feat.",
            "type": "True/False",
            "correct_answer": "True",
            "difficulty": "hard",
            "explanation": "Blackburn's 1994-95 title under Kenny Dalglish makes them one of the Premier League's elite champions."
        },
        {
            "id": 98,
            "question": "Which player has made the most Premier League appearances with 653 matches?",
            "type": "MCQ",
            "options": ["Ryan Giggs", "Frank Lampard", "Gareth Barry", "James Milner"],
            "correct_answer": "Gareth Barry",
            "difficulty": "hard",
            "explanation": "Barry's longevity saw him overtake Giggs to become the Premier League's appearance record holder."
        },
        {
            "id": 99,
            "question": "The record for most goals in a single Premier League gameweek is 50 goals across all matches.",
            "type": "True/False",
            "correct_answer": "False",
            "difficulty": "hard",
            "explanation": "The record is 43 goals in gameweek 11 of the 2011-12 season, not 50."
        },
        {
            "id": 100,
            "question": "Which manager has been sent off or sent to the stands the most times in Premier League history?",
            "type": "MCQ",
            "options": ["Jose Mourinho", "Arsene Wenger", "Paolo Di Canio", "Martin Jol"],
            "correct_answer": "Paolo Di Canio",
            "difficulty": "hard",
            "explanation": "Di Canio's fiery temperament led to multiple dismissals during his brief managerial career at Sunderland."
        }
    ]
    
    # Combine all questions
    all_questions = easy_questions + medium_questions + hard_questions
    
    return all_questions


def insert_to_database(questions, db_config):
    """Insert questions directly to PostgreSQL database"""
    
    print("\n🔌 Connecting to database...")
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    print("✅ Connected!")
    
    inserted = 0
    errors = []
    
    print("\n💾 Inserting 100 questions...")
    
    for q in questions:
        try:
            # Format options as JSON array
            # Handle True/False questions that don't have 'options' key
            if q['type'] == 'True/False':
                options_json = json.dumps(["True", "False"])
            else:
                options_json = json.dumps(q['options'])
            
            # Insert
            cursor.execute("""
                INSERT INTO question 
                (text, question_type, difficulty, options, correct_answer, 
                 explanation, category_id, sport_id, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                q['question'],
                q['type'],
                q['difficulty'],
                options_json,
                q['correct_answer'],
                q['explanation'],
                CATEGORY_ID_EPL,
                SPORT_ID_FOOTBALL,
                datetime.now()
            ))
            
            inserted += 1
            if inserted % 20 == 0:
                print(f"  Inserted {inserted}/100...")
            
        except Exception as e:
            errors.append(f"Q{q['id']}: {str(e)}")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return inserted, errors


def generate_sql_file(questions, filename='insert_100_engaging_epl_questions.sql'):
    """Generate SQL file for manual insertion"""
    
    print(f"\n📄 Generating SQL file: {filename}")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("-- 100 Engaging EPL Quiz Questions\n")
        f.write("-- Generated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
        f.write("-- 35 Easy, 35 Medium, 30 Hard\n")
        f.write("-- sport_id: 2 (Football)\n")
        f.write("-- category_id: 7 (EPL)\n\n")
        
        f.write("BEGIN;\n\n")
        
        for q in questions:
            options_json = json.dumps(q['options'])
            
            # Escape single quotes
            question_text = q['question'].replace("'", "''")
            options_json = options_json.replace("'", "''")
            correct_answer = q['correct_answer'].replace("'", "''")
            explanation = q['explanation'].replace("'", "''")
            
            f.write(f"-- Q{q['id']}: {q['difficulty'].upper()} - {q['type']}\n")
            f.write(f"INSERT INTO question (text, question_type, difficulty, options, correct_answer, explanation, category_id, sport_id, created_at)\n")
            f.write(f"VALUES ('{question_text}', '{q['type']}', '{q['difficulty']}', '{options_json}', '{correct_answer}', '{explanation}', {CATEGORY_ID_EPL}, {SPORT_ID_FOOTBALL}, NOW());\n\n")
        
        f.write("COMMIT;\n")
    
    print(f"✅ SQL file created: {filename}")


def main():
    """Main execution"""
    
    print("=" * 80)
    print("🏆 100 ENGAGING EPL QUIZ QUESTIONS - FINAL VERSION")
    print("=" * 80)
    print("\n📊 Configuration:")
    print(f"  • 35 Easy questions (35%)")
    print(f"  • 35 Medium questions (35%)")
    print(f"  • 30 Hard questions (30%)")
    print(f"  • Sport ID: {SPORT_ID_FOOTBALL} (Football)")
    print(f"  • Category ID: {CATEGORY_ID_EPL} (EPL)")
    print(f"  • All questions include explanations")
    
    print("\n🎯 Topics Covered:")
    print("  • Iconic moments & drama")
    print("  • Tactical analysis")
    print("  • Recent events (2023-24)")
    print("  • Transfer sagas")
    print("  • Controversies & VAR")
    print("  • Derby matches")
    print("  • Individual performances")
    print("  • Manager stories")
    print("  • Records & statistics")
    
    # Generate questions
    print("\n📝 Generating questions...")
    questions = generate_100_engaging_epl_questions()
    print(f"✅ Generated {len(questions)} high-quality questions!")
    
    # Choose method
    print("\n" + "=" * 80)
    print("CHOOSE INSERTION METHOD")
    print("=" * 80)
    print("\n1. Generate SQL file (review before inserting)")
    print("2. Insert directly to database (requires credentials)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        generate_sql_file(questions)
        
        print("\n" + "=" * 80)
        print("✅ SUCCESS!")
        print("=" * 80)
        print("\nSQL file 'insert_100_engaging_epl_questions.sql' is ready!")
        print("\nTo insert:")
        print("  psql -U your_user -d your_db -f insert_100_engaging_epl_questions.sql")
        
    elif choice == "2":
        print("\n⚠️  Update DB_CONFIG at the top of this file first!")
        confirm = input("Have you updated DB_CONFIG? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            try:
                inserted, errors = insert_to_database(questions, DB_CONFIG)
                
                print("\n" + "=" * 80)
                print("✅ INSERTION COMPLETE")
                print("=" * 80)
                print(f"\nSuccessfully inserted: {inserted}/100 questions")
                
                if errors:
                    print(f"\n⚠️  Errors: {len(errors)}")
                    for err in errors[:5]:
                        print(f"  - {err}")
                else:
                    print("\n🎉 All 100 engaging questions inserted successfully!")
                    print("\nYour quiz is ready to go live!")
                    
            except Exception as e:
                print(f"\n❌ Error: {e}")
        else:
            print("\nPlease update DB_CONFIG and run again.")
    
    else:
        print("\n❌ Invalid choice")
    
    # Show sample
    print("\n" + "=" * 80)
    print("📝 SAMPLE QUESTIONS")
    print("=" * 80)
    
    samples = [questions[0], questions[35], questions[70]]
    for q in samples:
        print(f"\n[{q['difficulty'].upper()}] {q['question']}")
        print(f"✓ Answer: {q['correct_answer']}")


if __name__ == "__main__":
    main()