from pydantic import (BaseModel, conint, root_validator, validator, ValidationError)
from typing import Optional
from datetime import date, datetime, time


class Odour(BaseModel):
    id: int
    userid: int
    category: str
    type: str
    intensity: str
    annoy: str
    duration: str
    observeddatetime: datetime
    observedtimeonly: time
    latitude: float
    longitude: float


class OdourType(BaseModel):
    id: int
    category: str
    type: str


class OdourIntensity(BaseModel):
    id: int
    value: int
    desc: str


class OdourAnnoy(BaseModel):
    id: int
    value: int
    desc: str


class OdourDuration(BaseModel):
    id: int
    desc: str


class OCRequest(BaseModel):
    type: Optional[conint(ge=0, le=9)]  # OdourCollect's odour type (called "category" here). 0 = All, 1-88 = filters
    subtype: Optional[conint(ge=0, le=89)]  # OdourCollect's odour subtype (called "type" here). 0 = All, 1-9 = filters
    minAnnoy: Optional[conint(ge=-4, le=4)]  # OdourCollect's "hedonic tone", from -4 to 4. 0 = neutral.
    maxAnnoy: Optional[conint(ge=-4, le=4)]
    minIntensity: Optional[conint(ge=0, le=6)]  # "intensity" in OdourCollect, from 0 to 6
    maxIntensity: Optional[conint(ge=0, le=6)]
    date_init: Optional[date]  # yyyy-mm-dd
    date_end: Optional[date]  # yyyy-mm-dd

    @root_validator()
    def validate_ocrequest(cls, values):
        if values.get('minannoy') and values.get('maxannoy'):
            if values.get('minannoy') > values.get('maxannoy'):
                raise ValueError('Min annoy can\'t be greater than max annoy')
        if values.get('minintensity') and values.get('maxintensity'):
            if values.get('minintensity') > values.get('maxintensity'):
                raise ValueError('Min intensity can\'t be greater than max intensity')
        if values.get('date_init') and values.get('date_end'):
            if values.get('date_init') > values.get('date_end'):
                raise ValueError('Starting date can\'t be later than ending date')
        return values


class GPScoords(BaseModel):
    lat: float
    long: float

    @validator('lat')
    def validate_lat(cls, v):
        # print('Validating: {}'.format(v))
        if v < -90.0 or v > 90.0:
            raise ValidationError(f'Incorrect GPS latitude value detected: {v}')
        return v

    @validator('long')
    def validate_long(cls, v):
        # print('Validating: {}'.format(v))
        if v < -180.0 or v > 180.0:
            raise ValidationError(f'Incorrect GPS longitude value detected: {v}')
        return v
