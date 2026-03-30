#!/usr/bin/env python3
"""
Script Generator - AI-powered video script creation for faceless YouTube channels
Supports multiple profitable niches
"""
import random
import hashlib

class ScriptGenerator:
    """Generate engaging YouTube video scripts for faceless channels"""
    
    def __init__(self):
        self.niches = {}
        self._init_niches()
    
    def _init_niches(self):
        """Initialize niche-specific content pools"""
        
        # NICHE 1: I Ching / 易經 Wisdom
        self.niches['iching'] = {
            'title_templates': [
                'The {adjective} Truth About {topic} (I Ching Secrets)',
                'How {topic} Was Used by Ancient Chinese Emperors',
                '{number} {topic} Secrets Your Ancestors Never Told You',
                'The Hidden Meaning Behind {topic} (Revealed)',
                'I Ching Hexagram {num}: What It Means For Your {area}',
            ],
            'topics': [
                'Business Decisions', 'Investment Timing', 'Career Changes',
                'Relationship Luck', 'Wealth Attraction', 'Health Energy',
                'Morning Rituals', 'Entrepreneur Mindset', 'Risk Management',
                'Team Leadership', 'Market Timing', 'Product Launches',
            ],
            'adjectives': ['Shocking', 'Hidden', 'Ancient', 'Untold', 'Forbidden'],
            'segments': {
                'intro': [
                    "Welcome back to your daily dose of ancient wisdom. Today we're diving into {topic}.",
                    "If you've ever wondered about {topic}, this is the video you've been waiting for.",
                    "Today I reveal the secrets of {topic} that ancient masters kept hidden for millennia.",
                ],
                'hook': [
                    "Here's something most people never learn: {topic} isn't just superstition.",
                    "The ancient Chinese discovered something remarkable about {topic}...",
                    "What I'm about to share changed my entire approach to {topic}.",
                ],
                'main': [
                    "According to the I Ching, {topic} is governed by the energy of hexagram {hex}.",
                    "The ancient text says: '{quote}' This applies directly to your {topic} today.",
                    "There are {number} key principles for mastering {topic}: First, {p1}. Second, {p2}. Third, {p3}.",
                    "The {topic} cycle follows the pattern of yin and yang — when one peaks, the other begins.",
                ],
                'cta': [
                    "If you found value in this, drop a comment below with your birth year — I'll send you a personalized {topic} reading.",
                    "Subscribe for daily I Ching insights delivered to your feed every morning.",
                    "Next week we'll explore hexagram {next_hex} — make sure you're subscribed so you don't miss it.",
                ],
            },
            'quotes': [
                "The superior person uses stillness to nourish wisdom.",
                "When the time comes, act. When it hasn't, wait.",
                "The creative force advances with proper timing.",
                "In chaos, find order. In order, find growth.",
                "Patience is the root of all breakthrough.",
            ],
            'hexagrams': [
                ('䷀', 'Creative', '乾為天'), ('䷁', 'Receptive', '坤為地'),
                ('䷄', 'Waiting', '水天需'), ('䷐', 'Following', '澤雷隨'),
                ('䷊', 'Peace', '地天泰'), ('䷓', 'Contemplation', '風地觀'),
                ('䷖', 'Return', '地雷復'), ('䷗', 'Innocence', '天雷无妄'),
            ],
        }
        
        # NICHE 2: Numerology / Life Path
        self.niches['numerology'] = {
            'title_templates': [
                'Your Life Path Number {num} Reveals Your True Purpose',
                'What Your Birth Date Says About Your {topic}',
                '{num} Signs You\'re a Life Path {num} (Are You?)',
                'The Secret Meaning of {num} in Numerology',
            ],
            'topics': [
                'Soul Purpose', 'Financial Destiny', 'Relationship Compatibility',
                'Career Calling', 'Health Patterns', 'Spiritual Growth',
                'Karmic Lessons', 'Lucky Numbers', 'Destiny Number',
            ],
            'segments': {
                'intro': ['Today we explore your life path number {num} and what it means for {topic}.'],
                'main': [
                    'Life path {num} individuals share these {number} key traits: {traits}',
                    'Your birth number {num} connects to the energy of {planet}.',
                    'The numerology chart reveals your {topic} through the {num} pathway.',
                ],
            },
        }
        
        # NICHE 3: AI Tools / Productivity
        self.niches['aitools'] = {
            'title_templates': [
                'I Tried {num} AI Tools For {topic} — Here\'s What Actually Works',
                'This Free AI Tool Changed My {topic} Forever',
                '{num} Must-Have AI Tools for {topic} in 2026',
                'The Best AI Tool For {topic} ( Honest Review )',
            ],
            'topics': [
                'Content Creation', 'Passive Income', 'Side Hustles',
                'Productivity', 'Email Writing', 'Video Editing',
                'Social Media', 'Business Planning', 'Time Management',
            ],
            'segments': {
                'intro': ['AI tools are evolving fast. Today I share the best ones for {topic}.'],
                'main': [
                    'Tool number one: {tool1}. It\'s completely free and does {benefit1}.',
                    'Tool number two: {tool2}. The standout feature is {benefit2}.',
                    'My top pick for {topic} is {tool3} because {benefit3}.',
                    'The results? {result}. This {topic} workflow has saved me {time_saved}.',
                ],
            },
        }
        
        # NICHE 4: Ancient Wisdom / Philosophy
        self.niches['ancientwisdom'] = {
            'title_templates': [
                'The {adjective} Wisdom of {philosopher} That Changed My Life',
                '{philosopher}\'s Secret to {topic} (Nobel Prize Winners Use This)',
                'What {number} Years of {philosopher}\'s Teachings Taught Me',
                'The Ancient Formula for {topic} (Backed by Modern Science)',
            ],
            'philosophers': [
                'Lao Tzu', 'Confucius', 'Sun Tzu', 'Buddha', 'Socrates', 'Marcus Aurelius',
                'Seneca', 'Aristotle', 'Zhuangzi', 'Mencius',
            ],
            'topics': [
                'Inner Peace', 'Success', 'Wealth', 'Relationships', 'Mental Health',
                'Decision Making', 'Leadership', 'Happiness', 'Legacy', 'Purpose',
            ],
            'segments': {
                'intro': ['Today I share the timeless wisdom of {philosopher} on {topic}.'],
                'main': [
                    '{philosopher} said: "{quote}" Let me explain what this means for your {topic}.',
                    'The first principle: {p1}. This changes how you approach {topic}.',
                    'Principle two: {p2}. Practical application: {application}.',
                    'Ancient wisdom meets modern science: {study} found that {finding}.',
                ],
            },
            'quotes': [
                "The journey of a thousand miles begins with a single step.",
                "He who knows others is wise; he who knows himself is enlightened.",
                "In the midst of chaos, there is also opportunity.",
                "The best time to plant a tree was twenty years ago. The second best time is now.",
                "Be content with what you have; rejoice in the way things are.",
            ],
        }
        
        # NICHE 5: Passive Income / Entrepreneurship
        self.niches['passiveincome'] = {
            'title_templates': [
                '{number} Passive Income Ideas For {topic} (No Fluff)',
                'I Made ${amount} From {topic} Last Month — Here\'s How',
                'The {adjective} Truth About Passive Income from {topic}',
                'How to Start {topic} With ${budget} (Step by Step)',
            ],
            'topics': [
                'Digital Products', 'Affiliate Marketing', 'SaaS',
                'Dividends', 'Rental Income', 'Online Courses',
                'Content Creation', 'Licensing', 'E-commerce',
            ],
            'segments': {
                'intro': ['Passive income is the holy grail of financial freedom. Here\'s {topic}.'],
                'main': [
                    'Idea {num}: {idea}. The setup cost is approximately ${cost}.',
                    'The key metric you need is {metric} — aim for at least {target}.',
                    'Most people quit too early. The truth is, {truth} takes {time}.',
                    'My results after {months} months: {result}. Your results will vary.',
                ],
            },
        }
    
    def generate_script(self, niche, topic_override=None, num_segments=5):
        """Generate a complete video script for the given niche"""
        niche_data = self.niches.get(niche.lower())
        if not niche_data:
            return None
        
        # Pick topic
        if topic_override:
            topic = topic_override
        else:
            topic = random.choice(niche_data.get('topics', ['Success']))
        
        # Pick hexagram (for iching niche)
        hex_data = random.choice(niche_data.get('hexagrams', [('', '', '')]))
        
        # Build title
        title_template = random.choice(niche_data.get('title_templates', ['{topic} Explained']))
        title = self._fill_template(title_template, topic=topic, niche=niche_data, hex=hex_data)
        
        # Build segments
        segments = []
        segment_templates = niche_data.get('segments', {})
        
        for i in range(num_segments):
            seg_type = 'main'
            template = random.choice(segment_templates.get(seg_type, ['{topic} is powerful.']))
            segment_text = self._fill_template(template, topic=topic, niche=niche_data, 
                                                hex=hex_data, num=i+1)
            
            segments.append({
                'text': segment_text,
                'sub': f'Point {i+1}',
                'duration': random.uniform(25, 45)  # 25-45 seconds per main segment
            })
        
        # Intro
        intro_templates = segment_templates.get('intro', ['Today we explore {topic}.'])
        intro = self._fill_template(random.choice(intro_templates), topic=topic, niche=niche_data)
        
        # Outro / CTA
        cta_templates = segment_templates.get('cta', ['Subscribe for more!'])
        outro = self._fill_template(random.choice(cta_templates), topic=topic, niche=niche_data)
        
        script = {
            'title': title,
            'subtitle': f'☯️ {topic} | Ancient Wisdom for Modern Life',
            'intro': intro,
            'segments': segments,
            'outro': outro,
            'niche': niche,
            'topic': topic,
        }
        
        return script
    
    def _fill_template(self, template, **kwargs):
        """Fill in template variables with random selections"""
        text = template
        
        replacements = {
            'topic': kwargs.get('topic', 'Success'),
            'num': kwargs.get('num', random.randint(1, 9)),
            'number': str(random.randint(3, 7)),
            'adjective': random.choice(['Hidden', 'Ancient', 'Forbidden', 'Shocking']),
            'hex': kwargs.get('hex', ('', '', ''))[0] if kwargs.get('hex') else '',
            'philosopher': random.choice(kwargs.get('niche', {}).get('philosophers', ['Ancient Master'])),
            'quote': random.choice(kwargs.get('niche', {}).get('quotes', ['Wisdom is power.'])),
            'amount': random.choice(['100', '500', '1,000', '5,000']),
            'budget': random.choice(['100', '500', '1,000', 'Zero']),
            'time': random.choice(['3 months', '6 months', '1 year', '2 years']),
            'months': str(random.randint(3, 18)),
            'result': random.choice(['significant growth', 'steady progress', 'breakthrough results']),
            'p1': random.choice(['timing matters most', 'consistency beats intensity', 'strategy before action']),
            'p2': random.choice(['adapt to circumstances', 'learn from failure', 'build leverage']),
            'p3': random.choice(['never stop learning', 'serve others first', 'think long-term']),
            'traits': random.choice(['leadership, creativity, and vision', 'analytical thinking and patience', 'empathy and strategic thinking']),
            'planet': random.choice(['Sun', 'Moon', 'Mercury', 'Venus', 'Jupiter']),
            'idea': random.choice(['Print-on-demand stores', 'Niche affiliate blogs', 'Digital templates', 'Online coaching']),
            'cost': random.choice(['50', '100', '500', '0']),
            'metric': random.choice(['conversion rate', 'monthly traffic', 'email list size', 'engagement rate']),
            'target': random.choice(['5%', '1000', '500 subscribers', '10%']),
            'truth': random.choice(['real passive income', 'sustainable growth', 'profitable niche']),
            'time_saved': random.choice(['10 hours/week', '20 hours/week', '3 hours/day']),
            'tool1': random.choice(['ChatGPT', 'Claude', 'Gemini', 'Perplexity']),
            'benefit1': random.choice(['content creation', 'research', 'writing', 'analysis']),
            'tool2': random.choice(['Canva', 'Capcut', 'Notion', 'Zapier']),
            'benefit2': random.choice(['speed', 'ease of use', 'automation', 'templates']),
            'tool3': random.choice(['the tool I use daily', 'this underrated option', 'my go-to choice']),
            'benefit3': random.choice(['it saves time', 'it\'s free', 'it\'s powerful', 'it\'s beginner-friendly']),
            'study': random.choice(['Stanford study', 'Harvard research', 'MIT findings']),
            'finding': random.choice(['ancient practices work', 'consistency is key', 'small improvements compound']),
            'application': random.choice(['start today', 'apply weekly', 'track monthly']),
            'next_hex': kwargs.get('hex', ('', '', ''))[0] if kwargs.get('hex') else '䷀',
        }
        
        for key, val in replacements.items():
            placeholder = '{' + key + '}'
            if placeholder in text:
                text = text.replace(placeholder, str(val))
        
        return text
    
    def generate_batch(self, niche, count=5, topics=None):
        """Generate multiple scripts for A/B testing"""
        scripts = []
        topic_list = topics or [None] * count
        
        for i, topic in enumerate(topic_list):
            script = self.generate_script(niche, topic_override=topic)
            if script:
                scripts.append(script)
        
        return scripts

if __name__ == '__main__':
    gen = ScriptGenerator()
    
    # Generate sample scripts
    print("=" * 60)
    print("FACELESS YOUTUBE SCRIPT FACTORY")
    print("=" * 60)
    
    for niche in ['iching', 'ancientwisdom', 'passiveincome']:
        print(f"\n📹 {niche.upper()} Channel")
        print("-" * 40)
        
        scripts = gen.generate_batch(niche, count=3)
        for i, s in enumerate(scripts):
            print(f"\n  Script {i+1}: {s['title']}")
            print(f"  Intro: {s['intro'][:60]}...")
            print(f"  Segments: {len(s['segments'])} content blocks")
            print(f"  CTA: {s['outro'][:60]}...")
