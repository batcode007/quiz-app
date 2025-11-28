import requests
from bs4 import BeautifulSoup
import json
import re
import pandas as pd
from datetime import datetime
import time

class SporcleQuizExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        })
    
    def extract_quiz_data_from_html(self, html_content):
        """Extract quiz answer data from HTML"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        quiz_data = {
            'title': None,
            'description': None,
            'creator': None,
            'answers': [],
            'answer_count': 0
        }
        
        # Extract basic info
        title = soup.find('h1', class_='quiz-name')
        if title:
            quiz_data['title'] = title.text.strip()
        
        description = soup.find('h2', class_='quiz-description')
        if description:
            button = description.find('button')
            if button:
                button.decompose()
            quiz_data['description'] = description.text.strip()
        
        creator = soup.find('div', class_='creator')
        if creator:
            creator_link = creator.find('a')
            if creator_link:
                quiz_data['creator'] = creator_link.text.strip()
        
        print(f"\n{'='*70}")
        print(f"QUIZ: {quiz_data['title']}")
        print(f"{'='*70}")
        
        # Find script tags containing answer data
        scripts = soup.find_all('script')
        
        for script in scripts:
            if not script.string:
                continue
            
            script_text = script.string
            
            # Look for answer patterns
            if 'answers' in script_text.lower() or 'gameanswers' in script_text.lower():
                
                # Try common patterns
                patterns = [
                    r'var\s+gameAnswers\s*=\s*(\[.*?\]);',
                    r'var\s+answers\s*=\s*(\[.*?\]);',
                    r'"answers":\s*(\[.*?\])',
                    r'answers:\s*(\[.*?\])',
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, script_text, re.DOTALL)
                    if match:
                        try:
                            json_str = match.group(1)
                            answers = json.loads(json_str)
                            
                            if isinstance(answers, list) and len(answers) > 0:
                                # Extract text from answers
                                extracted = []
                                for ans in answers:
                                    if isinstance(ans, str):
                                        extracted.append(ans)
                                    elif isinstance(ans, dict):
                                        if 'text' in ans:
                                            extracted.append(ans['text'])
                                        elif 'answer' in ans:
                                            extracted.append(ans['answer'])
                                
                                if extracted:
                                    quiz_data['answers'] = extracted
                                    quiz_data['answer_count'] = len(extracted)
                                    print(f"✅ Extracted {len(extracted)} answers!")
                                    return quiz_data
                                    
                        except json.JSONDecodeError:
                            continue
        
        print("⚠️ Could not extract answers automatically")
        print("Saving scripts for manual inspection...")
        
        with open('quiz_scripts.txt', 'w', encoding='utf-8') as f:
            for i, script in enumerate(scripts):
                if script.string and len(script.string) > 100:
                    f.write(f"\n{'='*70}\n")
                    f.write(f"SCRIPT {i}\n")
                    f.write(f"{'='*70}\n")
                    f.write(script.string)
                    f.write("\n\n")
        
        print("Saved to 'quiz_scripts.txt' - please check manually")
        
        return quiz_data
    
    def scrape_quiz_from_file(self, html_file):
        """Extract from saved HTML file"""
        print(f"\nReading: {html_file}")
        
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        return self.extract_quiz_data_from_html(html_content)
    
    def scrape_quiz_from_url(self, url, delay=3):
        """Extract from URL"""
        print(f"\nFetching: {url}")
        time.sleep(delay)
        
        response = self.session.get(url)
        response.raise_for_status()
        
        return self.extract_quiz_data_from_html(response.text)
    
    def scrape_multiple_quizzes_from_csv(self, csv_file, max_quizzes=None, delay=3):
        """Scrape multiple quizzes from CSV file"""
        print(f"\n{'='*70}")
        print(f"SCRAPING QUIZZES FROM: {csv_file}")
        print(f"{'='*70}")
        
        # Read CSV
        df = pd.read_csv(csv_file)
        quiz_urls = df['url'].tolist()
        
        if max_quizzes:
            quiz_urls = quiz_urls[:max_quizzes]
        
        print(f"Found {len(quiz_urls)} quizzes to scrape")
        
        all_quiz_data = []
        
        for i, url in enumerate(quiz_urls, 1):
            print(f"\n[{i}/{len(quiz_urls)}]")
            
            try:
                quiz_data = self.scrape_quiz_from_url(url, delay)
                all_quiz_data.append(quiz_data)
                
                if quiz_data['answers']:
                    print(f"✅ Success: {quiz_data['answer_count']} answers")
                else:
                    print(f"⚠️ No answers extracted")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
        
        return all_quiz_data
    
    def save_results(self, quiz_data_list, filename_prefix='quiz_answers'):
        """Save quiz data to files"""
        if not quiz_data_list:
            print("\n⚠️ No data to save")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Prepare CSV data
        csv_data = []
        for quiz in quiz_data_list:
            csv_data.append({
                'title': quiz['title'],
                'description': quiz['description'],
                'creator': quiz['creator'],
                'answer_count': quiz['answer_count'],
                'answers': ' | '.join(quiz['answers']) if quiz['answers'] else ''
            })
        
        # Save to CSV
        csv_file = f"{filename_prefix}_{timestamp}.csv"
        df = pd.DataFrame(csv_data)
        df.to_csv(csv_file, index=False, encoding='utf-8')
        print(f"\n✅ Saved to {csv_file}")
        
        # Save to JSON
        json_file = f"{filename_prefix}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(quiz_data_list, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved to {json_file}")
        
        # Save detailed text file
        txt_file = f"{filename_prefix}_detailed_{timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            for quiz in quiz_data_list:
                f.write(f"\n{'='*70}\n")
                f.write(f"QUIZ: {quiz['title']}\n")
                f.write(f"{'='*70}\n")
                f.write(f"Description: {quiz['description']}\n")
                f.write(f"Creator: {quiz['creator']}\n")
                f.write(f"Answer Count: {quiz['answer_count']}\n")
                f.write(f"\nAnswers:\n")
                for i, answer in enumerate(quiz['answers'], 1):
                    f.write(f"{i:3d}. {answer}\n")
                f.write("\n")
        
        print(f"✅ Saved detailed answers to {txt_file}")
        
        # Summary
        print(f"\n{'='*70}")
        print("📊 SUMMARY")
        print(f"{'='*70}")
        print(f"Total quizzes: {len(quiz_data_list)}")
        print(f"Quizzes with answers: {sum(1 for q in quiz_data_list if q['answers'])}")
        print(f"Total answers extracted: {sum(q['answer_count'] for q in quiz_data_list)}")


def main():
    """Main execution"""
    print("=" * 70)
    print("STEP 3: EXTRACT QUIZ ANSWERS")
    print("=" * 70)
    
    extractor = SporcleQuizExtractor()
    
    # METHOD 1: Test with single quiz (from saved HTML)
    print("\nMETHOD 1: Extract from saved quiz page")
    print("-" * 70)
    print("1. Open a quiz URL in browser")
    print("2. Save page as 'quiz_page.html'")
    print("3. Run this script")
    
    try:
        quiz_data = extractor.scrape_quiz_from_file('quiz_page.html')
        
        if quiz_data['answers']:
            print(f"\n✅ SUCCESS!")
            print(f"Extracted {quiz_data['answer_count']} answers")
            print(f"\nFirst 10 answers:")
            for i, ans in enumerate(quiz_data['answers'][:10], 1):
                print(f"  {i}. {ans}")
            
            extractor.save_results([quiz_data], 'single_quiz')
        
    except FileNotFoundError:
        print("\n⚠️ 'quiz_page.html' not found")
    
    # METHOD 2: Extract from multiple quizzes
    print("\n" + "=" * 70)
    print("METHOD 2: Extract from all quizzes in CSV")
    print("=" * 70)
    print("\nUncomment the code below to scrape from all quiz URLs")
    
    # UNCOMMENT TO USE:
    """
    # Load quiz URLs from Step 2
    csv_file = 'sporcle_epl_quizzes_XXXXXXXX.csv'  # Update with your filename
    
    # Scrape first 10 quizzes (for testing)
    all_quiz_data = extractor.scrape_multiple_quizzes_from_csv(
        csv_file, 
        max_quizzes=10,  # Set to None for all quizzes
        delay=3
    )
    
    # Save results
    extractor.save_results(all_quiz_data, 'all_epl_quizzes')
    """
    
    print("\n" + "=" * 70)
    print("INSTRUCTIONS")
    print("=" * 70)
    print("\n1. To test: Save one quiz page as 'quiz_page.html' and run")
    print("2. To extract all: Uncomment METHOD 2 code above")
    print("3. Update the CSV filename with your actual file from Step 2")


if __name__ == "__main__":
    main()