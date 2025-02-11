import collections
from .exceptions import FilterInvalidArgument


class Filter:
    """
    The base class for all filters.
    You can use these filters if you have the latest Lavalink version
    installed. If you do not have the latest Lavalink version,
    these filters will not work.
    """
    def __init__(self, payload=None):
        self.payload = payload

    @classmethod
    def none(cls):
        return cls({})

class Equalizer(Filter):
    """
    Filter which represents a 15 band equalizer.
    You can adjust the dynamic of the sound using this filter.
    i.e: Applying a bass boost filter to emphasize the bass in a song.
    The format for the levels is: List[Tuple[int, float]]
    """

    def __init__(self, *, levels: list, name: str = 'CustomEqualizer'):
        super().__init__()

        self.eq = self._factory(levels)
        self.raw = levels
        self._name = name
        self.payload = {"equalizer": self.eq}

    @property
    def name(self):
        """The Equalizers friendly name."""
        return self._name

    @staticmethod
    def _factory(levels: list):
        _dict = collections.defaultdict(int)

        _dict.update(levels)
        _dict = [{"band": i, "gain": _dict[i]} for i in range(15)]

        return _dict

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f"<Pomice.EqualizerFilter eq={self.eq} raw={self.eq}>"

    @classmethod
    def build(cls, *, levels: list, name: str = 'CustomEqualizer'):
        """Build a custom Equalizer class with the provided levels.
        Parameters
        ------------
        levels: List[Tuple[int, float]]
            A list of tuple pairs containing a band int and gain float.
        name: str
            An Optional string to name this Equalizer. Defaults to 'CustomEqualizer'
        """
        return cls(levels=levels, name=name)

    @classmethod
    def flat(cls):
        """Flat Equalizer.
        Resets your EQ to Flat.
        """
        levels = [(0, .0), (1, .0), (2, .0), (3, .0), (4, .0),
                  (5, .0), (6, .0), (7, .0), (8, .0), (9, .0),
                  (10, .0), (11, .0), (12, .0), (13, .0), (14, .0)]

        return cls(levels=levels, name='Flat')

    @classmethod
    def boost(cls):
        """Boost Equalizer.
        This equalizer emphasizes Punchy Bass and Crisp Mid-High tones.
        Not suitable for tracks with Deep/Low Bass.
        """
        levels = [(0, -0.075), (1, .125), (2, .125), (3, .1), (4, .1),
                  (5, .05), (6, 0.075), (7, .0), (8, .0), (9, .0),
                  (10, .0), (11, .0), (12, .125), (13, .15), (14, .05)]

        return cls(levels=levels, name='Boost')

    @classmethod
    def metal(cls):
        """Experimental Metal/Rock Equalizer.
        Expect clipping on Bassy songs.
        """
        levels = [(0, .0), (1, .1), (2, .1), (3, .15), (4, .13),
                  (5, .1), (6, .0), (7, .125), (8, .175), (9, .175),
                  (10, .125), (11, .125), (12, .1), (13, .075), (14, .0)]

        return cls(levels=levels, name='Metal')

    @classmethod
    def piano(cls):
        """Piano Equalizer.
        Suitable for Piano tracks, or tacks with an emphasis on Female Vocals.
        Could also be used as a Bass Cutoff.
        """
        levels = [(0, -0.25), (1, -0.25), (2, -0.125), (3, 0.0),
                  (4, 0.25), (5, 0.25), (6, 0.0), (7, -0.25), (8, -0.25),
                  (9, 0.0), (10, 0.0), (11, 0.5), (12, 0.25), (13, -0.025)]

        return cls(levels=levels, name='Piano')

class Timescale(Filter):
    """Filter which changes the speed and pitch of a track.
       Do be warned that this filter is bugged as of the lastest Lavalink dev version
       due to the filter patch not corresponding with the track time.

       In short this means that your track will either end prematurely or end later due to this.
       This is not the library's fault.
    """

    def __init__(
        self, 
        *, 
        speed: float = 1.0, 
        pitch: float = 1.0, 
        rate: float = 1.0
    ):
        super().__init__()

        if speed < 0:
            raise FilterInvalidArgument("Timescale speed must be more than 0.")
        if pitch < 0:
            raise FilterInvalidArgument("Timescale pitch must be more than 0.")
        if rate < 0:
            raise FilterInvalidArgument("Timescale rate must be more than 0.")

        self.speed = speed
        self.pitch = pitch
        self.rate = rate

        self.payload = {"timescale": {"speed": self.speed,
                                      "pitch": self.pitch,
                                      "rate": self.rate}}

    def __repr__(self):
        return f"<Pomice.TimescaleFilter speed={self.speed} pitch={self.pitch} rate={self.rate}>"


class Karaoke(Filter):
    """Filter which filters the vocal track from any song and leaves the instrumental.
       Best for karaoke as the filter implies.
    """

    def __init__(
        self,
        *,
        level: float = 1.0,
        mono_level: float = 1.0,
        filter_band: float = 220.0,
        filter_width: float = 100.0
    ):
        super().__init__()

        self.level = level
        self.mono_level = mono_level
        self.filter_band = filter_band
        self.filter_width = filter_width

        self.payload = {"karaoke": {"level": self.level,
                                    "monoLevel": self.mono_level,
                                    "filterBand": self.filter_band,
                                    "filterWidth": self.filter_width}}

    def __repr__(self):
        return (
            f"<Pomice.KaraokeFilter level={self.level} mono_level={self.mono_level} "
            f"filter_band={self.filter_band} filter_width={self.filter_width}>"
        )


