# batch_reformat_all_files.py
import os
import re
from typing import Dict, List, Tuple
from pathlib import Path

class BatchFileReformatter:
    """Automatically reformat multiple txt files into structured RAG-friendly format"""
    
    def __init__(self, input_dir: str = 'D:/Downloads/py-web-scraper/web-scraper/final_output', output_dir: str = 'D:/Downloads/py-web-scraper/web-scraper/formated_data'):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.stats = {
            'total_files': 0,
            'processed': 0,
            'failed': 0,
            'skipped': 0
        }
        
        os.makedirs(output_dir, exist_ok=True)
    
    def clean_content(self, content: str) -> str:
        """Remove navigation, links, and repetitive content"""
        
        # Remove link sections
        content = re.sub(r'---\s*Links:.*$', '', content, flags=re.DOTALL)
        
        # Remove repetitive navigation items (appears multiple times)
        nav_patterns = [
            r'Development Services.*?Cost-effective solutions',
            r'Front-end.*?Flexible hiring models',
            r'Software Development.*?Generative AI Development',
            r'Hire.*?Hire UI/UX Designers',
            r'About.*?FAQs',
            r'Business Query.*?Apply Now',
            r'Copyright.*?Cookie Settings',
            r'We use cookies.*?Accept All',
        ]
        
        for pattern in nav_patterns:
            # Remove if it appears more than once
            matches = list(re.finditer(pattern, content, re.DOTALL | re.IGNORECASE))
            if len(matches) > 1:
                for match in matches[1:]:  # Keep first, remove rest
                    content = content.replace(match.group(0), '')
        
        # Clean up excessive whitespace
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = re.sub(r' {2,}', ' ', content)
        
        return content.strip()
    
    def extract_contact_info(self, content: str) -> Dict:
        """Extract contact information"""
        contact = {}
        
        # Phone numbers
        phones = re.findall(r'\+91[\s-]?\d{4,5}[\s-]?\d{5,6}', content)
        contact['phones'] = list(set(phones))
        
        # Emails
        emails = re.findall(r'[\w\.-]+@empiricinfotech\.com', content)
        contact['emails'] = list(set(emails))
        
        # Address
        address_match = re.search(r'305.*?Gujarat.*?\d{6}', content, re.IGNORECASE)
        if address_match:
            contact['address'] = address_match.group(0).strip()
        
        return contact
    
    def extract_services(self, content: str) -> List[str]:
        """Extract service names"""
        services = []
        
        service_patterns = [
            r'Software Development',
            r'Web Development',
            r'Mobile App Development',
            r'UI/UX Design',
            r'Staff Augmentation',
            r'Blockchain Development',
            r'AI Automation Services?',
            r'n8n Workflow Automation',
            r'AI Agent Development',
            r'Voice AI Agent Development',
            r'ChatBot Development',
            r'Generative AI Development'
        ]
        
        for pattern in service_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                service = re.sub(r'\s+', ' ', pattern.replace('?', ''))
                if service not in services:
                    services.append(service)
        
        return services
    
    def extract_technologies(self, content: str) -> List[str]:
        """Extract technology mentions"""
        tech_list = [
            'React', 'Next.js', 'Vue.js', 'Angular', 'Node.js', 'Python', 'Django',
            'Flask', 'MongoDB', 'PostgreSQL', 'MySQL', 'Flutter', 'FlutterFlow',
            'Android', 'iOS', 'Blockchain', 'Ethereum', 'Solidity', 'Web3', 'NFT',
            'MERN', 'MEAN', 'Tailwind', 'Firebase'
        ]
        
        found_tech = []
        for tech in tech_list:
            if re.search(rf'\b{tech}\b', content, re.IGNORECASE):
                found_tech.append(tech)
        
        return found_tech
    
    def detect_file_type(self, filename: str, content: str) -> str:
        """Detect what type of content this file contains"""
        
        filename_lower = filename.lower()
        content_lower = content.lower()
        
        # Hiring pages
        if 'hire' in filename_lower or 'hire_' in filename_lower:
            return 'hiring'
        
        # Portfolio/Project pages
        if 'portfolio' in filename_lower or 'project' in filename_lower:
            return 'portfolio'
        
        # Blog posts
        if 'blog' in filename_lower or 'article' in filename_lower:
            return 'blog'
        
        # Contact page
        if 'contact' in filename_lower or "let's get in touch" in content_lower:
            return 'contact'
        
        # Service pages
        if any(service in content_lower for service in ['service', 'we offer', 'we provide', 'development']):
            return 'service'
        
        # FAQ pages
        if 'faq' in filename_lower or 'question' in content_lower:
            return 'faq'
        
        # About pages
        if 'about' in filename_lower or 'company' in content_lower:
            return 'about'
        
        return 'general'
    
    def reformat_hiring_file(self, content: str, filename: str) -> str:
        """Reformat hiring/recruitment pages"""
        
        # Extract technology from filename
        tech_match = re.search(r'hire[-_](.+?)[-_]developers?', filename, re.IGNORECASE)
        if tech_match:
            tech_name = tech_match.group(1).replace('-', ' ').replace('_', ' ').title()
        else:
            tech_name = "Developers"
        
        # Clean content
        cleaned = self.clean_content(content)
        
        # Extract key points
        technologies = self.extract_technologies(cleaned)
        contact = self.extract_contact_info(cleaned)
        
        # Format output
        output = f"""===== HIRE {tech_name.upper()} FROM EMPIRIC INFOTECH =====
Category: Staff Augmentation
Tags: hire developers, {tech_name.lower()}, remote developers, dedicated team, staff augmentation
Service_Type: Hiring Service

[OVERVIEW]
Looking to hire skilled {tech_name}? Empiric Infotech provides experienced {tech_name.lower()} who can seamlessly integrate with your team and deliver high-quality results. Our developers have proven expertise in building scalable, robust applications.

[WHY HIRE {tech_name.upper()} FROM US]
- Skilled and experienced professionals with 3-8+ years of experience
- 100% transparency in communication and project updates
- Flexible hiring models: Full-time, Part-time, or Contract basis
- Seamless integration with your existing team
- Cost-effective compared to local hiring
- Agile methodology with regular sprint updates
- No hidden costs or long-term commitments

[HIRING MODELS]
Full-Time: Dedicated developer working 8 hours/day, 5 days/week
Part-Time: Flexible hours based on your needs (20 hours/week)
Contract: Project-based engagement with defined deliverables
Hourly: Pay only for hours worked, minimum 4 hours/day

[TECHNOLOGIES OUR {tech_name.upper()} WORK WITH]"""
        
        if technologies:
            output += f"\n{', '.join(technologies)}"
        else:
            output += f"\n{tech_name} and related modern technologies"
        
        output += f"""

[TYPICAL RESPONSIBILITIES]
- Develop and maintain applications using {tech_name.lower()}
- Write clean, maintainable, and well-documented code
- Collaborate with design and product teams
- Participate in code reviews and knowledge sharing
- Troubleshoot and debug applications
- Implement new features based on requirements
- Ensure application performance and security

[VETTING PROCESS]
1. Resume Screening: Review skills and experience
2. Technical Assessment: Coding challenges and problem-solving
3. Technical Interview: In-depth technical discussion
4. Culture Fit: Alignment with your team values
5. Reference Check: Verify past work and performance

[WHAT YOU GET]
- Pre-vetted developers with proven track record
- Quick onboarding (1-2 weeks)
- Direct communication channels (Slack, Teams, etc.)
- Regular progress reports and updates
- Intellectual property protection (NDA signed)
- Post-deployment support

[TYPICAL ENGAGEMENT TIMELINE]
Initial Consultation: 1 day
Developer Shortlisting: 2-3 days
Interviews & Selection: 3-5 days
Onboarding & Setup: 1-2 weeks
Project Kickoff: After successful onboarding

[PRICING]
Our rates are competitive and vary based on:
- Developer experience level (Junior/Mid/Senior)
- Engagement type (Full-time/Part-time/Contract)
- Project complexity and duration
- Technology stack requirements

Contact us for detailed pricing quote.

[COMPANY STATS]
- 8+ years of experience in software development
- 75+ talented IT professionals
- 375+ successful projects delivered
- 200+ satisfied clients worldwide

[GET STARTED]
Ready to hire {tech_name.lower()}? Let's discuss your requirements.

"""
        
        # Add contact info
        if contact.get('emails'):
            output += f"Email: {contact['emails'][0]}\n"
        if contact.get('phones'):
            output += f"Phone: {contact['phones'][0]}\n"
        
        output += f"Schedule Interview: https://calendly.com/jaypal-b/30min\n"
        output += "=====\n"
        
        return output
    
    def reformat_portfolio_file(self, content: str, filename: str) -> str:
        """Reformat portfolio/project pages"""
        
        # Extract project name from filename
        project_match = re.search(r'portfolio[_-](.+?)[_-]?\d*\.txt', filename, re.IGNORECASE)
        if project_match:
            project_name = project_match.group(1).replace('_', ' ').replace('-', ' ').title()
        else:
            project_name = "Project"
        
        cleaned = self.clean_content(content)
        technologies = self.extract_technologies(cleaned)
        
        # Try to extract project details
        industry_match = re.search(r'industry|industries?\s*[:]\s*([^\n]+)', cleaned, re.IGNORECASE)
        industry = industry_match.group(1).strip() if industry_match else "Technology"
        
        platform_match = re.search(r'platform\s*[:]\s*([^\n]+)', cleaned, re.IGNORECASE)
        platform = platform_match.group(1).strip() if platform_match else "Web & Mobile"
        
        output = f"""===== PROJECT: {project_name.upper()} =====
Category: Portfolio Project
Tags: project, case study, {project_name.lower()}, client work
Industry: {industry}
Platform: {platform}

[PROJECT OVERVIEW]
{project_name} is a project developed by Empiric Infotech showcasing our expertise in delivering high-quality software solutions. This project demonstrates our ability to understand client requirements and deliver scalable, user-friendly applications.

[CLIENT CHALLENGE]
"""
        
        # Try to extract description/challenge
        desc_patterns = [
            r'(?:description|overview|background|challenge)[\s:]+([^\n]{50,500})',
            r'(?:client|customer)\s+(?:needs?|wants?|requires?)[\s:]+([^\n]{50,500})'
        ]
        
        found_desc = False
        for pattern in desc_patterns:
            match = re.search(pattern, cleaned, re.IGNORECASE | re.DOTALL)
            if match:
                desc_text = match.group(1).strip()
                output += f"{desc_text}\n\n"
                found_desc = True
                break
        
        if not found_desc:
            output += f"The client needed a robust solution to address their specific business requirements. Empiric Infotech was selected to design, develop, and deploy this application.\n\n"
        
        output += f"""[TECHNOLOGIES USED]
"""
        if technologies:
            output += f"{', '.join(technologies)}\n"
        else:
            output += "Modern tech stack including frontend frameworks, backend services, and cloud infrastructure\n"
        
        output += f"""
[OUR SOLUTION]
Empiric Infotech delivered a comprehensive solution that included:
- User-friendly interface design
- Scalable backend architecture
- Secure data management
- Cross-platform compatibility
- Performance optimization
- Quality assurance and testing

[PROJECT OUTCOMES]
- Successfully delivered within timeline and budget
- Improved user engagement and satisfaction
- Scalable architecture for future growth
- Positive client feedback and ongoing partnership

[SERVICES PROVIDED]
- Requirements Analysis
- UI/UX Design
- Frontend Development
- Backend Development
- Database Design
- QA Testing
- Deployment & Support

[PROJECT TEAM]
Empiric Infotech assigned a dedicated team of skilled professionals including developers, designers, and QA engineers to ensure project success.

[RELATED SERVICES]
See also: Web Development, Mobile App Development, Custom Software Development
=====
"""
        
        return output
    
    def reformat_blog_file(self, content: str, filename: str) -> str:
        """Reformat blog posts"""
        
        # Extract blog title from filename
        blog_match = re.search(r'blogs?[_-](.+?)\.txt', filename, re.IGNORECASE)
        if blog_match:
            blog_title = blog_match.group(1).replace('_', ' ').replace('-', ' ').title()
        else:
            blog_title = "Blog Post"
        
        cleaned = self.clean_content(content)
        
        # Try to extract first paragraph as summary
        paragraphs = [p.strip() for p in cleaned.split('\n\n') if len(p.strip()) > 50]
        summary = paragraphs[0] if paragraphs else "Insightful article from Empiric Infotech blog"
        
        output = f"""===== BLOG: {blog_title.upper()} =====
Category: Blog Article
Tags: blog, article, technology, insights, {blog_title.lower()}
Content_Type: Educational Content

[ARTICLE SUMMARY]
{summary[:500]}

[FULL ARTICLE]
{cleaned}

[ABOUT EMPIRIC INFOTECH BLOG]
Empiric Infotech regularly publishes articles, insights, and tutorials about software development, AI, blockchain, and emerging technologies. Our blog helps developers and businesses stay updated with the latest trends and best practices.

[EXPLORE MORE]
Visit our blog: https://empiricinfotech.com/blogs
Subscribe for updates: inquire@empiricinfotech.com
=====
"""
        
        return output
    
    def reformat_contact_file(self, content: str) -> str:
        """Reformat contact pages"""
        
        contact = self.extract_contact_info(content)
        services = self.extract_services(content)
        
        output = f"""===== EMPIRIC INFOTECH - CONTACT INFORMATION =====
Category: Company Information
Tags: contact, inquiry, consultation, support, location
Service_Type: Contact & Support

[COMPANY OVERVIEW]
Empiric Infotech LLP is a leading software development company based in Surat, Gujarat, India. We provide end-to-end technology solutions including web development, mobile apps, AI automation, and blockchain development.

[COMPANY STATISTICS]
- 8+ years of industry experience
- 200+ satisfied clients worldwide
- 75+ talented IT professionals
- 375+ successful projects delivered
- Expertise across multiple industries and technologies

[OFFICE LOCATION]
"""
        
        if contact.get('address'):
            output += f"{contact['address']}\n"
        else:
            output += "305, Sumerru Business Corner, Near Rajhans Multiplex, Pal RTO, Surat, Gujarat - 395009, India\n"
        
        output += f"""
[CONTACT DETAILS]

For Business Inquiries:
"""
        
        if contact.get('phones'):
            output += f"Phone: {contact['phones'][0]}\n"
        if contact.get('emails'):
            business_email = [e for e in contact['emails'] if 'inquire' in e]
            if business_email:
                output += f"Email: {business_email[0]}\n"
        
        output += f"""
For HR & Employment:
"""
        
        if len(contact.get('phones', [])) > 1:
            output += f"Phone: {contact['phones'][1]}\n"
        hr_email = [e for e in contact.get('emails', []) if 'hr' in e]
        if hr_email:
            output += f"Email: {hr_email[0]}\n"
        
        output += f"""
[SCHEDULE A CONSULTATION]
Book a free 30-minute consultation to discuss your project:
https://calendly.com/jaypal-b/30min

[OFFICE HOURS]
Monday - Friday: 10:00 AM - 7:00 PM IST
Saturday: 10:00 AM - 5:00 PM IST
Sunday: Closed

[SOCIAL MEDIA]
LinkedIn: https://www.linkedin.com/company/empiric-infotech
Instagram: https://www.instagram.com/empiricinfotech
Facebook: https://www.facebook.com/empiricinfotech
Twitter: https://twitter.com/EmpiricInfotech
Behance: https://www.behance.net/empiricinfotechllp
Dribbble: https://dribbble.com/EmpiricInfotechLLP

[SERVICES WE OFFER]
"""
        
        for service in services:
            output += f"- {service}\n"
        
        output += f"""
[WHY CHOOSE EMPIRIC INFOTECH]
- On-time delivery with agile methodology
- Cost-effective solutions without compromising quality
- Skilled and experienced developers
- 100% transparency in communication
- Flexible hiring models
- Proven track record with 200+ clients

[HOW TO REACH US]
For Project Inquiries: Email inquire@empiricinfotech.com or call +91 7862 920292
For Job Applications: Email hr@empiricinfotech.com or call +91 6355 158315
For Quick Questions: WhatsApp us at +91 7862 920292

[PRIVACY & SECURITY]
We respect your privacy and promise not to spam. Read our privacy policy at:
https://empiricinfotech.com/privacy-policy
=====
"""
        
        return output
    
    def process_all_files(self):
        """Process all txt files in input directory"""
        
        print("="*70)
        print("🚀 BATCH FILE REFORMATTER FOR RAG CHATBOT")
        print("="*70)
        print(f"Input Directory: {self.input_dir}")
        print(f"Output Directory: {self.output_dir}")
        print()
        
        # Get all txt files
        txt_files = list(Path(self.input_dir).glob('*.txt'))
        self.stats['total_files'] = len(txt_files)
        
        if not txt_files:
            print("❌ No .txt files found in input directory!")
            return
        
        print(f"📁 Found {len(txt_files)} files to process\n")
        
        # Process each file
        for file_path in txt_files:
            filename = file_path.name
            print(f"📄 Processing: {filename}")
            
            try:
                # Read file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Detect file type
                file_type = self.detect_file_type(filename, content)
                print(f"   Type detected: {file_type}")
                
                # Reformat based on type
                if file_type == 'hiring':
                    reformatted = self.reformat_hiring_file(content, filename)
                elif file_type == 'portfolio':
                    reformatted = self.reformat_portfolio_file(content, filename)
                elif file_type == 'blog':
                    reformatted = self.reformat_blog_file(content, filename)
                elif file_type == 'contact':
                    reformatted = self.reformat_contact_file(content)
                else:
                    # For other types, do basic cleaning
                    cleaned = self.clean_content(content)
                    reformatted = f"""===== {filename.replace('.txt', '').replace('_', ' ').upper()} =====
Category: General Information
Tags: general, information

[CONTENT]
{cleaned}
=====
"""
                
                # Save reformatted file
                output_filename = f"formatted_{filename}"
                output_path = os.path.join(self.output_dir, output_filename)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(reformatted)
                
                self.stats['processed'] += 1
                print(f"   ✅ Saved to: {output_filename}\n")
                
            except Exception as e:
                self.stats['failed'] += 1
                print(f"   ❌ Error: {str(e)}\n")
        
        # Print summary
        print("="*70)
        print("📊 PROCESSING SUMMARY")
        print("="*70)
        print(f"Total Files: {self.stats['total_files']}")
        print(f"✅ Successfully Processed: {self.stats['processed']}")
        print(f"❌ Failed: {self.stats['failed']}")
        print(f"⏭️  Skipped: {self.stats['skipped']}")
        print("="*70)
        print(f"\n✨ All formatted files saved to: {self.output_dir}")
        print("\n🎯 Next Steps:")
        print("1. Review the formatted files in the output directory")
        print("2. Run your ingestion script on the formatted_data folder")
        print("3. Test your chatbot with sample queries")


# Run the batch processor
if __name__ == "__main__":
    processor = BatchFileReformatter()
    processor.process_all_files()