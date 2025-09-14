from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Mock data for demonstration
SAMPLE_BADGES = [
    "Handmade with Love", "Eco-Friendly Materials", "Limited Edition",
    "Locally Sourced", "Award Winning", "Custom Orders Available"
]

CRAFT_DESCRIPTIONS = {
    "pottery": "Creating beautiful ceramic pieces using traditional wheel-throwing and hand-building techniques. Each piece is unique, with organic forms and glazes inspired by nature.",
    "jewelry": "Handcrafted jewelry featuring sustainable materials, unique gemstones, and artisan craftsmanship. Each piece tells a story and is made to last generations.",
    "textiles": "Woven textiles and fiber art created with natural dyes and traditional techniques. From scarves to wall hangings, each piece is a labor of love.",
    "wood": "Fine woodworking combining traditional joinery with contemporary design. Creating functional art pieces from sustainably sourced woods.",
    "glass": "Glass art featuring blown glass and fused glass techniques. Vibrant colors and organic forms inspired by the natural world.",
    "other": "Unique handmade creations crafted with attention to detail and passion for the artisanal process. Each piece is one-of-a-kind."
}

SOCIAL_IDEAS = {
    "pottery": [
        "Behind-the-scenes video of throwing clay on the wheel",
        "Glaze transformation before and after firing",
        "Studio tour showing tools and workspace"
    ],
    "jewelry": [
        "Close-up video of stone setting process",
        "How to style your handmade jewelry",
        "Meet the maker: my journey as a jeweler"
    ],
    "textiles": [
        "Time-lapse of weaving process",
        "Natural dyeing tutorial using plants",
        "How I source my sustainable materials"
    ],
    "wood": [
        "Wood grain close-ups showing natural beauty",
        "Joinery technique demonstration",
        "From tree to finished product journey"
    ],
    "glass": [
        "Glass blowing process in action",
        "Color mixing techniques demonstration",
        "How glass reacts to different temperatures"
    ],
    "other": [
        "A day in the life of an artisan",
        "How I find inspiration for my work",
        "The story behind my favorite creation"
    ]
}

PRODUCT_DESCRIPTIONS = {
    "pottery": [
        "Hand-thrown ceramic mug with unique glaze pattern. Perfect for your morning coffee or tea. Food-safe and dishwasher friendly.",
        "Artisanal serving bowl with organic texture. Each piece is unique with variations that make it special."
    ],
    "jewelry": [
        "Handcrafted silver pendant with genuine gemstone. Each piece is individually crafted with attention to detail.",
        "Artisan necklace featuring unique beads and sustainable materials. Adjustable length for perfect fit."
    ],
    "textiles": [
        "Handwoven scarf made with natural fibers. Soft, warm, and perfect for all seasons. Each piece is one-of-a-kind.",
        "Textile wall hanging adding texture and warmth to your space. Created with traditional weaving techniques."
    ],
    "wood": [
        "Handcrafted wooden cutting board from sustainably sourced hardwood. Functional art for your kitchen.",
        "Artisanal wooden bowl with natural edge. Showcasing the wood's natural grain and character."
    ],
    "glass": [
        "Handblown glass vase with vibrant colors. Each piece is unique with bubbles and variations that add character.",
        "Fused glass coaster set with geometric patterns. Functional art that protects your surfaces."
    ],
    "other": [
        "Handcrafted item made with care and attention to detail. Each piece is unique and tells a story.",
        "Artisanal creation combining traditional techniques with contemporary design. Made to be cherished."
    ]
}

BANNERS = [
    "Handcrafted with Love | Unique Artisan Creations",
    "Discover One-of-a-Kind Pieces | Support Local Artisans",
    "Made by Hand, Made with Heart | Artisan Crafts",
    "Where Tradition Meets Innovation | Handmade Quality"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate-content', methods=['POST'])
def generate_content():
    try:
        data = request.get_json()
        
        name = data.get('name', 'Artisan')
        craft_type = data.get('craft_type', 'other')
        description = data.get('description', '')
        
        # Generate mock portfolio content
        portfolio_text = CRAFT_DESCRIPTIONS.get(craft_type, CRAFT_DESCRIPTIONS['other'])
        if description:
            portfolio_text = f"{name} creates {craft_type}. {description}. {portfolio_text}"
        else:
            portfolio_text = f"{name} specializes in {craft_type}. {portfolio_text}"
        
        # Generate mock social ideas
        social_ideas = SOCIAL_IDEAS.get(craft_type, SOCIAL_IDEAS['other'])
        social_output = []
        for i, idea in enumerate(social_ideas[:3]):
            social_output.append({
                'title': f'Idea {i+1}',
                'content': idea,
                'hashtags': f'#{craft_type} #Handmade #Artisan #Craft'
            })
        
        # Generate mock product descriptions
        product_descriptions = PRODUCT_DESCRIPTIONS.get(craft_type, PRODUCT_DESCRIPTIONS['other'])
        
        # Select random banners
        selected_banners = random.sample(BANNERS, 2)
        
        # Select relevant badges
        relevant_badges = select_relevant_badges(craft_type, description)
        
        # Prepare response
        response = {
            'portfolio': portfolio_text,
            'social_ideas': social_output,
            'product_descriptions': product_descriptions,
            'banners': selected_banners,
            'badges': relevant_badges,
            'generated_at': datetime.now().isoformat()
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Error in generate_content: {e}")
        return jsonify({'error': 'Failed to generate content'}), 500

def select_relevant_badges(craft_type, description):
    badges = SAMPLE_BADGES.copy()
    
    # Always include these
    selected = ["Handmade with Love"]
    
    # Add badges based on craft type
    if craft_type in ["wood", "textiles", "other"]:
        selected.append("Eco-Friendly Materials")
    
    if craft_type in ["jewelry", "pottery", "glass"]:
        selected.append("Limited Edition")
    
    # Add badges based on description keywords
    description_lower = description.lower()
    if "local" in description_lower or "sourced" in description_lower:
        selected.append("Locally Sourced")
    
    if "custom" in description_lower or "bespoke" in description_lower:
        selected.append("Custom Orders Available")
    
    # Ensure we don't have duplicates
    return list(set(selected))

if __name__ == '__main__':
    app.run(debug=True, port=5000)