VIDEO_DATASET = [
    {
        "id": 1,
        "title": "Main Portfolio Intro",
        "category": "Vlogs",
        "url": "https://www.youtube.com/embed/your_video_id_1",
        "thumbnail": "https://via.placeholder.com/300x169",
        "description": "A personal layout overview showing off my daily workspace and routine."
    },
    {
        "id": 2,
        "title": "Sleek Text Animation",
        "category": "Motion Graphics",
        "url": "https://www.youtube.com/embed/your_video_id_2",
        "thumbnail": "https://via.placeholder.com/300x169",
        "description": "Kinetic typography overlay built entirely using After Effects."
    },
    {
        "id": 3,
        "title": "Cinematic TikTok Transition",
        "category": "Shorts",
        "url": "https://www.tiktok.com/embed/your_video_id_3",
        "thumbnail": "https://via.placeholder.com/300x169",
        "description": "High-energy fast cuts optimized for vertical mobile screens."
    }
]

def get_videos_by_category(category):
    # Mock data representing your videos/edits
    all_videos = [
        {"id": 1, "title": "Ageless Divas Promo", "category": "branding", "url": "#"},
        {"id": 2, "title": "Internet Safety Quest Teaser", "category": "educational", "url": "#"},
        {"id": 3, "title": "Cinematic 8K Showreel", "category": "video-editing", "url": "#"}
    ]
    
    if category.lower() == "all":
        return all_videos
        
    return [video for video in all_videos if video["category"] == category.lower()]