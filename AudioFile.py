class AudioFile:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):  # Prevent re-initialization
            self._initialized = True
            self.file = None  # Public attribute for file
            self._text = ''  # Private attribute for text
            self._summary = ''  # Private attribute for summary
            self._sentiment = ''  # Private attribute for sentiment

    @property
    def file(self):
        return self._file
    
    @file.setter
    def file(self, value):
        self._file = value
    
    @property
    def text(self):
        """The text property getter."""
        return self._text
    
    @text.setter
    def text(self, value):
        """The text property setter with validation."""
        if not isinstance(value, str):
            raise TypeError("Text must be a string.")
        self._text = value

    @property
    def summary(self):
        """The radius property getter."""
        return self._summary
    
    @summary.setter
    def summary(self, value):
        """The radius property setter with validation."""
        if not isinstance(value, str):
            raise TypeError("Summary must be a string.")
        self._summary = value
    
    @property
    def sentiment(self):
        """The radius property getter."""
        return self._sentiment
    
    @sentiment.setter
    def sentiment(self, value):
        """The radius property setter with validation."""
        if not isinstance(value, str):
            raise TypeError("Sentiment must be a string.")
        self._sentiment = value
    