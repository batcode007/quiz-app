import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
from datetime import datetime

class SporcleEPLScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        })
        self.base_url = "https://www.sporcle.com"
    
    def parse_epl_quizzes_from_html(self, html_content):
        """
        Parse EPL quizzes from the specific HTML structure:
        <div class="row">
            <div class="title">
                <a href="/games/..." class="stateful">Quiz Title</a>
            </div>
            <div class="count">123</div>
        </div>
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        print("Parsing HTML for EPL quizzes...")
        
        # Find all quiz rows
        quiz_rows = soup.find_all('div', class_='row')
        
        print(f"Found {len(quiz_rows)} quiz rows")
        
        quizzes = []
        
        for row in quiz_rows:
            try:
                # Find title container
                title_div = row.find('div', class_='title')
                if not title_div:
                    continue
                
                # Find the link
                link = title_div.find('a', class_='stateful')
                if not link:
                    continue
                
                # Extract data
                title = link.text.strip()
                href = link.get('href', '')
                
                # Build full URL
                if href.startswith('/'):
                    full_url = self.base_url + href
                else:
                    full_url = href
                
                # Find count/plays
                count_div = row.find('div', class_='count')
                count = count_div.text.strip() if count_div else 'N/A'
                
                quiz_data = {
                    'title': title,
                    'url': full_url,
                    'count': count,
                    'href': href,
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                quizzes.append(quiz_data)
                
            except Exception as e:
                print(f"Error parsing row: {e}")
                continue
        
        print(f"\n✅ Successfully parsed {len(quizzes)} quizzes")
        
        # Remove duplicates
        seen_urls = set()
        unique_quizzes = []
        for quiz in quizzes:
            if quiz['url'] not in seen_urls:
                unique_quizzes.append(quiz)
                seen_urls.add(quiz['url'])
        
        if len(quizzes) != len(unique_quizzes):
            print(f"   Removed {len(quizzes) - len(unique_quizzes)} duplicates")
        
        return unique_quizzes
    
    def scrape_from_file(self, html_file_path):
        """Scrape quizzes from saved HTML file"""
        print("=" * 70)
        print("SPORCLE EPL QUIZ SCRAPER")
        print("=" * 70)
        print(f"\nReading HTML from: {html_file_path}")
        
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        print(f"HTML file size: {len(html_content)} characters")
        
        # Parse quizzes
        quizzes = self.parse_epl_quizzes_from_html(html_content)
        
        return quizzes
    
    def scrape_from_url(self, url, delay=3):
        """Scrape quizzes directly from URL"""
        print("=" * 70)
        print("SPORCLE EPL QUIZ SCRAPER")
        print("=" * 70)
        print(f"\nFetching URL: {url}")
        
        time.sleep(delay)
        response = self.session.get(url)
        response.raise_for_status()
        
        print(f"Response status: {response.status_code}")
        print(f"Content length: {len(response.text)} characters")
        
        # Parse quizzes
        quizzes = self.parse_epl_quizzes_from_html(response.text)
        
        return quizzes
    
    def scrape_quiz_details(self, quiz_url, delay=3):
        """Scrape detailed information from individual quiz page"""
        print(f"\nFetching quiz details: {quiz_url}")
        
        try:
            time.sleep(delay)
            response = self.session.get(quiz_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            quiz_data = {
                'url': quiz_url,
                'title': None,
                'description': None,
                'difficulty': None,
                'plays': None,
                'rating': None,
                'tags': [],
                'questions_hint': None
            }
            
            # Extract title
            title = soup.find('h1', class_='game-header')
            if not title:
                title = soup.find('h1')
            if title:
                quiz_data['title'] = title.text.strip()
            
            # Extract description
            desc = soup.find('div', class_='description')
            if desc:
                quiz_data['description'] = desc.text.strip()
            
            # Extract stats (plays, rating, etc.)
            stats = soup.find_all('div', class_='stat')
            for stat in stats:
                stat_text = stat.text.lower()
                if 'play' in stat_text:
                    quiz_data['plays'] = stat.text.strip()
                elif 'rating' in stat_text or '/5' in stat_text:
                    quiz_data['rating'] = stat.text.strip()
            
            # Extract tags
            tags = soup.find_all('a', class_='tag')
            quiz_data['tags'] = [tag.text.strip() for tag in tags]
            
            # Try to find question count
            question_info = soup.find(string=lambda text: text and 'question' in text.lower())
            if question_info:
                quiz_data['questions_hint'] = question_info.strip()
            
            return quiz_data
            
        except Exception as e:
            print(f"❌ Error scraping quiz details: {e}")
            return None
    
    def save_results(self, data, filename_prefix='sporcle_epl'):
        """Save results to CSV and JSON"""
        if not data:
            print("\n⚠️ No data to save")
            return None, None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save to CSV
        csv_file = f"{filename_prefix}_{timestamp}.csv"
        df = pd.DataFrame(data)
        df.to_csv(csv_file, index=False, encoding='utf-8')
        print(f"\n✅ Saved {len(data)} quizzes to {csv_file}")
        
        # Save to JSON
        json_file = f"{filename_prefix}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved to {json_file}")
        
        # Print summary
        print(f"\n{'='*70}")
        print("📊 SUMMARY")
        print(f"{'='*70}")
        print(f"Total quizzes: {len(data)}")
        
        if 'count' in df.columns:
            print(f"\nTop 10 most popular quizzes (by count):")
            # Convert count to numeric for sorting
            df['count_numeric'] = pd.to_numeric(df['count'], errors='coerce')
            top_quizzes = df.nlargest(10, 'count_numeric')
            for idx, row in top_quizzes.iterrows():
                print(f"  {row['count']:>6} - {row['title']}")
        
        print(f"\n{'='*70}")
        
        return csv_file, json_file
    
    def display_sample(self, quizzes, n=10):
        """Display sample quiz data"""
        print(f"\n{'='*70}")
        print(f"SAMPLE QUIZZES (showing {min(n, len(quizzes))} of {len(quizzes)})")
        print(f"{'='*70}")
        
        for i, quiz in enumerate(quizzes[:n], 1):
            print(f"\n{i}. {quiz['title']}")
            print(f"   URL: {quiz['url']}")
            print(f"   Count: {quiz.get('count', 'N/A')}")


def main():
    """Main execution function"""
    scraper = SporcleEPLScraper()
    
    # Method 1: Scrape from saved HTML file (RECOMMENDED)
    print("\n" + "=" * 70)
    print("METHOD 1: SCRAPING FROM SAVED HTML FILE")
    print("=" * 70)
    
    try:
        quizzes = scraper.scrape_from_file('sporcle_page.html')
        
        if quizzes:
            # Display sample
            scraper.display_sample(quizzes, n=10)
            
            # Save results
            csv_file, json_file = scraper.save_results(quizzes, 'sporcle_epl_quizzes')
            
            # Ask if user wants to scrape details
            print("\n" + "=" * 70)
            print("NEXT STEP: SCRAPE QUIZ DETAILS?")
            print("=" * 70)
            print("\nDo you want to fetch detailed information for each quiz?")
            print("This will:")
            print("  - Take longer (3-5 seconds per quiz)")
            print("  - Get descriptions, ratings, tags, etc.")
            print(f"  - Process all {len(quizzes)} quizzes")
            
            # For demo, let's just do first 5
            print("\nScraping details for first 5 quizzes (demo)...")
            detailed_quizzes = []
            
            for i, quiz in enumerate(quizzes[:5], 1):
                print(f"\nProcessing {i}/5: {quiz['title']}")
                details = scraper.scrape_quiz_details(quiz['url'])
                if details:
                    # Merge original data with details
                    merged = {**quiz, **details}
                    detailed_quizzes.append(merged)
            
            if detailed_quizzes:
                scraper.save_results(detailed_quizzes, 'sporcle_epl_detailed')
            
            print("\n" + "=" * 70)
            print("✅ SCRAPING COMPLETE!")
            print("=" * 70)
            print(f"\nFiles created:")
            print(f"  1. {csv_file} - All quiz listings")
            print(f"  2. sporcle_epl_detailed_*.csv - Detailed info (5 quizzes)")
            
            print(f"\n🎯 Next steps:")
            print(f"  1. Review the CSV files")
            print(f"  2. To get ALL quiz details, modify line in code:")
            print(f"     Change: for quiz in quizzes[:5]")
            print(f"     To:     for quiz in quizzes")
            print(f"  3. To extract actual quiz questions, we'll need to:")
            print(f"     - Inspect individual quiz pages")
            print(f"     - Look for question data (might need Selenium)")
            
            return quizzes
            
        else:
            print("\n❌ No quizzes found in HTML file")
            print("Please check that 'sporcle_page.html' contains the quiz listing page")
            return None
            
    except FileNotFoundError:
        print("\n❌ File 'sporcle_page.html' not found!")
        print("\nPlease:")
        print("  1. Save your Postman response as 'sporcle_page.html'")
        print("  2. Make sure it's in the same directory as this script")
        print("  3. Run this script again")
        return None
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


# Alternative: Scrape directly from URL
def scrape_from_url_directly():
    """Try to scrape directly from URL (might not work due to bot detection)"""
    scraper = SporcleEPLScraper()
    
    url = "https://www.sporcle.com/games/subcategory/premierleague/alltime"
    
    try:
        quizzes = scraper.scrape_from_url(url)
        
        if quizzes:
            scraper.display_sample(quizzes)
            scraper.save_results(quizzes, 'sporcle_epl_direct')
            return quizzes
        else:
            print("\n⚠️ No quizzes found. The page might require JavaScript.")
            print("Please use the HTML file method instead.")
            return None
            
    except Exception as e:
        print(f"\n❌ Direct scraping failed: {e}")
        print("\nThis is expected if Sporcle has bot protection.")
        print("Please use the HTML file method instead.")
        return None


if __name__ == "__main__":
    # Run main scraper (from HTML file)
    quizzes = main()
    
    # Uncomment below to try direct URL scraping
    # quizzes = scrape_from_url_directly()