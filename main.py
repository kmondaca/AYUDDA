from flask import Flask, render_template, session, redirect, url_for, send_file
from flask_wtf import FlaskForm
from wtforms import (StringField , SubmitField,BooleanField ,
                     RadioField , SelectField , TextField , TextAreaField)

from wtforms.validators import DataRequired
from util import fill_one_pdf
import os

app = Flask(__name__) #create application

app.config['SECRET_KEY'] = 'mykey'

class InfoForm(FlaskForm):
    first = StringField('First Name: ', validators=[DataRequired()])
    last = StringField('Last Name: ', validators=[DataRequired()])
    lang = StringField('Primary Language:')
    phone = StringField('phone', validators=[DataRequired()])
    conpref =  RadioField('Contact Preference:',
                      choices=[('phone', 'Phone'), ('email', 'Email'), ('both', 'both')])
    email = TextAreaField('')
    conchoice =TextAreaField('')
    submit = SubmitField('Submit')


##############################

class SpanForm(FlaskForm):
    sfirst = StringField('Primer nombre: ', validators=[DataRequired()])
    slast = StringField('Apellido: ', validators=[DataRequired()])
    slang = StringField('Idioma principal:')
    sphone = StringField('Teléfono:', validators=[DataRequired()])
    sconpref =  RadioField('Cómo prefiere comunicarse:',
                      choices=[('phone', 'Teléfono'), ('email', 'Correo electrónico'), ('both', 'Ambos')])
    sconchoice =TextAreaField('')
    semail = TextAreaField('')
    submit = SubmitField('Submit')

class TestForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    dob = StringField("Date of Birth: ", validators=[DataRequired()])
    submit = SubmitField('Submit')

