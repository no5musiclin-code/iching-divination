#!/usr/bin/env python3
"""
TTS Engine - macOS built-in say command + FFmpeg conversion
No internet required, works offline
"""
import subprocess
import os
import sys
import hashlib

class TTSEngine:
    VOICES = {
        'en': 'Samantha',       # US English female
        'en-uk': 'Daniel',      # UK English male
        'zh': 'Tingting',       # Chinese female
        'ja': 'Kyoko',          # Japanese female
        'ko': 'Yuna',           # Korean female
        'default': 'Samantha'
    }
    
    def __init__(self, output_dir='/tmp/tts_output'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate(self, text, voice='en', speed=175, output_path=None):
        """Generate MP3 from text using macOS say command"""
        if not output_path:
            text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
            output_path = os.path.join(self.output_dir, f'tts_{text_hash}.mp3')
        
        aiff_path = output_path.replace('.mp3', '.aiff')
        
        # Find voice
        voice_name = self.VOICES.get(voice, self.VOICES['default'])
        
        # macOS say command
        cmd = ['say', '-v', voice_name, '-r', str(speed), '-o', aiff_path, '--']
        # Use shell for the text to avoid argument issues
        proc = subprocess.Popen(
            ' '.join([f"say -v '{voice_name}' -r {speed} -o '{aiff_path}'"] + [f'-- "{text.replace("'", "\\'")}"']),
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()
        
        if proc.returncode != 0:
            # Fallback: try without voice
            cmd_simple = f"say -r {speed} -o '{aiff_path}' -- '{text.replace(chr(39), chr(39)+chr(39))}'"
            proc2 = subprocess.Popen(cmd_simple, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout2, stderr2 = proc2.communicate()
            if proc2.returncode != 0:
                print(f"TTS Error: {stderr.decode()[:200]}", file=sys.stderr)
                return None
        
        # Convert AIFF to MP3
        if os.path.exists(aiff_path):
            mp3_path = output_path
            conv = subprocess.run([
                'ffmpeg', '-i', aiff_path,
                '-codec:a', 'libmp3lame', '-b:a', '48k',
                '-y', mp3_path
            ], capture_output=True)
            
            if conv.returncode == 0:
                os.remove(aiff_path)  # Clean up AIFF
                return mp3_path
            else:
                print(f"FFmpeg error: {conv.stderr.decode()[:200]}", file=sys.stderr)
                return aiff_path  # Return AIFF if MP3 fails
        return None
    
    def get_audio_duration(self, audio_path):
        """Get duration of audio file in seconds"""
        result = subprocess.run([
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            audio_path
        ], capture_output=True, text=True)
        try:
            return float(result.stdout.strip())
        except:
            return 0

if __name__ == '__main__':
    tts = TTSEngine()
    
    # Test
    test_text = "Welcome to the Faceless YouTube Factory. This system generates professional videos automatically."
    print(f"Generating TTS for: {test_text[:50]}...")
    
    result = tts.generate(test_text)
    if result:
        duration = tts.get_audio_duration(result)
        print(f"✅ TTS generated: {result} ({duration:.1f}s)")
    else:
        print("❌ TTS generation failed")
