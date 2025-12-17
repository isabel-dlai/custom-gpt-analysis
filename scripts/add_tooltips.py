"""
Script to add tooltips to the cluster visualization HTML
"""

# Data structure: [category_name, gpt_name, description, url]
cluster_data = {
    1: [
        ["Image & Visual Art Generation", "GPT Icon Generator", "Creates custom icons and visual branding elements for GPTs and applications", "https://chatgpt.com/g/g-00Lkphpld-gpt-icon-generator"],
        ["Logo & Brand Design", "Logo Creator", "Professional logo design with brand strategy and color psychology", "https://chatgpt.com/g/g-gFt1ghYJl-logo-creator"],
        ["Character & Avatar Creation", "CharForge", "Creates detailed character designs for games, stories, and creative projects", "https://chatgpt.com/g/g-00Lh1zR3f-charforge"],
        ["Story & Narrative Generation", "AI Story Generator", "Generates captivating tales and narratives with advanced storytelling techniques", "https://chatgpt.com/g/g-LzrB0QwAB-ai-story-generator"],
        ["Animation & GIF Creation", "GIF GPT", "Generates 8-bit style animated GIFs with retro aesthetic", "https://chatgpt.com/g/g-0f6fZG9q0-gif-gpt"],
        ["Meme & Viral Content Creation", "Meme Master", "Creates trending memes with cultural awareness and humor optimization", "https://chatgpt.com/g/g-a7VLbl0jm-meme-master"],
        ["Artistic Style Transfer", "Artistic Vision", "Transforms images using famous artistic styles and movements", "https://chatgpt.com/g/g-6tjd1B8sG-artistic-vision"],
    ],
    2: [
        ["Hard Sciences (Physics, Chemistry, Biology)", "Biochemistry, Genetics and Molecular Biology", "Explains genetic mutations, molecular mechanisms, and biochemical pathways with research-level depth", "https://chatgpt.com/g/g-80BBfRYBn-biochemistry-genetics-and-molecular-biology"],
        ["Mathematics & Advanced Computation", "ODE Calculator", "Scholarly ordinary differential equation solver with step-by-step proofs", "https://chatgpt.com/g/g-z1lIx3L13-ode-calculator"],
        ["Psychology & Behavioral Sciences", "Psychology Insight Analyzer", "Provides evidence-based psychological analysis and therapeutic frameworks", "https://chatgpt.com/g/g-00M3Go7mz-psychology-insight-analyzer"],
        ["Space & Astronomy", "Galaxy Chat", "Expert in astronomy, astrophysics, and space science communication", "https://chatgpt.com/g/g-057LZjps8-galaxy-chat"],
        ["Linguistics & Language Theory", "XenoLinguo", "Generates and analyzes constructed languages with linguistic rigor", "https://chatgpt.com/g/g-00Cjtpc0z-xenolinguo-alien-language-generated-by"],
        ["Philosophy & Ethics", "C.G. Jung", "Deep philosophical and psychological insights based on Jungian analytical psychology", "https://chatgpt.com/g/g-i21b4H7Mf-c-g-jung"],
        ["Advanced Engineering", "Nanofabrication", "Research and development of nanomaterial fabrication techniques", "https://chatgpt.com/g/g-67e749d83f0881918616c085b1a580d0-nanofabrication"],
    ],
    3: [
        ["Career & Professional Coaching", "Engineering Manager Coach", "Specialized coaching for engineering managers on leadership and team dynamics", "https://chatgpt.com/g/g-00Vxlldtm-engineering-manager-coach"],
        ["Life Coaching & Goal Setting", "Life Navigator", "Helps set meaningful goals and create actionable life plans", "https://chatgpt.com/g/g-8FixlbFKj-life-navigator"],
        ["Communication & Interpersonal Skills", "Feedback Coach", "Practice giving and receiving feedback through role-play scenarios", "https://chatgpt.com/g/g-ZWQuVnjkF-feedback-coach"],
        ["Leadership Development", "Leadership Coach", "Develops leadership skills with evidence-based frameworks and exercises", "https://chatgpt.com/g/g-sEKD2Zy0m-leadership-coach"],
        ["Habit Formation & Behavior Change", "Quit Alcohol | Tracy", "Compassionate guide for overcoming alcohol dependency with support strategies", "https://chatgpt.com/g/g-67b26a0a91d08191b37a0a289733ba82-quit-alcohol-tracy"],
        ["Confidence & Self-Esteem", "Confidence Builder", "Structured exercises to develop self-confidence and overcome self-doubt", "https://chatgpt.com/g/g-3kPQnXXfn-confidence-builder"],
        ["Mentorship & Guidance", "Red Team Mentor", "Mentorship for cybersecurity red team professionals", "https://chatgpt.com/g/g-03Nvt600n-red-team-mentor"],
    ],
    4: [
        ["Test Preparation (SAT, ACT, GRE)", "Study Buddy", "Comprehensive SAT, ACT, Accuplacer, and AP exam preparation with practice questions", "https://chatgpt.com/g/g-3guUZJ6qF-study-buddy"],
        ["Mathematics Tutoring", "Math Solver", "Step-by-step math problem solving with clear explanations", "https://chatgpt.com/g/g-PLYSLfAy3-math-solver"],
        ["Language Learning", "German Teacher GPT", "Conversation practice, grammar correction, and vocabulary building for German", "https://chatgpt.com/g/g-iNQwhh1qy-german-teacher-gpt"],
        ["STEM Education", "Universal Primer", "The fastest way to learn anything hard - complex STEM concepts made accessible", "https://chatgpt.com/g/g-GbLbctpPz-universal-primer"],
        ["Programming & Coding Education", "Code Buddy", "Educational assistant for beginners learning coding and AI fundamentals", "https://chatgpt.com/g/g-aOmUbFbcZ-code-buddy"],
        ["Academic Writing & Research", "Abstract Generator", "Guides college students through writing effective essay abstracts", "https://chatgpt.com/g/g-4UWODpApy-abstract-generator"],
        ["General Knowledge & Trivia", "WikiGPT", "Access and explain Wikipedia content with enhanced context", "https://chatgpt.com/g/g-sN4UpxD0L-wikigpt"],
    ],
    5: [
        ["Project Management", "Todoist Project Management Guide", "Organize tasks and projects with Todoist best practices", "https://chatgpt.com/g/g-46CgTNcL8"],
        ["Note-Taking & Knowledge Management", "Bullet Journaling Prodigy", "Create personalized bullet journals with custom layouts and habit tracking", "https://chatgpt.com/g/g-4uSQohyLW-bullet-journaling-prodigy"],
        ["Time Management & Scheduling", "Calendar Optimizer", "Analyzes schedules and suggests time management improvements", "https://chatgpt.com/g/g-7MsBmUB2d-calendar-optimizer"],
        ["Personal Assistant", "Apollo GPT", "Personal helper and organizer for practically everything", "https://chatgpt.com/g/g-DyxVk0WN0-apollo-gpt"],
        ["Workflow Automation", "GPT Cookbook Assistant", "Helps create automated workflows using GPT capabilities", "https://chatgpt.com/g/g-0Cjgm4Hmw-gpt-cookbook-assistant"],
        ["Document Organization", "Digital Legacy Planner", "Manage digital assets and plan for digital afterlife", "https://chatgpt.com/g/g-BQMN8wQ6j-digital-legacy-planner"],
    ],
    6: [
        ["Pitch Deck & Presentation Creation", "Pitch Deck GPT", "World-class pitch deck creation for startups and fundraising", "https://chatgpt.com/g/g-1XGd3uF1T-pitch-deck-gpt"],
        ["Business Planning & Strategy", "Business Ideas Plan Generator", "Generate low-competition business ideas with complete business plans", "https://chatgpt.com/g/g-VLxryqnlj-business-ideas-plan-generator"],
        ["Sales & Lead Generation", "Sales Assistant", "Ultimate sales tool with proposal writing and presentation skills", "https://chatgpt.com/g/g-CS0BEb5pJ-sales-assistant-ultimate-sales-tool-for-sellers"],
        ["Financial Analysis & Investment", "Buffett Investment Tool", "Investment analysis inspired by Warren Buffett's strategies", "https://chatgpt.com/g/g-u7kq0UsG2-buffett-investment-tool"],
        ["Consulting & Advisory", "Executive Insight", "Senior McKinsey-level executive insights and data-driven recommendations", "https://chatgpt.com/g/g-DLrpkpntx-executive-insight"],
        ["Market Research & Analysis", "Business Lookup", "Locate businesses and analyze market landscapes", "https://chatgpt.com/g/g-0DxZTgo0i-business-lookup"],
        ["SaaS & Technology Business", "SaaS", "Business-oriented discussions on SaaS models and strategies", "https://chatgpt.com/g/g-T2bAANodC-saas"],
    ],
    7: [
        ["SEO & Search Optimization", "Keyword Planner SEO", "SEO keyword research and content optimization strategies", "https://chatgpt.com/g/g-05Ju8F8Ts-keyword-planner-seo"],
        ["Social Media Content", "Viral Muse", "Transforms tweet ideas into viral-worthy content", "https://chatgpt.com/g/g-0LVKVFAOE-viral-muse"],
        ["Copywriting & Sales Copy", "Brand Crafter", "Creates compelling brand messaging and marketing copy", "https://chatgpt.com/g/g-07Kcpnfmn-brand-crafter"],
        ["Product Descriptions", "Product Description Generator", "Generates product descriptions for small business physical products", "https://chatgpt.com/g/g-Z6qhetSRr-product-description-generator"],
        ["Blog & Article Writing", "Newsletter Summarizer", "Summarizes newsletters to save time and extract key insights", "https://chatgpt.com/g/g-rkfllG5TM"],
        ["Email Marketing", "Responder", "Helps craft friendly and effective email responses", "https://chatgpt.com/g/g-Sdzx1bnMN-responder"],
        ["Brand Voice Development", "Execu-X Post Companion", "Professional X/Twitter posts that ensure engagement", "https://chatgpt.com/g/g-3wv1Wj3Rg-execu-x-post-companion"],
    ],
    8: [
        ["Contract Law & Drafting", "Law & Order", "AI legal assistant for contract law and NDA drafting", "https://chatgpt.com/g/g-23MFe5i3r-law-order"],
        ["Jurisdiction-Specific Law (US)", "LexiAI: US Law", "Multilingual AI legal assistant for US law queries and research", "https://chatgpt.com/g/g-26Ogj8JJ4-lexiai-us-law"],
        ["Jurisdiction-Specific Law (UK/International)", "Pre-Solicitor AI: UK Law Simplified", "Simplifies UK laws before consulting a solicitor, with real case examples", "https://chatgpt.com/g/g-COySiYHrU-pre-solicitor-aitm-uk-law-simplified-free"],
        ["Regulatory Compliance", "California Building Code Helper", "Expert in California building codes and construction regulations", "https://chatgpt.com/g/g-hiahMzXsY-california-building-code-helper"],
        ["Supreme Court & Case Law", "Supreme Court Rulings", "Analyzes and explains Supreme Court decisions and legal precedents", "https://chatgpt.com/g/g-prBU1ubiC-supreme-court-rulings"],
        ["Specialized Legal Domains", "Kazakhstani Law Assistant", "Specialized knowledge of Kazakhstan's legal system", "https://chatgpt.com/g/g-0BI04f09L-kazakhstani-law-assistant"],
    ],
    9: [
        ["Web Development (Frontend/Backend)", "CSS Code Helper", "CSS design assistance with code examples and best practices", "https://chatgpt.com/g/g-ihUOhctYf-css-code-helper"],
        ["Specific Languages (Python, JavaScript, etc.)", "JavaScript GPT", "Expert JavaScript programming assistance and debugging", "https://chatgpt.com/g/g-0Fjo9Edoq-javascript-gpt"],
        ["Database & SQL", "Beta SQL Expert Pro", "Advanced SQL optimization and complex query development", "https://chatgpt.com/g/g-6740a711568c819189f561c15e0707e6-beta-sql-expert-pro"],
        ["DevOps & Infrastructure", "Linux Specialist", "Expert in Linux, DevOps, and Infrastructure as Code", "https://chatgpt.com/g/g-EkGy9mnx9-linux-specialist"],
        ["Smart Contracts & Blockchain", "Contract Builder 2.0", "Latest strategies for reducing gas costs in EVM smart contracts", "https://chatgpt.com/g/g-jUMcG3wTK-contract-builder-2-0"],
        ["IDE & Development Tools", "Visual Studio Code Expert", "Expert advice on VS Code features and workflow optimization", "https://chatgpt.com/g/g-FYMRmDqEY-visual-studio-code-expert"],
        ["Code Review & Debugging", "Code Whiz Pro", "Advanced code review and debugging assistance", "https://chatgpt.com/g/g-0Sjxa4A1J-code-whiz-pro"],
    ],
    10: [
        ["Dermatology & Skin Care", "Dermatology Advisor", "Upload skin condition photos for analysis and treatment suggestions", "https://chatgpt.com/g/g-XdmUwHrDs-dermatology-advisor"],
        ["Nutrition & Diet Planning", "Chef NutriGourmet", "Chef and nutritionist specializing in low-carb recipes and meal plans", "https://chatgpt.com/g/g-P0TXECLkv-chef-nutrigourmet"],
        ["Mental Health Support", "Mental Health Conversation Guide", "Supportive conversations for mental health and emotional well-being", "https://chatgpt.com/g/g-0Unl1Zwyp-mental-health-conversation-guide"],
        ["Fitness & Exercise", "Swim Coach Pro", "Personal swim training expert for technique, fitness, and motivation", "https://chatgpt.com/g/g-088Zut1ap-swim-coach-pro"],
        ["Medical Information & Conditions", "COVID-19", "Information and guidance about COVID-19 pandemic", "https://chatgpt.com/g/g-0Vutlfcvf-covid-19"],
        ["Specialized Health Conditions", "ARFID Helper", "Supportive guide for ARFID sufferers with detailed food descriptions", "https://chatgpt.com/g/g-0t6atNK4C-arfid-helper"],
        ["Healthcare Professional Support", "Healthcare Support Workers Assistant", "Enhances healthcare workers' daily tasks and workflows", "https://chatgpt.com/g/g-a30IbALzW-healthcare-support-workers-all-other-assistant"],
    ],
    11: [
        ["Role-Playing Games (RPG)", "The Oracle", "Perfect oracle for solo or cooperative RPG GM emulation and storytelling", "https://chatgpt.com/g/g-qdH2XGV5M-the-oracle"],
        ["Video Game Guides", "Soul Seeker GPT", "Guide for souls-like games blending gameplay strategies with lore", "https://chatgpt.com/g/g-ySVdGHfgB-soul-seeker-gpt"],
        ["Sports Analysis & Statistics", "Tracer Bullet", "Player performance information during IPL 2024 cricket matches", "https://chatgpt.com/g/g-3HyguSH8I-tracer-bullet"],
        ["Interactive Story Games", "Text Quest", "Interactive text-based adventure game with dynamic storytelling", "https://chatgpt.com/g/g-09Gpm0Nti-text-quest"],
        ["Battle Simulators", "Battle GPT", "AI battle realism simulator with policy-compliant visuals", "https://chatgpt.com/g/g-GsRUjaYvz-battle-gpt"],
        ["Puzzle & Challenge Games", "Situation Puzzle", "Solve situation puzzles (海龟汤) with logical deduction", "https://chatgpt.com/g/g-KHcdRU9or-situation-puzzle-hai-gui-tang"],
        ["Survival & Strategy Games", "Survival Mentor", "Engaging survival challenge game with dynamic scenarios", "https://chatgpt.com/g/g-0i2rSQUGt-survival-mentor"],
    ],
    12: [
        ["Tarot & Card Reading", "Tarot Love", "Tarot card readings focused on relationship guidance", "https://chatgpt.com/g/g-turuXxK5O-tarot-love"],
        ["Astrology & Horoscopes", "Daily Horoscope Numbers & Biorhythms", "Daily astrological forecasts with numerology and biorhythm analysis", "https://chatgpt.com/g/g-aLVuuBB9z-daily-horoscope-numbers-biorhythms-from-seeds-net"],
        ["Oracle & Divination", "The Oracle of Delphai", "Ancient oracle wisdom and prophetic insights", "https://chatgpt.com/g/g-0Aiuh2Npa-the-oracle-of-delphai-apollo-the-seer"],
        ["Religious & Spiritual Texts", "KJV Scripture Scholar", "King James Version Bible expert with interpretations", "https://chatgpt.com/g/g-Ijn8Z6frl-kjv-scripture-scholar"],
        ["Palmistry & Physical Divination", "Palm Reader", "Interprets palm readings from uploaded hand images", "https://chatgpt.com/g/g-5woUyUDBR-palm-reader"],
        ["Wisdom & Philosophy", "Oracle of Wisdom", "Ancient wisdom and philosophical insights for modern life", "https://chatgpt.com/g/g-TaAYv7qNm-oracle-of-wisdom"],
        ["Direct Divine Communication", "Talk to God", "Spiritual conversations framed as divine communication", "https://chatgpt.com/g/g-7T7TFTXxM-talk-to-god"],
    ],
    13: [
        ["Sports & Fitness Coaching", "Swimming Coach", "Specialized swimming technique and training guidance", "https://chatgpt.com/g/g-0Tkruotfk-swimming-coach"],
        ["Crafts & DIY Projects", "Beehive Builder", "Helper for DIY builders designing horizontal beehives", "https://chatgpt.com/g/g-ccSSArTEk-beehive-builder"],
        ["Textile Arts (Quilting, Sewing, Knitting)", "Patchwork Pal Quilter's Aid", "Quilting projects with pattern ideas, sewing tips, and fabric advice", "https://chatgpt.com/g/g-yaLSMy7Q2-patchwork-pal-quilter-s-aid"],
        ["Home Decor & Interior Design", "Christmas Decorations", "Festive guide to Christmas decorations and holiday home decor", "https://chatgpt.com/g/g-waqDkUJEv-christmas-decorations"],
        ["Travel & Tourism", "Flights", "Flight search and travel planning assistance", "https://chatgpt.com/g/g-0A9Iqsdml-flights"],
        ["Wedding Planning", "Best Man/Maid of Honor Wedding Speech", "Craft memorable wedding speeches for best man or maid of honor", "https://chatgpt.com/g/g-0Msyma1Ec-best-man-maid-of-honor-wedding-speech"],
        ["Specialized Collecting & Hobbies", "Horse Racing Form Analyst", "Detailed analysis of horse racing data and performance trends", "https://chatgpt.com/g/g-V8DkAO9eK-horse-racing-form-analyst"],
    ],
}

def generate_tooltip_html(category_name, gpt_name, description, url):
    return f'''                    <li class="sub-cluster">
                        {category_name}
                        <div class="tooltip">
                            <span class="tooltip-title">{gpt_name}</span>
                            <div class="tooltip-desc">{description}</div>
                            <a href="{url}" target="_blank" class="tooltip-link">Try it →</a>
                        </div>
                    </li>'''

# Generate HTML for each cluster
for cluster_num, subclusters in cluster_data.items():
    print(f"\n<!-- Cluster {cluster_num} Sub-Clusters -->")
    print("                <ul class=\"sub-clusters\">")
    for subcluster in subclusters:
        print(generate_tooltip_html(*subcluster))
    print("                </ul>")
