from datetime import datetime
import io
import textwrap

import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from sqlmodel import create_engine, select, Session

from api.models.posts import Post
from api.models.teams import Team
from api.models.utils.enums import PostStatus
from core.secrets import env



GEMINI_API_KEY = env.gemini_api_key
DATABASE_URL = env.database_url

engine = create_engine(DATABASE_URL)



def get_response_from_chatbot(query:str):
    """Get a response from Gemini Pro Assistant."""

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')

    source = get_motorcycle_club_info()
    prompt = make_prompt(query, source)
    answer = model.generate_content(prompt)

    return answer.text



def make_prompt(query:str, source:str):
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
                    members += f"marca {motorcycle.brand.name}, modelo {motorcycle.model}, "
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



def get_membership_card(
    name:str,
    surname:str,
    team:str,
    role:str,
    doc_type:str,
    doc_number:str,
    rh:str,
    location:str,
    telephone:str,
    photo_path:str='static/images/profile.jpg',
    output_format:str='PNG'
):
    """Generate the membership card of an user."""

    width, height = 600, 375
    small_font = ImageFont.truetype("arial.ttf", 14)
    small_bold_font = ImageFont.truetype("arialbd.ttf", 14)
    regular_font = ImageFont.truetype("arial.ttf", 18)
    regular_bold_font = ImageFont.truetype("arialbd.ttf", 20)
    large_font = ImageFont.truetype("arialbd.ttf", 40)
    mlarge_font = ImageFont.truetype("arialbd.ttf", 50)
    xlarge_font = ImageFont.truetype("arialbd.ttf", 60)
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    # Add graphic elements
    d.rounded_rectangle(
        [(0, 0), (width, height // 2)],
        fill=(35, 45, 121),
        radius=20,
        corners=(True, True, False, False))
    d.rounded_rectangle(
        [(0, height // 2), (width, height)],
        fill=(75, 85, 181),
        radius=20,
        corners=(False, False, True, True))
    d.rectangle([(570, 275), (width, 350)], fill=(255, 165, 0))
    # Add text
    team_text = f"Miembro del Equipo {team}".upper()
    location_text = f"{location}, Colombia"
    role_text = role.upper()
    name_text = name.upper()
    surname_text = surname.upper()
    fullname_text = f"{name_text} {surname_text}"
    id_text = f"{doc_type}: {doc_number}".upper()
    rh_text = f"RH: {rh}".upper()
    tel_text = f"Tel: {telephone}"
    d.text((25, 25), team_text, fill=(199, 203, 242), font=small_font)
    d.text((25, 42), location_text, fill=(199, 203, 242), font=regular_bold_font)
    if len(fullname_text) >= 12:
        d.text((30, 140), name_text, fill=(255, 255, 255), font=large_font)
        d.text((30, 188), surname_text, fill=(255, 255, 255), font=large_font)
    elif 9 < len(fullname_text) < 12:
        d.text((30, 163), fullname_text, fill=(255, 255, 255), font=mlarge_font)
    else:
        d.text((30, 163), fullname_text, fill=(255, 255, 255), font=xlarge_font)
    d.text((30, 265), id_text, fill=(255, 255, 255), font=regular_font)
    d.text((30, 290), tel_text, fill=(255, 255, 255), font=regular_font)
    d.text((30, 315), rh_text, fill=(255, 255, 255), font=regular_font)
    if len(role_text) >13:
        d.text((400, 210), role_text, fill=(199, 203, 242), font=small_bold_font)
    else:
        d.text((400, 210), role_text, fill=(199, 203, 242), font=regular_bold_font)
    # Add photo
    logo = Image.open(photo_path)
    if logo.mode in ('RGBA', 'LA'):
        logo = logo.convert("RGBA")
        white_bg = Image.new("RGB", logo.size, (255, 255, 255))
        logo = Image.alpha_composite(white_bg.convert("RGBA"), logo)
    logo.thumbnail((150, 150), Image.Resampling.LANCZOS)
    img.paste(logo, (400, 50))
    # Save image in the indicated format
    if output_format == 'PNG':
        output = io.BytesIO()
        img.save(output, format='PNG')
        output.seek(0)
    elif output_format == 'PDF':
        card_width, card_height = 3.375 * inch, 2.125 * inch
        output = io.BytesIO()
        pdf = canvas.Canvas(output, pagesize=(card_width, card_height))
        pdf.drawImage(ImageReader(img), 0, 0, width=card_width, height=card_height)
        pdf.save()
        output.seek(0)
    return output.getvalue()
