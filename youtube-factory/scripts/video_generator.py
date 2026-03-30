#!/usr/bin/env python3
"""
Video Generator - Create faceless YouTube videos using MoviePy + Pillow
Ken Burns effect, animated text, subtitle overlays
"""
import os
import sys
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

class VideoGenerator:
    def __init__(self, output_dir='/tmp/video_output', assets_dir=None):
        self.output_dir = output_dir
        self.assets_dir = assets_dir or '/Users/lingo/.openclaw/workspace/shaishalin/projects/youtube-factory/assets'
        os.makedirs(output_dir, exist_ok=True)
    
    def create_gradient_background(self, width=1920, height=1080, color1=(10, 10, 30), color2=(30, 15, 60)):
        """Create a dark gradient background"""
        img = Image.new('RGB', (width, height))
        for y in range(height):
            ratio = y / height
            r = int(color1[0] * (1-ratio) + color2[0] * ratio)
            g = int(color1[1] * (1-ratio) + color2[1] * ratio)
            b = int(color1[2] * (1-ratio) + color2[2] * ratio)
            for x in range(width):
                img.putpixel((x, y), (r, g, b))
        return img
    
    def add_gold_particles(self, img, count=50):
        """Add gold sparkle particles to background"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        import random
        random.seed(42)
        for _ in range(count):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(1, 3)
            alpha = random.randint(100, 255)
            color = (201, 168, 76, alpha)
            # Simple gold dots
            for dx in range(-size, size+1):
                for dy in range(-size, size+1):
                    if 0 <= x+dx < width and 0 <= y+dy < height:
                        px = img.getpixel((x+dx, y+dy))
                        blend = alpha / 255 * 0.3
                        new_r = int(px[0] * (1-blend) + 201 * blend)
                        new_g = int(px[1] * (1-blend) + 168 * blend)
                        new_b = int(px[2] * (1-blend) + 76 * blend)
                        img.putpixel((x+dx, y+dy), (new_r, new_g, new_b))
        return img
    
    def add_hexagram_symbol(self, img, position=(960, 540), size=300, opacity=30):
        """Add a faint I Ching hexagram watermark"""
        draw = ImageDraw.Draw(img)
        cx, cy = position
        s = size // 2
        # Draw simple hexagram-like pattern with rectangles
        alpha = int(255 * opacity / 100)
        gold = (201, 168, 76)
        
        # Three horizontal bars
        bar_height = size // 12
        for i, y_offset in enumerate([-s//2, 0, s//2]):
            draw.rectangle([cx - s, cy + y_offset - bar_height//2,
                          cx + s, cy + y_offset + bar_height//2],
                         fill=gold)
        return img
    
    def create_text_frame(self, text, sub='', duration=5.0, width=1920, height=1080):
        """Create a single frame with text overlay"""
        # Background
        img = self.create_gradient_background(width, height)
        img = self.add_gold_particles(img)
        draw = ImageDraw.Draw(img)
        
        # Main text - centered, wrapped
        max_chars = 40
        words = text.split()
        lines = []
        current = ''
        for word in words:
            if len(current) + len(word) + 1 <= max_chars:
                current += (' ' if current else '') + word
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        
        # Title
        title_size = 80
        try:
            font_title = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', title_size)
            font_body = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 48)
            font_sub = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Italic.ttf', 36)
        except:
            font_title = ImageFont.load_default()
            font_body = font_title
            font_sub = font_title
        
        total_text_height = (title_size + 20) * len(lines) + (48 + 10) * (len(lines) - 1) if lines else 0
        start_y = (height - total_text_height) // 2
        
        y = start_y
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font_title)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            
            # Gold text with shadow
            shadow_offset = 3
            draw.text((x + shadow_offset, y + shadow_offset), line, font=font_title, fill=(50, 40, 10))
            draw.text((x, y), line, font=font_title, fill=(201, 168, 76))
            y += title_size + 20
        
        # Subtitle
        if sub:
            bbox = draw.textbbox((0, 0), sub, font=font_sub)
            sw = bbox[2] - bbox[0]
            sx = (width - sw) // 2
            draw.text((sx, height - 150), sub, font=font_sub, fill=(100, 100, 120))
        
        return np.array(img)
    
    def frames_to_video(self, frames, fps=30, output_path=None):
        """Convert frames to video using ffmpeg"""
        if not output_path:
            import uuid
            output_path = os.path.join(self.output_dir, f'video_{uuid.uuid4().hex[:8]}.mp4')
        
        import tempfile
        tmp_dir = tempfile.mkdtemp()
        
        # Save frames as PNG
        for i, frame in enumerate(frames):
            img = Image.fromarray(frame)
            img.save(os.path.join(tmp_dir, f'frame_{i:05d}.png'))
        
        # Use ffmpeg to create video
        cmd = [
            'ffmpeg', '-framerate', str(fps),
            '-i', os.path.join(tmp_dir, 'frame_%05d.png'),
            '-c:v', 'libx264', '-preset', 'fast',
            '-crf', '23', '-pix_fmt', 'yuv420p',
            '-y', output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True)
        
        # Cleanup
        for f in os.listdir(tmp_dir):
            os.remove(os.path.join(tmp_dir, f))
        os.rmdir(tmp_dir)
        
        if result.returncode == 0:
            return output_path
        else:
            print(f"FFmpeg error: {result.stderr.decode()[-500:]}", file=sys.stderr)
            return None
    
    def generate_video_from_script(self, script_data, output_path=None, fps=30):
        """
        script_data = {
            'title': 'Video Title',
            'segments': [
                {'text': 'First point...', 'sub': 'Optional subtitle', 'duration': 5},
                {'text': 'Second point...', 'sub': '', 'duration': 5},
            ],
            'intro': 'Welcome message...',
            'outro': 'Subscribe prompt...'
        }
        """
        import uuid
        if not output_path:
            output_path = os.path.join(self.output_dir, f'yt_{uuid.uuid4().hex[:8]}.mp4')
        
        frames = []
        frame_duration = 1.0 / fps
        
        # Title frame
        title_frame = self.create_text_frame(
            script_data.get('title', 'Faceless YouTube'),
            script_data.get('subtitle', ''),
            duration=3.0
        )
        for _ in range(int(3.0 * fps)):
            frames.append(title_frame)
        
        # Intro
        if 'intro' in script_data:
            intro_frame = self.create_text_frame(script_data['intro'], '', duration=3.0)
            for _ in range(int(3.0 * fps)):
                frames.append(intro_frame)
        
        # Content segments
        for seg in script_data.get('segments', []):
            duration = seg.get('duration', 5.0)
            text = seg.get('text', '')
            sub = seg.get('sub', '')
            
            # Split text into chunks if too long
            words = text.split()
            if len(words) > 40:
                # Create multiple frames for long text
                chunk_size = 30
                chunks = []
                current = []
                for w in words:
                    current.append(w)
                    if len(current) >= chunk_size:
                        chunks.append(' '.join(current))
                        current = []
                if current:
                    chunks.append(' '.join(current))
                
                chunk_duration = duration / len(chunks)
                for chunk in chunks:
                    chunk_frame = self.create_text_frame(chunk, sub, duration=chunk_duration)
                    for _ in range(int(chunk_duration * fps)):
                        frames.append(chunk_frame)
            else:
                seg_frame = self.create_text_frame(text, sub, duration=duration)
                for _ in range(int(duration * fps)):
                    frames.append(seg_frame)
        
        # Outro
        if 'outro' in script_data:
            outro_frame = self.create_text_frame(script_data['outro'], '🔔 Subscribe for more!', duration=5.0)
            for _ in range(int(5.0 * fps)):
                frames.append(outro_frame)
        
        print(f"Generating video: {len(frames)} frames at {fps}fps...")
        return self.frames_to_video(frames, fps=fps, output_path=output_path)
    
    def add_audio_to_video(self, video_path, audio_path, output_path=None, volume=1.0):
        """Add audio track to video"""
        if not output_path:
            output_path = video_path.replace('.mp4', '_with_audio.mp4')
        
        cmd = [
            'ffmpeg', '-i', video_path, '-i', audio_path,
            '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
            '-shortest', '-y', output_path
        ]
        result = subprocess.run(cmd, capture_output=True)
        
        if result.returncode == 0:
            return output_path
        else:
            print(f"Audio merge error: {result.stderr.decode()[-300:]}", file=sys.stderr)
            return None

if __name__ == '__main__':
    gen = VideoGenerator()
    
    # Test
    test_script = {
        'title': 'The Secret of I Ching for Business Success',
        'subtitle': '☯️ Ancient Wisdom for Modern Entrepreneurs',
        'intro': 'Today we explore the ancient secrets of I Ching...',
        'segments': [
            {'text': 'The first secret is understanding the energy of timing.', 'sub': '☯ Timing is everything', 'duration': 4},
            {'text': 'Hexagram one teaches us about creative force and new beginnings.', 'sub': '䷀ The Creative', 'duration': 5},
            {'text': 'When you combine ancient wisdom with modern strategy, the results are powerful.', 'sub': '⚡ Ancient meets Modern', 'duration': 4},
        ],
        'outro': 'If you found this valuable, subscribe for daily wisdom insights!'
    }
    
    print("Generating test video...")
    result = gen.generate_video_from_script(test_script)
    if result:
        print(f"✅ Video generated: {result}")
    else:
        print("❌ Video generation failed")
