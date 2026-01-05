"""
Generate sample fake news data for training
"""
import pandas as pd
import os

def generate_fake_news_data():
    """Generate sample fake news dataset"""
    # Sample data with realistic examples
    data = {
        'text': [
            # Real news examples
            "Government announces new infrastructure spending bill to boost economy",
            "Scientists discover breakthrough treatment for Alzheimer's disease",
            "Federal Reserve holds interest rates steady amid economic uncertainty",
            "Renewable energy investments reach record high in third quarter",
            "International climate summit reaches agreement on carbon emissions",
            "New educational initiative aims to improve literacy rates nationwide",
            "Health officials recommend annual flu vaccinations for all citizens",
            "University researchers develop more efficient solar panel technology",
            "Major tech companies report strong quarterly earnings growth",
            "City council approves funding for new public transportation system",
            
            # Fake news examples
            "You won't believe what celebrities are hiding about their health!",
            "Shocking conspiracy reveals truth about moon landing cover-up",
            "Alien invasion imminent - government preparing secret bunkers",
            "Miracle weight loss pill burns fat while you sleep - doctors hate this trick!",
            "Celebrity death hoax spreads across social media platforms",
            "Secret government experiments cause mysterious weather phenomena",
            "Breaking: Local man discovers cure for all cancers in kitchen cabinet",
            "Exclusive: Time travel technology leaked from classified facility",
            "Urgent: Banking system crash imminent - withdraw money now!",
            "Vaccines cause supernatural powers according to leaked documents",
            
            # More realistic examples
            "Study confirms Mediterranean diet reduces risk of heart disease",
            "New policy aims to reduce carbon footprint by 2030",
            "Tech giant announces layoffs affecting thousands of employees",
            "Researchers develop early detection method for pancreatic cancer",
            "International trade agreement signed between major economies",
            "Local school district adopts new curriculum standards",
            "Public health campaign promotes mental wellness awareness",
            "Renewable energy jobs surpass fossil fuel employment",
            "Central bank warns of potential economic recession",
            "Archaeologists unearth ancient civilization ruins",
            
            # More fake examples
            "EXCLUSIVE: Hollywood stars involved in secret illuminati rituals",
            "Government hiding evidence of UFO landings since 1947",
            "Big Pharma suppresses natural cancer cure for profit",
            "Weather manipulation technology used to control elections",
            "Cell phone towers cause mass bird deaths worldwide",
            "Chemtrails spread mind-controlling substances over cities",
            "Ancient aliens built the pyramids according to new research",
            "Superfood scam exposed: Kale linked to alien abductions",
            "Breaking: Bitcoin crashes to zero - investors lose everything!",
            "Scientists accidentally create portal to parallel universe"
        ],
        'label': [
            # Real news labels (0)
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            # Fake news labels (1)
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            # More real news labels (0)
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            # More fake news labels (1)
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1
        ]
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV in root directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '../../news_data.csv')
    df.to_csv(data_path, index=False)
    
    print(f"Generated {len(df)} fake news samples")
    print(f"Data saved to: {data_path}")
    return df

if __name__ == "__main__":
    generate_fake_news_data()