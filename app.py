import streamlit as st
import random
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Lilova ✨ Your Soft Girl Bestie",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for soft girl aesthetic
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #ffeef8 0%, #f0e6ff 100%);
        color: #c44569;
    }
    
    .stApp {
        background: linear-gradient(135deg, #ffeef8 0%, #f0e6ff 100%);
        color: #c44569;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 20px;
        border: 2px solid #ffb3d9;
        box-shadow: 0 8px 32px rgba(255, 179, 217, 0.3);
        backdrop-filter: blur(10px);
        margin: 10px 0;
        color: #c44569;
    }
    
    .affirmation-card {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        color: #c44569;
        font-size: 18px;
        font-weight: 500;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(255, 154, 158, 0.4);
    }
    
    .glow-text {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        background: linear-gradient(45deg, #ff6b9d, #c44569, #f8b500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(255, 107, 157, 0.5);
        margin-bottom: 20px;
    }
    
    .bestie-chat {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 20px;
        border-radius: 20px;
        border-left: 5px solid #ff6b9d;
        margin: 15px 0;
        color: #c44569;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #ffeef8 0%, #f0e6ff 100%);
    }
    
    .success-message {
        background: linear-gradient(135deg, #98fb98 0%, #90ee90 100%);
        padding: 15px;
        border-radius: 15px;
        color: #2d5a2d;
        margin: 10px 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {}
    if 'journal_entries' not in st.session_state:
        st.session_state.journal_entries = []
    if 'skincare_routine' not in st.session_state:
        st.session_state.skincare_routine = {}
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'daily_affirmation' not in st.session_state:
        st.session_state.daily_affirmation = None
    if 'last_affirmation_date' not in st.session_state:
        st.session_state.last_affirmation_date = None

init_session_state()

# Data for recommendations
SKINCARE_ROUTINES = {
    "oily": {
        "morning": ["Gentle foaming cleanser", "Niacinamide serum", "Lightweight moisturizer", "SPF 30+ sunscreen"],
        "evening": ["Oil cleanser", "Salicylic acid cleanser", "Retinol serum (2-3x/week)", "Night moisturizer"]
    },
    "dry": {
        "morning": ["Cream cleanser", "Hyaluronic acid serum", "Rich moisturizer", "SPF 30+ sunscreen"],
        "evening": ["Micellar water", "Gentle cleanser", "Face oil", "Heavy night cream"]
    },
    "combination": {
        "morning": ["Gel cleanser", "Vitamin C serum", "Lightweight moisturizer", "SPF 30+ sunscreen"],
        "evening": ["Double cleanse", "BHA toner (3x/week)", "Niacinamide serum", "Moisturizer"]
    },
    "sensitive": {
        "morning": ["Gentle cleanser", "Ceramide serum", "Fragrance-free moisturizer", "Mineral sunscreen"],
        "evening": ["Gentle cleanser", "Soothing toner", "Barrier repair cream", "Face oil"]
    }
}

FASHION_TIPS = {
    "soft girl": ["Pastel colors", "Oversized cardigans", "High-waisted jeans", "Crop tops", "Sneakers", "Hair accessories"],
    "dark academia": ["Tweed blazers", "Pleated skirts", "Oxford shoes", "Turtlenecks", "Trench coats", "Gold jewelry"],
    "cottagecore": ["Flowy dresses", "Cardigans", "Mary Jane shoes", "Floral prints", "Linen fabrics", "Vintage accessories"],
    "minimalist": ["Neutral colors", "Clean lines", "Quality basics", "Structured pieces", "Simple jewelry", "Classic shoes"]
}

MAKEUP_LOOKS = {
    "natural glow": ["Tinted moisturizer", "Cream blush", "Clear lip gloss", "Mascara", "Brow gel"],
    "soft glam": ["Medium coverage foundation", "Neutral eyeshadow", "Winged eyeliner", "False lashes", "Nude lipstick"],
    "dewy skin": ["Hydrating primer", "Light foundation", "Liquid highlighter", "Cream products", "Glossy lips"],
    "bold lips": ["Full coverage base", "Neutral eyes", "Statement lipstick", "Subtle highlight", "Defined brows"]
}

AFFIRMATIONS = [
    "I am worthy of love and respect exactly as I am ✨",
    "My feminine energy is powerful and magnetic 🌙",
    "I choose to see beauty in myself every day 🌸",
    "I trust my intuition and inner wisdom 💎",
    "I am becoming the woman I'm meant to be 🦋",
    "My confidence grows stronger every day 💪",
    "I deserve all the good things coming my way 🌟",
    "I am soft and strong at the same time 🌺",
    "My energy attracts my tribe 💕",
    "I am worthy of my dreams and goals ✨"
]

JOURNAL_PROMPTS = [
    "What made me feel most beautiful today?",
    "How did I show myself love this week?",
    "What are three things I'm grateful for about my body?",
    "When do I feel most confident and why?",
    "What feminine qualities do I admire in myself?",
    "How can I be kinder to myself tomorrow?",
    "What boundaries do I need to set for my wellbeing?",
    "What makes me feel most authentically me?",
    "How have I grown in the past month?",
    "What would I tell my younger self about self-love?"
]

AESTHETIC_MOODS = {
    "soft girl vibes": ["🌸 Pink sunsets", "☁️ Fluffy clouds", "🍑 Peach aesthetics", "✨ Glitter details", "🌙 Moon phases"],
    "dark academia": ["📚 Old books", "🕯️ Candlelight", "🍂 Autumn leaves", "☕ Coffee shops", "🏛️ Classical architecture"],
    "cottagecore dream": ["🌻 Wildflowers", "🍄 Mushroom forests", "🥖 Fresh bread", "🐝 Busy bees", "🌿 Herb gardens"],
    "ethereal fairy": ["🧚‍♀️ Fairy lights", "🌙 Crescent moons", "✨ Starry skies", "🦋 Butterflies", "🌸 Cherry blossoms"]
}

# Helper functions
def get_daily_affirmation():
    """Get a consistent daily affirmation"""
    today = datetime.now().date()
    if st.session_state.last_affirmation_date != today:
        st.session_state.daily_affirmation = random.choice(AFFIRMATIONS)
        st.session_state.last_affirmation_date = today
    return st.session_state.daily_affirmation

def generate_chat_response(user_input):
    """Generate response based on user input"""
    user_input_lower = user_input.lower()
    
    # Keyword-based responses
    if any(word in user_input_lower for word in ['sad', 'down', 'depressed', 'upset']):
        return "Oh sweetie, I hear you. It's okay to feel sad sometimes. You're human and your feelings are valid. Want to try a quick mood boost? Take three deep breaths with me. Remember, this feeling will pass and brighter days are coming. You're stronger than you know! 💕"
    
    elif any(word in user_input_lower for word in ['stressed', 'overwhelmed', 'anxious', 'worried']):
        return "I can feel your stress, babe. Let's take a moment together. Close your eyes and breathe slowly. You're doing your best, and that's enough. What's one small thing you can do right now to feel a little better? Maybe some water, a quick walk, or a favorite song? You've got this! ✨"
    
    elif any(word in user_input_lower for word in ['confident', 'good', 'great', 'amazing', 'happy']):
        return "YES QUEEN! I love this energy! You're absolutely glowing today. Keep radiating that confidence - it looks amazing on you! What's making you feel so empowered today? I want to celebrate with you! 🌟"
    
    elif any(word in user_input_lower for word in ['insecure', 'ugly', 'worthless', 'not good enough']):
        return "Sweet girl, those negative thoughts are lying to you. You are worthy, beautiful, and enough exactly as you are. What would you say to your best friend if they felt this way? Show yourself that same love. You're more amazing than you realize! 💖"
    
    elif any(word in user_input_lower for word in ['skincare', 'skin', 'routine']):
        return "Ooh, skincare talk! I love it! ✨ Your skin is beautiful and deserves to be pampered. Check out my skincare routine generator - I can help you create the perfect routine for your skin type. Remember, consistency is key and you're already glowing! 🌸"
    
    elif any(word in user_input_lower for word in ['fashion', 'style', 'outfit', 'clothes']):
        return "Fashion queen! 👗 I'm so excited to talk style with you! Your personal style is a beautiful expression of who you are. Check out my fashion styling tips - I can help you curate looks that make you feel absolutely amazing. You have such good taste! ✨"
    
    else:
        return "That's so interesting, bestie! I'm here to listen and support you. Remember, you're absolutely amazing and I believe in you! What else is going on in your world? 💕✨"

# Sidebar Navigation
st.sidebar.markdown("# 🌸 Navigation")
page = st.sidebar.selectbox(
    "Choose your glow-up journey:",
    ["🏠 Home", "✨ Skincare Routine", "👗 Fashion Styling", "💄 Makeup Tips", 
     "🌙 Feminine Energy", "💪 Confidence Booster", "📅 Glow-Up Planner", 
     "📝 Journal Prompts", "🎨 Aesthetic Moodboard", "💬 Chat with Lilova"]
)

# Main content based on selected page
if page == "🏠 Home":
    st.markdown('<div class="glow-text">Lilova ✨</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 24px; color: #c44569;">Your Soft Girl Bestie</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="bestie-chat">
        <h3>Hey gorgeous! 💕</h3>
        <p>Welcome to your personal glow-up space! I'm Lilova, and I'm here to be your supportive bestie on this beautiful journey of self-love and growth. Whether you need skincare advice, fashion inspo, or just a confidence boost, I've got you covered!</p>
        
        <p><strong>What we can explore together:</strong></p>
        <ul>
            <li>✨ Personalized skincare routines</li>
            <li>👗 Fashion styling for your vibe</li>
            <li>💄 Makeup looks that enhance your natural beauty</li>
            <li>🌙 Feminine energy and self-love practices</li>
            <li>💪 Daily confidence boosters</li>
            <li>📝 Mindful journaling prompts</li>
        </ul>
        
        <p>Remember: You're already perfect, we're just here to help you glow even brighter! 🌟</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick daily affirmation
    st.markdown("### 💫 Today's Affirmation")
    daily_affirmation = get_daily_affirmation()
    st.markdown(f'<div class="affirmation-card">{daily_affirmation}</div>', unsafe_allow_html=True)

elif page == "✨ Skincare Routine":
    st.markdown("# ✨ Skincare Routine Generator")
    st.markdown("Let's create your perfect skincare routine, bestie! 💕")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Tell me about your skin:")
        skin_type = st.selectbox("What's your skin type?", ["oily", "dry", "combination", "sensitive"])
        skin_concerns = st.multiselect(
            "Any specific concerns?",
            ["acne", "aging", "hyperpigmentation", "dullness", "large pores", "sensitivity"]
        )
        budget = st.selectbox("Budget range:", ["drugstore", "mid-range", "luxury", "mixed"])
    
    with col2:
        st.markdown("### Lifestyle factors:")
        climate = st.selectbox("Your climate:", ["humid", "dry", "cold", "tropical"])
        time_available = st.selectbox("Time for routine:", ["5 minutes", "10-15 minutes", "20+ minutes"])
        experience = st.selectbox("Skincare experience:", ["beginner", "intermediate", "advanced"])
    
    if st.button("✨ Generate My Routine"):
        routine = SKINCARE_ROUTINES.get(skin_type, SKINCARE_ROUTINES["combination"])
        
        st.markdown("### 🌅 Morning Routine")
        for i, step in enumerate(routine["morning"], 1):
            st.markdown(f"**Step {i}:** {step}")
        
        st.markdown("### 🌙 Evening Routine")
        for i, step in enumerate(routine["evening"], 1):
            st.markdown(f"**Step {i}:** {step}")
        
        # Save routine to session state
        st.session_state.skincare_routine = {
            "skin_type": skin_type,
            "routine": routine,
            "date_created": datetime.now().strftime("%Y-%m-%d")
        }
        
        st.markdown("""
        <div class="bestie-chat">
            <h4>Bestie Tips! 💡</h4>
            <ul>
                <li>Always patch test new products</li>
                <li>Introduce actives slowly</li>
                <li>Consistency is key - give products 4-6 weeks</li>
                <li>Don't forget sunscreen is your BFF!</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif page == "👗 Fashion Styling":
    st.markdown("# 👗 Fashion Styling Tips")
    st.markdown("Let's find your perfect style, gorgeous! ✨")
    
    aesthetic = st.selectbox(
        "What aesthetic speaks to your soul?",
        ["soft girl", "dark academia", "cottagecore", "minimalist"]
    )
    
    occasion = st.selectbox(
        "What's the occasion?",
        ["everyday casual", "date night", "work/school", "special event", "cozy day"]
    )
    
    season = st.selectbox("Current season:", ["spring", "summer", "fall", "winter"])
    
    if st.button("💫 Get My Style Tips"):
        tips = FASHION_TIPS.get(aesthetic, FASHION_TIPS["soft girl"])
        
        st.markdown(f"### Perfect pieces for your {aesthetic} vibe:")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Must-have items:**")
            for item in tips[:3]:
                st.markdown(f"✨ {item}")
        
        with col2:
            st.markdown("**Styling accessories:**")
            for item in tips[3:]:
                st.markdown(f"✨ {item}")
        
        st.markdown(f"""
        <div class="bestie-chat">
            <h4>Style Inspo for {occasion}! 💕</h4>
            <p>Mix and match these pieces to create looks that feel authentically YOU. Remember, confidence is your best accessory!</p>
            
            <p><strong>Pro tip:</strong> Start with one statement piece and build around it. You've got this, bestie! 🌟</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "💄 Makeup Tips":
    st.markdown("# 💄 Makeup Recommendations")
    st.markdown("Let's enhance your natural beauty! 🌸")
    
    col1, col2 = st.columns(2)
    
    with col1:
        look_type = st.selectbox(
            "What look are you going for?",
            ["natural glow", "soft glam", "dewy skin", "bold lips"]
        )
        
        skin_tone = st.selectbox(
            "Your skin undertone:",
            ["warm", "cool", "neutral", "not sure"]
        )
    
    with col2:
        experience_level = st.selectbox(
            "Makeup experience:",
            ["beginner", "intermediate", "advanced"]
        )
        
        time_budget = st.selectbox(
            "Time available:",
            ["5 minutes", "15 minutes", "30+ minutes"]
        )
    
    if st.button("✨ Get My Makeup Guide"):
        products = MAKEUP_LOOKS.get(look_type, MAKEUP_LOOKS["natural glow"])
        
        st.markdown(f"### Perfect {look_type} look:")
        
        for i, product in enumerate(products, 1):
            st.markdown(f"**Step {i}:** {product}")
        
        st.markdown("""
        <div class="bestie-chat">
            <h4>Makeup Bestie Tips! 💄</h4>
            <ul>
                <li>Less is more - enhance, don't hide your beauty</li>
                <li>Blend, blend, blend for seamless looks</li>
                <li>Good skincare = better makeup application</li>
                <li>Practice makes perfect - have fun with it!</li>
                <li>Your natural features are already gorgeous ✨</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif page == "🌙 Feminine Energy":
    st.markdown("# 🌙 Feminine Energy & Affirmations")
    st.markdown("Connect with your divine feminine energy, queen! ✨")
    
    energy_focus = st.selectbox(
        "What do you want to cultivate today?",
        ["self-love", "confidence", "intuition", "creativity", "sensuality", "inner peace"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🌟 Generate Affirmation"):
            affirmation = random.choice(AFFIRMATIONS)
            st.markdown(f'<div class="affirmation-card">{affirmation}</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("🌙 Feminine Energy Practice"):
            practices = {
                "self-love": "Take 5 minutes to look in the mirror and speak kindly to yourself",
                "confidence": "Stand in a power pose for 2 minutes and breathe deeply",
                "intuition": "Sit quietly and ask your heart what it needs today",
                "creativity": "Spend 10 minutes doing something creative without judgment",
                "sensuality": "Light a candle, play soft music, and appreciate your senses",
                "inner peace": "Practice gentle breathing and body appreciation"
            }
            
            practice = practices.get(energy_focus, practices["self-love"])
            st.markdown(f"""
            <div class="bestie-chat">
                <h4>Today's Practice: {energy_focus.title()} ✨</h4>
                <p>{practice}</p>
                <p><em>Remember: You are worthy of love, respect, and all beautiful things 💕</em></p>
            </div>
            """, unsafe_allow_html=True)

elif page == "💪 Confidence Booster":
    st.markdown("# 💪 Confidence Booster Corner")
    st.markdown("Building your confidence one day at a time! 🌟")
    
    confidence_area = st.selectbox(
        "Which area needs a boost today?",
        ["body image", "social situations", "career/goals", "relationships", "self-expression", "general confidence"]
    )
    
    if st.button("💫 Boost My Confidence"):
        boosters = {
            "body image": [
                "List 3 things your body did for you today",
                "Practice the mirror meditation: look at yourself with love",
                "Wear something that makes you feel good",
                "Remember: Your worth isn't determined by your appearance"
            ],
            "social situations": [
                "Remember: Everyone is focused on themselves, not judging you",
                "Practice one genuine compliment to someone today",
                "Your unique perspective adds value to conversations",
                "Start small - smile at one person today"
            ],
            "career/goals": [
                "Write down 3 skills you've developed this year",
                "Celebrate small wins along the way",
                "Remember: You belong in rooms you enter",
                "Your dreams are valid and achievable"
            ],
            "relationships": [
                "You deserve relationships that lift you up",
                "Practice setting healthy boundaries",
                "Your authentic self attracts the right people",
                "Quality over quantity in friendships"
            ],
            "self-expression": [
                "Your voice and opinions matter",
                "Practice expressing one authentic thought today",
                "Creativity is your birthright - use it freely",
                "There's no wrong way to be yourself"
            ],
            "general confidence": [
                "You've overcome challenges before, you can do it again",
                "Celebrate your unique qualities",
                "Progress, not perfection",
                "You are enough exactly as you are"
            ]
        }
        
        tips = boosters.get(confidence_area, boosters["general confidence"])
        
        st.markdown(f"### {confidence_area.title()} Confidence Boosters:")
        for tip in tips:
            st.markdown(f"✨ {tip}")
        
        st.markdown("""
        <div class="affirmation-card">
            You are capable, worthy, and enough exactly as you are right now! 🌟
        </div>
        """, unsafe_allow_html=True)

elif page == "📅 Glow-Up Planner":
    st.markdown("# 📅 Glow-Up Planner")
    st.markdown("Plan your transformation journey, bestie! ✨")
    
    tab1, tab2, tab3 = st.tabs(["🎯 Goals", "📋 Weekly Plan", "📊 Progress"])
    
    with tab1:
        st.markdown("### Set Your Glow-Up Goals")
        
        goal_areas = st.multiselect(
            "Areas to focus on:",
            ["skincare", "fitness", "mindset", "style", "relationships", "career", "hobbies", "self-care"]
        )
        
        goals_set = []
        for area in goal_areas:
            goal = st.text_input(f"Your {area} goal:", key=f"goal_{area}")
            if goal:
                goals_set.append(f"{area.title()}: {goal}")
                st.markdown(f'<div class="success-message">✨ {area.title()} goal set: {goal}</div>', unsafe_allow_html=True)
        
        if goals_set:
            st.session_state.user_profile['goals'] = goals_set
    
    with tab2:
        st.markdown("### This Week's Glow-Up Plan")
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for day in days:
            with st.expander(f"✨ {day}"):
                self_care = st.text_input(f"Self-care activity for {day}:", key=f"care_{day}")
                growth = st.text_input(f"Growth activity for {day}:", key=f"growth_{day}")
                affirmation = st.text_input(f"Affirmation for {day}:", key=f"aff_{day}")
    
    with tab3:
        st.markdown("### Track Your Glow-Up Journey")
        
        mood_rating = st.slider("How are you feeling today? (1-10)", 1, 10, 7)
        confidence_rating = st.slider("Confidence level today? (1-10)", 1, 10, 7)
        
        wins = st.text_area("Today's wins (big or small!):")
        gratitude = st.text_area("What are you grateful for today?")
        
        if st.button("💕 Save Today's Check-in"):
            check_in = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "mood": mood_rating,
                "confidence": confidence_rating,
                "wins": wins,
                "gratitude": gratitude
            }
            
            if 'check_ins' not in st.session_state:
                st.session_state.check_ins = []
            st.session_state.check_ins.append(check_in)
            
            st.markdown('<div class="success-message">Your glow-up journey is recorded! Keep shining, bestie! ✨</div>', unsafe_allow_html=True)

elif page == "📝 Journal Prompts":
    st.markdown("# 📝 Journal Prompt Generator")
    st.markdown("Let's dive deep into self-reflection, beautiful! 🌸")
    
    prompt_type = st.selectbox(
        "What kind of reflection do you need?",
        ["self-love", "growth", "gratitude", "dreams", "relationships", "body positivity", "mindfulness"]
    )
    
    if st.button("✨ Generate Prompt"):
        # Filter prompts based on type
        if prompt_type == "self-love":
            prompts = [p for p in JOURNAL_PROMPTS if any(word in p.lower() for word in ["love", "beautiful", "kind"])]
        elif prompt_type == "body positivity":
            prompts = [p for p in JOURNAL_PROMPTS if "body" in p.lower()]
        elif prompt_type == "growth":
            prompts = [p for p in JOURNAL_PROMPTS if any(word in p.lower() for word in ["grow", "grown", "confident"])]
        else:
            prompts = JOURNAL_PROMPTS
        
        if not prompts:  # Fallback if no prompts match
            prompts = JOURNAL_PROMPTS
            
        prompt = random.choice(prompts)
        
        st.markdown(f"""
        <div class="bestie-chat">
            <h3>Today's Journal Prompt ✨</h3>
            <p style="font-size: 18px; font-style: italic;">"{prompt}"</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📖 Your Reflection Space")
        journal_entry = st.text_area("Write your thoughts here...", height=200, key="journal_text")
        
        if st.button("💕 Save Entry") and journal_entry:
            entry = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "prompt": prompt,
                "entry": journal_entry,
                "type": prompt_type
            }
            st.session_state.journal_entries.append(entry)
            st.markdown('<div class="success-message">Your beautiful thoughts are saved! 🌟</div>', unsafe_allow_html=True)
    
    if st.session_state.journal_entries:
        st.markdown("### 📚 Your Recent Journal Entries")
        for entry in reversed(st.session_state.journal_entries[-3:]):  # Show last 3 entries in reverse order
            with st.expander(f"Entry from {entry['date']}"):
                st.markdown(f"**Prompt:** {entry['prompt']}")
                st.markdown(f"**Reflection:** {entry['entry']}")

elif page == "🎨 Aesthetic Moodboard":
    st.markdown("# 🎨 Aesthetic Moodboard Ideas")
    st.markdown("Create your visual inspiration, gorgeous! ✨")
    
    aesthetic_choice = st.selectbox(
        "Choose your aesthetic vibe:",
        ["soft girl vibes", "dark academia", "cottagecore dream", "ethereal fairy"]
    )
    
    if st.button("🌟 Generate Moodboard Ideas"):
        ideas = AESTHETIC_MOODS.get(aesthetic_choice, AESTHETIC_MOODS["soft girl vibes"])
        
        st.markdown(f"### {aesthetic_choice.title()} Moodboard Elements:")
        
        cols = st.columns(3)
        for i, idea in enumerate(ideas):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="feature-card" style="text-align: center;">
                    <h4>{idea}</h4>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="bestie-chat">
            <h4>Moodboard Creation Tips! 🎨</h4>
            <ul>
                <li>Use Pinterest or Canva to collect images</li>
                <li>Include colors, textures, and objects that speak to you</li>
                <li>Add quotes or words that inspire you</li>
                <li>Make it personal - what makes YOU feel beautiful?</li>
                <li>Update it regularly as you grow and evolve ✨</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif page == "💬 Chat with Lilova":
    st.markdown("# 💬 Chat with Lilova")
    st.markdown("Hey bestie! What's on your mind today? 💕")
    
    # Chat input
    user_input = st.text_input("Talk to me, gorgeous:", key="chat_input")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        send_button = st.button("💫 Send")
    with col2:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    if send_button and user_input.strip():
        # Generate response
        response = generate_chat_response(user_input)
        
        # Add to chat history
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Lilova", response))
        
        # Clear input (this will happen on rerun)
        st.rerun()
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### 💬 Our Conversation")
        
        # Show recent messages (last 10 messages)
        recent_messages = st.session_state.chat_history[-10:]
        
        for speaker, message in recent_messages:
            if speaker == "You":
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.6); padding: 15px; border-radius: 15px; margin: 10px 0; border-left: 4px solid #ff6b9d;">
                    <strong>You:</strong> {message}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="bestie-chat">
                    <strong>Lilova:</strong> {message}
                </div>
                """, unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div class="bestie-chat">
            <h4>Start our conversation! 💕</h4>
            <p>I'm here to listen, support, and chat about anything on your mind. Whether you need advice, want to share something exciting, or just need a friend - I'm here for you, gorgeous! ✨</p>
            
            <p><strong>Some things we can talk about:</strong></p>
            <ul>
                <li>How you're feeling today</li>
                <li>Your dreams and goals</li>
                <li>Self-care and beauty tips</li>
                <li>Confidence and self-love</li>
                <li>Or anything else that's on your heart!</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #c44569;">
    <p>✨ Remember: You're a work of art, bestie! Keep glowing! ✨</p>
    <p><small>Made with 💕 for all the beautiful souls on their glow-up journey</small></p>
</div>
""", unsafe_allow_html=True)