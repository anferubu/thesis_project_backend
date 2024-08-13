from datetime import datetime
import textwrap

import google.generativeai as genai
from sqlmodel import create_engine, select, Session

from api.models.posts import Post
from api.models.teams import Team
from api.models.utils.enums import PostStatus
from core.secrets import env



GEMINI_API_KEY = env.gemini_api_key
DATABASE_URL = env.database_url

engine = create_engine(DATABASE_URL)



def get_response_from_chatbot(query):
    """Get a response from Gemini Pro Assistant."""

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')

    source = get_motorcycle_club_info()
    prompt = make_prompt(query, source)
    answer = model.generate_content(prompt)

    return answer.text



def make_prompt(query, source):
    """Make the prompt for the chatbot using user input and a data source."""

    now = datetime.now()
    escaped = source.replace("'", "").replace('"', "").replace("\n", " ")
    prompt = textwrap.dedent("""
    Eres un chatbot informativo que responde preguntas usando el texto de la fuente como referencia incluido a continuación. Asegúrate de responder en una oración completa, de manera exhaustiva e incluyendo toda la información de fondo relevante. Sin embargo, estás hablando con una audiencia no técnica, así que no menciones la fuente y asegúrate de desglosar los conceptos complicados y adoptar un tono amigable y conversacional. Si la información fuente es irrelevante para la respuesta, puedes ignorarla.
    PREGUNTA: '{query}'
    FECHA Y HORA DE LA PREGUNTA: '{now}'
    FUENTE: '{source}'
    RESPUESTA:
    """).format(query=query, now=now, source=escaped)
    return prompt



def get_motorcycle_club_info():
    """Get the current information about the motorcycle club."""

    with Session(engine) as session:
        query = select(Team).where(Team.deleted == False)
        teams = session.exec(query).all()
        text = "A continuación se muestra la información actual acerca de los EQUIPOS DEL CLUB DE MOTOCICLISTAS:\n\n"
        for index, team in enumerate(teams, 1):
            # team information
            name = team.name
            location = team.location.name
            # members information
            members = ""
            for i, member in enumerate(team.members, 1):
                members += f"{i}- {member.first_name} {member.last_name}: rol {member.user.role.name}, tel. {member.telephone}, nacimiento {member.birthdate}, motocicletas: "
                for motorcycle in member.motorcycles:
                    members += f"{motorcycle.brand.name} {motorcycle.model}, "
                members = members[:-2] + ".\n"
            # events information
            events = ""
            for i, event in enumerate(team.events, 1):
                participants = [
                    f"{p.member.first_name} {p.member.last_name}"
                    for p in event.members
                ]
                events += f"{i}- {event.name} ({event.type.value}) [{event.start_date}-{event.end_date}]: {event.description}.\n  Punto de encuentro: {event.meeting_point} ({event.location.name}).\n  Organizador: {event.organizer.first_name} {event.organizer.last_name}.\n  Participantes: {participants}.\n"
            # agreements information
            agreements = ""
            for i, agreement in enumerate(team.agreements, 1):
                agreements += f"{i}- {agreement.name} [{agreement.start_date}-{agreement.end_date}]: {agreement.description}.\n  Empresa: {agreement.company.name} ({agreement.company.contact_address}, {agreement.company.location.name}).\n"
            # summary teams text
            text += f"EQUIPO {index}: {name} ({location}).\nMIEMBROS:\n{members}\nEVENTOS:\n{events}\nCONVENIOS COMERCIALES:\n{agreements}\n"
        # posts information
        query = select(Post).where(
            Post.deleted == False, Post.status == PostStatus.PUBLISHED
        )
        posts = session.exec(query).all()
        text += "PUBLICACIONES:\n"
        for i, post in enumerate(posts, 1):
            text += f"{i}- {post.title} (fecha de creación: {post.created_at}): {post.content}\n"
        return text
