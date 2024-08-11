from enum import Enum



class FeedbackStatus(str, Enum):
    """Sets the possible values of the feedback.status attribute."""
    PENDING = "pendiente"
    UNDER_REVIEW = "en revisión"
    RESOLVED = "resuelto"


class PostStatus(str, Enum):
    """Sets the possible values of the post.status attribute when post.type is
    POST."""
    UNPUBLISHED = "no publicado"
    PUBLISHED = "publicado"


class UserStatus(str, Enum):
    """Sets the possible values of the user.status attribute."""
    ACTIVE = "activo"
    INACTIVE = "inactivo"



class DocumentType(str, Enum):
    """Sets the possible values of the user.document_type attribute."""
    CC = "cédula de ciudadanía"
    TI = "tarjeta de identificación"
    RC = "registro civil"
    PP = "pasaporte"
    TE = "tarjeta de extranjería"
    CE = "cédula de extranjería"
    PEP = "permiso especial de permanencia"
    DIE = "documento de identificación extranjero"


class EventType(str, Enum):
    """Sets the possible values of the event.type attribute."""
    RIDE = "rodada"
    MEETING = "reunión informativa"
    SOCIAL = "reunión social"
    CHARITY = "evento de caridad"
    EXHIBITION = "exhibición"
    COMPETITION = "competición"
    TRAINING = "educacional"


class FeedbackType(str, Enum):
    """Sets the possible values of the feedback.type attribute."""
    QUESTION = "pregunta"
    SUGGESTION = "sugerencia"
    COMPLAINT = "queja"


class GenderType(str, Enum):
    """Sets the possible values of the user.gender attribute."""
    MALE = "masculino"
    FEMALE = "femenino"
    OTHER = "otro"
    NOT_SPECIFIED = "no especificado"


class LocationType(str, Enum):
    """Sets the possible values of the location.type attribute."""
    CITY = "ciudad"
    DEPARTMENT = "departamento"


class ReactionType(str, Enum):
    """Sets the possible values of the comment_reaction.type attribute."""
    LIKE = "me gusta"
    DISLIKE = "no me gusta"


class RHType(str, Enum):
    """Sets the possible values of the user.rh attribute."""
    O_POS = "O+"
    O_NEG = "O-"
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
