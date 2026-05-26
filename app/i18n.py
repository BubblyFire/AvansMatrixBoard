# Translations for the UI. Add a new language by adding a new key to this dict.
# Keys follow the pattern 'page.element', e.g. 'nav.home' or 'config.save_btn'.
TRANSLATIONS = {
    'en': {
        # Navigation
        'nav.home':         'Home',
        'nav.text':         'Text',
        'nav.draw':         'Draw',
        'nav.image':        'Image',
        'nav.imagepicker':  'Pick an image',
        'nav.slideshow':    'Slideshow',
        'nav.preview':      'Preview',
        'nav.config':       'Config',
        'nav.clear':        'Clear',

        # Preview page
        'preview.title':    'Live Matrix Preview',
        'preview.subtitle': 'Shows what is currently on the LED matrix. Updates a few times per second.',
        'preview.paused':   'Paused',
        'preview.live':     'Live',

        # Clear button confirmation
        'clear.confirm':    'Clear the matrix?',
        'clear.success':    'Matrix cleared.',
        'clear.failed':     'Failed to clear the matrix.',

        # Home page
        'home.title':       'Home',
        'home.welcome':     'Welcome back',

        # Draw page
        'draw.title':           'Draw on the Matrix',
        'draw.subtitle':        'Use the grid below to paint pixels that will be sent to the LED matrix.',
        'draw.paint_color':     'Paint color',
        'draw.mode':            'Current mode:',
        'draw.mode_drawing':    'Drawing',
        'draw.btn_draw':        'Draw',
        'draw.btn_erase':       'Erase',
        'draw.btn_clear':       'Clear',
        'draw.btn_save':        'Save image',

        # Text page
        'text.title':       'Send Text to Matrix',
        'text.subtitle':    'Control up to three lines of text with custom colors.',
        'text.line_color':  'Line {n} color',
        'text.line_text':   'Line {n} text',
        'text.placeholder': 'Enter text for line {n}',
        'text.send_btn':    'Send line {n}',

        # Image upload page
        'image.title':          'Matrix Image Upload',
        'image.subtitle':       'Choose an image from your computer or from the Raspberry Pi file browser.',
        'image.local_title':    'Local File Picker',
        'image.local_subtitle': 'Select an image from your computer.',
        'image.preview':        'Preview:',
        'image.upload_btn':     'Upload selected file',
        'image.pi_title':       'Raspberry Pi File Picker',
        'image.new_folder':     'New folder',
        'image.pi_subtitle':    'Browse files already on the Pi.',
        'image.selected_file':  'Selected file:',
        'image.use_btn':        'Use Selected Pi File',
        'image.loading':        'Loading\u2026',

        # Image picker page
        'imagepicker.title':        'Pick an image',
        'imagepicker.subtitle':     'Browse the folders and select an image to display on the LED matrix.',
        'imagepicker.folders':      'Folders',
        'imagepicker.preview':      'Preview',
        'imagepicker.no_selection': 'Select an image from the folder tree.',
        'imagepicker.send_btn':     'Show on matrix',
        'imagepicker.sending':      'Sending\u2026',
        'imagepicker.sent':         'Shown on matrix!',
        'imagepicker.empty':        'This folder is empty.',

        # Config page
        'config.title':                 'Matrix Configuration',
        'config.subtitle':              'Adjust the settings stored in config/config.json.',
        'config.save_btn':              'Save configuration',
        # Hardware section
        'config.section_hardware':      'Hardware',
        'config.brightness_label':      'Brightness',
        'config.brightness_help':       'Value between 0 and 1.',
        'config.auto_write_label':      'Enable NeoPixel auto_write',
        # Text section
        'config.section_text':          'Text scrolling',
        'config.scroll_delay_label':    'Scroll delay (seconds)',
        'config.scroll_delay_help':     'Delay between scroll frames (e.g. 0.05 to 0.2).',
        'config.font_offset_label':     'Font baseline offset',
        'config.font_offset_help':      'Vertical offset of the text in pixels.',
        # GIF section
        'config.section_gif':           'GIF playback',
        'config.gif_delay_label':       'GIF speed multiplier',
        'config.gif_delay_help':        '1.0 = normal, lower is faster, higher is slower.',
        # Image processing section
        'config.section_image':         'Image processing',
        'config.contrast_label':        'Contrast',
        'config.contrast_help':         '1.0 = unchanged. Higher values increase contrast.',
        'config.saturation_label':      'Saturation',
        'config.saturation_help':       '1.0 = unchanged. Higher values make colors more vivid.',
        'config.gamma_label':           'Gamma',
        'config.gamma_help':            'Controls brightness curve. Lower = brighter midtones (default 0.70).',
        'config.posterize_label':       'Posterize bits',
        'config.posterize_help':        'Reduces color depth. 1–8 bits per channel. Lower = fewer colors (default 5).',
        'config.black_level_label':     'Black level',
        'config.black_level_help':      'Minimum brightness (0–255) applied to near-black pixels so the matrix does not go fully dark.',
        'config.black_threshold_label': 'Black threshold',
        'config.black_threshold_help':  'Sum of R+G+B below which a pixel is treated as black (0–765, default 28).',
        'config.auto_crop_label':       'Auto-crop images',
        'config.auto_crop_help':        'Crop uniform borders before displaying so the image fills the matrix better.',
    },

    'nl': {
        # Navigatie
        'nav.home':         'Home',
        'nav.text':         'Tekst',
        'nav.draw':         'Tekenen',
        'nav.image':        'Afbeelding',
        'nav.imagepicker':  'Kies een afbeelding',
        'nav.slideshow':    'Diashow',
        'nav.preview':      'Voorbeeld',
        'nav.config':       'Instellingen',
        'nav.clear':        'Leeg',

        # Voorbeeldpagina
        'preview.title':    'Live matrix-voorbeeld',
        'preview.subtitle': 'Toont wat er nu op de LED-matrix staat. Ververst enkele keren per seconde.',
        'preview.paused':   'Gepauzeerd',
        'preview.live':     'Live',

        # Leeg-knop bevestiging
        'clear.confirm':    'Matrix leegmaken?',
        'clear.success':    'Matrix leeggemaakt.',
        'clear.failed':     'Matrix leegmaken mislukt.',

        # Home pagina
        'home.title':       'Home',
        'home.welcome':     'Welkom terug',

        # Tekenpagina
        'draw.title':           'Tekenen op het Matrix',
        'draw.subtitle':        'Gebruik het raster om pixels te tekenen die naar het LED matrix worden gestuurd.',
        'draw.paint_color':     'Tekenkleur',
        'draw.mode':            'Huidige modus:',
        'draw.mode_drawing':    'Tekenen',
        'draw.btn_draw':        'Tekenen',
        'draw.btn_erase':       'Wissen',
        'draw.btn_clear':       'Leegmaken',
        'draw.btn_save':        'Afbeelding opslaan',

        # Tekstpagina
        'text.title':       'Tekst naar Matrix sturen',
        'text.subtitle':    'Bestuur maximaal drie regels tekst met eigen kleuren.',
        'text.line_color':  'Regel {n} kleur',
        'text.line_text':   'Regel {n} tekst',
        'text.placeholder': 'Voer tekst in voor regel {n}',
        'text.send_btn':    'Verstuur regel {n}',

        # Afbeelding uploadpagina
        'image.title':          'Matrix Afbeelding Upload',
        'image.subtitle':       'Kies een afbeelding van je computer of vanuit de Raspberry Pi bestandsbrowser.',
        'image.local_title':    'Lokale bestandskiezer',
        'image.local_subtitle': 'Selecteer een afbeelding van je computer.',
        'image.preview':        'Voorbeeld:',
        'image.upload_btn':     'Upload geselecteerd bestand',
        'image.pi_title':       'Raspberry Pi Bestandskiezer',
        'image.new_folder':     'Nieuwe map',
        'image.pi_subtitle':    'Blader door bestanden op de Pi.',
        'image.selected_file':  'Geselecteerd bestand:',
        'image.use_btn':        'Gebruik geselecteerd Pi-bestand',
        'image.loading':        'Laden\u2026',

        # Afbeeldingskiezerpagina
        'imagepicker.title':        'Kies een afbeelding',
        'imagepicker.subtitle':     'Blader door de mappen en selecteer een afbeelding om op het LED matrix te tonen.',
        'imagepicker.folders':      'Mappen',
        'imagepicker.preview':      'Voorbeeld',
        'imagepicker.no_selection': 'Selecteer een afbeelding uit de mappenstructuur.',
        'imagepicker.send_btn':     'Toon op matrix',
        'imagepicker.sending':      'Verzenden\u2026',
        'imagepicker.sent':         'Weergegeven op matrix!',
        'imagepicker.empty':        'Deze map is leeg.',

        # Configuratiepagina
        'config.title':                 'Matrix Configuratie',
        'config.subtitle':              'Pas de instellingen aan die worden opgeslagen in config/config.json.',
        'config.save_btn':              'Configuratie opslaan',
        # Hardware sectie
        'config.section_hardware':      'Hardware',
        'config.brightness_label':      'Helderheid',
        'config.brightness_help':       'Waarde tussen 0 en 1.',
        'config.auto_write_label':      'NeoPixel auto_write inschakelen',
        # Tekst sectie
        'config.section_text':          'Tekst scrollen',
        'config.scroll_delay_label':    'Scroll vertraging (seconden)',
        'config.scroll_delay_help':     'Vertraging tussen scroll frames (bijv. 0.05 tot 0.2).',
        'config.font_offset_label':     'Lettertype basislijn offset',
        'config.font_offset_help':      'Verticale offset van de tekst in pixels.',
        # GIF sectie
        'config.section_gif':           'GIF afspelen',
        'config.gif_delay_label':       'GIF snelheidsmultiplicator',
        'config.gif_delay_help':        '1.0 = normaal, lager is sneller, hoger is langzamer.',
        # Beeldverwerking sectie
        'config.section_image':         'Beeldverwerking',
        'config.contrast_label':        'Contrast',
        'config.contrast_help':         '1.0 = ongewijzigd. Hogere waarden verhogen het contrast.',
        'config.saturation_label':      'Verzadiging',
        'config.saturation_help':       '1.0 = ongewijzigd. Hogere waarden maken kleuren levendiger.',
        'config.gamma_label':           'Gamma',
        'config.gamma_help':            'Bepaalt de helderheid van middentonen. Lager = lichter (standaard 0.70).',
        'config.posterize_label':       'Posterize bits',
        'config.posterize_help':        'Vermindert kleurdiepte. 1–8 bits per kanaal. Lager = minder kleuren (standaard 5).',
        'config.black_level_label':     'Zwart niveau',
        'config.black_level_help':      'Minimale helderheid (0–255) voor bijna-zwarte pixels, zodat het matrix niet volledig donker wordt.',
        'config.black_threshold_label': 'Zwart drempelwaarde',
        'config.black_threshold_help':  'Som van R+G+B waaronder een pixel als zwart wordt beschouwd (0–765, standaard 28).',
        'config.auto_crop_label':       'Afbeeldingen automatisch bijsnijden',
        'config.auto_crop_help':        'Snijdt uniforme randen bij zodat de afbeelding het matrix beter vult.',
    },
}

SUPPORTED_LANGUAGES = list(TRANSLATIONS.keys())
DEFAULT_LANGUAGE = 'en'


def get_translation(lang: str, key: str, **kwargs) -> str:
    """Return the translated string for the given language and key.
    Supports format placeholders, e.g. t('text.line_color', n=1).
    Falls back to English if the key is missing in the requested language."""
    text = TRANSLATIONS.get(lang, {}).get(key)
    if text is None:
        text = TRANSLATIONS[DEFAULT_LANGUAGE].get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text
