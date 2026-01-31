settings = None
audio_manager = None

def init_globals():
    global settings, audio_manager
    
    from settings_manager import Settings
    from audio_manager import AudioManager
    
    settings = Settings()
    audio_manager = AudioManager()