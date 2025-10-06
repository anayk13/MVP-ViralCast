#!/usr/bin/env python3
"""
Real Video Input Helper
Helps you input real YouTube video data for testing
"""

def get_real_video_data():
    """Interactive helper to input real video data"""
    
    print("🎬 REAL YOUTUBE VIDEO DATA INPUT HELPER")
    print("=" * 50)
    print("Enter real YouTube video data for testing")
    print()
    
    # Get video data from user
    title = input("📹 Video Title: ").strip()
    description = input("📝 Description: ").strip()
    
    try:
        duration = int(input("⏱️  Duration (seconds): "))
    except ValueError:
        print("❌ Please enter a valid number for duration")
        return None
    
    try:
        likes = int(input("👍 Likes: "))
        dislikes = int(input("👎 Dislikes: "))
    except ValueError:
        print("❌ Please enter valid numbers for likes/dislikes")
        return None
    
    upload_date = input("📅 Upload Date (YYYY-MM-DD): ").strip()
    
    try:
        upload_hour = int(input("🕐 Upload Hour (0-23): "))
        if not 0 <= upload_hour <= 23:
            print("❌ Upload hour must be between 0 and 23")
            return None
    except ValueError:
        print("❌ Please enter a valid hour (0-23)")
        return None
    
    tags = input("🏷️  Tags (comma-separated): ").strip()
    
    # Create video data dictionary
    video_data = {
        "title": title,
        "description": description,
        "duration": duration,
        "like_count": likes,
        "dislike_count": dislikes,
        "upload_date": upload_date,
        "upload_hour": upload_hour,
        "tags": tags
    }
    
    print("\n✅ Video data collected!")
    print("📊 Summary:")
    print(f"   Title: {title}")
    print(f"   Duration: {duration} seconds ({duration/60:.1f} minutes)")
    print(f"   Engagement: {likes} likes, {dislikes} dislikes")
    print(f"   Upload: {upload_date} at {upload_hour}:00")
    print(f"   Tags: {tags}")
    
    return video_data

def suggest_real_videos():
    """Suggest where to find real videos for testing"""
    
    print("\n🔍 WHERE TO FIND REAL VIDEOS FOR TESTING:")
    print("=" * 50)
    
    suggestions = [
        {
            "category": "Educational",
            "channels": ["Khan Academy", "Crash Course", "TED-Ed", "3Blue1Brown"],
            "search_terms": "python tutorial, math explained, science experiment"
        },
        {
            "category": "Cooking",
            "channels": ["Tasty", "Binging with Babish", "Joshua Weissman", "Gordon Ramsay"],
            "search_terms": "chocolate chip cookies, pasta recipe, easy cooking"
        },
        {
            "category": "Gaming",
            "channels": ["Markiplier", "Jacksepticeye", "Game Grumps", "PewDiePie"],
            "search_terms": "minecraft tutorial, game review, gaming tips"
        },
        {
            "category": "Tech",
            "channels": ["Marques Brownlee", "Linus Tech Tips", "Unbox Therapy", "TechLinked"],
            "search_terms": "iphone review, laptop comparison, tech news"
        },
        {
            "category": "DIY/Crafts",
            "channels": ["5-Minute Crafts", "Tasty", "DIY Creators", "Home Renovision"],
            "search_terms": "diy home decor, easy crafts, home improvement"
        }
    ]
    
    for suggestion in suggestions:
        print(f"\n📺 {suggestion['category']}:")
        print(f"   Popular Channels: {', '.join(suggestion['channels'])}")
        print(f"   Search Terms: {suggestion['search_terms']}")
    
    print(f"\n💡 TIPS:")
    print("• Look for videos with 1K-100K views (not viral content)")
    print("• Choose videos from 2023-2024 for recent data")
    print("• Pick educational/tutorial content for best results")
    print("• Avoid celebrity or viral videos")

def main():
    """Main function"""
    print("Choose an option:")
    print("1. Input real video data now")
    print("2. Get suggestions for finding real videos")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        video_data = get_real_video_data()
        if video_data:
            print(f"\n🎯 Ready to test! Use this data in the web interface.")
    elif choice == "2":
        suggest_real_videos()
    else:
        print("❌ Invalid choice. Please run again and choose 1 or 2.")

if __name__ == "__main__":
    main()
