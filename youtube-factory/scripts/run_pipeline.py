#!/usr/bin/env python3
"""
YouTube Factory Pipeline - Main execution script
Run: python3 run_pipeline.py --niche iching --count 3
"""
import os
import sys
import argparse
from pathlib import Path

# Add scripts dir to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from script_generator import ScriptGenerator
from tts_engine import TTSEngine
from video_generator import VideoGenerator

class YouTubeFactory:
    """End-to-end faceless YouTube video factory"""
    
    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir or '/Users/lingo/.openclaw/workspace/shaishalin/projects/youtube-factory')
        self.output_dir = self.base_dir / 'output'
        self.tts_dir = self.base_dir / 'temp' / 'tts'
        self.video_dir = self.base_dir / 'temp' / 'videos'
        
        for d in [self.output_dir, self.tts_dir, self.video_dir]:
            d.mkdir(parents=True, exist_ok=True)
        
        self.script_gen = ScriptGenerator()
        self.tts = TTSEngine(output_dir=str(self.tts_dir))
        self.video_gen = VideoGenerator(output_dir=str(self.video_dir))
    
    def create_video(self, niche, topic=None, voice='en', produce_audio=True, produce_video=True):
        """Create one complete video from script to final MP4"""
        
        # 1. Generate script
        print(f"  📝 Generating script for {niche}...")
        script = self.script_gen.generate_script(niche, topic_override=topic)
        if not script:
            print(f"  ❌ Unknown niche: {niche}")
            return None
        
        print(f"  ✅ Title: {script['title']}")
        print(f"  ✅ Topic: {script['topic']}")
        print(f"  ✅ Segments: {len(script['segments'])}")
        
        # 2. Generate TTS for each segment
        audio_files = []
        total_duration = 0
        
        if produce_audio:
            print(f"  🎙️  Generating TTS...")
            
            # Intro
            intro_path = self.tts.generate(script['intro'], voice=voice)
            if intro_path:
                audio_files.append({'path': intro_path, 'type': 'intro'})
                total_duration += self.tts.get_audio_duration(intro_path)
            
            # Main segments
            for i, seg in enumerate(script['segments']):
                seg_path = self.tts.generate(seg['text'], voice=voice)
                if seg_path:
                    audio_files.append({'path': seg_path, 'type': 'segment', 'index': i})
                    total_duration += self.tts.get_audio_duration(seg_path)
                    print(f"      Segment {i+1}: {self.tts.get_audio_duration(seg_path):.1f}s")
            
            # Outro
            outro_path = self.tts.generate(script['outro'], voice=voice)
            if outro_path:
                audio_files.append({'path': outro_path, 'type': 'outro'})
                total_duration += self.tts.get_audio_duration(outro_path)
            
            print(f"  ✅ Total audio duration: {total_duration:.1f}s")
        
        # 3. Generate video
        if produce_video:
            print(f"  🎬 Generating video ({total_duration:.0f}s @ 30fps)...")
            video_path = self.video_gen.generate_video_from_script(script)
            
            if video_path and produce_audio and audio_files:
                # Combine all audio
                print(f"  🎵 Merging audio tracks...")
                combined_audio = self._combine_audio(audio_files)
                if combined_audio:
                    final_path = video_path.replace('.mp4', '_final.mp4')
                    result = self.video_gen.add_audio_to_video(video_path, combined_audio, final_path)
                    if result:
                        video_path = result
            
            if video_path:
                # Move to output
                final_output = self.output_dir / f"{niche}_{Path(video_path).name}"
                os.rename(video_path, final_output)
                print(f"  ✅ Video saved: {final_output}")
                return {'script': script, 'video': str(final_output), 'audio': audio_files}
        
        return {'script': script, 'video': None, 'audio': audio_files}
    
    def _combine_audio(self, audio_files):
        """Combine multiple audio files using ffmpeg"""
        if not audio_files:
            return None
        
        # Create concat file
        concat_file = self.tts_dir / 'concat.txt'
        with open(concat_file, 'w') as f:
            for af in audio_files:
                if af['path'] and os.path.exists(af['path']):
                    f.write(f"file '{af['path']}'\n")
        
        output = self.tts_dir / 'combined.mp3'
        cmd = ['ffmpeg', '-f', 'concat', '-safe', '0',
               '-i', str(concat_file),
               '-c', 'copy', '-y', str(output)]
        
        result = os.system(' '.join(cmd) + ' 2>/dev/null')
        if result == 0 and output.exists():
            return str(output)
        return None
    
    def run_batch(self, niche, count=3, voice='en'):
        """Generate multiple videos"""
        print(f"\n{'='*60}")
        print(f"🎬 YOUTUBE FACTORY — {niche.upper()} CHANNEL")
        print(f"{'='*60}")
        
        results = []
        topics = [
            'Business Decisions', 'Investment Timing', 'Wealth Attraction',
            'Morning Rituals', 'Risk Management', 'Team Leadership',
            'Career Changes', 'Entrepreneur Mindset', 'Market Timing',
        ]
        
        for i in range(count):
            topic = topics[i % len(topics)] if topics else None
            print(f"\n--- Video {i+1}/{count} ---")
            result = self.create_video(niche, topic=topic, voice=voice)
            if result:
                results.append(result)
        
        print(f"\n{'='*60}")
        print(f"✅ COMPLETE: {len(results)}/{count} videos generated")
        print(f"📁 Output: {self.output_dir}")
        print(f"{'='*60}")
        
        return results

def main():
    parser = argparse.ArgumentParser(description='YouTube Faceless Video Factory')
    parser.add_argument('--niche', default='iching', 
                       choices=['iching', 'numerology', 'aitools', 'ancientwisdom', 'passiveincome'],
                       help='Content niche')
    parser.add_argument('--count', type=int, default=3, help='Number of videos to generate')
    parser.add_argument('--voice', default='en', help='TTS voice (en, en-uk, zh, ja, ko)')
    parser.add_argument('--topic', help='Specific topic override')
    parser.add_argument('--list-niches', action='store_true', help='List available niches')
    
    args = parser.parse_args()
    
    if args.list_niches:
        print("Available niches:")
        for n in ['iching', 'numerology', 'aitools', 'ancientwisdom', 'passiveincome']:
            print(f"  - {n}")
        return
    
    factory = YouTubeFactory()
    
    if args.topic:
        result = factory.create_video(args.niche, topic=args.topic, voice=args.voice)
        if result:
            print(f"\n✅ Video created: {result['video']}")
    else:
        factory.run_batch(args.niche, count=args.count, voice=args.voice)

if __name__ == '__main__':
    main()
