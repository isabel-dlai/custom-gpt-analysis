"""
Generate complete visualization HTML with all 13 clusters
"""

# Read the header from the demo file
header = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GPT Ecosystem Taxonomy Visualization</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            text-align: center;
        }

        h1 {
            color: #2d3748;
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .stats {
            color: #718096;
            font-size: 1.1em;
            margin-top: 15px;
        }

        .stats strong {
            color: #667eea;
        }

        .cluster-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }

        .cluster-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .cluster-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }

        .cluster-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }

        .cluster-title {
            font-size: 1.3em;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 5px;
        }

        .cluster-count {
            font-size: 1.8em;
            font-weight: 800;
            padding: 5px 15px;
            border-radius: 10px;
            color: white;
            min-width: 80px;
            text-align: center;
        }

        .cluster-percentage {
            font-size: 0.9em;
            color: #718096;
            margin-bottom: 15px;
        }

        .progress-bar {
            height: 8px;
            background: #e2e8f0;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 20px;
        }

        .progress-fill {
            height: 100%;
            border-radius: 10px;
            transition: width 1s ease-out;
        }

        .sub-clusters {
            list-style: none;
        }

        .sub-cluster {
            padding: 8px 0;
            color: #4a5568;
            font-size: 0.95em;
            border-bottom: 1px solid #e2e8f0;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .sub-cluster:hover {
            color: #667eea;
            background-color: #f7fafc;
        }

        .sub-cluster:last-child {
            border-bottom: none;
        }

        .sub-cluster-header {
            display: flex;
            align-items: center;
            padding: 4px 0;
        }

        .sub-cluster-header::before {
            content: '▸';
            color: #a0aec0;
            margin-right: 10px;
            font-size: 0.8em;
            transition: transform 0.2s ease;
        }

        .sub-cluster.expanded .sub-cluster-header::before {
            transform: rotate(90deg);
        }

        .sub-cluster-details {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
            padding-left: 24px;
        }

        .sub-cluster.expanded .sub-cluster-details {
            max-height: 200px;
            margin-top: 8px;
        }

        .example-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 15px;
            border-radius: 8px;
            margin-bottom: 8px;
        }

        .example-title {
            font-weight: 700;
            font-size: 1em;
            margin-bottom: 6px;
        }

        .example-desc {
            font-size: 0.85em;
            line-height: 1.4;
            opacity: 0.95;
            margin-bottom: 8px;
        }

        .example-link {
            display: inline-block;
            padding: 5px 12px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            font-size: 0.8em;
            text-decoration: none;
            color: white;
            transition: background 0.2s ease;
        }

        .example-link:hover {
            background: rgba(255, 255, 255, 0.3);
        }

        /* Color scheme for clusters */
        .cluster-1 { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .cluster-2 { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
        .cluster-3 { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
        .cluster-4 { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
        .cluster-5 { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }
        .cluster-6 { background: linear-gradient(135deg, #30cfd0 0%, #330867 100%); }
        .cluster-7 { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); }
        .cluster-8 { background: linear-gradient(135deg, #ff9a56 0%, #ff6a88 100%); }
        .cluster-9 { background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); }
        .cluster-10 { background: linear-gradient(135deg, #ff6e7f 0%, #bfe9ff 100%); }
        .cluster-11 { background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%); }
        .cluster-12 { background: linear-gradient(135deg, #f8ceec 0%, #a88beb 100%); }
        .cluster-13 { background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%); }
        .cluster-14 { background: linear-gradient(135deg, #fdcbf1 0%, #e6dee9 100%); }

        @media (max-width: 768px) {
            .cluster-grid {
                grid-template-columns: 1fr;
            }

            h1 {
                font-size: 1.8em;
            }
        }

        footer {
            text-align: center;
            color: white;
            padding: 20px;
            font-size: 0.9em;
            opacity: 0.8;
        }

        .demo-note {
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
            border-left: 4px solid #667eea;
        }

        .demo-note strong {
            color: #667eea;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 GPT Ecosystem Taxonomy</h1>
            <div class="stats">
                <strong>8,092</strong> English GPTs analyzed from ChatGPT Store<br>
                <strong>77.8%</strong> Classified | <strong>22.2%</strong> Unclassified<br>
                Generated: December 15, 2025
            </div>
        </header>

        <div class="demo-note">
            <strong>✨ Click on any sub-cluster</strong> to expand and see an example GPT with description and link!<br>
            Click the arrow to reveal representative examples from each category.
        </div>

        <div class="cluster-grid">
"""

footer = """        </div>

        <footer>
            Generated: December 15, 2025 | Data Source: 8,092 English-only GPTs from ChatGPT Store
        </footer>
    </div>

    <script>
        // Animate progress bars on load
        window.addEventListener('load', function() {
            setTimeout(function() {
                document.querySelectorAll('.progress-fill').forEach(function(bar) {
                    bar.style.width = bar.getAttribute('data-width');
                });
            }, 300);
        });

        // Toggle sub-cluster expansion
        document.addEventListener('DOMContentLoaded', function() {
            const subClusters = document.querySelectorAll('.sub-cluster');

            subClusters.forEach(function(cluster) {
                cluster.addEventListener('click', function() {
                    this.classList.toggle('expanded');
                });
            });
        });
    </script>
</body>
</html>
"""

# Cluster data with all information
clusters = [
    {
        "num": 1,
        "title": "Creative Content Generation",
        "count": 1373,
        "percentage": "17.0%",
        "width": "17%",
        "subclusters": [
            ["Image & Visual Art Generation", "GPT Icon Generator", "Creates custom icons and visual branding elements for GPTs and applications", "https://chatgpt.com/g/g-00Lkphpld-gpt-icon-generator"],
            ["Logo & Brand Design", "Logo Creator", "Professional logo design with brand strategy and color psychology", "https://chatgpt.com/g/g-gFt1ghYJl-logo-creator"],
            ["Character & Avatar Creation", "CharForge", "Creates detailed character designs for games, stories, and creative projects", "https://chatgpt.com/g/g-00Lh1zR3f-charforge"],
            ["Story & Narrative Generation", "AI Story Generator", "Generates captivating tales and narratives with advanced storytelling techniques", "https://chatgpt.com/g/g-LzrB0QwAB-ai-story-generator"],
            ["Animation & GIF Creation", "GIF GPT", "Generates 8-bit style animated GIFs with retro aesthetic", "https://chatgpt.com/g/g-0f6fZG9q0-gif-gpt"],
            ["Meme & Viral Content Creation", "Meme Master", "Creates trending memes with cultural awareness and humor optimization", "https://chatgpt.com/g/g-a7VLbl0jm-meme-master"],
            ["Artistic Style Transfer", "Artistic Vision", "Transforms images using famous artistic styles and movements", "https://chatgpt.com/g/g-6tjd1B8sG-artistic-vision"],
        ]
    },
    {
        "num": 2,
        "title": "Specialized Domain Experts",
        "count": 1120,
        "percentage": "13.8%",
        "width": "13.8%",
        "subclusters": [
            ["Hard Sciences (Physics, Chemistry, Biology)", "Biochemistry, Genetics and Molecular Biology", "Explains genetic mutations, molecular mechanisms, and biochemical pathways with research-level depth", "https://chatgpt.com/g/g-80BBfRYBn-biochemistry-genetics-and-molecular-biology"],
            ["Mathematics & Advanced Computation", "ODE Calculator", "Scholarly ordinary differential equation solver with step-by-step proofs", "https://chatgpt.com/g/g-z1lIx3L13-ode-calculator"],
            ["Psychology & Behavioral Sciences", "Psychology Insight Analyzer", "Provides evidence-based psychological analysis and therapeutic frameworks", "https://chatgpt.com/g/g-00M3Go7mz-psychology-insight-analyzer"],
            ["Space & Astronomy", "Galaxy Chat", "Expert in astronomy, astrophysics, and space science communication", "https://chatgpt.com/g/g-057LZjps8-galaxy-chat"],
            ["Linguistics & Language Theory", "XenoLinguo", "Generates and analyzes constructed languages with linguistic rigor", "https://chatgpt.com/g/g-00Cjtpc0z-xenolinguo-alien-language-generated-by"],
            ["Philosophy & Ethics", "C.G. Jung", "Deep philosophical and psychological insights based on Jungian analytical psychology", "https://chatgpt.com/g/g-i21b4H7Mf-c-g-jung"],
            ["Advanced Engineering", "Nanofabrication", "Research and development of nanomaterial fabrication techniques", "https://chatgpt.com/g/g-67e749d83f0881918616c085b1a580d0-nanofabrication"],
        ]
    },
    {
        "num": 3,
        "title": "Personal Development & Coaching",
        "count": 592,
        "percentage": "7.3%",
        "width": "7.3%",
        "subclusters": [
            ["Career & Professional Coaching", "Engineering Manager Coach", "Specialized coaching for engineering managers on leadership and team dynamics", "https://chatgpt.com/g/g-00Vxlldtm-engineering-manager-coach"],
            ["Life Coaching & Goal Setting", "Life Navigator", "Helps set meaningful goals and create actionable life plans", "https://chatgpt.com/g/g-8FixlbFKj-life-navigator"],
            ["Communication & Interpersonal Skills", "Feedback Coach", "Practice giving and receiving feedback through role-play scenarios", "https://chatgpt.com/g/g-ZWQuVnjkF-feedback-coach"],
            ["Leadership Development", "Leadership Coach", "Develops leadership skills with evidence-based frameworks and exercises", "https://chatgpt.com/g/g-sEKD2Zy0m-leadership-coach"],
            ["Habit Formation & Behavior Change", "Quit Alcohol | Tracy", "Compassionate guide for overcoming alcohol dependency with support strategies", "https://chatgpt.com/g/g-67b26a0a91d08191b37a0a289733ba82-quit-alcohol-tracy"],
            ["Confidence & Self-Esteem", "Confidence Builder", "Structured exercises to develop self-confidence and overcome self-doubt", "https://chatgpt.com/g/g-3kPQnXXfn-confidence-builder"],
            ["Mentorship & Guidance", "Red Team Mentor", "Mentorship for cybersecurity red team professionals", "https://chatgpt.com/g/g-03Nvt600n-red-team-mentor"],
        ]
    },
    {
        "num": 4,
        "title": "Educational & Learning",
        "count": 522,
        "percentage": "6.5%",
        "width": "6.5%",
        "subclusters": [
            ["Test Preparation (SAT, ACT, GRE)", "Study Buddy", "Comprehensive SAT, ACT, Accuplacer, and AP exam preparation with practice questions", "https://chatgpt.com/g/g-3guUZJ6qF-study-buddy"],
            ["Mathematics Tutoring", "Math Solver", "Step-by-step math problem solving with clear explanations", "https://chatgpt.com/g/g-PLYSLfAy3-math-solver"],
            ["Language Learning", "German Teacher GPT", "Conversation practice, grammar correction, and vocabulary building for German", "https://chatgpt.com/g/g-iNQwhh1qy-german-teacher-gpt"],
            ["STEM Education", "Universal Primer", "The fastest way to learn anything hard - complex STEM concepts made accessible", "https://chatgpt.com/g/g-GbLbctpPz-universal-primer"],
            ["Programming & Coding Education", "Code Buddy", "Educational assistant for beginners learning coding and AI fundamentals", "https://chatgpt.com/g/g-aOmUbFbcZ-code-buddy"],
            ["Academic Writing & Research", "Abstract Generator", "Guides college students through writing effective essay abstracts", "https://chatgpt.com/g/g-4UWODpApy-abstract-generator"],
            ["General Knowledge & Trivia", "WikiGPT", "Access and explain Wikipedia content with enhanced context", "https://chatgpt.com/g/g-sN4UpxD0L-wikigpt"],
        ]
    },
    {
        "num": 5,
        "title": "Productivity & Organization",
        "count": 409,
        "percentage": "5.1%",
        "width": "5.1%",
        "subclusters": [
            ["Project Management", "Todoist Project Management Guide", "Organize tasks and projects with Todoist best practices", "https://chatgpt.com/g/g-46CgTNcL8"],
            ["Note-Taking & Knowledge Management", "Bullet Journaling Prodigy", "Create personalized bullet journals with custom layouts and habit tracking", "https://chatgpt.com/g/g-4uSQohyLW-bullet-journaling-prodigy"],
            ["Time Management & Scheduling", "Calendar Optimizer", "Analyzes schedules and suggests time management improvements", "https://chatgpt.com/g/g-7MsBmUB2d-calendar-optimizer"],
            ["Personal Assistant", "Apollo GPT", "Personal helper and organizer for practically everything", "https://chatgpt.com/g/g-DyxVk0WN0-apollo-gpt"],
            ["Workflow Automation", "GPT Cookbook Assistant", "Helps create automated workflows using GPT capabilities", "https://chatgpt.com/g/g-0Cjgm4Hmw-gpt-cookbook-assistant"],
            ["Document Organization", "Digital Legacy Planner", "Manage digital assets and plan for digital afterlife", "https://chatgpt.com/g/g-BQMN8wQ6j-digital-legacy-planner"],
        ]
    },
    {
        "num": 6,
        "title": "Professional Business Tools",
        "count": 382,
        "percentage": "4.7%",
        "width": "4.7%",
        "subclusters": [
            ["Pitch Deck & Presentation Creation", "Pitch Deck GPT", "World-class pitch deck creation for startups and fundraising", "https://chatgpt.com/g/g-1XGd3uF1T-pitch-deck-gpt"],
            ["Business Planning & Strategy", "Business Ideas Plan Generator", "Generate low-competition business ideas with complete business plans", "https://chatgpt.com/g/g-VLxryqnlj-business-ideas-plan-generator"],
            ["Sales & Lead Generation", "Sales Assistant", "Ultimate sales tool with proposal writing and presentation skills", "https://chatgpt.com/g/g-CS0BEb5pJ-sales-assistant-ultimate-sales-tool-for-sellers"],
            ["Financial Analysis & Investment", "Buffett Investment Tool", "Investment analysis inspired by Warren Buffett's strategies", "https://chatgpt.com/g/g-u7kq0UsG2-buffett-investment-tool"],
            ["Consulting & Advisory", "Executive Insight", "Senior McKinsey-level executive insights and data-driven recommendations", "https://chatgpt.com/g/g-DLrpkpntx-executive-insight"],
            ["Market Research & Analysis", "Business Lookup", "Locate businesses and analyze market landscapes", "https://chatgpt.com/g/g-0DxZTgo0i-business-lookup"],
            ["SaaS & Technology Business", "SaaS", "Business-oriented discussions on SaaS models and strategies", "https://chatgpt.com/g/g-T2bAANodC-saas"],
        ]
    },
    {
        "num": 7,
        "title": "Writing & Content Marketing",
        "count": 375,
        "percentage": "4.6%",
        "width": "4.6%",
        "subclusters": [
            ["SEO & Search Optimization", "Keyword Planner SEO", "SEO keyword research and content optimization strategies", "https://chatgpt.com/g/g-05Ju8F8Ts-keyword-planner-seo"],
            ["Social Media Content", "Viral Muse", "Transforms tweet ideas into viral-worthy content", "https://chatgpt.com/g/g-0LVKVFAOE-viral-muse"],
            ["Copywriting & Sales Copy", "Brand Crafter", "Creates compelling brand messaging and marketing copy", "https://chatgpt.com/g/g-07Kcpnfmn-brand-crafter"],
            ["Product Descriptions", "Product Description Generator", "Generates product descriptions for small business physical products", "https://chatgpt.com/g/g-Z6qhetSRr-product-description-generator"],
            ["Blog & Article Writing", "Newsletter Summarizer", "Summarizes newsletters to save time and extract key insights", "https://chatgpt.com/g/g-rkfllG5TM"],
            ["Email Marketing", "Responder", "Helps craft friendly and effective email responses", "https://chatgpt.com/g/g-Sdzx1bnMN-responder"],
            ["Brand Voice Development", "Execu-X Post Companion", "Professional X/Twitter posts that ensure engagement", "https://chatgpt.com/g/g-3wv1Wj3Rg-execu-x-post-companion"],
        ]
    },
    {
        "num": 8,
        "title": "Legal & Compliance",
        "count": 363,
        "percentage": "4.5%",
        "width": "4.5%",
        "subclusters": [
            ["Contract Law & Drafting", "Law & Order", "AI legal assistant for contract law and NDA drafting", "https://chatgpt.com/g/g-23MFe5i3r-law-order"],
            ["Jurisdiction-Specific Law (US)", "LexiAI: US Law", "Multilingual AI legal assistant for US law queries and research", "https://chatgpt.com/g/g-26Ogj8JJ4-lexiai-us-law"],
            ["Jurisdiction-Specific Law (UK/International)", "Pre-Solicitor AI: UK Law Simplified", "Simplifies UK laws before consulting a solicitor, with real case examples", "https://chatgpt.com/g/g-COySiYHrU-pre-solicitor-aitm-uk-law-simplified-free"],
            ["Regulatory Compliance", "California Building Code Helper", "Expert in California building codes and construction regulations", "https://chatgpt.com/g/g-hiahMzXsY-california-building-code-helper"],
            ["Supreme Court & Case Law", "Supreme Court Rulings", "Analyzes and explains Supreme Court decisions and legal precedents", "https://chatgpt.com/g/g-prBU1ubiC-supreme-court-rulings"],
            ["Specialized Legal Domains", "Kazakhstani Law Assistant", "Specialized knowledge of Kazakhstan's legal system", "https://chatgpt.com/g/g-0BI04f09L-kazakhstani-law-assistant"],
        ]
    },
    {
        "num": 9,
        "title": "Technical & Coding",
        "count": 329,
        "percentage": "4.1%",
        "width": "4.1%",
        "subclusters": [
            ["Web Development (Frontend/Backend)", "CSS Code Helper", "CSS design assistance with code examples and best practices", "https://chatgpt.com/g/g-ihUOhctYf-css-code-helper"],
            ["Specific Languages (Python, JavaScript, etc.)", "JavaScript GPT", "Expert JavaScript programming assistance and debugging", "https://chatgpt.com/g/g-0Fjo9Edoq-javascript-gpt"],
            ["Database & SQL", "Beta SQL Expert Pro", "Advanced SQL optimization and complex query development", "https://chatgpt.com/g/g-6740a711568c819189f561c15e0707e6-beta-sql-expert-pro"],
            ["DevOps & Infrastructure", "Linux Specialist", "Expert in Linux, DevOps, and Infrastructure as Code", "https://chatgpt.com/g/g-EkGy9mnx9-linux-specialist"],
            ["Smart Contracts & Blockchain", "Contract Builder 2.0", "Latest strategies for reducing gas costs in EVM smart contracts", "https://chatgpt.com/g/g-jUMcG3wTK-contract-builder-2-0"],
            ["IDE & Development Tools", "Visual Studio Code Expert", "Expert advice on VS Code features and workflow optimization", "https://chatgpt.com/g/g-FYMRmDqEY-visual-studio-code-expert"],
            ["Code Review & Debugging", "Code Whiz Pro", "Advanced code review and debugging assistance", "https://chatgpt.com/g/g-0Sjxa4A1J-code-whiz-pro"],
        ]
    },
    {
        "num": 10,
        "title": "Health & Wellness",
        "count": 305,
        "percentage": "3.8%",
        "width": "3.8%",
        "subclusters": [
            ["Dermatology & Skin Care", "Dermatology Advisor", "Upload skin condition photos for analysis and treatment suggestions", "https://chatgpt.com/g/g-XdmUwHrDs-dermatology-advisor"],
            ["Nutrition & Diet Planning", "Chef NutriGourmet", "Chef and nutritionist specializing in low-carb recipes and meal plans", "https://chatgpt.com/g/g-P0TXECLkv-chef-nutrigourmet"],
            ["Mental Health Support", "Mental Health Conversation Guide", "Supportive conversations for mental health and emotional well-being", "https://chatgpt.com/g/g-0Unl1Zwyp-mental-health-conversation-guide"],
            ["Fitness & Exercise", "Swim Coach Pro", "Personal swim training expert for technique, fitness, and motivation", "https://chatgpt.com/g/g-088Zut1ap-swim-coach-pro"],
            ["Medical Information & Conditions", "COVID-19", "Information and guidance about COVID-19 pandemic", "https://chatgpt.com/g/g-0Vutlfcvf-covid-19"],
            ["Specialized Health Conditions", "ARFID Helper", "Supportive guide for ARFID sufferers with detailed food descriptions", "https://chatgpt.com/g/g-0t6atNK4C-arfid-helper"],
            ["Healthcare Professional Support", "Healthcare Support Workers Assistant", "Enhances healthcare workers' daily tasks and workflows", "https://chatgpt.com/g/g-a30IbALzW-healthcare-support-workers-all-other-assistant"],
        ]
    },
    {
        "num": 11,
        "title": "Entertainment & Gaming",
        "count": 249,
        "percentage": "3.1%",
        "width": "3.1%",
        "subclusters": [
            ["Role-Playing Games (RPG)", "The Oracle", "Perfect oracle for solo or cooperative RPG GM emulation and storytelling", "https://chatgpt.com/g/g-qdH2XGV5M-the-oracle"],
            ["Video Game Guides", "Soul Seeker GPT", "Guide for souls-like games blending gameplay strategies with lore", "https://chatgpt.com/g/g-ySVdGHfgB-soul-seeker-gpt"],
            ["Sports Analysis & Statistics", "Tracer Bullet", "Player performance information during IPL 2024 cricket matches", "https://chatgpt.com/g/g-3HyguSH8I-tracer-bullet"],
            ["Interactive Story Games", "Text Quest", "Interactive text-based adventure game with dynamic storytelling", "https://chatgpt.com/g/g-09Gpm0Nti-text-quest"],
            ["Battle Simulators", "Battle GPT", "AI battle realism simulator with policy-compliant visuals", "https://chatgpt.com/g/g-GsRUjaYvz-battle-gpt"],
            ["Puzzle & Challenge Games", "Situation Puzzle", "Solve situation puzzles (海龟汤) with logical deduction", "https://chatgpt.com/g/g-KHcdRU9or-situation-puzzle-hai-gui-tang"],
            ["Survival & Strategy Games", "Survival Mentor", "Engaging survival challenge game with dynamic scenarios", "https://chatgpt.com/g/g-0i2rSQUGt-survival-mentor"],
        ]
    },
    {
        "num": 12,
        "title": "Spiritual & Mystical",
        "count": 167,
        "percentage": "2.1%",
        "width": "2.1%",
        "subclusters": [
            ["Tarot & Card Reading", "Tarot Love", "Tarot card readings focused on relationship guidance", "https://chatgpt.com/g/g-turuXxK5O-tarot-love"],
            ["Astrology & Horoscopes", "Daily Horoscope Numbers & Biorhythms", "Daily astrological forecasts with numerology and biorhythm analysis", "https://chatgpt.com/g/g-aLVuuBB9z-daily-horoscope-numbers-biorhythms-from-seeds-net"],
            ["Oracle & Divination", "The Oracle of Delphai", "Ancient oracle wisdom and prophetic insights", "https://chatgpt.com/g/g-0Aiuh2Npa-the-oracle-of-delphai-apollo-the-seer"],
            ["Religious & Spiritual Texts", "KJV Scripture Scholar", "King James Version Bible expert with interpretations", "https://chatgpt.com/g/g-Ijn8Z6frl-kjv-scripture-scholar"],
            ["Palmistry & Physical Divination", "Palm Reader", "Interprets palm readings from uploaded hand images", "https://chatgpt.com/g/g-5woUyUDBR-palm-reader"],
            ["Wisdom & Philosophy", "Oracle of Wisdom", "Ancient wisdom and philosophical insights for modern life", "https://chatgpt.com/g/g-TaAYv7qNm-oracle-of-wisdom"],
            ["Direct Divine Communication", "Talk to God", "Spiritual conversations framed as divine communication", "https://chatgpt.com/g/g-7T7TFTXxM-talk-to-god"],
        ]
    },
    {
        "num": 13,
        "title": "Niche Hobby & Lifestyle",
        "count": 107,
        "percentage": "1.3%",
        "width": "1.3%",
        "subclusters": [
            ["Sports & Fitness Coaching", "Swimming Coach", "Specialized swimming technique and training guidance", "https://chatgpt.com/g/g-0Tkruotfk-swimming-coach"],
            ["Crafts & DIY Projects", "Beehive Builder", "Helper for DIY builders designing horizontal beehives", "https://chatgpt.com/g/g-ccSSArTEk-beehive-builder"],
            ["Textile Arts (Quilting, Sewing, Knitting)", "Patchwork Pal Quilter's Aid", "Quilting projects with pattern ideas, sewing tips, and fabric advice", "https://chatgpt.com/g/g-yaLSMy7Q2-patchwork-pal-quilter-s-aid"],
            ["Home Decor & Interior Design", "Christmas Decorations", "Festive guide to Christmas decorations and holiday home decor", "https://chatgpt.com/g/g-waqDkUJEv-christmas-decorations"],
            ["Travel & Tourism", "Flights", "Flight search and travel planning assistance", "https://chatgpt.com/g/g-0A9Iqsdml-flights"],
            ["Wedding Planning", "Best Man/Maid of Honor Wedding Speech", "Craft memorable wedding speeches for best man or maid of honor", "https://chatgpt.com/g/g-0Msyma1Ec-best-man-maid-of-honor-wedding-speech"],
            ["Specialized Collecting & Hobbies", "Horse Racing Form Analyst", "Detailed analysis of horse racing data and performance trends", "https://chatgpt.com/g/g-V8DkAO9eK-horse-racing-form-analyst"],
        ]
    },
    {
        "num": 14,
        "title": "Unclassified",
        "count": 1799,
        "percentage": "22.2%",
        "width": "22.2%",
        "subclusters": [
            ["Extremely niche or unique purposes", "Proxy", "Description too vague to classify: 'New version of GPT available'", "https://chatgpt.com/g/g-0WRddrQEG-proxy"],
            ["Generic descriptions", "Various GPTs", "GPTs without clear specialization or unique value proposition", ""],
            ["Multi-purpose tools", "Various GPTs", "Tools that span multiple categories and don't fit a single cluster", ""],
            ["Experimental prototypes", "Various GPTs", "Early-stage or experimental GPT projects", ""],
            ["Language-specific tools", "Various GPTs", "GPTs designed for specific languages or cultural contexts", ""],
            ["Incomplete descriptions", "Various GPTs", "GPTs with broken or insufficient description data", ""],
        ]
    },
]

def generate_cluster_html(cluster):
    """Generate HTML for a single cluster"""
    html = f"""            <!-- Cluster {cluster['num']} -->
            <div class="cluster-card">
                <div class="cluster-header">
                    <div>
                        <div class="cluster-title">{cluster['num']}. {cluster['title']}</div>
                        <div class="cluster-percentage">{cluster['percentage']} of ecosystem</div>
                    </div>
                    <div class="cluster-count cluster-{cluster['num']}">{cluster['count']:,}</div>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill cluster-{cluster['num']}" style="width: 0%" data-width="{cluster['width']}"></div>
                </div>
                <ul class="sub-clusters">
"""

    for subcluster in cluster['subclusters']:
        category_name, gpt_name, description, url = subcluster
        html += f"""                    <li class="sub-cluster">
                        <div class="sub-cluster-header">{category_name}</div>
                        <div class="sub-cluster-details">
                            <div class="example-card">
                                <div class="example-title">{gpt_name}</div>
                                <div class="example-desc">{description}</div>
"""
        if url:
            html += f"""                                <a href="{url}" target="_blank" class="example-link">Try it →</a>
"""
        html += """                            </div>
                        </div>
                    </li>
"""

    html += """                </ul>
            </div>

"""
    return html

# Generate complete HTML
print(header)
for cluster in clusters:
    print(generate_cluster_html(cluster))
print(footer)
