import arcade

class MyGame(arcade.Window):
    def __init__(self):
        from settings import settings
        
        super().__init__(
            1920,  # SCREEN_WIDTH
            1080,  # SCREEN_HEIGHT
            "ELF ADVENTURES",  # TITLE
            fullscreen=settings.current_settings["fullscreen"]
        )
        
        self.set_update_rate(1/60)
        
        from views.menu_view import MenuView
        menu_view = MenuView()
        menu_view.setup()
        self.show_view(menu_view)
        
    def on_resize(self, width, height):
        if self.current_view and hasattr(self.current_view, 'setup'):
            self.current_view.setup()
        print(f"Окно изменило размер: {width}x{height}")