#will continue to have this coded in English, need to fix discriptions to Spanish
class SectionA(FlaskForm):
    childName = StringField('Nombre completo: ', validators=[DataRequired()])
    childDOB = StringField("Fecha de nacimiento: ", validators=[DataRequired()])
    childSex = RadioField('Sexo:',
                      choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')])
    AHCCCS =StringField('Numero de cuenta de AHCCCS (Si corresponde):')
    language = StringField('Idioma principal:', validators=[DataRequired()])
    childAddress = StringField('Direccion residencial (Numero, Calle):', validators=[DataRequired()])
    childCity = StringField('Ciudad:', validators=[DataRequired()])
    childState = StringField('Estado:', validators=[DataRequired()])
    childZip = StringField('Codigo postal:', validators=[DataRequired()])
    childPhone = StringField('Teléfono:', validators=[DataRequired()])
    #It doesn't like ethnicity for some reason
    ethnicity = RadioField('Etnia:',
                         choices=[('Indígena de los EE UU/Alaska', 'Indígena de los EE UU/Alaska'),
                                  ('Negra/Afroamericana (no Hispánica)', 'Negra/Afroamericana (no Hispánica)') ,
                                  ('Asiática/Indígena de la Polinesia', 'Asiática/Indígena de la Polinesia'),
                                  ('Hispánica o Latina', 'Hispánica o Latina'),
                                  ('Otra', 'Otra'),
                                  ('Blanca (no Hispánica)', 'Blanca (no Hispánica)')])
    tribe = StringField('Tribu (Si corresponde):')
    childMailAddress = StringField('Dirección postal (Si corresponde):')
    childMailCity = StringField('Ciudad:')
    childMailState = StringField('Estado:')
    childMailZip = StringField('Código postal:')
    childConpref = RadioField('Cómo prefiere comunicarse::',
                         choices=[('Teléfono', 'Teléfono'), ('Correo electrónico', 'Correo electrónico'), ('Ambos', 'Ambos')])
    childEmail = StringField('Correo electrónico:')
    vote = RadioField('¿Desea registrarse para votar?',
                         choices=[('Sí', 'Sí'), ('No', 'No')])
    submit = SubmitField('Enviar')


class SectionA1(FlaskForm):
    profName = StringField('Nombre de contacto', validators=[DataRequired()])
    profPhone = StringField('Teléfono de contacto', validators=[DataRequired()])
    type = StringField('Tipo de profesional', validators=[DataRequired()])
    date = StringField('Fecha de evaluación', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class SectionB(FlaskForm):
    parentName = StringField('Nombre completo:', validators=[DataRequired()])
    relationship = StringField("Parentesco:", validators=[DataRequired()])
    parentPhone = StringField('Teléfono:', validators=[DataRequired()])
    parentEmail = StringField('Correo electrónico:')
    parentAddress = StringField('Dirección (si diferente al solicitante):')
    parentCity = StringField('Ciudad:')
    parentState = StringField('Estado:')
    parentZip = StringField('Código postal:')
    parentConpref = RadioField('Mejor manera de contactarlo:',
                         choices=[('phone', 'Phone'), ('email', 'correo electronico'), ('both', 'ambos')])
    legalName = StringField('Nombre del tutor legal (Si diferente al anterior):')
    legalRelationship = StringField("Parentesco:")
    legalPhone = StringField('Teléfono:')
    legalAddress = StringField('Dirección:')
    legalCity = StringField('Ciudad:')
    legalState = StringField('Estado:')
    legalZip = StringField('Código postal:')
    submit = SubmitField('Enviar')

class SectionC(FlaskForm):
    coverage = StringField('Tipo de cobertura(privada,pública, etc.):', validators=[DataRequired()])
    healthPlan = StringField('Nombre del plan de salud:', validators=[DataRequired()])
    policyName = StringField('Nombre del titular de la póliza:', validators=[DataRequired()])
    IDNum = StringField('Número de ID/Grupo:', validators=[DataRequired()])
    policyNum = StringField('Número de póliza:', validators=[DataRequired()])
    policyDate = StringField('Fecha de vigencia:', validators=[DataRequired()])
    dob = StringField("Fecha de nacimiento del titular:", validators=[DataRequired()])
    submit = SubmitField('Enviar')

class SectionD(FlaskForm):
    program = StringField('Estado del Programa de Intervención Temprana o Nombre de la escuela y del distrito escolar:', validators=[DataRequired()])
    typeSupport = StringField('Tipo de Apoyo (Servicios o tipo de plan tal cómo Plande Educación Individual o Plan 504):', validators=[DataRequired()])
    eduDate = StringField('Fechas que asistió:', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class SectionHIPAA(FlaskForm):
    #concat name ,last, first middle (cannot get previous since middle isn't specified
    childLast = StringField("Nombre de persona/cliente cuya información de la salud se compartirá:", validators=[DataRequired()])
    childFirst = StringField("Apellido de persona/cliente cuya información de la salud se compartirá::", validators=[DataRequired()])
    childMiddle = StringField("Segundo de persona/cliente cuya información de la salud se compartirá::", validators=[DataRequired()])
    #DOB request, gather from Section A
    describeInfo = TextAreaField('')
    agency = StringField("Persona/Agencia que solicita o necesita la información:", validators=[DataRequired()])
    requestDate= StringField("Fecha de solicitud:", validators=[DataRequired()])
    #get Parent name
    #need a physical signature....
    authorizationDate = StringField("Fecha de autorización:", validators=[DataRequired()])
    submit = SubmitField('Enviar')

class SectionRelease(FlaskForm):
    #get concat version from SectionHIPAA of name
    #get dob from SectionA
    #get agency
    #get request date
    office = RadioField('¿Qué oficina de la División de Discapacidades del Desarrollo es la más cercana?:',
                               choices=[('Chandler', 'Chandler'),
                                        ('Flagstaff', 'Flagstaff'),
                                        ('Tucson', 'Tucson'),
                                        ('Phoenix (Oeste)', 'Phoenix (Oeste)'),
                                        ('Phoenix (Central)', 'Phoenix (Central)')])
    #autofill the location of the office
    permissions = SelectField("Permito que la informacion de salud protegida marcada a continuacion se comparta con el profesionalmedico, la agencia, el entorno educativo u otro indicado anteriormente::",
                               choices=[('Expedientes medicos', 'Expedientes medicos'),
                                        ('Informes/Expedientes de audiologia', 'Informes/Expedientes de audiologia'),
                                        ('Informes del habla y lenguaje', 'Informes del habla y lenguaje'),
                                        ('Informe de Plan 504 o Plan de Educacion Individual y Evaluacion mas reciente', 'Informe de Plan 504 o Plan de Educacion Individual y Evaluacion mas reciente'),
                                        ('Registros de recien nacidos', 'Registros de recien nacidos'),
                                        ('Informes psicologicos', 'Informes psicologicos'),
                                        ('Informes de terapia fisica', 'Informes de terapia fisica'),
                                        ('Registros de nacimiento y parto', 'Registros de nacimiento y parto'),
                                        ('Informes de terapia ocupacional', 'Informes de terapia ocupacional'),
                                        ('Expedientes de salud conductual', 'Expedientes de salud conductual'),
                                        ('Otro (Especifique):', 'Otro (Especifique):')])
    other = StringField("")
    #get parent name
    #requires real signature
    #get date of authorization
    submit = SubmitField('Enviar')
####################################################################
""""
# This is 90% of the magic right here (see https://pypi.org/project/fillpdf/):
from fillpdf.fillpdfs import (
    get_form_fields,
    write_fillable_pdf,
)

# constants for filenames
BLANK_FORM = "DDD-2069A-S-blank.pdf"
COMPLETED_FORM = "DDD-2069A-S-completed.pdf"

#pdf is in directory it knows what to get
form_fields = get_form_fields(BLANK_FORM)

# Just to see how everything starts out
for childName, current_value in form_fields.items():
    if current_value == "":
        current_value = "<blank>"
    print(f"{childName}: {current_value}")

# Prep data to fill out a few entries
updates = dict(
    SecA_Name="gfhgfd" ,
    Sex="Female",
    HomeAdd="La Casita",
    A_City1="Cartagena, Colombia",
    A1_name1="Abuela Alma",
    A1_Type1="Matriarch",
    A1_Date1="11/24/2021"
)

# Produce a non-editable version with entries filled in
write_fillable_pdf(BLANK_FORM, COMPLETED_FORM, updates, flatten=True)

# MAC ONLY
os.system(f"open {COMPLETED_FORM}")

"""
####################################################################

@app.route('/english', methods=['GET', 'POST'])
def english():

    form = InfoForm()
    if form.validate_on_submit():
        session['first']= form.first.data
        session['last'] = form.last.data
        session['lang'] = form.lang.data
        session['phone'] = form.phone.data
        session['conpref'] = form.conpref.data
        session['conchoice'] = form.conchoice.data
        session['email'] = form.email.data
        #session['submit'] = form.submit.data

        return redirect(url_for("thankyou"))#only when form submitted

    return render_template('english.html',form=form) #app


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/falso')
def falso():
    return render_template('fake.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/gracias')
def gracias():
    return render_template('gracias.html')

@app.route('/einfo')
def einfo():
    return render_template('einfo.html')

@app.route('/sinfo')
def sinfo():
    return render_template('sinfo.html')


@app.route('/spanish', methods=['GET', 'POST'])
def spanish():
    form = SpanForm()
    if form.validate_on_submit():
        session['sfirst'] = form.sfirst.data
        session['slast'] = form.slast.data
        session['slang'] = form.slang.data
        session['sphone'] = form.sphone.data
        session['sconpref'] = form.sconpref.data
        session['sconchoice'] = form.sconchoice.data
        session['semail'] = form.semail.data
        # session['submit'] = form.submit.data

        return redirect(url_for("gracias"))  # only when form submitted

    return render_template('spanish.html', form=form)  # app

@app.route('/sectionA1',methods=['GET', 'POST'])
def sectionA1():
    form = SectionA1()
    if form.validate_on_submit():
        session['profName'] = form.profName.data
        session['type'] = form.type.data
        session['date'] = form.date.data

        return redirect(url_for("sectionHIPAA"))  # only when form submitted
    return render_template('SectionA1.html', form=form)

@app.route('/sectionA',methods=['GET', 'POST'])
def sectionA():
    form = SectionA()
    if form.validate_on_submit():
        session['childName'] = form.childName.data
        session['childDOB'] = form.childDOB.data
        session['childSex'] = form.childSex.data
        session['AHCCCS'] = form.AHCCCS.data
        session['language'] = form.language.data
        session['childAddress'] = form.childAddress.data
        session['childCity'] = form.childCity.data
        session['childState'] = form.childState.data
        session['childZip'] = form.childZip.data
        session['childPhone'] = form.childPhone.data
        session['ethnicity'] = form.ethnicity.data
        session['tribe'] = form.tribe.data
        session['childMailAddress'] = form.childMailAddress.data
        session['childMailCity'] = form.childMailCity.data
        session['childMailState'] = form.childMailState.data
        session['childMailZip'] = form.childMailZip.data
        session['childConpref'] = form.childConpref.data
        session['childEmail'] = form.childEmail.data
        session['vote'] = form.vote.data
        return redirect(url_for("sectionC"))  # only when form submitted

    return render_template('SectionA.html', form=form)

@app.route('/sectionC',methods=['GET', 'POST'])
def sectionC():
    form = SectionC()
    if form.validate_on_submit():
        session['coverage'] = form.coverage.data
        session['healthPlan'] = form.healthPlan.data
        session['policyName'] = form.policyName.data
        session['IDNum'] = form.IDNum.data
        session['dob'] = form.dob.data
        session['policyDate'] = form.policyDate.data

        return redirect(url_for("sectionD"))  # only when form submitted

    return render_template('SectionC.html', form = form)

@app.route('/sectionD',methods=['GET', 'POST'])
def sectionD():
    form = SectionD()
    if form.validate_on_submit():
        session['program'] = form.program.data
        session['typeSupport'] = form.typeSupport.data
        session['eduDate'] = form.eduDate.data

        return redirect(url_for("sectionA1"))  # only when form submitted

    return render_template('SectionD.html', form=form)

@app.route('/sectionHIPAA',methods=['GET', 'POST'])
def sectionHIPAA():
    form = SectionHIPAA()
    if form.validate_on_submit():
        session['childLast'] = form.childLast.data
        session['childFirst'] = form.childFirst.data
        session['childMiddle'] = form.childMiddle.data
        session['describeInfo'] = form.describeInfo.data
        session['agency'] = form.agency.data
        session['requestDate'] = form.requestDate.data
        session['authorizationDate'] = form.authorizationDate.data

        return redirect(url_for("release"))  # only when form submitted

    return render_template('HIPAA.html', form=form)

@app.route('/release',methods=['GET', 'POST'])
def release():
    form = SectionRelease()
    if form.validate_on_submit():
        session['office'] = form.office.data
        session['permissions'] = form.permissions.data
        session['other'] = form.other.data

        return redirect(url_for("goodbye"))  # only when form submitted

    return render_template('Release.html', form=form)

@app.route('/app', methods=['GET', 'POST'])
def sectionB():
    #Section B
    #Section A
    #Section C
    #Section D
    #Section A.1
    #HIPAA
    #Release

    #maybe nested ifs until the end.....otherwise just move it to the respective rendering
    #issues figuring out how to run it.....
    form = SectionB()
    if form.validate_on_submit():
        session['parentName'] = form.parentName.data
        session['relationship'] = form.relationship.data
        session['parentPhone'] = form.parentPhone.data
        session['parentEmail'] = form.parentEmail.data
        session['parentAddress'] = form.parentAddress.data
        session['parentCity'] = form.parentCity.data
        session['parentState'] = form.parentState.data
        session['parentZip'] = form.parentZip.data
        session['parentConpref'] = form.parentConpref.data
        session['legalName'] = form.legalName.data
        session['legalRelationship'] = form.legalRelationship.data
        session['legalPhone'] = form.legalPhone.data
        session['legalAddress'] = form.legalAddress.data
        session['legalCity'] = form.legalCity.data
        session['legalState'] = form.legalState.data
        session['legalZip'] = form.legalZip.data
        #it is not reading this redirect, I have tried changing it to another to see if it
        #would read it but no luck, really don't know what to do
        return redirect(url_for("sectionA"))  # only when form submitted

    return render_template('SectionB.html', form=form)  #this form refers to the form we set on 371

@app.route('goodbye', methods=['GET', 'POST'])
def goodbye():
    #some of the spanish variables are actually in english jajajajajajajajajajaj
    #I regret not looking at these variables sooner
    all_pdf_fields = ['secA_AppName','APPLICANT_DOB','APPLICANT_Sex','secA_AHCCCS','secA_Language','secA_HomeAddress','secA_City1', 'secA_State1','secA_Zip1','SecA_Phone','secA_Ethnicity','secA_Tribe','secA_MailingAdd', 'secA_City2','secA_State2','secA_Zip2','secA_Contract','secA_ContactPrefer', 'secA_Vote'
                      'SecA_nombre1', 'SecA_Tipo1', 'SecA_fecha1', 'SecA_nombre2','Sec_Tipo2','SecA_fecha2','SecA_nombre3','SecA_Tipo3','SecA_fecha3',
                      'secB_Name', 'secB_Relationship1', 'secB_Phone1', 'secB_Email1', 'secB_City1','secB_State1','secB_Zip1','secB_Relationship2','secB_Address1','secB_BestWay','secB_Phone2','secB_Alt','secB_LGName','secB_Address2', 'secB_City2', 'secB_Zip2', 'secB_State2',
                      'secCtipo1','secC_plan1','secCTitular1','secC_num1', 'secC_vigencia1','secC_naci1','secC_tipo2','secC_plan2','secC_Titular2','secC_num2','secC_vigencia2','secC_naci2',
                      'secD_estado1', 'secD_tipo1','secD_fechas1', 'secD_estado2','secD_tipo2', 'secD_fechas2','SIG_Name','SIG_Relationship','SIG_Date',
                      '3_DOB', '3_Name', '3_Describe', '3_Date1','3_agency','3_padre','3_Date2',
                      '4_Name1','4_DOB', '4_Date1','MedicalPro', 'DDD_Address1','4_Zip1', '4_State1', '4_City1','4_Fax1', '4_Phone1', 'InfoTipo1', 'InfoTipo2','InfoTipo3, InfoTipo4','InfoTipo5','InfoTipo6','InfoTipo7', 'InfoTipo8','InfoTipo9','InfoTipo10', '4_Specify1', 'InfoTipo11','4_padre','4_Date2']  # not the real field names, especially in the Spanish version!

    data_for_pdf = {}

    for key in all_pdf_fields:
        if key not in session:
        # oops! somehow this never got set!!
        else:
            data_for_pdf[key] = session[key]

""""
@app.route('/test', methods=['GET', 'POST'])
def test():
    # for the other classes, I can just so SectionB.variable.data to grab the info
    if form.validate_on_submit():
        print("HERE")
        data_for_pdf = dict(
            SecA_Name=form.Childname.data,
            appDOB=form.childDOB.data,
            Sex=form.childSex.data,
            HomeAdd=form.childAddress.data,
            A_City1=form.childCity.data,
            A_State1=form.childState.data,
            A_Zip=form.childZip.data,
            A_Phone=form.phone.data,
            A_ethnicity=form.ethnicity.data,
            A_tribe=form.tribe.data,
            A_mailAdd=form.childMailAddress.data,
            A_MailCity=form.childMailCity.data,
            A_MailState=form.childMailState.data,
            A_MailZip=form.childMailZip.data,
            A_conpref = form.conpref.data,
            A_email = form.email.data,
            A_conchoice = form.conchoice.data,
            A_vote = form.vote.data,
            A1_name1="Abuela Alma",
            A1_Type1="Matriarch",
            A1_Date1="11/24/2021"
        )
        complete_pdf = fill_one_pdf("DDD-2069A-S", data_for_pdf)
        return send_file(complete_pdf, as_attachment=True)
    else:
        return render_template('test.html', form=form)
"""



if __name__ == '__main__':
    app.run(debug=True)
