#!/usr/bin/env python3
"""
Verify and fix business data by scraping their actual websites
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from sqlalchemy import text
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.database import SessionLocal

def clean_phone(phone_text):
    """Extract and clean phone number from text"""
    if not phone_text:
        return None
    
    # Look for phone patterns
    phone_patterns = [
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (808) 123-4567 or 808-123-4567
        r'\d{3}[-.\s]\d{3}[-.\s]\d{4}',          # 808 123 4567
    ]
    
    for pattern in phone_patterns:
        match = re.search(pattern, phone_text)
        if match:
            # Extract just the numbers
            numbers = re.sub(r'\D', '', match.group())
            if len(numbers) == 10:
                return f"({numbers[:3]}) {numbers[3:6]}-{numbers[6:]}"
    
    return None

def scrape_website_info(url, company_name):
    """Scrape a website to extract contact information"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract phone numbers from the page
        page_text = soup.get_text()
        phone = clean_phone(page_text)
        
        # Look for contact or about page links
        contact_links = []
        for link in soup.find_all('a', href=True):
            href = link['href'].lower()
            text = link.get_text().lower()
            if any(word in href or word in text for word in ['contact', 'about', 'location', 'info']):
                if href.startswith('http'):
                    contact_links.append(href)
                elif href.startswith('/'):
                    from urllib.parse import urljoin
                    contact_links.append(urljoin(url, href))
        
        # Try to get more specific contact info from contact pages
        if contact_links and not phone:
            for contact_url in contact_links[:2]:  # Try first 2 contact pages
                try:
                    contact_response = requests.get(contact_url, headers=headers, timeout=10)
                    contact_soup = BeautifulSoup(contact_response.content, 'html.parser')
                    contact_text = contact_soup.get_text()
                    phone = clean_phone(contact_text)
                    if phone:
                        break
                except:
                    continue
        
        # Extract business description from meta tags or first paragraph
        description = ""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            description = meta_desc['content'][:200]
        else:
            # Try to find the first meaningful paragraph
            paragraphs = soup.find_all('p')
            for p in paragraphs:
                text = p.get_text().strip()
                if len(text) > 50 and company_name.lower() in text.lower():
                    description = text[:200]
                    break
        
        return {
            'phone': phone,
            'description': description,
            'status': 'success'
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'phone': None,
            'description': None,
            'status': f'error: {str(e)}',
            'working': False
        }
    except Exception as e:
        return {
            'phone': None,
            'description': None,
            'status': f'parsing error: {str(e)}',
            'working': False
        }

def verify_all_businesses():
    """Verify and update all business information"""
    db = SessionLocal()
    
    try:
        # Get all companies
        companies = db.execute(text("SELECT id, name, website, phone, description FROM companies")).fetchall()
        
        print(f"Verifying {len(companies)} businesses...")
        
        updated_count = 0
        working_websites = 0
        
        for company in companies:
            company_id, name, website, current_phone, current_desc = company
            print(f"\n{name}:")
            print(f"  Website: {website}")
            
            if not website:
                print("  ❌ No website to verify")
                continue
                
            # Scrape the website
            scraped_info = scrape_website_info(website, name)
            
            if scraped_info['status'] == 'success':
                working_websites += 1
                print("  ✅ Website is working")
                
                # Update phone if we found a better one
                if scraped_info['phone'] and scraped_info['phone'] != current_phone:
                    db.execute(text("UPDATE companies SET phone = :phone WHERE id = :id"), {
                        'phone': scraped_info['phone'],
                        'id': company_id
                    })
                    print(f"  📞 Updated phone: {scraped_info['phone']}")
                    updated_count += 1
                elif scraped_info['phone']:
                    print(f"  📞 Phone verified: {scraped_info['phone']}")
                else:
                    print("  📞 No phone found on website")
                
                # Update description if we found a better one
                if scraped_info['description'] and len(scraped_info['description']) > len(current_desc or ''):
                    db.execute(text("UPDATE companies SET description = :desc WHERE id = :id"), {
                        'desc': scraped_info['description'],
                        'id': company_id
                    })
                    print(f"  📝 Updated description")
                    updated_count += 1
                    
            else:
                print(f"  ❌ Website issue: {scraped_info['status']}")
                
            time.sleep(1)  # Be respectful with requests
        
        db.commit()
        
        print(f"\n📊 Verification Summary:")
        print(f"  Working websites: {working_websites}/{len(companies)}")
        print(f"  Updates made: {updated_count}")
        
        # Show businesses with missing or problematic data
        print(f"\n🔍 Data Quality Check:")
        
        # Businesses without phones
        no_phone = db.execute(text("SELECT name, website FROM companies WHERE phone IS NULL OR phone = ''")).fetchall()
        if no_phone:
            print(f"  Businesses without phone numbers: {len(no_phone)}")
            for name, website in no_phone:
                print(f"    - {name}: {website}")
        
        # Businesses with short descriptions
        short_desc = db.execute(text("SELECT name, description FROM companies WHERE LENGTH(description) < 50")).fetchall()
        if short_desc:
            print(f"  Businesses with short descriptions: {len(short_desc)}")
            for name, desc in short_desc:
                print(f"    - {name}: {desc}")
                
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

def test_website_access():
    """Test if websites are accessible"""
    db = SessionLocal()
    
    try:
        companies = db.execute(text("SELECT name, website FROM companies WHERE website IS NOT NULL")).fetchall()
        
        print("Testing website accessibility...")
        working = 0
        
        for name, website in companies:
            try:
                response = requests.head(website, timeout=5, allow_redirects=True)
                if response.status_code < 400:
                    print(f"✅ {name}: {website}")
                    working += 1
                else:
                    print(f"❌ {name}: {website} (Status: {response.status_code})")
            except Exception as e:
                print(f"❌ {name}: {website} (Error: {str(e)[:50]})")
            
            time.sleep(0.5)
        
        print(f"\nWorking websites: {working}/{len(companies)}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

def manual_fix_known_issues():
    """Manually fix known data issues"""
    db = SessionLocal()
    
    try:
        # Fix known phone numbers and websites based on manual research
        fixes = [
            {
                'name': 'Caswell Orthodontics',
                'phone': '(808) 955-4449',
                'website': 'https://www.caswellorthodontics.com',
                'address': '1319 Punahou St Ste 1150, Honolulu, HI 96826'
            },
            {
                'name': 'Sweet Tooth Dental',
                'phone': '(808) 329-0889',
                'website': 'https://www.sweettoothdental.net',
                'address': '75-5995 Kuakini Hwy Suite 103, Kailua-Kona, HI 96740'
            },
            {
                'name': 'Kauai Family Dentistry',
                'phone': '(808) 245-9407',
                'website': 'http://www.kauaifamilydentistry.com',
                'address': '4366 Kukui Grove St Suite 101, Lihue, HI 96766'
            },
            {
                'name': 'Beach House Restaurant',
                'phone': '(808) 742-1424',
                'website': 'http://www.the-beach-house.com',
                'address': '5022 Lawai Rd, Koloa, HI 96756'
            }
        ]
        
        print("Applying manual fixes...")
        
        for fix in fixes:
            db.execute(text("""
                UPDATE companies 
                SET phone = :phone, website = :website, address = :address 
                WHERE name = :name
            """), fix)
            print(f"✅ Fixed {fix['name']}")
        
        db.commit()
        print("Manual fixes applied!")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            test_website_access()
        elif sys.argv[1] == 'fix':
            manual_fix_known_issues()
        else:
            print("Usage: python verify_and_fix_business_data.py [test|fix]")
    else:
        verify_all_businesses()