class HotelSearchArgs:
    def __init__(self, location: str, 
               date_from: str, 
               date_to: str, 
               has_spa: str | None = None, 
               stars: int|None = None) -> None:
        self.location = location 
        self.date_from = date_from 
        self.date_to = date_to 
        self.has_spa = has_spa
        self.stars = stars 