class Tremolo(Filter):
    """Filter which produces a wavering tone in the music,
       causing it to sound like the music is changing in volume rapidly.
    """

    def __init__(
        self, 
        *, 
        frequency: float = 2.0, 
        depth: float = 0.5
    ):
        super().__init__()

        if frequency < 0:
            raise FilterInvalidArgument(
                "Tremolo frequency must be more than 0.")
        if depth < 0 or depth > 1:
            raise FilterInvalidArgument(
                "Tremolo depth must be between 0 and 1.")

        self.frequency = frequency
        self.depth = depth

        self.payload = {"tremolo": {"frequency": self.frequency,
                                    "depth": self.depth}}

    def __repr__(self):
        return f"<Pomice.TremoloFilter frequency={self.frequency} depth={self.depth}>"


class Vibrato(Filter):
    """Filter which produces a wavering tone in the music, similar to the Tremolo filter,
       but changes in pitch rather than volume.
    """

    def __init__(
        self, 
        *, 
        frequency: float = 2.0, 
        depth: float = 0.5
    ):

        super().__init__()
        if frequency < 0 or frequency > 14:
            raise FilterInvalidArgument(
                "Vibrato frequency must be between 0 and 14.")
        if depth < 0 or depth > 1:
            raise FilterInvalidArgument(
                "Vibrato depth must be between 0 and 1.")

        self.frequency = frequency
        self.depth = depth

        self.payload = {"vibrato": {"frequency": self.frequency,
                                    "depth": self.depth}}

    def __repr__(self):
        return f"<Pomice.VibratoFilter frequency={self.frequency} depth={self.depth}>"


class Rotation(Filter):
    """Filter which produces a stereo-like panning effect, which sounds like
    the audio is being rotated around the listener's head
    """

    def __init__(self, *, rotation_hertz: float = 0.2):
        super().__init__()

        self.rotation_hertz = rotation_hertz
        self.payload = {"rotation": {"rotationHz": self.rotation_hertz}}

    def __repr__(self) -> str:
        return f"<Pomice.RotationFilter rotation_hertz={self.rotation_hertz}>"


class ChannelMix(Filter):
    """Filter which manually adjusts the panning of the audio, which can make
    for some cool effects when done correctly.
    """

    def __init__(
        self,
        *,
        left_to_left: float = 1,
        right_to_right: float = 1,
        left_to_right: float = 0,
        right_to_left: float = 0
    ):
        super().__init__()

        if 0 > left_to_left > 1:
            raise ValueError(
                "'left_to_left' value must be more than or equal to 0 or less than or equal to 1.")
        if 0 > right_to_right > 1:
            raise ValueError(
                "'right_to_right' value must be more than or equal to 0 or less than or equal to 1.")
        if 0 > left_to_right > 1:
            raise ValueError(
                "'left_to_right' value must be more than or equal to 0 or less than or equal to 1.")
        if 0 > right_to_left > 1:
            raise ValueError(
                "'right_to_left' value must be more than or equal to 0 or less than or equal to 1.")

        self.left_to_left = left_to_left
        self.left_to_right = left_to_right
        self.right_to_left = right_to_left
        self.right_to_right = right_to_right

        self.payload = {"channelMix": {"leftToLeft": self.left_to_left, 
                                        "leftToRight": self.left_to_right, 
                                        "rightToLeft": self.right_to_left, 
                                        "rightToRight": self.right_to_right}
                                        }

    def __repr__(self) -> str:
        return ( 
        f"<Pomice.ChannelMix left_to_left={self.left_to_left} left_to_right={self.left_to_right} "
        f"right_to_left={self.right_to_left} right_to_right={self.right_to_right}>" 
        )

class Distortion(Filter):
    """Filter which generates a distortion effect. Useful for certain filter implementations where
    distortion is needed. 
    """

    def __init__(
        self,
        *,
        sin_offset: float =  0,
        sin_scale: float = 1,
        cos_offset: float = 0,
        cos_scale: float = 1,
        tan_offset: float = 0,
        tan_scale: float = 1,
        offset: float = 0,
        scale: float = 1
    ):
        super().__init__()

        self.sin_offset = sin_offset
        self.sin_scale = sin_scale
        self.cos_offset = cos_offset
        self.cos_scale = cos_scale
        self.tan_offset = tan_offset
        self.tan_scale = tan_scale
        self.offset = offset
        self.scale = scale

        self.payload = {"distortion": {
            "sinOffset": self.sin_offset,
            "sinScale": self.sin_scale,
            "cosOffset": self.cos_offset,
            "cosScale": self.cos_scale,
            "tanOffset": self.tan_offset,
            "tanScale": self.tan_scale,
            "offset": self.offset,
            "scale": self.scale
        }}

    def __repr__(self) -> str:
        return (
        f"<Pomice.Distortion sin_offset={self.sin_offset} sin_scale={self.sin_scale}> "
        f"cos_offset={self.cos_offset} cos_scale={self.cos_scale} tan_offset={self.tan_offset} "
        f"tan_scale={self.tan_scale} offset={self.offset} scale={self.scale}"
        )


class LowPass(Filter):
    """Filter which supresses higher frequencies and allows lower frequencies to pass.
    You can also do this with the Equalizer filter, but this is an easier way to do it.
    """

    def __init__(self, *, smoothing: float = 20):
        super().__init__()

        self.smoothing = smoothing
        self.payload = {"lowPass": {"smoothing": self.smoothing}}

    def __repr__(self) -> str:
        return f"<Pomice.LowPass smoothing={self.smoothing}>"
